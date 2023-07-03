"""
Feature 02 - Filter and Search on SubmittedAssessment in Assessment services
"""

import sys
import os
import json
import copy
import behave
from uuid import uuid4
sys.path.append("../")
from common.models import (Assessment, Learner, User, SubmittedAssessment,
                          LearningExperience, LearningObject)
from e2e.setup import post_method, get_method, put_method, delete_method
from e2e.test_object_schemas import (TEST_PRACTICE_ASSESSMENT, TEST_LEARNER,
      TEST_SUBMITTED_ASSESSMENT_INPUT, TEST_ASSESSOR, TEST_USER,
      TEST_LEARNING_EXPERIENCE, TEST_FINAL_ASSESSMENT, TEST_INSTRUCTOR,
      TEST_LEARNING_OBJECT)
from e2e.test_config import API_URL_ASSESSMENT_SERVICE


API_URL = API_URL_ASSESSMENT_SERVICE


# ---------------------------POSITIVE----------------------------------------
# Scenario: Fetch list of all SubmittedAssessments submitted by a learner
@behave.given(
    "that an existing student has submitted a bunch of assessments"
)
def step_impl_1(context):

  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  context.submission_request = test_submission_request
  context.url = f"{API_URL}/submitted-assessment"

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.uuid

  # create an instructor for the assessment
  test_instructor = {**TEST_INSTRUCTOR}
  instructor = User()
  instructor = instructor.from_dict(test_instructor)
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id
  instructor.user_type_ref = learner.id
  instructor.update()

  # create an assessment
  test_assessment = {**TEST_PRACTICE_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.instructor_id = instructor.user_id
  assessment.update()

  context.submission_request["assessment_id"] = assessment.uuid

  context.submission_request["learner_id"] = context.learner_id
  #SubmittedAssessment1
  sa1 = SubmittedAssessment()
  sa1 = sa1.from_dict(context.submission_request)
  sa1.uuid = ""
  sa1.save()
  sa1.uuid = sa1.id
  sa1.update()
  #SubmittedAssessment2
  sa2 = SubmittedAssessment()
  sa2 = sa2.from_dict(context.submission_request)
  sa2.uuid = ""
  sa2.save()
  sa2.uuid = sa2.id
  sa2.update()


@behave.when(
    "API request is sent to fetch list of all SubmittedAssessments by that learner"
)
def step_impl_2(context):
  context.get_url = f"{API_URL}/learner/{context.learner_id}/submitted-assessments"
  context.get_res = get_method(url=context.get_url, query_params={"limit": 2})
  context.get_res_data = context.get_res.json()

@behave.then("the API gives response with the list of all SubmittedAssessments for that learner")
def step_impl_3(context):
  print("!!!!!!!!!!")
  print(context.get_res)
  print(context.get_res_data)
  assert context.get_res.status_code == 200
  assert context.get_res_data[
      "message"] == "Successfully fetched the submitted assessments"
  assert len(context.get_res_data["data"]) == 2


# -----------------------------NEGATIVE------------------------------------
# Scenario: Fetch list of all SubmittedAssessments submitted by a learner when leaner id is not found
@behave.given(
    "that a student has submitted a bunch of assessments but the learner id is not created for the student"
)
def step_impl_1(context):

  context.learner_id = "Random ID"
  context.url = f"{API_URL}/learner/{context.learner_id}/submitted-assessments"

@behave.when(
    "API request is sent to fetch list of all SubmittedAssessments by that learner for the given learner id"
)
def step_impl_2(context):
  context.res = get_method(
      url=context.url)
  context.res_data = context.res.json()


@behave.then("the API gives ResourceNotFound Exception as the learner id does not exist")
def step_impl_3(context):
   assert context.res.status_code == 404
   assert context.res_data["success"] is False


# ---------------------------POSITIVE----------------------------------------
# Scenario: Fetch unique values of type, result and competency for all manually graded submitted assessments assigned to an existing assessor
@behave.given(
    "that an assessor has access to Assessment Service and wants to fetch all the unique values of type, result and competency for all manually graded submitted assessments assigned to an assessor"
)
def step_impl_1(context):

  # create url and incorrect query parameters for filter api
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  test_user = {**TEST_USER, "user_type":"assessor"}
  test_learning_experience = {**TEST_LEARNING_EXPERIENCE}
  test_learning_object = {**TEST_LEARNING_OBJECT}

  # create an assesssment
  test_assessment = {**TEST_FINAL_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()

  # create a user
  user = User()
  user = user.from_dict(test_user)
  user.user_type_ref = learner.id
  user.user_id = ""
  user.save()
  user.user_id = user.id 
  user.update()
  
  # create a learning experience
  learning_experience = LearningExperience()
  learning_experience = learning_experience.from_dict(test_learning_experience)
  learning_experience.uuid = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  # create a learning object
  learning_object = LearningObject()
  learning_object = learning_object.from_dict(test_learning_object)
  learning_object.child_nodes = {"assessments": [assessment.id]}
  learning_object.parent_nodes = {
    "learning_experiences": [learning_experience.id]}
  learning_object.uuid = ""
  learning_object.save()
  learning_object.uuid = learning_object.id
  learning_object.update()

  # update child node of learning experience
  learning_experience.child_nodes = {"learning_objects": [learning_object.id]}
  learning_experience.update()

  assessment.parent_nodes = {"learning_objects": [learning_object.id]}
  assessment.instructor_id = user.id
  assessment.update()

  # create a submitted assessment for assessment1
  submitted_assessment = SubmittedAssessment()
  submitted_assessment = submitted_assessment.from_dict(test_submission_request)
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.assessor_id = user.id
  submitted_assessment.learner_id = learner.id
  submitted_assessment.attempt_no = 1
  submitted_assessment.type = "project"
  submitted_assessment.uuid = ""
  submitted_assessment.status = "completed"
  submitted_assessment.result = "Pass"
  submitted_assessment.is_autogradable = False
  submitted_assessment.save()
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()
  
  # create url and correct query parameters to fetch unique values for
  # competency, type and result
  context.unit_name = learning_experience.name
  context.result = submitted_assessment.result
  context.type = assessment.type
  context.url = f"{API_URL}/submitted-assessments/unique"
  context.query_params = {
      "assessor_id": [user.id],
      "is_autogradable": submitted_assessment.is_autogradable,
      "status": submitted_assessment.status
    }

@behave.when(
    "API request is sent to fetch the unique values with correct assessor id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
      "all the unique values of type, result and competency for all manually graded submitted assessments assigned to the assessor are returned")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully fetched the unique values for submitted assessments."
  assert context.unit_name in context.res_data.get("data")["unit_names"], \
    f"""{set(context.res_data.get("data")["unit_names"])} ---------- {set([context.unit_name])}"""
  assert context.type in context.res_data.get("data")["types"], \
    f"""{set(context.res_data.get("data")["types"])} ========== {set([context.type])}"""
  assert context.result in context.res_data.get("data")["results"], \
    f"""{set(context.res_data.get("data")["results"])} :::::::::: {set([context.result])}""" 


# ---------------------------NEGATIVE----------------------------------------
# Scenario: Fetch unique values of type, result and competency for all manually graded submitted assessments assigned to a nonexistant assessor
@behave.given(
    "that an assessor has access to Assessment Service and needs to fetch all the unique values of type, result and competency for all manually graded submitted assessments assigned to an assessor"
)
def step_impl_1(context):
  
  assessor_id = str(uuid4())
  # create url and correct query parameters to fetch unique values for
  # competency, type and result
  context.url = f"{API_URL}/submitted-assessments/unique"
  context.query_params = {
    "assessor_id": assessor_id,
    "is_autogradable": False
  }


@behave.when(
    "API request is sent to fetch the unique values with incorrect assessor id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
      "the unique values of type, result and competency will not be fetched and Assessment Service will throw a ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False


# ---------------------------POSITIVE----------------------------------------
# Scenario: Filter manual graded Submitted Assessments assigned to an existing assessor based on type and result and ascending sort by time to review with correct skip and limit values
@behave.given(
    "that an existing assessor has access to Assessment Service and wants to fetch all the manual graded Submitted Assessments assigned to him based on a list of type and result and sorted by time to review in ascending order"
)
def step_impl_1(context):

  # create url and incorrect query parameters for filter api
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  test_user = {**TEST_USER, "user_type":"assessor"}
  test_learning_experience = {**TEST_LEARNING_EXPERIENCE}

  # create an assesssment
  test_assessment = {**TEST_FINAL_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_name = assessment.display_name

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()

  # create a user
  user = User()
  user = user.from_dict(test_user)
  user.user_type_ref = learner.id
  user.user_id = ""
  user.save()
  user.user_id = user.id 
  user.update()
  
  # create a learning experience
  learning_experience = LearningExperience()
  learning_experience = learning_experience.from_dict(test_learning_experience)
  learning_experience.child_nodes = {"assessments": [assessment.id]}
  learning_experience.uuid = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  assessment.parent_nodes = {"learning_experiences": [learning_experience.id]}
  assessment.instructor_id = user.id
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()

  # create a submitted assessment for assessment1
  submitted_assessment = SubmittedAssessment()
  submitted_assessment = submitted_assessment.from_dict(test_submission_request)
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.assessor_id = user.id
  submitted_assessment.learner_id = learner.id
  submitted_assessment.type = "project"
  submitted_assessment.attempt_no = 1
  submitted_assessment.uuid = ""
  submitted_assessment.status = "evaluated"
  submitted_assessment.is_autogradable = False
  submitted_assessment.result = "Pass"
  submitted_assessment.save()
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()
  
  # create url and correct query parameters for filter api
  context.url = f"{API_URL}/submitted-assessments"
  context.query_params = {"result": [submitted_assessment.result],
                          "type": [assessment.type],
                          "assessor_id": [user.id],
                          "is_autogradable":
                            submitted_assessment.is_autogradable}


@behave.when(
    "API request is sent to fetch filtered Submitted Assessments assigned to the assessor with correct skip and limit value"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
      "all the manual graded Submitted Assessments objects assigned to the assessor containing that type and result are fetched in ascending order of time to review")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data[
      "message"] == "Successfully fetched the submitted assessments."
  assert context.res_data["data"][0]["assessor_id"] == \
    context.query_params["assessor_id"][0]
  assert context.res_data["data"][0]["result"] == \
    context.query_params["result"][0]
  assert context.res_data["data"][0]["type"] == \
    context.query_params["type"][0]
  assert context.res_data["data"][0]["is_autogradable"] == \
    context.query_params["is_autogradable"][0]
  assert context.res_data["data"][0]["assessment_name"] == \
    context.assessment_name


# ---------------------------POSITIVE----------------------------------------
# Scenario: Filter on type and result and search on name and ascending sort by time to review for manual graded Submitted Assessments assigned to an existing assessor with correct skip and limit values
@behave.given(
    "that an existing assessor has access to Assessment Service and wants to fetch the manual graded Submitted Assessments assigned to him by filtering on a list of type and result and searching on name and sorted by time to review in ascending order"
)
def step_impl_1(context):

  # create url and incorrect query parameters for filter api
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  test_user = {**TEST_USER, "user_type":"assessor"}
  test_learning_experience = {**TEST_LEARNING_EXPERIENCE}

  # create an assesssment
  test_assessment = {**TEST_FINAL_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_name = assessment.display_name

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()

  # create a user
  user = User()
  user = user.from_dict(test_user)
  user.user_type_ref = learner.id
  user.user_id = ""
  user.save()
  user.user_id = user.id 
  user.update()
  
  # create a learning experience
  learning_experience = LearningExperience()
  learning_experience = learning_experience.from_dict(test_learning_experience)
  learning_experience.child_nodes = {"assessments": [assessment.id]}
  learning_experience.uuid = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  assessment.parent_nodes = {"learning_experiences": [learning_experience.id]}
  assessment.instructor_id = user.id
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()

  # create a submitted assessment for assessment1
  submitted_assessment = SubmittedAssessment()
  submitted_assessment = submitted_assessment.from_dict(test_submission_request)
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.type = "project"
  submitted_assessment.assessor_id = user.id
  submitted_assessment.learner_id = learner.id
  submitted_assessment.attempt_no = 1
  submitted_assessment.uuid = ""
  submitted_assessment.status = "evaluated"
  submitted_assessment.result = "Pass"
  submitted_assessment.is_autogradable = False
  submitted_assessment.save()
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  # create url and correct query parameters for filter api
  context.url = f"{API_URL}/submitted-assessments"
  context.query_params = {"status": [submitted_assessment.status],
                          "type": [assessment.type],
                          "assessor_id": [user.id],
                          "is_autogradable":
                              submitted_assessment.is_autogradable}


@behave.when(
    "API request is sent to fetch filtered and searched Submitted Assessments assigned to an assessor with correct skip and limit value"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
      "all the manual graded Submitted Assessments objects assigned to the assessor containing that type, result and name are fetched in ascending order of time to review")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status is {context.res.status_code}"
  assert context.res_data[
      "message"] == "Successfully fetched the submitted assessments."
  assert context.res_data["data"]["records"][0]["assessor_id"] == \
    context.query_params["assessor_id"][0]
  assert context.res_data["data"]["records"][0]["status"] == \
    context.query_params["status"][0]
  assert context.res_data["data"]["records"][0]["type"] == \
    context.query_params["type"][0]
  assert context.res_data["data"]["records"][0]["is_autogradable"] == \
    context.query_params["is_autogradable"][0]
  assert context.res_data["data"]["records"][0]["assessment_name"] == \
    context.assessment_name


# ---------------------------NEGATIVE----------------------------------------
# Scenario: Filter/Search Submitted Assessments assigned to an existing assessor with incorrect skip and limit values
@behave.given(
    "that an existing assessor has access to Assessment Service and needs to fetch all the filtered/searched Submitted Assessments assigned to him"
)
def step_impl_1(context):
  # create url and incorrect query parameters for filter api
  context.url = f"{API_URL}/submitted-assessments"
  context.query_params = {"skip": -1, "limit": 2}

@behave.when(
    "API request is sent to fetch filtered/searched Submitted Assessments assigned to him with incorrect skip and limit value"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
      "the Submitted Assessment objects assigned to him will not be fetched and Assessment Service will throw a Validation error")
def step_impl_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get("message") == \
    "Validation Failed", \
    "unknown response received"
  assert context.res_data["success"] == False


# ---------------------------NEGATIVE----------------------------------------
# Scenario: Filter/Search Submitted Assessments assigned to a nonexisting assessor with correct skip and limit values
@behave.given(
    "that a nonexisting assessor has access to Assessment Service and needs to fetch all the filtered/searched Submitted Assessments assigned to him"
)
def step_impl_1(context):
  random_assessor_id = str(uuid4())
  # create url and incorrect query parameters for filter api
  context.url = f"{API_URL}/submitted-assessments"
  context.query_params = {"assessor_id": random_assessor_id}

@behave.when(
    "API request is sent to fetch filtered/searched Submitted Assessments assigned to him with correct skip and limit value"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()

@behave.then(
      "the Submitted Assessment objects assigned to him will not be not be fetched and Assessment Service will throw a ResourceNotFound error")
def step_impl_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False


# Assessor wants to see the list of submitted assessments sorted by ascending order for time to review that are required by the assessor to evaluate
# ---------------------------POSITIVE----------------------------------------
@behave.given(
    "that an assessor has access to Assessment Service and wants to fetch the Submitted Assessments that are required to be evaulated sorted by ascending order for time to review"
)
def step_impl_1(context):
  # create url and incorrect query parameters for filter api
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  test_user = {**TEST_USER, "user_type":"assessor"}
  test_learning_experience = {**TEST_LEARNING_EXPERIENCE}

  # create an assesssment
  test_assessment = {**TEST_FINAL_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()
  context.assessment_name = assessment.display_name

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()

  # create a user
  user = User()
  user = user.from_dict(test_user)
  user.user_type_ref = learner.id
  user.user_id = ""
  user.save()
  user.user_id = user.id 
  user.update()
  
  # create a learning experience
  learning_experience = LearningExperience()
  learning_experience = learning_experience.from_dict(test_learning_experience)
  learning_experience.child_nodes = {"assessments": [assessment.id]}
  learning_experience.uuid = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  assessment.parent_nodes = {"learning_experiences": [learning_experience.id]}
  assessment.instructor_id = user.id
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()

  # create a submitted assessment
  submitted_assessment = SubmittedAssessment()
  submitted_assessment = submitted_assessment.from_dict(test_submission_request)
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.assessor_id = user.id
  submitted_assessment.learner_id = learner.id
  submitted_assessment.attempt_no = 1
  submitted_assessment.uuid = ""
  submitted_assessment.status = "evaluation_pending"
  submitted_assessment.save()
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  context.assessor_id = user.id
  context.query_params = {"assessor_id": [user.id], "status": ["evaluation_pending"]}
  context.url = f"{API_URL}/submitted-assessments"

@behave.when(
    "API request is sent to fetch the Submitted Assessments that are required to be evaluated by the assessor"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
      "the list of Submitted Assessments that are required to be evaluated are fetched in ascending order by time to review")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status code is {context.res.status_code}"
  assert context.res_data[
      "message"] == "Successfully fetched the submitted assessments.", \
        f"""Message is {context.res_data["message"]}"""
  assert context.res_data["success"] == True, f"""Success is {context.res_data["success"]}"""
  assert len(context.res_data["data"]) > 0, "Data not fetched"
  assert context.res_data["data"][0]["assessor_id"] == context.assessor_id,\
    f"""Data fetched for {context.res_data["data"][0]["assessor_id"]}"""
  assert context.res_data["data"][0]["assessment_name"] == \
    context.assessment_name


# Assessor wants to see the list of submitted assessments sorted by ascending order for time to review that are required by the assessor to evaluate with wrong assessor_id
# ---------------------------NEGATIVE----------------------------------------

@behave.given(
    "that an assessor has access to Assessment Service and wants to fetch the Submitted Assessments that are required to be evaulated with wrong assessor_id"
)
def step_impl_1(context):
  # create url and incorrect query parameters for filter api
  context.assessor_id = "random_id"
  context.url = context.url = f"{API_URL}/submitted-assessments"
  context.query_params = {"assessor_id": ["assessor_id"]}

@behave.when(
    "API request is sent to fetch the Submitted Assessments that are required to be evaluated by the assessor with wrong assessor_id"
)
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params=context.query_params)
  context.res_data = context.res.json()


@behave.then(
      "Assessment Service raises 404 User not Found Exception")
def step_impl_3(context):
  assert context.res.status_code == 404, f"Status code is {context.res.status_code}"


# Assessor wants to see the list of submitted assessments of a learner for given experience that can be reviewed
# ------------------------------POSITIVE----------------------------------------

@behave.given("that an Assessor has access to Assessment Service and wants to fetch the Submitted Assessments of a learner for a given experience that can be reviewed")
def step_impl_1(context):
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}
  test_user = {**TEST_USER, "user_type":"assessor"}
  test_learning_experience = {**TEST_LEARNING_EXPERIENCE}
  test_learning_object = {**TEST_LEARNING_OBJECT}

  # create an assesssment
  test_assessment = {**TEST_FINAL_ASSESSMENT}
  assessment = Assessment()
  assessment = assessment.from_dict(test_assessment)
  assessment.uuid = test_submission_request["assessment_id"]
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()

  # create a user
  user = User()
  user = user.from_dict(test_user)
  user.user_type_ref = learner.id
  user.user_id = ""
  user.save()
  user.user_id = user.id 
  user.update()
  
  # create a learning experience
  learning_experience = LearningExperience()
  learning_experience = learning_experience.from_dict(test_learning_experience)
  learning_experience.uuid = ""
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.update()

  # create a learning object
  learning_object = LearningObject()
  learning_object = learning_object.from_dict(test_learning_object)
  learning_object.parent_nodes = {"learning_experiences": [learning_experience.id]}
  learning_object.uuid = ""
  learning_object.save()
  learning_object.uuid = learning_object.id
  learning_object.update()

  assessment.parent_nodes = {"learning_objects": [learning_object.id]}
  assessment.instructor_id = user.id
  assessment.uuid = ""
  assessment.save()
  assessment.uuid = assessment.id
  assessment.update()

  learning_experience.child_nodes = {"learning_objects": [learning_object.id]}
  learning_experience.update()
  
  learning_object.child_nodes = {"assessments": [assessment.id]}
  learning_object.update()

  # create a submitted assessment
  submitted_assessment = SubmittedAssessment()
  submitted_assessment = submitted_assessment.from_dict(test_submission_request)
  submitted_assessment.assessment_id = assessment.id
  submitted_assessment.assessor_id = user.id
  submitted_assessment.learner_id = learner.id
  submitted_assessment.attempt_no = 1
  submitted_assessment.is_autogradable = False
  submitted_assessment.uuid = ""
  submitted_assessment.save()
  submitted_assessment.uuid = submitted_assessment.id
  submitted_assessment.update()

  context.learner_id = learner.uuid
  context.url = f"{API_URL}/learner/{learner.uuid}/learning-experience/{learning_experience.uuid}/submitted-assessments/manual-evaluation"

@behave.when("API request is sent to fetch the Submitted Assessments of a learner for a given experience that can be reviewed")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("the list of Submitted Assessments belonging to a learner and the given experience that can be reviewed will be fetched")
def step_impl_3(context):
  assert context.res.status_code == 200, f"Status code is {context.res.status_code}"
  assert context.res_data["message"] == "Successfully fetched the submitted assessments", f"Message is {context.res_data['message']}"
  assert context.res_data["success"] == True, f"Success is {context.res_data['success']}"
  assert len(context.res_data["data"]) > 0, "Data not fetched"
  for data in context.res_data["data"]:
    assert data["submitted_assessments"][0]["learner_id"] == context.learner_id
    assert data["submitted_assessments"][0]["is_autogradable"] is False


# Assessor wants to see the list of submitted assessments of a learner for given experience that can be reviewed with wrong learner_id
# ------------------------------NEGATIVE----------------------------------------

@behave.given("that an Assessor has access to Assessment Service and wants to fetch the Submitted Assessments of a learner for a given experience that can be reviewed with wrong learner_id")
def step_impl_1(context):
  # create a learning experience
  test_learning_experience = {**TEST_LEARNING_EXPERIENCE}
  le = LearningExperience()
  le = le.from_dict(test_learning_experience)
  le.uuid = ""
  le.save()
  le.uuid = le.id
  le.update()

  learner_id = "random_id"
  context.url = f"{API_URL}/learner/{learner_id}/learning-experience/{le.uuid}/submitted-assessments/manual-evaluation"

@behave.when("API request is sent to fetch the Submitted Assessments of a learner for a given experience that can be reviewed with wrong learner_id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Assessment Service raises 404 Learner not Found Exception")
def step_impl_3(context):
  assert context.res.status_code == 404, f"Status code is {context.res.status_code}"
  assert context.res_data["message"] == "Learner with uuid random_id not found"


# Assessor wants to see the list of submitted assessments of a learner for given experience that can be reviewed with wrong learning_experience_id
# ------------------------------NEGATIVE----------------------------------------

@behave.given("that an Assessor has access to Assessment Service and wants to fetch the Submitted Assessments of a learner for a given experience that can be reviewed with wrong learning_experience_id")
def step_impl_1(context):
  test_submission_request = {**TEST_SUBMITTED_ASSESSMENT_INPUT}

  # create a learner
  test_learner = {**TEST_LEARNER}
  learner = Learner()
  learner = learner.from_dict(test_learner)
  learner.uuid = test_submission_request["learner_id"]
  learner.save()
  learner.uuid = learner.id
  learner.update()

  le_id = "random_id"
  context.url = f"{API_URL}/learner/{learner.uuid}/learning-experience/{le_id}/submitted-assessments/manual-evaluation"

@behave.when("API request is sent to fetch the Submitted Assessments of a learner for a given experience that can be reviewed with wrong learning_experience_id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Assessment Service raises 404 LearningExperience not Found Exception")
def step_impl_3(context):
  assert context.res.status_code == 404, f"Status code is {context.res.status_code}"
  assert context.res_data["message"] == "Learning Experience with uuid random_id not found"
