"""
Feature 01 - CRUD for managing Submitted Assessment model in Assessment service
"""

import os
import sys
import behave

from uuid import uuid4
from copy import deepcopy
sys.path.append("../")

from common.models import (SubmittedAssessment, Assessment, Learner, User, AssociationGroup, CurriculumPathway, LearningExperience, LearningObject)
from e2e.setup import post_method, get_method, put_method, delete_method
from e2e.test_object_schemas import (TEST_CURRICULUM_PATHWAY,TEST_FINAL_ASSESSMENT, TEST_LEARNING_EXPERIENCE, TEST_LEARNING_OBJECT, TEST_PRACTICE_ASSESSMENT, TEST_LEARNER,
      TEST_ASSESSOR, TEST_INSTRUCTOR, TEST_SUBMITTED_ASSESSMENT_INPUT,
      TEST_UPDATE_SUBMITTED_ASSESSMENT, TEST_USER, TEST_ASSOCIATION_GROUP)
from e2e.test_config import (API_URL_ASSESSMENT_SERVICE, API_URL_USER_MANAGEMENT,
  TESTING_OBJECTS_PATH, API_URL_LEARNING_OBJECT_SERVICE)
from environment import (TEST_LEARNING_HIERARCHY_SIMPLIFIED_PATH)


API_URL = API_URL_ASSESSMENT_SERVICE
UM_API_URL = f"{API_URL_USER_MANAGEMENT}/association-groups"

global_sa_uuid = None


# ---------------------------POSITIVE----------------------------------------
# Scenario: Create a Submitted Assessment for existing learner and assessment 
# with correct request payload
@behave.given("that an existing student needs to answer an existing assessment")
def step_impl_1(context):
  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.uuid

  # create a User for the learner
  test_user = {**TEST_USER}
  user = User()
  user = user.from_dict(test_user)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.user_type_ref = learner.id
  user.update()

  # create a test assessor
  test_assessor = {**TEST_ASSESSOR}
  assessor = User()
  assessor = assessor.from_dict(test_assessor)
  assessor.user_id = ""
  assessor.save()
  assessor.user_id = assessor.id
  assessor.update()

  # -----------Ingesting Learning Hierarchy----------------

  with open(TEST_LEARNING_HIERARCHY_SIMPLIFIED_PATH, encoding="UTF-8") \
    as hierarchy_data:
    created_hierarchy = post_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import"
          f"/json", files={"json_file": hierarchy_data})
    assert created_hierarchy.status_code == 200, "Hierarchy Ingestion Failed"
    created_hierarchy = created_hierarchy.json()

  hierarchy_id = created_hierarchy["data"][0]
  hierarchy = get_method(
    url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{hierarchy_id}",
    query_params={"frontend_response": False, "fetch_tree": True})

  assert hierarchy.status_code == 200, f"Failed to Fetch the Learning " \
                                       f"Hierarchy for {hierarchy_id}"
  hierarchy = hierarchy.json()["data"]
  discipline_id = hierarchy["child_nodes"]["curriculum_pathways"][0][
    "child_nodes"]["curriculum_pathways"][0]["uuid"]
  los = hierarchy["child_nodes"]["curriculum_pathways"][0][
    "child_nodes"]["curriculum_pathways"][0]["child_nodes"][
    "curriculum_pathways"][0][
    "child_nodes"]["learning_experiences"][0]["child_nodes"]["learning_objects"]

  assessment_id = los[2]["child_nodes"]["assessments"][0]["uuid"]

  # -----------Creating Instructor & Assessor----------------

  users_uuids = []
  for i in range(5):
    users_dict = deepcopy(TEST_USER)
    users_dict["email"] = f"e2e-ag-{uuid4()}@gmail.com"

    post_users = post_method(url=f"{API_URL_USER_MANAGEMENT}/user",
                             request_body=users_dict)
    assert post_users.status_code == 200

    post_users_data = post_users.json()
    users_uuids.append(post_users_data["data"]["user_id"])

  users = []
  for i, uuid in enumerate(users_uuids):
    doc = {"user": uuid, "status": "active",
           "user_group_type": "assessor" if i % 2 == 1 else "instructor"}
    users.append(doc)

  # -----------create association group----------------

  associations = {
    "curriculum_pathways": [
      {
        "pathway_id": discipline_id,
        "status": "active"
      }
    ]
  }
  association_group_dict = deepcopy(TEST_ASSOCIATION_GROUP)
  association_group_dict["name"] = f"Discipline Association Group - {uuid4()}"
  context.payload = association_group_dict

  post_group = post_method(url=f"{UM_API_URL}/discipline-association",
                           request_body=context.payload)
  context.post_group_data = post_group.json()
  context.group_uuid = context.post_group_data["data"]["uuid"]

  group = AssociationGroup.find_by_uuid(context.group_uuid)
  group.users = users
  group.associations = associations
  group.update()

  # -----------Post Submit Assessment----------------

  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  context.submission_request = test_submission_request
  context.submission_request["assessment_id"] = assessment_id
  context.submission_request["learner_id"] = learner.id
  context.url = f"{API_URL}/submitted-assessment"


