"""Maps skill to nodes from topic tree of learning resource."""

from common.models.knowledge import Concept, KnowledgeServiceLearningObjective, KnowledgeServiceLearningUnit, SubConcept
from common.models import (Skill, KnowledgeServiceLearningContent)
from common.utils.logging_handler import Logger
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from services.skill_to_knowledge.skill_to_node_data import (Skill_Passage,
                                                            Skill_LU, Skill_LO,
                                                            Skill_SubConcept,
                                                            Skill_Concept)

# pylint: disable=broad-exception-raised,invalid-name

class Skill_Query:
  """Skill class for query inputs"""

  def __init__(self, name, description):
    """Initialize all the instance variables with the necessary attributes
       for the knowledge data."""
    self.name = name
    self.description = description


class SkillNodeAlignment:
  """skill to knowledge node alignment"""

  def map_skill_to_nodes_by_ids(self, req_body, update_flag=False):
    """
    Given the skill ids, this method maps knowledge nodes from given
    learning resource IDs.

    Args:
      request_body: request body containing list of input skill ids
      and list of learning_resource_ids
    Returns:
      response_dict: Dict - Dictionary containing mapped nodes
    """
    if req_body.get("learning_resource_ids"):
      learning_resource_ids = req_body["learning_resource_ids"]
    else:
      learning_resources = KnowledgeServiceLearningContent.collection.fetch()
      learning_resource_ids = [lr.id for lr in learning_resources]
    skill_ids = req_body.get("ids", [])
    source_names = req_body.get("source_name", [])
    response_dict = {}
    aligned_nodes = []
    skill_list = []
    if skill_ids:
      Logger.info("Processing given Skill IDs")
      for skill_id in skill_ids:
        skill = Skill.find_by_uuid(skill_id)
        skill_list.append(skill)
    elif source_names:
      for source_name in source_names:
        Logger.info(f"Processing all skills for {source_name}")
        skill_list = Skill.find_by_source_name(source_name)
    else:
      raise Exception("Both Skill ID and Source name cannot be empty.")

    if skill_list:
      for skill in skill_list:
        Logger.info(f"Processing skill_id: {skill.uuid}")
        query = skill.name if skill.source_name == "emsi" else skill.name +\
            ". " + skill.description
        response = self.map_nodes(query, learning_resource_ids)
        if response:
          response_dict[skill.uuid] = response
          aligned_nodes.append(response)

    if update_flag:
      Logger.info("Updating knowledge alignments in Firestore")
      update_skills = req_body.get("update_alignments")
      self.update_mapped_nodes(skill_list, aligned_nodes, update_skills)
    return {"data": response_dict}

  def update_mapped_nodes(self, skill_list, aligned_nodes_list, update_skills):
    """
    Updates knowledge alignment in firestore documents for given list of skill
    objects

    Args:
      skill_list: list of input Skill objects
      aligned_nodes_list: list of knowledge nodes from given
                          learning_resource_ids mapped to a skill
      update_skills - (bool) If True - update firestore doc
                                False - append to firestore doc
    Returns: None
    """
    for skill, skill_node_response in zip(skill_list, aligned_nodes_list):
      knowledge_nodes = skill_node_response
      if "knowledge_alignment" not in skill.alignments:
        skill.alignments["knowledge_alignment"] = {}

      if not update_skills and skill.alignments["knowledge_alignment"]:
        # Appending knowledge alignments in firestore
        for key in skill.alignments["knowledge_alignment"]["suggested"].keys():
          value = skill.alignments["knowledge_alignment"]["suggested"][key]
          if key in knowledge_nodes.keys():
            for k in knowledge_nodes[key].keys():
              if k in value.keys():
                knowledge_nodes[key][k].extend(value[k])
                knowledge_nodes[key][k] = list({v["id"]:v for v \
                  in knowledge_nodes[key][k]}.values())
              else:
                knowledge_nodes[key][k] = value
          else:
            knowledge_nodes[key] = value
      skill.alignments["knowledge_alignment"]["suggested"] = knowledge_nodes
      skill.update()
      Logger.info(skill.uuid)

  def map_skill_to_nodes_by_query(self, req_body):
    """
    This method maps given skill name and/or description to knowledge nodes
    of given learning resource IDs

    Args:
      request_body: request body containing skill name and/or description
      and list of learning_resource_ids
    Returns:
      response_dict: Dict - Dictionary containing mapped nodes
    """
    skill_name = req_body.get("name", "")
    skill_description = req_body.get("description", "")

    if req_body.get("learning_resource_ids"):
      learning_resource_ids = req_body["learning_resource_ids"]
    else:
      learning_resources = KnowledgeServiceLearningContent.collection.fetch()
      learning_resource_ids = [lr.id for lr in learning_resources]
    if skill_name and skill_description:
      skill = Skill_Query(skill_name, skill_description)
      query = skill_name + ". " + skill_description
    elif skill_description:
      skill = Skill_Query("", skill_description)
      query = skill_description
    elif skill_name:
      skill = Skill_Query(skill_name, "")
      query = skill_name
    else:
      raise Exception("Both name and description cannot be empty.")

    response = self.map_nodes(query, learning_resource_ids)
    if response:
      response["name"] = skill.name
      response["description"] = skill.description

    return {"data": response}

  def map_nodes(self, query, learning_resource_ids):
    """Retrieves knowledge nodes semantically similar to the skill
      Args:
        req_body: query: (str) - Skill name and/or description
                  learning_resource_ids - list of learning resource ids to use
                                    for knowledge nodes
      Returns:
        response: dict - dictionary containing
                  skill_id - firestore document id for the skill
                  mapped_passages - list of dictionaries containing
                            id - passage id
                            score - similarity score with skill
                  mapped_lus - list of dictionaries containing
                            id - LU firestore document id
                            score - similarity score with skill
                  mapped_los - list of dictionaries containing
                            id - LO firestore document id
                            score - similarity score with skill
                  mapped_subconcepts - list of dictionaries containing
                            id - Subconcept firestore document id
                            score - similarity score with skill
                  mapped_concepts - list of dictionaries containing
                            id - Concept firestore document id
                            score - similarity score with skill
                  mapped_learning_resource - list containing learning resource
                                            firestore document ids
                  all_mapped_lus - list containing all mapped learning unit
                                   firestore document ids
    """
    response = {}
    for learning_resource_id in learning_resource_ids:
      skill_to_passage_nodes = []
      skill_to_lu_nodes = []
      skill_to_lo_nodes = []
      skill_to_subconcept_nodes = []
      skill_to_concept_nodes = []
      skill_to_lr_nodes = []
      learning_resource = KnowledgeServiceLearningContent.find_by_id(
        learning_resource_id)
      lr_mapped = False
      #learning_resource.load_tree()
      lr_fields = learning_resource.get_fields()
      lr_data = ParentChildNodesHandler.return_child_nodes_data(lr_fields)
      lr_specific_concepts = []
      for concept_dict in lr_data["child_nodes"]["concepts"]:
        concept = Concept.find_by_uuid(concept_dict["uuid"])
        concept_specific_subconcepts = []
        for sub_concept_dict in concept_dict["child_nodes"]["sub_concepts"]:
          sub_concept = SubConcept.find_by_uuid(sub_concept_dict["uuid"])
          subconcept_specific_los = []
          for learning_objective_dict in sub_concept_dict\
            ["child_nodes"]["learning_objectives"]:
            learning_objective = KnowledgeServiceLearningObjective.\
              find_by_uuid(learning_objective_dict["uuid"])
            lo_specific_lus = []
            for learning_unit_dict in learning_objective_dict\
              ["child_nodes"]["learning_units"]:
              learning_unit = KnowledgeServiceLearningUnit.\
                find_by_uuid(learning_unit_dict["uuid"])
              passages = learning_unit.text.split("<p>")
              lu_specific_passages = []
              for i, passage in enumerate(passages):
                metadata = {"passage_text": passage, "skill_description": query}
                passage_id = learning_unit.id + "##" + str(i)
                passage_title = learning_unit.title + "_##Passage_" + str(i)
                skill_to_passage_node = Skill_Passage(passage_id, passage_title,
                                                      metadata)
                lu_specific_passages.append(skill_to_passage_node)
                if skill_to_passage_node.mapped:
                  skill_to_passage_nodes.append(skill_to_passage_node)
                  if not lr_mapped:
                    lr_mapped = True
                    skill_to_lr_nodes.append(learning_resource_id)
              skill_to_lu_node = Skill_LU(learning_unit.id, learning_unit.title,
                                          lu_specific_passages)
              if skill_to_lu_node.mapped:
                skill_to_lu_nodes.append(skill_to_lu_node)
              lo_specific_lus.append(skill_to_lu_node)
            skill_to_lo_node = Skill_LO(learning_objective.id,
                                        learning_objective.title,
                                        lo_specific_lus)
            if skill_to_lo_node.mapped:
              skill_to_lo_nodes.append(skill_to_lo_node)
            subconcept_specific_los.append(skill_to_lo_node)
          skill_to_subconcept_node = Skill_SubConcept(sub_concept.id,
                                                      sub_concept.title,
                                                      subconcept_specific_los)
          if skill_to_subconcept_node.mapped:
            skill_to_subconcept_nodes.append(skill_to_subconcept_node)
          concept_specific_subconcepts.append(skill_to_subconcept_node)
        skill_to_concept_node = Skill_Concept(concept.id, concept.title,
                                              concept_specific_subconcepts)
        if skill_to_concept_node.mapped:
          skill_to_concept_nodes.append(skill_to_concept_node)
        lr_specific_concepts.append(skill_to_concept_node)

      response[learning_resource_id] = {}
      response[learning_resource_id]["mapped_passages"] = \
        self.filter_nodes(skill_to_passage_nodes)
      response[learning_resource_id]["mapped_lus"] = \
        self.filter_nodes(skill_to_lu_nodes)
      response[learning_resource_id]["mapped_los"] = \
        self.filter_nodes(skill_to_lo_nodes)
      response[learning_resource_id]["mapped_subconcepts"] = \
        self.filter_nodes(skill_to_subconcept_nodes)
      response[learning_resource_id]["mapped_concepts"] = \
        self.filter_nodes(skill_to_concept_nodes)
    return response

  def filter_nodes(self, list_nodes):
    """Returns dictionary of only those nodes which are mapped to the skill.
      Args:
        list_nodes: list of Node objects

      Returns:
        list of mapped Node dictionary elements
    """
    return [node.get_item_dict() for node in list_nodes if node.mapped]


def batch_update_skill_to_nodes(request_body):
  """Updates all the skill document fields to knowledge nodes
    Args:
      req_body: dict - dictionary containing
                learning_resource_ids - list of learning resource ids to use
                                  for knowledge nodes
                update_alignments - (bool) If True - update firestore doc
                                                  False - append firestore doc
                data_source - "snhu", "emsi" or "all"
    Returns:
      job_status: status message if all the skills are updated successfully
                  or not.
  """
  skill_node_map_object = SkillNodeAlignment()
  _ = skill_node_map_object.map_skill_to_nodes_by_ids(
      request_body, update_flag=True)
  Logger.info("Updated skills to knowledge nodes for all skills.")
  status = {"status": "succeeded"}
  return status
