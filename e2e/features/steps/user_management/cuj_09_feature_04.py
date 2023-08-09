"""
Feature: Adding users to the discipline association group
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import (AssociationGroup,
                            Learner,
                            User,
                            UserGroup,
                            CurriculumPathway,
                            LearningExperience,
                            LearningObject,
                            Assessment,
                            SubmittedAssessment)
from e2e.test_object_schemas import (TEST_USER,
                                  TEST_LEARNER,
                                  TEST_USER_GROUP,
                                  TEST_ASSOCIATION_GROUP,
                                  TEST_CURRICULUM_PATHWAY,
                                  TEST_ADD_USERS_ASSOCIATION_GROUP,
                                  TEST_LEARNING_EXPERIENCE,
                                  TEST_LEARNING_OBJECT,
                                  TEST_FINAL_ASSESSMENT,
                                  TEST_SUBMITTED_ASSESSMENT_INPUT)
from e2e.test_config import (API_URL_USER_MANAGEMENT,
                          DEL_KEYS,
                          API_URL_ASSESSMENT_SERVICE,
                          API_URL_LEARNING_OBJECT_SERVICE)
from e2e.setup import create_immutable_user_groups, post_method, get_method, set_cache, get_cache

ASSESSMENT_SERVICE_API_URI = f"{API_URL_ASSESSMENT_SERVICE}/submitted-assessment"
UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"


# Scenario: add the user into the discipline association group with the correct request payload
@behave.given("discipline association group already exist")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()

  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  #create a user of discipline type
  context.user_dict = {**TEST_USER, "user_type": "instructor"}
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]
  instructor_user_group_id = create_immutable_user_groups("instructor")
  user_group = UserGroup.find_by_uuid(instructor_user_group_id)
  setattr(user_group, 'users', [context.user_id])

  existing_user = User.find_by_uuid(context.user_id)
  setattr(existing_user, 'user_groups', [user_group.uuid])
  existing_user.update()

@behave.when(
    "an API request sent to add the user into the discipline association group with the correct request payload"
)
def step_impl_2(context):

  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then(
    "the corresponding discipline association group object will be updated and also contain the list of user"
)
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully added the users to the discipline association group"
  assert context.user_id in context.res_data["data"]["users"][0]["user"]


# Scenario: unable to add the user into the discipline association group with the incorrect request payload
@behave.given("discipline association group already exists")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"


@behave.when(
    "an API request sent to add the user into the discipline association group with an incorrect request payload"
)
def step_impl_2(context):

  add_users = {"users": ["user_id"], "status": "active"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then("a validation error will thrown")
def step_impl_3(context):

  assert context.res.status_code == 404
  assert context.res_data["success"] == False


# Scenario: unable to add the user into the discipline association group with the incorrect request payload
@behave.given("discipline association group already exists with a user added")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  context.user_dict = {**TEST_USER, "user_type": "instructor"}
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]
  instructor_user_group_id = create_immutable_user_groups("instructor")
  user_group = UserGroup.find_by_uuid(instructor_user_group_id)
  setattr(user_group, 'users', [context.user_id])

  existing_user = User.find_by_uuid(context.user_id)
  setattr(existing_user, 'user_groups', [user_group.uuid])
  existing_user.update()

  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"
  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()
  print(context.res_data)
  assert context.res.status_code == 200

@behave.when(
    "an API request sent to add the same existing user into the discipline association group"
) 
def step_impl_2(context):

  add_users = {"users": [context.user_id], "status": "active"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"

  context.res = post_method(url=context.url, request_body=add_users)
  context.res_data = context.res.json()


@behave.then("a validation error will be thrown")
def step_impl_3(context):

  assert context.res.status_code == 422
  assert context.res_data["success"] == False
  assert context.res_data["message"
      ] == f"User {context.user_id} is already present in the discipline association group"


# Scenario: remove the user from the discipline association group with the correct request payload
@behave.given("discipline association group is an already exist")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"

  #create a user of discipline type and add to the discipline group
  context.user_dict = {**TEST_USER, "user_type": "instructor"}
  context.user_dict["email"] = f"{uuid4()}@gmail.com"
  context.url = f"{API_URL_USER_MANAGEMENT}/user"
  context.post_user_res = post_method(
      url=context.url, request_body=context.user_dict)
  assert context.post_user_res.status_code == 200
  context.user_id = context.post_user_res.json()["data"]["user_id"]
  instructor_user_group_id = create_immutable_user_groups("instructor")
  user_group = UserGroup.find_by_uuid(instructor_user_group_id)
  setattr(user_group, 'users', [context.user_id])

  existing_user = User.find_by_uuid(context.user_id)
  setattr(existing_user, 'user_groups', [user_group.uuid])
  existing_user.update()

  # add created user to discipline association group
  req_body = deepcopy(TEST_ADD_USERS_ASSOCIATION_GROUP)
  req_body["users"] = [context.user_id]
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/users/add"
  context.res = post_method(url=context.url, request_body=req_body)
  context.res_data = context.res.json()
  assert context.res.status_code == 200
  assert context.res_data["success"] == True
  assert context.res_data[
      "message"] == "Successfully added the users to the discipline association group"


@behave.when(
    "an API request sent to remove the user from the discipline association group with the correct request payload"
)
def step_impl_2(context):

  remove_user = {"user": context.user_id}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then(
    "the user will remove from the corresponding discipline association group object"
)
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the user from the discipline association group"
  assert len(context.res_data["data"]["users"]) == 0


# Scenario: 
@behave.given("discipline association group already exists with a user of instructor type and discipline")
def step_impl_1(context):
  # Create Instructor
  email_1 = str(uuid4())
  user_dict_1 = {**TEST_USER}
  user_dict_1["email"] = f"{email_1}@gmail.com"
  user_dict_1["user_type"] = "instructor"
  user_dict_1["user_type_ref"] = ""
  user_1 = User.from_dict(user_dict_1)
  user_1.user_id = ""
  user_1.save()
  user_1.user_id = user_1.id
  user_1.update()
  user_dict_1["user_id"] = user_1.id
  context.instructor_id = user_1.user_id

  # Create Curriculum Pathway - Discipline
  pathway_dict = deepcopy(TEST_CURRICULUM_PATHWAY)

  pathway_dict["alias"] = "discipline"
  for key in DEL_KEYS:
    if key in pathway_dict:
      del pathway_dict[key]
  cp = CurriculumPathway.from_dict(pathway_dict)
  cp.uuid = ""
  cp.save()
  cp.uuid = cp.id
  cp.update()
  context.discipline_id = cp.id

  # Create discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  post_group = post_method(
      url=f"{UM_API_URL}/discipline-association", request_body=association_group_dict)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]
  assert post_group.status_code == 200

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = [{"user": context.instructor_id, "user_type": "instructor", "status": "active"}]
  group.associations = {
    "curriculum_pathways": [{"curriculum_pathway_id": context.discipline_id, "status": "active"}]
  }
  group.update()

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


@behave.when("an API request sent to remove the user of instructor type from the discipline association group with correct request payload")
def step_impl_2(context):

  remove_user = {"user": context.instructor_id}
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then("the user of instructor type will get removed from the corresponding discipline association group object")
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the user from the discipline association group"
  assert len(context.res_data["data"]["users"]) == 0


@behave.then("the instructor will also get removed from the Learner Association Group where it exists")
def step_impl_3(context):
  learner_group_url = f"{UM_API_URL}/learner-association/{context.learner_group_uuid}"
  get_response = get_method(learner_group_url)
  get_response_data = get_response.json()
  assert get_response.status_code == 200
  assert len(get_response_data["data"]["associations"]["instructors"]) == 0



# Scenario: unable to remove the user from the discipline association group with the incorrect request payload
@behave.given("discipline association group is already been exist")
def step_impl_1(context):

  # create an discipline association group
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = str(uuid4())
  context.request_body = association_group_dict
  context.url = f"{UM_API_URL}/discipline-association"
  context.res = post_method(url=context.url, request_body=context.request_body)
  context.res_data = context.res.json()
  context.discipline_association_uuid = context.res_data["data"]["uuid"]
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully created the association group"


@behave.when(
    "an API request sent to remove the user from the discipline association group with the incorrect request payload"
)
def step_impl_2(context):

  remove_user = {"user": "user_id"}
  context.url = f"{UM_API_URL}/discipline-association/{context.discipline_association_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()


@behave.then("a validations error is thrown")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data["success"] == False
  assert context.res_data["message"] == f"User with uuid user_id "\
        f"is not a part of Association Group with uuid {context.discipline_association_uuid}"

#----------------------------------------------------------
# Scenario: remove the user of assessor type from the discipline association 
#           group with the correct request payload when multiple assessors exists
#----------------------------------------------------------

@behave.given("discipline association group already exists with multiple users of assessor type and discipline")
def step_impl_1(context):
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

  # Create Assessor 2
  email_2 = str(uuid4())
  user_dict_2 = {**TEST_USER}
  user_dict_2["email"] = f"{email_2}@gmail.com"
  user_dict_2["user_type"] = "assessor"
  user_dict_2["user_type_ref"] = ""
  user_2 = User.from_dict(user_dict_2)
  user_2.user_id = ""
  user_2.save()
  user_2.user_id = user_2.id
  user_2.update()
  user_dict_2["user_id"] = user_2.id
  context.assessor_id_2 = user_2.user_id

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
                    "user": context.assessor_id_1,
                    "user_type": "assessor",
                    "status": "active"
                  },{
                    "user": context.assessor_id_2,
                    "user_type": "assessor",
                    "status": "active"
                  }
                ]
  group.associations = {
    "curriculum_pathways": [
                              {
                                "curriculum_pathway_id": context.discipline_id,
                                "status": "active"
                              }
                            ]
  }
  group.update()

  print("dag:")
  print(group.get_fields(reformat_datetime = True))

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

  print("before assessor removal")
  print(submitted_assessment.get_fields(reformat_datetime=True))

  set_cache("discipline_id", context.discipline_id)
  set_cache("assessor_2", context.assessor_id_2)
  set_cache("assessment_learner_id", context.learner_id)
  set_cache("group_id", context.group_uuid)
  set_cache("submitted_assessment_id", context.submitted_assessment_id)


@behave.when("an API request sent to remove a single user of assessor type from the discipline association group with correct request payload")
def step_impl_2(context):

  remove_user = {"user": context.assessor_id_1}
  context.url = f"{UM_API_URL}/discipline-association/{context.group_uuid}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()
  print(context.res_data)

@behave.then("the user of assessor type will get removed from the corresponding discipline association group object")
def step_impl_3(context):

  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the user from the discipline association group"
  assert len(context.res_data["data"]["users"]) == 1

@behave.then("the assessor will also get replaced from the Submitted Assessments of the same discipline where it exists")
def step_impl_4(context):
  submitted_assessment = SubmittedAssessment.find_by_uuid(context.submitted_assessment_id)
  submitted_assessment = submitted_assessment.get_fields(reformat_datetime = True)

  print("after assessor removal")
  print(submitted_assessment)

  assert submitted_assessment["assessor_id"] != context.assessor_id_1
  assert submitted_assessment["assessor_id"] == context.assessor_id_2
  


#----------------------------------------------------------
# Scenario: remove the user of assessor type from the discipline association
#           group with the correct request payload when single assessor exists
#----------------------------------------------------------

@behave.given("discipline association group already exists with single user of assessor type and discipline")
def step_impl_1(context):
  context.discipline_id = get_cache("discipline_id")
  context.assessor_id_2 = get_cache("assessor_2")
  context.learner_id = get_cache("assessment_learner_id")
  context.group_id = get_cache("group_id")
  context.submitted_assessment_id = get_cache("submitted_assessment_id")

@behave.when("an API request sent to remove the only user of assessor type from the discipline association group with correct request payload")
def step_impl_2(context):
  remove_user = {"user": context.assessor_id_2}
  context.url = f"{UM_API_URL}/discipline-association/{context.group_id}/user/remove"

  context.res = post_method(url=context.url, request_body=remove_user)
  context.res_data = context.res.json()

@behave.then("the only user of assessor type will get removed from the corresponding discipline association group object")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully removed the user from the discipline association group"
  assert len(context.res_data["data"]["users"]) == 0


@behave.then("the assessor will also get removed from the Submitted Assessments of the same discipline where it exists")
def step_impl_4(context):
  res = get_method(f"{API_URL_ASSESSMENT_SERVICE}/submitted-assessment/{context.submitted_assessment_id}")
  res_json = res.json()
  print(res_json)
  assert res.status_code == 200
  assert res_json["success"] == True
  assert res_json["message"] == "Successfully fetched the submitted assessment."
  assert res_json["data"]["assessor_id"] != context.assessor_id_2
  assert res_json["data"]["assessor_id"] == ""
