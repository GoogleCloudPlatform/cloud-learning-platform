"""
Feature - Positive and Negative scenarios for fetching Instructor Details
"""

import behave
import sys
from uuid import uuid4
sys.path.append("../")
from e2e.setup import get_method
from common.models import User, CurriculumPathway, Staff, Learner, AssociationGroup
from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_USER, TEST_CURRICULUM_PATHWAY, TEST_STAFF, TEST_LEARNER,
                              TEST_ASSOCIATION_GROUP)


# ------------------------------ Scenario 01 -----------------------------------
"""
Fetch Instructor details for a valid discipline and a learner
"""
@behave.given("that a valid learner, valid discipline, valid instructor exists and a valid AssociationGroup is present in the DB where the learner, discipline and instructor have already been added")
def step_impl1(context):

    # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()
  context.staff_id = staff.uuid

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD DISCIPLINE DETAILS
  discipline = CurriculumPathway.from_dict(TEST_CURRICULUM_PATHWAY)
  discipline.uuid = ""
  discipline.alias = "discipline"
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = TEST_ASSOCIATION_GROUP
  lag = AssociationGroup.from_dict(lag_body)
  lag.users = [
    {"user": learner_user.user_id,
    "status": "active"
  }]
  lag.associations = {
      "coaches": [],
      "instructors": [
        {
          "instructor": instructor.id,
          "status": "active",
          "curriculum_pathway_id": discipline.id
        }
      ]
    }
  lag.association_type = "learner"
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner.id}/curriculum-pathway/{discipline.id}/instructor"

@behave.when("the valid discipline uuid and a valid learner uuid is correctly passed")
def step_impl2(context):
  instructor_details = get_method(url=context.url)
  context.res_status = instructor_details.status_code
  context.res_body = instructor_details.json()

@behave.then("the instructor details are fetched")
def step_impl3(context):
  assert context.res_status == 200, f"Status Code = {context.res_status}"
  assert context.res_body["success"] is True
  assert context.res_body["message"] == "Successfully fetched instructor"
  assert context.res_body["data"]["instructor_staff_id"] == context.staff_id



# ------------------------------ Scenario 02 -----------------------------------
"""
Fetch Instructor details for a valid discipline and but invalid learner ID
"""
@behave.given("that all valid data exists except for Learner")
def step_impl1(context):

    # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD DISCIPLINE DETAILS
  discipline = CurriculumPathway.from_dict(TEST_CURRICULUM_PATHWAY)
  discipline.uuid = ""
  discipline.alias = "discipline"
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/learner_id/curriculum-pathway/{discipline.id}/instructor"

@behave.when("the endpoint is hit to fetch instructor details with invalid learner ID")
def step_impl2(context):
  instructor_details = get_method(url=context.url)
  context.res_status = instructor_details.status_code
  context.res_body = instructor_details.json()

@behave.then("endpoint throws ResourceNotFoundException for the given learner ID")
def step_impl3(context):
  assert context.res_status == 404, f"Status Code = {context.res_status}"
  assert context.res_body["message"] == "Learner with uuid learner_id not found", f"Message = {context.res_body['message']}"

# ------------------------------ Scenario 03 -----------------------------------
"""
Fetch Instructor details for an invalid discipline but a valid learner ID
"""
@behave.given("that all valid data exists except for discipline")
def step_impl1(context):

    # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner.id}/curriculum-pathway/curriculum_pathway_id/instructor"

@behave.when("the endpoint is hit to fetch instructor details with invalid pathway ID")
def step_impl2(context):
  instructor_details = get_method(url=context.url)
  context.res_status = instructor_details.status_code
  context.res_body = instructor_details.json()

@behave.then("endpoint throws ResourceNotFoundException for the given pathway ID")
def step_impl3(context):
  assert context.res_status == 404
  assert context.res_body["message"] == "Curriculum Pathway with uuid curriculum_pathway_id not found", f"Message = {context.res_body['message']}"


# ------------------------------ Scenario 04 -----------------------------------
"""
Fetch Instructor details for a invalid pathwayID where alias is not discipline and a valid learner ID
"""
@behave.given("that all valid data exists except for pathway where alias is not discipline")
def step_impl1(context):

    # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD DISCIPLINE DETAILS
  discipline = CurriculumPathway.from_dict(TEST_CURRICULUM_PATHWAY)
  discipline.uuid = ""
  discipline.alias = "program"
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()
  context.curriculum_pathway_id = discipline.id

  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner.id}/curriculum-pathway/{discipline.id}/instructor"

@behave.when("the endpoint is hit to fetch instructor details with pathway ID where alias is not discipline")
def step_impl2(context):
  instructor_details = get_method(url=context.url)
  context.res_status = instructor_details.status_code
  context.res_body = instructor_details.json()

@behave.then("endpoint throws ValidationError for the given pathway ID where alias is not discipline")
def step_impl3(context):
  assert context.res_status == 422, f"Status Code = {context.res_status}"
  assert context.res_body["message"] == f"Pathway with {context.curriculum_pathway_id} has alias as program instead of discipline", f"Message = {context.res_body['message']}"


