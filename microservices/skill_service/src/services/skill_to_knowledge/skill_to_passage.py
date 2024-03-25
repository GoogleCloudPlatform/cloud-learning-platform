"""Maps skill to passages from learning resource."""

from services.embedding import Embedding
from common.models import (Skill, KnowledgeServiceLearningUnit,
                          KnowledgeServiceLearningContent,
                          KnowledgeServiceLearningObjective, SubConcept)
from common.utils.logging_handler import Logger
from common.utils.errors import ValidationError
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from collections import defaultdict
from config import (RERANKER_THRESHOLD, BI_ENCODER_MODELS, CROSS_ENCODER_MODELS)

# pylint: disable=broad-exception-raised,invalid-name

class LearningResourceMapping:
  """Learning Resource to LU mapping"""

  @staticmethod
  def create_lr_concept_mapping():
    """Maps learning unit ids to their Concept ids

      Returns:
        learning_resource_concept_mapping: dictionary
                  {"lr_id": [list of concept ids]}
    """
    learning_resource_concept_mapping = defaultdict(list)

    all_learning_resources = KnowledgeServiceLearningContent.collection.fetch()
    all_learning_resource_ids = [lr.id for lr in all_learning_resources]
    for learning_resource_id in all_learning_resource_ids:
      learning_resource = KnowledgeServiceLearningContent.find_by_id(
        learning_resource_id)
      learning_resource_concept_mapping[learning_resource_id] = \
        learning_resource.child_nodes["concepts"]
    return learning_resource_concept_mapping


