"""
Feature: Adding/Removing Discipline from Discipline Association Groups
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import (CurriculumPathway,
                            AssociationGroup,
                            User,
                            LearningExperience,
                            LearningObject,
                            Assessment,
                            SubmittedAssessment)
from e2e.test_object_schemas import (TEST_ASSOCIATION_GROUP,
                                  TEST_CURRICULUM_PATHWAY,
                                  TEST_USER,
                                  TEST_LEARNING_EXPERIENCE,
                                  TEST_LEARNING_OBJECT,
                                  TEST_FINAL_ASSESSMENT,
                                  TEST_SUBMITTED_ASSESSMENT_INPUT)
from e2e.test_config import (API_URL_USER_MANAGEMENT,
                          DEL_KEYS,
                          API_URL_ASSESSMENT_SERVICE)
from e2e.setup import post_method, get_method, put_method, delete_method

UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"

# Scenario : Add a Discipline to associations in an already created Discipline Association Group

@behave.given("A user has permission to user management and wants to add a discipline to the Discipline Association Group")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"

  cp_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.alias = "discipline"
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.cp_id = cp.id
  context.cp = cp

  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]


@behave.when("API request is sent to add a Discipline to the Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.request_body = {
    "curriculum_pathway_id": context.cp.id,
    "status": "active"
  }

  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will be updated in the database with updated association from the request payload")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status Code = {context.res.status_code}"
  assert context.res_data["message"] == "Successfully added the discipline to the association group", f"{context.res_data['message']}"
  association_group_uuid = context.res_data["data"]["uuid"]
  url = f"{UM_API_URL}/discipline-association/{association_group_uuid}"
  request = get_method(url)
  group_data = request.json()
  assert request.status_code == 200
  assert group_data["success"] is True
  assert group_data["message"] == "Successfully fetched the association group"
  assert group_data["data"]["associations"] == {"curriculum_pathways": [context.request_body]}


# --- Add a Discipline to associations in an already created Discipline Association Group with invalid Discipline Association Group ID ---
@behave.given("A user has permission to user management and wants to add a discipline to the Discipline Association Group with invalid ID")
def step_impl_1(context):
  context.association_group_uuid = "wrong_id"
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.request_body = {
    "curriculum_pathway_id": "abc",
    "status": "active"
  }

@behave.when("API request is sent to add a Discipline to the Discipline Association Group with correct request payload but invalid Discipline Association Group ID")
def step_impl_2(context):
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()


@behave.then("the API would raise ResourceNotFoundException")
def step_impl_3(context):
  assert context.res.status_code == 404


# --- Add a Discipline to associations in an already created Discipline Association Group with invalid request body ---
@behave.given("A user has permission to user management and wants to add a discipline to the Discipline Association Group with invalid request body")
def step_impl_1(context):
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]

@behave.when("API request is sent to add a Discipline to the Discipline Association Group with incorrect request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.request_body = {
    "curriculum_pathway_id": "abc",
    "status": "wrong_status"
  }
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()


@behave.then("the API would raise ValidationError")
def step_impl_3(context):
  assert context.res.status_code == 422


# --- Add a already associated Discipline to associations in an already created Discipline Association Group---
@behave.given("A user has permission to user management and wants to add an already associated discipline to the Discipline Association Group")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"

  cp_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.alias = "discipline"
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.cp_id = cp.id
  context.cp = cp

  context.payload = {"curriculum_pathway_id": cp.id, "status": "active"}
  context.request_body = association_group_dict

  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()

  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]

  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.res = post_method(url=context.url, request_body=context.payload)
  assert context.res.status_code == 200, "Association of Discipline failed"


@behave.when("API request is sent to add already associated Discipline to the Discipline Association Group")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("the API would raise ValidationError for the given discipline")
def step_impl_3(context):
  assert context.res.status_code == 422, f"Status Code = {context.res.status_code}"


# --- Remove a Discipline to associations in an already created Discipline Association Group---
@behave.given("A user has permission to user management and wants to remove a discipline to the Discipline Association Group")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  
  cp_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.alias = "discipline"
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.cp_id = cp.id
  context.cp = cp

  context.payload = {"curriculum_pathway_id": cp.id, "status": "active"}
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]

  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/add"
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Discipline Association to Group Failed"


@behave.when("API request is sent to remove a Discipline to the Discipline Association Group with correct request payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/remove"
  context.payload = {"curriculum_pathway_id": context.cp_id}
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("Discipline Association Group object will be updated in the database and the discipline will be removed")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status Code = {context.res.status_code}"
  assert context.res_data["data"]["associations"] == {"curriculum_pathways": []}, "Association not removed successfully"


# ---Remove a Discipline to associations in an already created Discipline Association Group with invalid association group ID---
@behave.given("A user has permission to user management and wants to remove a discipline to the Discipline Association Group with invalid association group ID")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = {"curriculum_pathway_id": "abc", "status": "active"}
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]


@behave.when("API request is sent to remove a Discipline to the Discipline Association Group with invalid assoication group ID")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/wrong_id/discipline/remove"
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("the API would raise ResourceNotFoundException with 404 status code")
def step_impl_3(context):
  assert context.res.status_code == 404, f"Status Code = {context.res.status_code}"


# ---Remove a Discipline to associations in an already created Discipline Association Group with invalid payload---
@behave.given("A user has permission to user management and wants to remove a discipline to the Discipline Association Group with invalid payload")
def step_impl_1(context):

  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association" 
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200, "Create Association Group Failed"
  context.association_group_uuid = context.res_data["data"]["uuid"]

  cp_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  cp = CurriculumPathway.from_dict(cp_dict)
  cp.alias = "discipline"
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.cp_id = cp.id
  context.cp = cp

@behave.when("API request is sent to remove a Discipline to the Discipline Association Group with invalid payload")
def step_impl_2(context):
  context.url = f"{UM_API_URL}/discipline-association/{context.association_group_uuid}/discipline/remove"
  context.payload = {"curriculum_pathway_id": context.cp_id}
  context.res = post_method(url=context.url, request_body=context.payload)
  context.res_data = context.res.json()


@behave.then("the API would raise ValidationError with 422 status code")
def step_impl_3(context):
  assert context.res.status_code == 422, f"Status Code = {context.res.status_code}"



# Scenario: Remove the Discipline from the discipline association group with the correct request payload
@behave.given("Discipline association group already exists with a user (instructor) actively associated to a discipline")
def step_impl_1(context):
  # Create Instructor
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "faculty"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.instructor_id = user_1.user_id

  # Create Assessor 1
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "assessor"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.assessor_id_1 = user_1.user_id

  # Create Learner
  email_3 = str(uuid4())
  user_dict_3 = {**TEST_USER}
  user_dict_3["email"] = f"{email_3}@gmail.com"
  for key in DEL_KEYS:
    if key in user_dict_3:
      del user_dict_3[key]

  res = post_method(
                    url = f"{API_URL_USER_MANAGEMENT}/user",
                    request_body=user_dict_3                
                  )
  assert res.status_code == 200
  res_json = res.json()
  context.learner_id = res_json["data"]["user_type_ref"]

  # Create Curriculum Pathway - Discipline
  pathway_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  pathway_dict["alias"] = "discipline"
  for key in DEL_KEYS:
    if key in pathway_dict:
      del pathway_dict[key]
  discipline = CurriculumPathway.from_dict(pathway_dict)
  discipline.uuid = ""
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()
  context.discipline_id = discipline.id

  # Create Unit
  pathway_dict = deepcopy(TEST_CURRICULUM_PATHWAY)
  pathway_dict["alias"] = "unit"
  for key in DEL_KEYS:
    if key in pathway_dict:
      del pathway_dict[key]
  unit = CurriculumPathway.from_dict(pathway_dict)
  unit.uuid = ""
  unit.save()
  unit.uuid = unit.id
  unit.parent_nodes = {"curriculum_pathways": [discipline.uuid]}
  unit.update()
  context.unit_id = unit.uuid

  discipline = CurriculumPathway.find_by_uuid(context.discipline_id)
  discipline.child_nodes["curriculum_pathways"] = [unit.uuid]
  discipline.update()

  # Create Learning Experience
  learning_experience_dict = deepcopy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in learning_experience_dict:
      del learning_experience_dict[key]
  le = LearningExperience.from_dict(learning_experience_dict)
  le.uuid = ""
  le.save()
  le.uuid = le.id
  le.parent_nodes={"curriculum_pathways": [unit.uuid]}
  le.update()
  context.le_id = le.uuid

  unit = CurriculumPathway.find_by_uuid(context.unit_id)
  unit.child_nodes["learning_experiences"] = [le.uuid]
  unit.update()

  # Create Learning Object
  learning_object_dict = deepcopy(TEST_LEARNING_OBJECT)
  for key in DEL_KEYS:
    if key in learning_object_dict:
      del learning_object_dict[key]
  lo = LearningObject.from_dict(learning_object_dict)
  lo.uuid = ""
  lo.save()
  lo.uuid = lo.id
  lo.parent_nodes = {"learning_experiences": [le.uuid]}
  lo.update()
  context.lo_id = lo.uuid

  le = LearningExperience.find_by_uuid(context.le_id)
  le.child_nodes["learning_objects"] = [lo.uuid]
  le.update()

  # Create Human Graded Assessment
  test_assessment = {**TEST_FINAL_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = ""
  assessment.parent_nodes = {"learning_objects": [context.lo_id]}
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_id = assessment.uuid

  lo = LearningObject.find_by_uuid(context.lo_id)
  lo.child_nodes["assessments"] = [context.assessment_id]
  lo.update()

  # Create discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [
                  {
                    "user": context.instructor_id,
                    "user_group_type": "instructor",
                    "status": "active"
                  },
                  {
                    "user": context.assessor_id_1,
                    "user_type": "assessor",
                    "status": "active"
                  }
                ]
  group.associations = {
    "curriculum_pathways": [{"curriculum_pathway_id": context.discipline_id, "status": "active"}]
  }
  group.update()

  # Create Submitted Assessment
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  submitted_assessment = SubmittedAssessment()
  submitted_assessment = submitted_assessment.from_dict(test_submission_request)
  submitted_assessment.assessment_id = context.assessment_id
  submitted_assessment.assessor_id = context.assessor_id_1
  submitted_assessment.learner_id = context.learner_id
  submitted_assessment.attempt_no = 1
  submitted_assessment.type = "project"
  submitted_assessment.uuid = ""
  submitted_assessment.status = "evaluation_pending"
  submitted_assessment.result = "Pass"
  submitted_assessment.is_autogradable = False
  submitted_assessment.save()
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()
  context.submitted_assessment_id = submitted_assessment.id

  # Create Learner association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Learner Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/learner-association", request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.learner_group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  learner_group = AssociationGroup.find_by_uuid(context.learner_group_uuid)
  learner_group.users = []
  learner_group.associations = {
    "instructors": [{"instructor": context.instructor_id,
                     "curriculum_pathway_id": context.discipline_id,
                     "status": "active"}],
    "coaches": []
  }
  learner_group.update()
  context.learner_group = learner_group


@behave.when("an API request sent to remove the Discipline from the discipline association group with correct request payload")
def step_impl_2(context):

  remove_discipline = {"curriculum_pathway_id": context.discipline_id}
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/discipline/remove"

  context.res = post_method(url=context.url, request_body=remove_discipline)
  context.res_data = context.res.json()


@behave.then("discipline will get removed from the corresponding discipline association group object")
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the discipline from the association group"
  assert len(context.res_data["data"]["associations"]["curriculum_pathways"]) == 0


@behave.then("the user of instructor type associated to the discipline will also get removed from all Learner Association Group where it exists")
def step_impl_3(context):
  learner_group_url = f"{UM_API_URL}/learner-association/{context.learner_group_uuid}"
  get_response = get_method(learner_group_url)
  get_response_data = get_response.json()
  assert get_response.status_code == 200
  assert len(get_response_data["data"]["associations"]["instructors"]) == 0

@behave.then("the user of assessor type associated to the discipline will also get removed from all submitted assessments where it exists")
def step_impl_4(context):
  res = get_method(f"{API_URL_ASSESSMENT_SERVICE}/submitted-assessment/{context.submitted_assessment_id}")
  res_json = res.json()
  print(res_json)
  assert res.status_code == 200
  assert res_json["success"] == True
  assert res_json["message"] == "Successfully fetched the submitted assessment."
  assert res_json["data"]["assessor_id"] != context.assessor_id_1
  assert res_json["data"]["assessor_id"] == ""
