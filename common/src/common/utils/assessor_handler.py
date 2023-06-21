"""
    This module is responsible to handle Assessor related
    functionality that can be used by other services
"""
from common.models import SubmittedAssessment, AssociationGroup
from common.utils.collection_references import (collection_references)
from typing import Optional

def get_last_submitted_assessement_of_assessments(assessment_ids, assessor_id):
  """Returns last submitted assessment whose assessor
    is not equal to assessor_id and
    related to assessments of aand repl discipline"""
  collection_manager = SubmittedAssessment.collection
  if len(assessment_ids) <= 30:
    last_submitted_assessments = collection_manager.filter(
        "assessment_id", "in", assessment_ids).order("-created_time").fetch()
    for submitted_assessment in last_submitted_assessments:
      if not submitted_assessment == assessor_id:
        last_submitted_assessment = submitted_assessment
        break
  else:
    collection_manager = collection_manager.order("-created_time").fetch()
    for assessment in collection_manager:
      if assessment.assessment_id in assessment_ids and \
        not assessment.assessor_id == assessor_id:
        last_submitted_assessment = assessment
        break
  return last_submitted_assessment

def get_assessors_of_dag(dag_id):
  """Function to get assessors tagged to Discipline Association Groups"""
  group = AssociationGroup.find_by_uuid(dag_id)
  group = group.get_fields(reformat_datetime = True)

  users_list = group["users"]
  assessors_list = []

  for user in users_list:
    if user["user_type"] == "assessor" and \
      user["status"] == "active":
      assessors_list.append(user)

  return assessors_list

def remove_assessor_for_submitted_assessments(submitted_assessments):
  """Unassigns assessor of submitted assessments"""
  for sub_assessment in submitted_assessments:
    # FIXME: Assign None for the assessor.
    # fireo=1.4.1 is not supporting none value while updating
    sub_assessment.assessor_id = ""
    sub_assessment.assessor_session_id = ""
    sub_assessment.update()

def replace_assessor_of_submitted_assessments(
    dag_id,
    submitted_assessments,
    assessment_ids,
    exclude_user_id: Optional[str] = None):
  """Replaces assessor of submitted assessments"""
  assessor_list = get_assessors_of_dag(dag_id)
  if not assessor_list:
    remove_assessor_for_submitted_assessments(submitted_assessments)
    return
  assessor_list = [
      assessor["user"]
      for assessor in assessor_list
      if not assessor["user"] == exclude_user_id
  ]
  if assessor_list and len(assessor_list) > 0:

    last_submitted_assessment = get_last_submitted_assessement_of_assessments(
        assessment_ids, exclude_user_id)

    if last_submitted_assessment:
      last_submitted_assessment = last_submitted_assessment.get_fields(
          reformat_datetime=True)
      if last_submitted_assessment["assessor_id"] is None:
        index = 0
      elif last_submitted_assessment[
          "assessor_id"] is not None and last_submitted_assessment[
              "assessor_id"] == assessor_list[-1]:
        index = 0
      else:
        if last_submitted_assessment["assessor_id"] not in assessor_list:
          index = 0
        else:
          index = (assessor_list.index(last_submitted_assessment\
                      ["assessor_id"]) + 1) %len(assessor_list)
    else:
      index = 0
    for sub_assessment in submitted_assessments:
      sub_assessment.assessor_id = assessor_list[index % len(assessor_list)]
      sub_assessment.assessor_session_id = ""
      sub_assessment.update()
      index += 1
  else:
    remove_assessor_for_submitted_assessments(submitted_assessments)

def filter_submitted_assessments(assessment_ids,
                        assessor_id: Optional[str] = None):
  """Filters non_evaluated submitted assessments based on assessment_ids and
   assessor_id"""
  collection_manager = collection_references["submitted_assessments"].collection
  collection_manager = collection_manager.filter("status", "==",
                                            "evaluation_pending")
  if assessor_id:
    collection_manager = collection_manager.filter("assessor_id", "==",
                            assessor_id)
  if len(assessment_ids) <= 30:
    collection_manager = collection_manager.filter("assessment_id", "in",
                                                   assessment_ids).fetch()
  else:
    collection_manager = collection_manager.fetch()
    collection_manager = [
        sub_assessment for sub_assessment in collection_manager
        if sub_assessment.assessement_id in assessment_ids
    ]
  return collection_manager

def get_all_assessments_of_a_discipline(discipline_id, collection_type,
                                        child_collection_type, assessment_ids):
  """This function is to traverse from curriculum_pathway with
  alias discipline to assessments and returns assessment ids"""
  node = collection_references[collection_type].find_by_uuid(discipline_id)
  node = node.get_fields(reformat_datetime=True)
  if node.get("child_nodes"):
    for cp_unit in node.get("child_nodes").get(child_collection_type, []):
      if collection_type == "curriculum_pathways" and node.get(
          "alias") == "discipline":
        get_all_assessments_of_a_discipline(cp_unit, child_collection_type,
                                            "learning_experiences",
                                            assessment_ids)
      elif collection_type == "curriculum_pathways" and node.get(
          "alias") == "unit":
        get_all_assessments_of_a_discipline(cp_unit, child_collection_type,
                                            "learning_objects", assessment_ids)
      elif collection_type == "learning_experiences":
        get_all_assessments_of_a_discipline(cp_unit, child_collection_type,
                                            "assessments", assessment_ids)
      elif collection_type == "learning_objects":
        assessment_ids.append(cp_unit)
  return assessment_ids

def traverse_down(uuid,level,child_level,res):
  """This function is to traverse from curriculum_pathway with
  alias discipline to assessments and returns assessment ids"""
  node = collection_references[level].find_by_uuid(uuid)
  node = node.get_fields(reformat_datetime=True)
  child_nodes =  node.get("child_nodes")
  if child_nodes:
    for child_node in node.get("child_nodes"):
      if child_node == child_level:
        res +=child_nodes[child_node]
      for cp_unit in child_nodes.get(child_node,[]):
        traverse_down(cp_unit,child_node,child_level,res)
  return res

def update_assessor_of_submitted_assessments_of_a_discipline(
  dag_id: str,
  discipline_id: str,
  input_assessor = None
):
  """Function to update assessor for submitted assessments of discipline"""
  assessor_id = None
  if input_assessor:
    assessor_id = input_assessor.get("user")
  assessment_ids = []
  assessment_ids = traverse_down(
      discipline_id, "curriculum_pathways", "assessments",assessment_ids)
  assessment_ids = list(set(assessment_ids))

  task_status = 0

  response_msg= "No assessments found for discipline "\
        f"with uuid {discipline_id}"
  if assessment_ids:
    submitted_assessments = filter_submitted_assessments(
                                        assessment_ids, assessor_id)
    if assessor_id:
      replace_assessor_of_submitted_assessments(
                  dag_id,submitted_assessments,
                  assessment_ids,assessor_id)
      task_status = 1
      response_msg = f"Successfully replaced assessor {assessor_id} "\
        f"for submitted assessments of discipline with uuid {discipline_id}."
    else:
      remove_assessor_for_submitted_assessments(submitted_assessments)
      task_status = 1
      response_msg = "Successfully unassigned assessor for all evaluation "\
      f"pending submitted assessments of discipline with uuid {discipline_id}"

  return task_status, response_msg
