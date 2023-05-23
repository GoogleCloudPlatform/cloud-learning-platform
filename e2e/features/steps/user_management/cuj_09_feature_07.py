"""
Feature: Adding/Removing Discipline from Discipline Association Groups
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import CurriculumPathway, User, AssociationGroup
from e2e.test_object_schemas import TEST_ASSOCIATION_GROUP, TEST_CURRICULUM_PATHWAY, TEST_USER
from e2e.test_config import API_URL_USER_MANAGEMENT
from e2e.setup import post_method, get_method, put_method, delete_method

UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"

# Scenario : Update all association groups with active program ID and its discipline IDs

@behave.given("A user has permission to user management to update all association groups with new active program ID")
def step_impl_1(context):

  # Preparing Instructor Data
  user_dict = deepcopy(TEST_USER)
  context.user = User.from_dict(user_dict)
  context.user.user_id = ""
  context.user.user_type = "instructor"
  context.user.user_type_ref = ""
  context.user.save()
  context.user.user_id = context.user.id
  context.user.update()
  context.users = [{"user": context.user.user_id, "status": "active"}]

  # Prepare Data for one program and discipline
  program_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.program = CurriculumPathway.from_dict(program_dict)
  context.program.uuid = ""
  context.program.alias = "program"
  context.program.is_active = True
  context.program.save()
  context.program.uuid = context.program.id
  context.program.update()

  discipline_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.discipline = CurriculumPathway.from_dict(discipline_dict)
  context.discipline.uuid = ""
  context.discipline.alias = "discipline"
  context.discipline.save()
  context.discipline.uuid = context.discipline.id
  context.discipline.parent_nodes = {"curriculum_pathways": [context.program.id]}
  context.discipline.update()

  context.program.child_nodes = {"curriculum_pathways": [context.discipline.id]}
  context.program.update()

  # Preparing Association Group Data
  # Discipline Association Group
  discipline_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  context.discipline_group = AssociationGroup.from_dict(discipline_group_dict)
  context.discipline_group.uuid = ""
  context.discipline_group.association_type = "discipline"
  context.discipline_group.users = context.users
  context.discipline_group.associations = {"curriculum_pathways":[
    {"curriculum_pathway_id": context.discipline.id, "status": "active"}]
    }
  context.discipline_group.save()
  context.discipline_group.uuid = context.discipline_group.id
  context.discipline_group.update()

  # Learner Association Group
  learner_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  context.learner_group = AssociationGroup.from_dict(learner_group_dict)
  context.learner_group.uuid = ""
  context.learner_group.association_type = "learner"
  context.learner_group.save()
  context.learner_group.associations = {
    "instructors": [{"instructor": context.user.id,
                     "curriculum_pathway_id": context.discipline.id,
                     "status": "active"}],
    "curriculum_pathway_id": context.program.id
  }
  context.learner_group.uuid = context.learner_group.id
  context.learner_group.update()

  # Preparing Data for program2
  program2_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.program2 = CurriculumPathway.from_dict(program2_dict)
  context.program2.uuid = ""
  context.program2.alias = "program"
  context.program2.is_active = True
  context.program2.save()
  context.program2.uuid = context.program2.id
  context.program2.update()

  discipline2_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  context.discipline2 = CurriculumPathway.from_dict(discipline2_dict)
  context.discipline2.uuid = ""
  context.discipline2.alias = "discipline"
  context.discipline2.save()
  context.discipline2.uuid = context.discipline2.id
  context.discipline2.parent_nodes = {"curriculum_pathways": [context.program2.id]}
  context.discipline2.update()

  context.program2.child_nodes = {"curriculum_pathways": [context.discipline.id]}
  context.program2.update()


@behave.when("API request is sent to update all association groups with the new program ID and its disciplines")
def step_impl_2(context):
  context.input_request = {
    "program_id": context.program2.id,
    "disciplines": [{"uuid": context.discipline2.id,
                     "name": context.discipline2.name,
                     "alias": context.discipline2.alias}]
  }
  context.program.is_active = False
  context.program.update()

  context.url = f"{UM_API_URL}/active-curriculum-pathway/update-all"
  context.resp = put_method(url=context.url, request_body=context.input_request)
  context.response = context.resp.json()


@behave.then("All association groups are updated with the new active program ID and its discipline IDs")
def step_impl_3(context):
  context.resp.status_code == 200, f"Status code = {context.resp.status_code}, not 200"
  context.response["data"] == [context.learner_group, context.discipline_group], f"{context.response['data']}"
  
  learner_group = AssociationGroup.find_by_uuid(context.learner_group.id)
  learner_group_associations = learner_group.associations
  assert learner_group_associations["curriculum_pathway_id"] == context.program2.id, f"{learner_group_associations} ---------------- {context.program2.id}"
  instructors = [{
    "instructor": context.user.id,
    "curriculum_pathway_id": context.discipline2.id,
    "status": "active"
  }]
  assert learner_group_associations["instructors"] == instructors, f"{learner_group_associations} ----------------- {instructors}"
  
  discipline_group = AssociationGroup.find_by_uuid(context.discipline_group.id)
  discipline_group_associations = discipline_group.associations
  discipline_associations = [{"curriculum_pathway_id": context.discipline2.id, "status": "active"}]
  assert discipline_group_associations["curriculum_pathways"] == discipline_associations, f"{discipline_group_associations} -----------------, {discipline_associations}"