@behave.when("API request is sent to create a Submitted Assessment with "
             "correct request payload")
def step_impl_2(context):
  context.post_res = post_method(url=context.url,
                                 request_body=context.submission_request)
  context.post_res_data = context.post_res.json()


@behave.then("that Submitted Assessment object will be created in the database")
def step_impl_3(context):
  mes = "Successfully created the submitted assessment."
  mes_2 = "Successfully fetched the submitted assessment."

  assert context.post_res.status_code == 200
  assert context.post_res_data["message"] == mes

  submitted_assessment_uuid = context.post_res_data["data"]["uuid"]
  url = f"{API_URL}/submitted-assessment/{submitted_assessment_uuid}"
  get_res = get_method(url)
  get_res_data = get_res.json()
  global global_sa_uuid
  global_sa_uuid = submitted_assessment_uuid

  assert get_res.status_code == 200
  assert get_res_data["message"] == mes_2
  assert context.post_res_data["data"] == get_res_data["data"]


# -----------------------------NEGATIVE------------------------------------
# Scenario: Create a Submitted Assessment for nonexistent learner and assessment with correct request payload
@behave.given(
    "that a nonexistent student needs to answer a non-existent assessment"
)
def step_impl_1(context):

  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  # assign a random assesment which does not exist in the database
  test_submission_request["assessment_id"] = str(uuid4())
  # assign a random learner which does not exist in the database
  test_submission_request["learner_id"] = str(uuid4())
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"


@behave.when(
    "API request is sent to create Submitted Assessment with correct request payload"
)
def step_impl_2(context):
  context.res = post_method(
      url=context.url, request_body=context.submission_request)
  context.res_data = context.res.json()


@behave.then("that Submitted Assessment object will not be created and Assessment Service will throw a ResourceNotFound error")
def step_impl_3(context):
   assert context.res_data["success"] is False


# -----------------------------NEGATIVE------------------------------------
# Scenario: Create a Submitted Assessment for existing learner and assessment with incorrect request payload
@behave.given(
    "that an existing student wants to answer an existing assessment"
)
def step_impl_1(context):

  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  del test_submission_request["learner_session_id"]
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"


@behave.when(
    "API request is sent to create a Submitted Assessment with incorrect request payload"
)
def step_impl_2(context):
  context.res = post_method(
      url=context.url, request_body=context.submission_request)
  context.res_data = context.res.json()


@behave.then("that Submitted Assessment object will not be created and Assessment Service will throw a Validation error")
def step_impl_3(context):
   assert context.res_data["success"] is False


# -------------------------------POSITIVE------------------------------------
# Scenario: Fetch all the Submitted Assessments for an existing learner and assessment
@behave.given(
    "that an assessor has access to Assessment Service and need to fetch all the Submitted Assessments for an existing learner and assessment"
)
def step_impl_1(context):

  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.id

  # create learner's user
  test_learner_user = {**TEST_INSTRUCTOR}
  learner_user = User()
  learner_user = learner_user.from_dict(test_learner_user)
  learner_user.user_id = ""
  learner_user.user_type = "learner"
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # create a test assessor
  test_assessor = {**TEST_ASSESSOR}
  assessor = User()
  assessor = assessor.from_dict(test_assessor)
  assessor.user_id = ""
  assessor.user_type = "assessor"
  assessor.save()
  assessor.user_id = assessor.id
  assessor.update()

  # create an assessment
  test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.instructor_id = ""
  assessment.instructor_name = "Unassigned"
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_id = assessment.id

  context.submission_request["assessment_id"] = assessment.id
  context.submission_request["learner_id"] = learner.id
  context.res = post_method(
      url=context.url, request_body=context.submission_request)
  context.res_data = context.res.json()
  sa_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/submitted-assessment/{sa_id}/"+\
                f"learner/all-submissions"


