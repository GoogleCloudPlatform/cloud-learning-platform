"""Map skill to all the items"""

from services.skill_parsing.skill_parsing import SkillParser
from services.skill_alignment.skill_alignment import (SkillAlignment,
                                              align_skill_in_background)
from services.skill_to_knowledge.skill_to_node import (SkillNodeAlignment,
                                              batch_update_skill_to_nodes)
from common.utils.logging_handler import Logger

class SkillUnifiedAlignment:
  """class for unified skill alignment"""

  def align_by_id(self, request_body):
    """
    Method to perform unified alignment by id.
    """
    input_type = request_body.get("input_type")
    alignment_sources = request_body.get("output_alignment_sources")
    if input_type == "skill":
      # Skill to Skill
      # Skill to Knowledge
      aligned_knowledge = {}
      aligned_skills = {}
      if alignment_sources["learning_resource_ids"]:
        aligned_knowledge = self.get_knowledge_alignments(request_body, "id")
      if alignment_sources["skill_sources"]:
        aligned_skills = self.get_skill_alignments_by_id(request_body)
      response = self.create_response(
        request_body,
        create_for="id",
        aligned_knowledge=aligned_knowledge,
        aligned_skills=aligned_skills)
    else:
      raise NotImplementedError(
        "Knowledge id to Skill, EmploymentRole id to Skill, "
        "and Curriculum id to Skill are yet to be implemented")
    return response

  def align_by_query(self, request_body):
    """
    Method to perform unified alignment by query.
    """
    input_type = request_body.get("input_type")
    alignment_sources = request_body.get("output_alignment_sources")
    if input_type == "skill":
      # skill to knowledge
      # skill to skill
      aligned_knowledge = {}
      aligned_skills = {}
      if alignment_sources["learning_resource_ids"]:
        aligned_knowledge = self.get_knowledge_alignments(request_body, "query")
      if alignment_sources["skill_sources"]:
        aligned_skills = self.get_skill_alignments_by_query(request_body)
      response = self.create_response(
        request_body,
        create_for="query",
        aligned_knowledge=aligned_knowledge,
        aligned_skills=aligned_skills
      )
    elif input_type in ["role", "curriculum"]:
      # role to skill
      # curriculum to skill
      alignment_obj = SkillParser()
      aligned_skills = alignment_obj.get_relevant_skills(request_body)
      aligned_skills = aligned_skills["mapped_skills"]
      response = self.create_response(
        request_body,
        create_for="query",
        aligned_skills=aligned_skills
      )
    else:
      raise NotImplementedError(
        "Knowledge query to Skill/EmploymentRole/Curriculum "
        "is yet to be implemented")
    return response

  def create_response(self, request_body, create_for, **kwargs):
    """
    Method to combine all alignments and create response for unified
    alignment.
    """
    aligned_items = {}
    alignment_sources = request_body["output_alignment_sources"]
    if create_for == "id":
      aligned_skills = kwargs.get("aligned_skills")
      aligned_knowledge = kwargs.get("aligned_knowledge")
      aligned_knowledge = aligned_knowledge.get("data", [])
      query_skills = request_body.get("ids")
      for skill_id in query_skills:
        aligned_items[skill_id] = {}
        if alignment_sources["skill_sources"]:
          aligned_items[skill_id]["aligned_skills"] = aligned_skills[skill_id]
        if alignment_sources["learning_resource_ids"]:
          aligned_items[skill_id]["aligned_knowledge"] = \
            aligned_knowledge[skill_id]

    elif create_for == "query":
      if request_body["input_type"] == "skill":
        aligned_skills = kwargs.get("aligned_skills")
        aligned_knowledge = kwargs.get("aligned_knowledge")
        aligned_knowledge = aligned_knowledge.get("data", [])
        aligned_items["name"] = request_body["name"]
        aligned_items["description"] = request_body["description"]
        if alignment_sources["skill_sources"]:
          aligned_items["aligned_skills"] = aligned_skills
        if alignment_sources["learning_resource_ids"]:
          aligned_knowledge.pop("name")
          aligned_knowledge.pop("description")
          aligned_items["aligned_knowledge"] = aligned_knowledge
      elif request_body["input_type"] in ["role", "curriculum"]:
        aligned_skills = kwargs.get("aligned_skills")
        aligned_items["name"] = request_body["name"]
        aligned_items["description"] = request_body["description"]
        aligned_items["aligned_skills"] = aligned_skills
    response = {
      "data": aligned_items
    }
    return response

  def get_knowledge_alignments(self, request_body, input_type):
    """
    Method to get skill to knowledge alignments
    """
    alignment_obj = SkillNodeAlignment()
    if input_type == "id":
      mapped_nodes = alignment_obj.map_skill_to_nodes_by_ids(request_body)
    elif input_type == "query":
      mapped_nodes = alignment_obj.map_skill_to_nodes_by_query(request_body)
    return mapped_nodes

  def get_skill_alignments_by_id(self, request_body):
    """
    Method to get skill to skill alignments by id.
    """
    alignment_sources = request_body.get("skill_alignment_sources")
    query_skills = request_body.get("ids")
    aligned_skills = {}

    for skill_id in query_skills:
      aligned_skills[skill_id] = {}
      for source in alignment_sources:
        aligned_skills[skill_id][source] = []

    for source in alignment_sources:
      db_index = "skill" + "_" + source
      alignment_obj = SkillAlignment(source=source, db_index=db_index)
      skills_list = alignment_obj.align_skills_by_ids(request_body)
      for i, skills in enumerate(skills_list):
        aligned_skills[query_skills[i]][source].extend(skills)
    return aligned_skills

  def get_skill_alignments_by_query(self, request_body):
    """
    Method to get skill to skill alignments by query.
    """
    skill_name = request_body.get("name")
    skill_statement = request_body.get("description")
    top_k = request_body.get("top_k")
    alignment_sources = request_body.get("skill_alignment_sources")
    aligned_skills = {}
    for source in alignment_sources:
      db_index = "skill" + "_" + source
      alignment_obj = SkillAlignment(source=source, db_index=db_index)
      skills_list = alignment_obj.align_skills_by_query(
        skill_name, skill_statement, top_k)
      aligned_skills[source] = skills_list[0]
    return aligned_skills

def batch_unified_alignment(request_body):
  """
  Method for unified alignment to update the alignments in Firestore.
  """
  input_type = request_body["input_type"]
  alignment_sources = request_body["output_alignment_sources"]
  if input_type == "skill":
    skill_alignment_sources = alignment_sources.get("skill_sources")
    learning_resource_ids = alignment_sources.get("learning_resource_ids")

    if skill_alignment_sources:
      if skill_alignment_sources == ["*"]:
        request_body["skill_alignment_sources"] = []
      else:
        request_body["skill_alignment_sources"] = skill_alignment_sources
      Logger.info("Processing Skill Alignment")
      _ = align_skill_in_background(request_body)

    if learning_resource_ids:
      if learning_resource_ids == ["*"]:
        request_body["learning_resource_ids"] = []
      else:
        request_body["learning_resource_ids"] = learning_resource_ids
      Logger.info("Processing Skill to Knowledge Alignment")
      _ = batch_update_skill_to_nodes(request_body)
  status = {"status": "succeeded"}
  return status
