"""Module to parse skills"""

from common.utils.logging_handler import Logger
from common.models import Skill, EmploymentRole
from common.utils.errors import ValidationError
from services.embedding import Embedding
from config import (BI_ENCODER_MODELS, CROSS_ENCODER_MODELS,
                    SKILL_PARSER_RERANKED_THRESHOLD)

# pylint: disable = invalid-name

class SkillParser(Embedding):
  """Parsing Skills from given description"""
  BI_ENCODER_MODEL_NAME = BI_ENCODER_MODELS["SKILL_PARSING"]
  CROSS_ENCODER_MODEL_NAME = CROSS_ENCODER_MODELS["SKILL_PARSING"]


  def __init__(self, source, db_index) -> None:
    """Initialize all the instance variables with the necessary attributes
       for the skill parsing."""
    super().__init__(self.BI_ENCODER_MODEL_NAME,
                     self.CROSS_ENCODER_MODEL_NAME)
    self.source = source
    self.DB_INDEX = db_index

  def create_reranker_input(self, query, passages):
    """
    Creates input to be passed to the re-ranker model

    Args:
      query: the description which will be used as a query
      passages: list of passages that will be reranked

    Returns:
      reranker_input: List(List[str]) list of query and passage pairs
        containing query along with passage
    """
    reranker_input = []
    for passage in passages:
      reranker_input.append([query, passage])
    return reranker_input

  def filter_docs(self, docs):
    """Filter docs that are below the threshold"""
    docs = [d for d in docs if d["score"] > SKILL_PARSER_RERANKED_THRESHOLD]
    return docs

  def create_response(self, skill):
    """Creates a response dict for each skill/query

    Args:
      skill (dict): Dictionary containing reranker score, skill name, skill id,
                    and skill description.

    Returns: dict containing skill statement and skill names
    dict with additional params
    """
    response = {
      "name": skill["name"],
      "id": skill["id"],
      "score": round(skill["score"], 3)
    }
    return response

  def get_relevant_skills(self, req_body):
    """Retrieves skills from the given description.
      Args:
        req_body: dict - dictionary containing query and top_k(optional)
      Returns:
        response: dict - dictionary containing query (i.e. description),
        skills - List containing skill name, skill description and
        relevance score.
    """
    name = req_body.get("name", "")
    description = req_body.get("description", "")
    if name == "" and description == "":
      raise ValidationError("Both name and description cannot be empty.")
    if name == "":
      query = description
    else:
      query = name + ". " + description
    top_k = req_body.get("top_k", 10)
    document_ids = self.search_docs([query], top_k)
    document_ids = document_ids = [
      [v["id"] for k, v in document.items()] for document in document_ids]
    document_ids = [item for doc_id in document_ids for item in doc_id]
    skill_desc = []
    skill_name = []
    skill_id = []
    docs = []
    for doc_id in document_ids:
      doc_obj = Skill.find_by_uuid(doc_id)
      if doc_obj.name not in skill_name:
        skill_desc.append(doc_obj.description)
        skill_name.append(doc_obj.name)
        skill_id.append(doc_obj.uuid)
        docs.append(doc_obj.to_dict())

    reranker_input = self.create_reranker_input(query, skill_desc)
    Logger.info("Created Re-ranked Input")
    ranked_scores = self.rerank_docs(reranker_input)
    Logger.info("Re-ranked the passages")
    skills = [{"score": score.item(), "desc": desc, "name": name,
          "id": id_} for score, desc, name, id_ in zip(
        ranked_scores, skill_desc, skill_name, skill_id)]
    filtered_skills = self.filter_docs(skills)
    ranked_skills = sorted(filtered_skills,
      key = lambda x: x["score"], reverse = True)
    Logger.info("Filtered the passages based on threshold")
    top_k_skills = ranked_skills[:top_k]
    response_list = []
    for skill in top_k_skills:
      response = self.create_response(skill)
      response_list.append(response)
    return response_list


  def parse_skills_by_role_ids(self, request_body, update_flag):
    """
    Given the role ids, this method finds skill candidates for mapping

    Args:
      request_body: request body containing input role_ids(firestore ids),
      top_k and list of alignment sources
    Returns:
      response_list: List[List[dict]] - List of top_k aligned skills
      for each role_id
    """
    ids = request_body.get("ids", [])
    top_k = request_body.get("top_k", 10)
    source_names = request_body.get("source_name", [])
    aligned_skills = []
    roles = []
    roles_dict = {}

    if ids:
      for id_ in ids:
        Logger.info("Parsing given role IDs")
        role = EmploymentRole.find_by_uuid(id_)
        roles.append(role)
    elif source_names:
      for source_name in source_names:
        Logger.info(f"Parsing all roles for {source_name}")
        roles = EmploymentRole.find_by_source_name(source_name)
    else:
      raise ValidationError(
          "Both EmploymentRole IDs and Source name cannot be empty.")

    for role in roles:
      Logger.info(f"Parsing role_id: {role.id}")
      role_request = {"top_k": top_k, "name": "", "description":\
         role.description}
      parsed_skills = self.get_relevant_skills(role_request)
      roles_dict[role.id] = parsed_skills
      aligned_skills.append(parsed_skills)

    if update_flag:
      Logger.info("Updating parsed skills in firestore")
      update_skills = request_body.get("update_alignments")
      self.update_aligned_skills(roles, aligned_skills, update_skills)
    return roles_dict


  def update_aligned_skills(self, input_object_list, aligned_skills_list,
                            update_skills):
    """
    Updates alignment in firestore documents for given list of input objects

    Args:
      input_object_list: list of input objects (roles/curriculums/assessments)
      aligned_skills_list: list of candiates skills for each given input object
      update_skills - (bool) If True - update firestore doc
                                False - append to firestore doc
    Returns: None
    """
    for input_obj, aligned_skills in zip(input_object_list,
                                        aligned_skills_list):
      if not update_skills:
        # Appending skill alignments to firestore
        aligned_skills.extend(
            input_obj.alignments.get("skill_alignment",
                                 {}).get(self.source,
                                         {}).get("suggested", []))
      if "skill_alignment" not in input_obj.alignments:
        input_obj.alignments["skill_alignment"] = {}
      if self.source not in input_obj.alignments[
        "skill_alignment"]:
        input_obj.alignments["skill_alignment"][
        self.source] = {}
      if "aligned" not in input_obj.alignments[
        "skill_alignment"][self.source]:
        input_obj.alignments["skill_alignment"][
          self.source]["aligned"] = []
      input_obj.alignments["skill_alignment"][
        self.source]["suggested"] = aligned_skills
      input_obj.update()


def batch_update_role_to_skills(request_body):
  """
  Method to be called by batch job for aligning role to skills.
  Args:
    request_body: request body containing input role_ids(firestore ids),
    top_k and list of skill_alignment_sources
  Returns:
    status: status of batch job containing job_name and status
  """
  alignment_sources = request_body.get("skill_alignment_sources")
  for source in alignment_sources:
    db_index = "skill" + "_" + source
    skill_parse_obj = SkillParser(source=source, db_index=db_index)
    _ = skill_parse_obj.parse_skills_by_role_ids(request_body, update_flag=True)
    Logger.info(f"Sucessfully found skill aligments from {source}")
  status = {"status": "succeeded"}
  return status