@behave.when(
    "API request is sent to fetch all the Submitted Assessments with correct submitted assessment id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("all the Submitted Assessment objects for a learner for an assessment will be fetched")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status code is {context.res.status_code}"
  assert context.res_data[
      "message"] == "Successfully fetched the submitted assessments."
  assert context.res_data["data"]["records"][0]["assessment_id"] == \
    context.assessment_id
  assert context.res_data["data"]["records"][0]["learner_id"] == \
    context.learner_id


# -------------------------------NEGATIVE------------------------------------
# Scenario: Fetch all the Submitted Assessments for a non-existent learner and assessment
@behave.given(
    "that an assessor has access to Assessment Service and need to fetch all the Submitted Assessments for a non-existent learner and assessment"
)
def step_impl_1(context):

  submitted_assessment_uuid = str(uuid4())

  context.url = f"{API_URL}/submitted-assessment/{submitted_assessment_uuid}/"+\
                f"learner/all-submissions"


@behave.when(
    "API request is sent to fetch all the Submitted Assessments with incorrect submitted assessment id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("all the Submitted Assessment objects will not be fetched and Assessment Service will throw a ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False


# -------------------------------POSITIVE------------------------------------
# Scenario: Fetch the last Submitted Assessment for an existing learner and assessment
@behave.given(
    "that an assessor has access to Assessment Service and need to fetch the last Submitted Assessment for an existing learner and assessment"
)
def step_impl_1(context):
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.id

  # create a User for the learner
  test_user = {**TEST_USER}
  user = User()
  user = user.from_dict(test_user)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.user_type_ref = learner.id
  user.update()

  # create a test assessor
  test_assessor = {**TEST_ASSESSOR}
  assessor = User()
  assessor = assessor.from_dict(test_assessor)
  assessor.user_id = ""
  assessor.user_type = "assessor"
  assessor.save()
  assessor.user_id = assessor.id
  assessor.update()

  # create an assessment
  test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.instructor_id = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_id = assessment.id

  context.submission_request["assessment_id"] = assessment.id
  context.submission_request["learner_id"] = learner.id
  context.res = post_method(
      url=context.url, request_body=context.submission_request)
  context.res_data = context.res.json()
  sa_id = context.res_data["data"]["uuid"]
  context.url = f"{API_URL}/submitted-assessment/{sa_id}/"+\
                f"learner/latest-submission"


@behave.when(
    "API request is sent to fetch the Submitted Assessment with correct submitted assessment id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("the last Submitted Assessment object for a learner for an assessment will be fetched")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully fetched the submitted assessment."



# -------------------------------NEGATIVE------------------------------------
# Scenario: Fetch the last Submitted Assessment for a non-existent learner and assessment
@behave.given(
    "that an assessor has access to Assessment Service and need to fetch a Submitted Assessment for a non-existent learner and assessment"
)
def step_impl_1(context):

  submitted_assessment_uuid = str(uuid4())

  context.url = f"{API_URL}/submitted-assessment/{submitted_assessment_uuid}/"+\
                f"learner/latest-submission"


@behave.when(
    "API request is sent to fetch the Submitted Assessment with incorrect submitted assessment id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("the last Submitted Assessment object will not be fetched and Assessment Service will throw a ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False


# -------------------------------POSITIVE------------------------------------
# Scenario: Fetch a particular Submitted Assessment with correct id
@behave.given(
    "that an assessor has access to Assessment Service and want to fetch a Submitted Assessment"
)
def step_impl_1(context):

  # create a submitted assessment
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.id

  # create an instructor for the assessment
  test_instructor = {**TEST_INSTRUCTOR}
  instructor = User()
  instructor = instructor.from_dict(test_instructor)
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id
  instructor.user_type_ref = learner.id
  instructor.update()

  # create a test assessor
  test_assessor = {**TEST_ASSESSOR}
  assessor = User()
  assessor = assessor.from_dict(test_assessor)
  assessor.user_id = ""
  assessor.save()
  assessor.user_id = assessor.id
  assessor.update()

  # create an assessment
  test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.instructor_id = instructor.user_id
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_id = assessment.id

  context.submission_request["assessment_id"] = assessment.id
  context.submission_request["learner_id"] = learner.id
  post_res = post_method(
      url=context.url, request_body=test_submission_request)
  context.post_res_data = post_res.json()
  assert post_res.status_code == 200, "Submitted Assessment Creation Failed"

  submission_id = context.post_res_data["data"]["uuid"]

  context.url = f"{API_URL}/submitted-assessment/{submission_id}"


@behave.when(
    "API request is sent to fetch the Submitted Assessment with correct id"
)
def step_impl_2(context):
  context.get_res = get_method(url=context.url)
  context.get_res_data = context.get_res.json()


@behave.then("the Submitted Assessment object will be fetched")
def step_impl_3(context):
  assert context.get_res.status_code == 200
  assert context.get_res_data[
      "message"] == "Successfully fetched the submitted assessment."
  assert context.post_res_data["data"] == context.get_res_data["data"]



# -------------------------------NEGATIVE------------------------------------
# Scenario: Fetch a particular Submitted Assessment with incorrect id
@behave.given(
    "that an assessor has access to Assessment Service and need to fetch a Submitted Assessment"
)
def step_impl_1(context):

  submission_id = str(uuid4())

  context.url = f"{API_URL}/submitted-assessment/{submission_id}"


@behave.when(
    "API request is sent to fetch the Submitted Assessment with incorrect id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("the Submitted Assessment object will not be fetched and Assessment Service will throw a ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False



# -------------------------------POSITIVE------------------------------------
# Scenario: Update a particular Submitted Assessment with correct id
@behave.given(
    "that an assessor has access to Assessment Service and wants to update a Submitted Assessment"
)
def step_impl_1(context):

  # create a submitted assessment
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.id

  # create an instructor for the assessment
  test_instructor = {**TEST_INSTRUCTOR}
  instructor = User()
  instructor = instructor.from_dict(test_instructor)
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id
  instructor.user_type_ref = learner.id
  instructor.update()

  # create a test assessor
  test_assessor = {**TEST_ASSESSOR}
  assessor = User()
  assessor = assessor.from_dict(test_assessor)
  assessor.user_id = ""
  assessor.save()
  assessor.user_id = assessor.id
  assessor.update()

  # create an assessment
  test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.instructor_id = instructor.user_id
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_id = assessment.id

  context.submission_request["assessment_id"] = assessment.id
  context.submission_request["learner_id"] = learner.id
  post_res = post_method(
      url=context.url, request_body=test_submission_request)
  context.post_res_data = post_res.json()
  assert post_res.status_code == 200, "Submitted Assessment Creation Failed"
  submission_id = context.post_res_data["data"]["uuid"]
  context.update_submission_request = {**TEST_UPDATE_SUBMITTED_ASSESSMENT}
  context.url = f"{API_URL}/submitted-assessment/{submission_id}"


@behave.when(
    "API request is sent to update the Submitted Assessment with correct id"
)
def step_impl_2(context):
  context.res = put_method(
    url=context.url, request_body=context.update_submission_request)
  context.res_data = context.res.json()


@behave.then("the Submitted Assessment object will be updated in the database")
def step_impl_3(context):
  context.res.status_code
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully updated the submitted assessment."



# -------------------------------NEGATIVE------------------------------------
# Scenario: Update a particular Submitted Assessment with incorrect id
@behave.given(
    "that an assessor has access to Assessment Service and need to update a Submitted Assessment"
)
def step_impl_1(context):

  submission_id = str(uuid4())

  context.update_submission_request = {**TEST_UPDATE_SUBMITTED_ASSESSMENT}

  context.url = f"{API_URL}/submitted-assessment/{submission_id}"


@behave.when(
    "API request is sent to update the Submitted Assessment with incorrect id"
)
def step_impl_2(context):
  context.res = put_method(
    url=context.url, request_body=context.update_submission_request)
  context.res_data = context.res.json()


@behave.then("the Submitted Assessment object will not be updated and Assessment Service will throw a ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False


# -------------------------------POSITIVE------------------------------------
# Scenario: Delete a particular Submitted Assessment with correct id
@behave.given(
    "that an assessor has access to Assessment Service and want to delete a Submitted Assessment"
)
def step_impl_1(context):

  # create a submitted assessment
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.id

  # create an instructor for the assessment
  test_instructor = {**TEST_INSTRUCTOR}
  instructor = User()
  instructor = instructor.from_dict(test_instructor)
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id
  instructor.user_type_ref = learner.id
  instructor.update()

  # create a test assessor
  test_assessor = {**TEST_ASSESSOR}
  assessor = User()
  assessor = assessor.from_dict(test_assessor)
  assessor.user_id = ""
  assessor.save()
  assessor.user_id = assessor.id
  assessor.update()

  # create an assessment
  test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.instructor_id = instructor.user_id
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_id = assessment.id

  context.submission_request["assessment_id"] = assessment.id
  context.submission_request["learner_id"] = learner.id
  post_res = post_method(
      url=context.url, request_body=test_submission_request)
  context.post_res_data = post_res.json()
  assert post_res.status_code == 200, "Submitted Assessment Creation Failed"
  context.submission_id = context.post_res_data["data"]["uuid"]
  context.delete_url = f"{API_URL}/submitted-assessment/{context.submission_id}"


@behave.when(
    "API request is sent to delete the Submitted Assessment with correct id"
)
def step_impl_2(context):
  context.res = delete_method(url=context.delete_url)
  context.res_data = context.res.json()


@behave.then("the Submitted Assessment object will be deleted from the database")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully deleted the submitted assessment."
  # check if the submitted assessment exists
  get_url = f"{API_URL}/submitted-assessment/{context.submission_id}"
  get_res = get_method(url=get_url)
  get_res_data = get_res.json()
  assert get_res_data["success"] is False


# -------------------------------NEGATIVE------------------------------------
# Scenario: Delete a particular Submitted Assessment with incorrect id
@behave.given(
    "that an assessor has access to Assessment Service and need to delete a Submitted Assessment"
)
def step_impl_1(context):

  submission_id = str(uuid4())
  context.url = f"{API_URL}/submitted-assessment/{submission_id}"


@behave.when(
    "API request is sent to delete the Submitted Assessment with incorrect id"
)
def step_impl_2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("the Submitted Assessment object will not be deleted and Assessment Service will throw a ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False

# ---------------------------POSITIVE----------------------------------------
# Scenario: Assigning the assessor id while 
# ceating a Submitted Assessment for 
# existing learner and assessment 
@behave.given(
    "that an existing student needs to answer existing assessment"
)
def step_impl_1(context):

  # create a submitted assessment
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"

  # create a learner
  test_learner = {**TEST_LEARNER,"email":f"{uuid4()}@gmail.com"}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.id

  # create an instructor for the assessment
  test_instructor = {**TEST_INSTRUCTOR,"email":f"{uuid4()}@gmail.com"}
  instructor = User()
  instructor = instructor.from_dict(test_instructor)
  instructor.user_id = ""
  instructor.user_type = "instructor"
  instructor.save()
  instructor.user_id = instructor.id
  instructor.user_type_ref = learner.id
  instructor.update()

  # create a test assessor
  test_assessor = {**TEST_ASSESSOR, "email":f"{uuid4()}@gmail.com"}
  assessor = User()
  assessor = assessor.from_dict(test_assessor)
  assessor.user_id = ""
  assessor.user_type = "assessor"
  assessor.save()
  assessor.user_id = assessor.id
  assessor.update()

  # create an assessment
  test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.instructor_id = instructor.user_id
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_id = assessment.id
  context.submission_request["assessment_id"] = context.assessment_id
  context.submission_request["learner_id"] = instructor.user_type_ref

  api_url = f"{API_URL_USER_MANAGEMENT}/users"
  query_params = {"skip": 0, "limit": 30, "user_type": "assessor"}

  assessors = get_method(
      url=api_url,
      query_params=query_params)
  
  context.assessor_list = []
  if assessors.status_code == 200:
    assessor_list = assessors.json()
    context.assessor_list = [assessor["user_id"] for assessor in assessor_list["data"]["records"]]

@behave.when(
    "API request is sent to create a Submitted Assessment with correct request payload. Assessor will automatically get added from the list of available assessor using round robin algorithm"
)
def step_impl_2(context):
  context.post_res = post_method(
      url=context.url, request_body=context.submission_request)
  context.post_res_data = context.post_res.json()

@behave.then("that Submitted Assessment object having assessor id will be created")
def step_impl_3(context):
  assert context.post_res.status_code == 200
  assert context.post_res_data[
      "message"] == "Successfully created the submitted assessment."
  # FIXME: This cannot be validated as all assessments are marked autogradable
  # and autogradable assessments are not assigned assessors
  assert context.post_res_data["data"]["assessor_id"] is None