# ------------------------------ Scenario 05 -----------------------------------
"""
Scenario: Fetch Instructor details for a valid discipline and a valid learner but the learner is not associated to any AssociationGroup of type learner
"""
@behave.given("that all valid data exists except for a AssociationGroup of type learner")
def step_impl1(context):

    # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()
  context.learner_user_id = learner_user.id

  # ADD DISCIPLINE DETAILS
  discipline = CurriculumPathway.from_dict(TEST_CURRICULUM_PATHWAY)
  discipline.uuid = ""
  discipline.alias = "discipline"
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner.id}/curriculum-pathway/{discipline.id}/instructor"

@behave.when("the endpoint is hit to fetch instructor details with pathway ID where Leaner is not added to any AssociationGroup")
def step_impl2(context):
  instructor_details = get_method(url=context.url)
  context.res_status = instructor_details.status_code
  context.res_body = instructor_details.json()

@behave.then("endpoint throws ValidationError as Leaner is not added to any AssociationGroup")
def step_impl3(context):
  assert context.res_status == 422, f"Status Code = {context.res_status}"
  assert context.res_body["message"] == f"Learner with User ID {context.learner_user_id} not found in any Association Groups", f"Message = {context.res_body['message']}"


# ------------------------------ Scenario 06 -----------------------------------
"""
Scenario: Fetch Instructor details for a valid discipline and a valid learner but there are no active instructors
"""
@behave.given("that all valid data exists except for an active instructor")
def step_impl1(context):

    # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD DISCIPLINE DETAILS
  discipline = CurriculumPathway.from_dict(TEST_CURRICULUM_PATHWAY)
  discipline.uuid = ""
  discipline.alias = "discipline"
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()
  context.curriculum_pathway_id = discipline.id

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = TEST_ASSOCIATION_GROUP
  lag = AssociationGroup.from_dict(lag_body)
  lag.users = [
    {"user": learner_user.user_id,
    "status": "active"
  }]
  lag.associations = {
      "coaches": [],
      "instructors": [
        {
          "instructor": instructor.id,
          "status": "inactive",
          "curriculum_pathway_id": discipline.id
        }
      ]
    }
  lag.association_type = "learner"
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  context.lag_id = lag.id
  lag.update()
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner.id}/curriculum-pathway/{discipline.id}/instructor"

@behave.when("the endpoint is hit with valid IDs")
def step_impl2(context):
  instructor_details = get_method(url=context.url)
  context.res_status = instructor_details.status_code
  context.res_body = instructor_details.json()

@behave.then("endpoint throws ValidationError as there are no active instructors for the given learner and instructor ID")
def step_impl3(context):
  assert context.res_status == 422, f"Status Code = {context.res_status}"
  assert context.res_body["message"] == f"No Active Instructors Available for the given CurriculumPathway = {context.curriculum_pathway_id} in AssociationGroup = {context.lag_id}", f"Message = {context.res_body['message']}"



# ------------------------------ Scenario 07 -----------------------------------
"""
Fetch details for instructors corresponding to a valid program and a learner
"""
@behave.given("that a valid learner, discipline, program, instructor exists and tagged to a Learner AssociationGroup")
def step_impl1(context):

  # ADD INSTRUCTOR DETAILS
  instructor = User.from_dict(TEST_USER)
  instructor.user_type = "instructor"
  instructor.email = str(uuid4()) + "@gmail.com"
  instructor.user_id = ""
  instructor.save()
  instructor.user_id = instructor.id
  context.instructor_user_id = instructor.user_id

  staff = Staff.from_dict(TEST_STAFF)
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()
  context.staff_id = staff.uuid

  instructor.user_type_ref = staff.id
  instructor.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD DISCIPLINE DETAILS
  discipline = CurriculumPathway.from_dict(TEST_CURRICULUM_PATHWAY)
  discipline.uuid = ""
  discipline.alias = "discipline"
  discipline.save()
  discipline.uuid = discipline.id
  discipline.update()
  context.discipline_id = discipline.uuid

  # ADD PROGRAM DETAILS
  program = CurriculumPathway.from_dict(TEST_CURRICULUM_PATHWAY)
  program.uuid = ""
  program.alias = "program"
  program.save()
  program.uuid = program.id
  program.child_nodes["curriculum_pathways"] = [discipline.uuid]
  program.update()

  discipline.parent_nodes["curriculum_pathways"] = [program.uuid]
  discipline.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = TEST_ASSOCIATION_GROUP
  lag = AssociationGroup.from_dict(lag_body)
  lag.users = [
    {"user": learner_user.user_id,
    "status": "active"
  }]
  lag.associations = {
      "coaches": [],
      "instructors": [
        {
          "instructor": instructor.id,
          "status": "active",
          "curriculum_pathway_id": discipline.id
        }
      ],
      "curriculum_pathway_id": program.uuid
    }
  lag.association_type = "learner"
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner.id}/curriculum-pathway/{program.id}/instructors"


@behave.when("API request is sent to fetch details for all instructors by providing valid program id and learner id")
def step_impl2(context):
  instructor_details = get_method(url=context.url)
  context.res_status = instructor_details.status_code
  context.res_body = instructor_details.json()


@behave.then("list of details for all instructor tagged to the given learner and program are fetched")
def step_impl3(context):
  assert context.res_status == 200, f"Status Code = {context.res_status}"
  assert context.res_body["success"] is True
  assert context.res_body["message"] == "Successfully fetched instructor details"
  assert context.res_body["data"][0]["user_id"] == context.instructor_user_id
  assert context.res_body["data"][0]["staff_id"] == context.staff_id
  assert context.res_body["data"][0]["discipline_id"] == context.discipline_id
