"""Map skill to skill"""
from common.models import Skill
from common.utils.logging_handler import Logger
from services.embedding import Embedding
from config import (BI_ENCODER_MODELS, CROSS_ENCODER_MODELS)

# pylint: disable = raise-missing-from,broad-exception-raised,invalid-name

class SkillAlignment(Embedding):
  """Class for skill alignment"""

  BI_ENCODER_MODEL_NAME = BI_ENCODER_MODELS["SKILL_ALIGNMENT"]
  CROSS_ENCODER_MODEL_NAME = CROSS_ENCODER_MODELS["SKILL_ALIGNMENT"]
  BI_ENCODER_TOP_K = 32

  def __init__(self, source, db_index) -> None:
    super().__init__(self.BI_ENCODER_MODEL_NAME,
      self.CROSS_ENCODER_MODEL_NAME)
    self.skill_source = source
    self.DB_INDEX = db_index

  @staticmethod
  def prepare_text_for_embedding(skill_name = None,
    skill_statement = None):
    """
      Method for preparing input for embedding model
      Args:
        skill_name - skill name
        skill_statement - skill statement/ skill description
      Returns:
        text - concatenated skill name and skill statement
    """
    if skill_name and skill_statement:
      text = skill_name + ". " + skill_statement
    elif skill_name:
      text = skill_name
    elif skill_statement:
      text = skill_statement
    else:
      raise Exception("For embedding input alteast one out of "
      "skill_name and skill_statement should be present.")
    return text

  def align_skills(self, queries, top_k):
    """Given query and top_k, this function return top_k
       skills from database which are good candidates for the alignment

      Args:
        queries: List[str] - list of queries (skill_name, skill_description
        or skill_name + skill_description)
      Returns:
        response_list: List[List[dict]] - List of top_k aligned skills
        for each internal_skill
    """

    document_ids = self.search_docs(queries, self.BI_ENCODER_TOP_K)
    document_ids = [
      [v["id"] for k, v in document.items()] for document in document_ids]
    skill_docs = []
    for doc_ids in document_ids:
      skill_docs.append([Skill.find_by_uuid(id) for id in doc_ids])
    response_list = []
    for query, doc_ids, skill_doc in zip(queries, document_ids, skill_docs):
      matched_skills = []
      reranker_input = [[query, SkillAlignment.prepare_text_for_embedding(
        doc.name, doc.description)] for doc in skill_doc]
      scores_passages = self.rerank_docs(reranker_input)
      for i, score in enumerate(scores_passages):
        matched_skills.append({
          "name": skill_doc[i].name,
          "id": doc_ids[i],
          "score": score
        })
      matched_skills = sorted(matched_skills,
      key = lambda x: x["score"], reverse = True)
      response_list.append(matched_skills[:top_k])
    return response_list

  def update_aligned_skill(self, internal_skills, aligned_skills_list,
                          update_skills):
    """
    Updates alignment in firestore document

    Args:
      internal_skills: list of skill objects
      aligned_skills_list: list of candiates skills for each given skill object
      update_skills - (bool) If True - update firestore doc
                                False - append to firestore doc
    Returns: None
    """
    for skill, aligned_skills in zip(internal_skills, aligned_skills_list):
      if not update_skills:
        # Appending skill alignments to firestore
        aligned_skills.extend(
            skill.alignments.get("skill_alignment",
                                 {}).get(self.skill_source,
                                         {}).get("suggested", []))
      if "skill_alignment" not in skill.alignments:
        skill.alignments["skill_alignment"] = {}
      if self.skill_source not in skill.alignments[
        "skill_alignment"]:
        skill.alignments["skill_alignment"][
        self.skill_source] = {}
      if "aligned" not in skill.alignments[
        "skill_alignment"][self.skill_source]:
        skill.alignments["skill_alignment"][
          self.skill_source]["aligned"] = []
      skill.alignments["skill_alignment"][
        self.skill_source]["suggested"] = aligned_skills
      skill.update()


  def align_skills_by_ids(self, request_body, update_flag=False):
    """
    Given the input skill ids or source name, this method find skill
    candidates for mapping

    Args:
      request_body: request body containing input skill ids(firestor ids) or
      input skill source name and top_k
    Returns:
      response_list: List[List[dict]] - List of top_k aligned skills
      for each input skill
    """
    ids = request_body.get("ids", [])
    top_k = request_body.get("top_k", 10)
    source_names = request_body.get("source_name", [])
    queries = []
    input_skills = []
    if ids:
      Logger.info("Processing given Skill IDs")
      for id_ in ids:
        input_skill = Skill.find_by_uuid(id_)
        queries.append(SkillAlignment.prepare_text_for_embedding(
          input_skill.name, input_skill.description))
        input_skills.append(input_skill)
    elif source_names:
      for source_name in source_names:
        Logger.info(f"Processing all skills for {source_name}")
        input_skills = Skill.find_by_source_name(source_name)
        for input_skill in input_skills:
          queries.append(SkillAlignment.prepare_text_for_embedding(
            input_skill.name, input_skill.description))
    else:
      raise Exception("Both Skill IDs and Source name cannot be empty.")
    result = self.align_skills(queries, top_k)
    if update_flag:
      Logger.info("Updating skill alignments in firestore")
      update_skills = request_body.get("update_alignments")
      self.update_aligned_skill(input_skills, result, update_skills)
    return result


  def align_skills_by_query(self, skill_name = None,
    skill_statement = None, top_k=10):
    """
    Given the skill_name, skill_description or both and queries,
    this method find skill candidates for mapping

    Args:
      request_body:
        skill_name: name of the skill
        skill_statement: description/statement of the skill
        top_k: number of skill candidates to be returned
    Returns:
      response_list: List[List[dict]] - List of top_k aligned skills
      for each internal_skill
    """
    if skill_name or skill_statement:
      query = SkillAlignment.prepare_text_for_embedding(skill_name,
        skill_statement)
    else:
      raise Exception("Atleast one param out of skill_name or skill_statement "
      "should be present.")
    result = self.align_skills([query], top_k)
    return result


def align_skill_in_background(request_body):
  """
  Method to be called by batch job for aligning skills.
  Args:
    request_body: request body containing input skill_ids(firestor ids),
    top_k and list of skill_alignment_sources
  Returns:
    status: status of batch job containing job_name and status
  """
  alignment_sources = request_body.get("skill_alignment_sources")
  for source in alignment_sources:
    db_index = "skill" + "_" + source
    alignment_obj = SkillAlignment(source=source, db_index=db_index)
    _ = alignment_obj.align_skills_by_ids(request_body, update_flag = True)
    Logger.info(f"Sucessfully found skill aligments from {source}")
  status = {"status": "succeeded"}
  return status