# pylint: disable=broad-except, unnecessary-dict-index-lookup, raise-missing-from
class SkillKnowledgeAlignment(Embedding):
  """skill to knowledge alignment"""

  BI_ENCODER_MODEL_NAME = BI_ENCODER_MODELS["SKILL_TO_PASSAGE"]
  CROSS_ENCODER_MODEL_NAME = CROSS_ENCODER_MODELS["SKILL_TO_PASSAGE"]
  DB_INDEX = "skill-to-knowledge"
  INDEX_DESCRIPTION = "Embeddings for learning resource passages"
  TOP_K = 10


  def __init__(self) -> None:
    super().__init__(self.BI_ENCODER_MODEL_NAME,
                     self.CROSS_ENCODER_MODEL_NAME)
    self.lu_paragraph_count = {}
    self.LEARNING_RESOURCE_CONCEPT_MAPPING = \
      LearningResourceMapping.create_lr_concept_mapping()

  def get_similar_passages(self, req_body):
    """Retrieves passages from the learning resources similar to the skill.
      Args:
        req_body: dict - dictionary containing skill ids, skill_names
              and skill_statements
      Returns:
        similar_passages: skill_name (str) and dictionary of learning_units
    """
    skill_ids = req_body.get("ids", [])
    skill_names = req_body.get("name", "")
    skill_statements = req_body.get("description", "")
    output_skill_ids = []
    queries = []
    if skill_ids:
      skill_names = []
      skill_statements = []
      skill_types = []
      for skill_id in skill_ids:
        skill = Skill.find_by_uuid(skill_id)
        skill_names.append(skill.name)
        skill_statements.append(skill.description)
        skill_types.append(skill.source_name)
      queries = list(
        map(lambda x: x[0] if x[2] == "emsi" else x[0] + ". " + x[1], zip(
          skill_names, skill_statements, skill_types))
      )
      output_skill_ids = skill_ids
      output_skill_names = skill_names
      output_skill_descriptions = skill_statements
    elif skill_statements and skill_names:
      queries = [skill_names + ". " + skill_statements]
      output_skill_names = [skill_names]
      output_skill_descriptions = [skill_statements]
    elif skill_statements:
      queries = [skill_statements]
      output_skill_names = [""]
      output_skill_descriptions = [skill_statements]
    elif skill_names:
      queries = [skill_names]
      output_skill_names = [skill_names]
      output_skill_descriptions = [""]
    else:
      raise ValidationError(
        "Either of IDs or Name or Description are required")

    document_ids = self.search_docs(queries, self.TOP_K)
    response_list = []
    for i, query in enumerate(queries):
      reranker_input, similar_lu_ids = self.create_reranker_input(
          query, document_ids[i])
      scores_passages = self.rerank_docs(reranker_input)
      passages, scores, filtered_lu_ids = self.filter_passages(
        scores_passages, reranker_input, similar_lu_ids)
      output_skill_id = output_skill_ids[i] if output_skill_ids else ""
      response = self.create_response(
        filtered_lu_ids,
        output_skill_names[i],
        output_skill_descriptions[i],
        output_skill_id,
        scores, passages)
      response_list.append(response)
    if skill_ids:
      response = {"data": response_list}
    else:
      response = {"data": response_list[0]}
    return response

  def create_response(
    self, lu_ids, skill, skill_description, skill_id, scores, passages):
    """Creates a response dict for each skill/query

    Args:
      lu_ids: list of mapped learning unit ids
      skill: skill name
      skill_description: skill description
      skill_id: skill id
      scores: Score of each passages
      passages: mapped knowledge text/passages

    Returns: dict containing skill statement and learning units
    dict with additional params
    """

    lu_index = defaultdict(list)
    for i, lu_id in enumerate(lu_ids):
      lu_index[lu_id].append(i)

    if skill_id:
      response = {"id": skill_id}
    else:
      response = {"name": skill,
                  "description": skill_description,
                  "learning_units": []
                 }

    learning_units = []
    for key, value in lu_index.items():
      learning_unit_dict = {}
      learning_unit_dict["lu_id"] = key
      lu_object = KnowledgeServiceLearningUnit.find_by_id(key)
      lu_passages = [passages[i] for i in value]
      lu_passage_scores = [scores[i] for i in value]
      learning_unit_dict["passages"] = [passage for _, passage in sorted(
          zip(lu_passage_scores, lu_passages), reverse=True)]
      learning_unit_dict["passage_scores"] = sorted([scores[i] for i in value],
          reverse=True)
      learning_unit_dict["lu_score"] = len(learning_unit_dict["passages"])/len(
          lu_object.text.split("<p>"))
      learning_unit_dict["learning_resource_id"] = \
          self.get_mapped_learning_resource(lu_object)
      learning_units.append(learning_unit_dict)
    response["learning_units"] = learning_units
    return response

  def get_mapped_learning_resource(self, lu_object):
    """Get the learning resource id for a learning unit id

      Args:
        lu_id: learning unit id (str)
      Returns:
        learning_resource_id (str)
    """
    lo_id = lu_object.parent_nodes["learning_objectives"][0]
    lo_object = KnowledgeServiceLearningObjective.find_by_uuid(lo_id)
    subconcept_id = lo_object.parent_nodes["sub_concepts"][0]
    subconcept_obj = SubConcept.find_by_uuid(subconcept_id)
    actual_concept_id = subconcept_obj.parent_nodes["concepts"][0]
    for lr_id, concept_ids in self.LEARNING_RESOURCE_CONCEPT_MAPPING.items(
      ):
      if actual_concept_id in concept_ids:
        return lr_id
    return "Not found"


  def filter_passages(self, norm_score_passages, reranker_input,
                      similar_lu_ids):
    """Filter passages which are below the threshold"""

    passages = [
        query_passage[1]
        for i, query_passage in enumerate(reranker_input)
        if norm_score_passages[i] > RERANKER_THRESHOLD
    ]
    scores = [score for score in norm_score_passages
              if score > RERANKER_THRESHOLD]
    filtered_lu_ids = [
        lu_id for i, lu_id in enumerate(similar_lu_ids)
        if norm_score_passages[i] > RERANKER_THRESHOLD
    ]
    return passages, scores, filtered_lu_ids

  def create_reranker_input(self, query, para_ids_dict):
    """
    Creates input to be passed to the re-ranker model

    Args:
      query: the skill whose mapping to knowledge is being done
      para_ids_list: list of paragraph ids

    Returns:
      reranker_input: List(List[str]) list of query and passage pairs
        containing query along with passage
      similar_lu_ids: (List[str]) list of mapped learning unit ids
    """
    reranker_input = []
    similar_lu_ids = []
    for _, para_id in para_ids_dict.items():
      lu_id, para_idx = para_id["id"].split("##")
      lu_text = KnowledgeServiceLearningUnit.find_by_id(lu_id).text
      paragraphs = lu_text.split("<p>")
      self.lu_paragraph_count[lu_id] = len(paragraphs)
      para_text = paragraphs[int(para_idx)]
      reranker_input.append([query, para_text])
      similar_lu_ids.append(lu_id)
    return reranker_input, similar_lu_ids

  def get_learning_units(self, lr_id):
    """returns all learning units for a given learning resource"""
    learning_resource = KnowledgeServiceLearningContent.find_by_id(lr_id)
    #learning_resource.load_tree()
    lr_fields = learning_resource.get_fields()
    lr_data = ParentChildNodesHandler.return_child_nodes_data(lr_fields)
    learning_unit_list = []
    for concept in lr_data["child_nodes"]["concepts"]:
      for sub_concept in concept["child_nodes"]["sub_concepts"]:
        for learning_objective in sub_concept\
          ["child_nodes"]["learning_objectives"]:
          learning_unit_list.extend(learning_objective\
            ["child_nodes"]["learning_units"])
    learning_unit_list = [KnowledgeServiceLearningUnit.find_by_uuid(\
      lu["uuid"]) for lu in learning_unit_list]
    return learning_unit_list

  def store_embeddings_knowledge(self, req_body):
    """
    Creates and stores embedding of the passages of the
      given learning resource or learning units

    Args:
      req_body: dict containing learning resource ids or learning unit ids
    """
    learning_resource_ids = req_body.get("learning_resource_ids", [])
    if learning_resource_ids:
      try:
        for lr_id in learning_resource_ids:
          learning_units = self.get_learning_units(lr_id)
          all_passages = []
          all_passage_ids = []
          for _, lu in enumerate(learning_units):
            passages = lu.text.split("<p>")
            passage_ids = [lu.id + "##" + str(i) for i in range(len(passages))]
            all_passages.extend(passages)
            all_passage_ids.extend(passage_ids)

          gcs_path = self.export_embedding_csv(
            all_passages, all_passage_ids, self.DB_INDEX , str(lr_id))

        Logger.info(f"Upload all CSV to GCS: {gcs_path}")
        self.populate_embedding_db(
          gcs_path, self.DB_INDEX, self.INDEX_DESCRIPTION, "knowledge")
      except Exception as e:
        raise Exception(str(e))
    else:
      raise Exception("Provide atleast one Learning Resource ID")

    return {"status": "Successfully generated and saved embeddings."}

def batch_populate_knowledge_embeddings(request_body):
  """Starts a batch job to populate Embedding for
    skill to knowledge alignment
  Args:
    request_body: dict - containing:
      learning_resource_ids: List[str] - learning resource ids
        for which embedding has to be created
  Returns:
    None"""
  try:
    Logger.info(f"Populating embeddings from: {request_body}")
    alignment_obj = SkillKnowledgeAlignment()
    alignment_obj.store_embeddings_knowledge(request_body)
    Logger.info("Generated embeddings for given Learning Resource")
  except Exception as e:
    raise Exception(f"Failed to populate embeddings. Error: {e}")
