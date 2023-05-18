"""
Feature - Positive and Negative scenarios for fetching Coach Details
"""

import behave
import sys
from uuid import uuid4
sys.path.append("../")
from setup import get_method
from common.models import User, Staff, Learner, AssociationGroup
from test_config import API_URL_LEARNER_PROFILE_SERVICE, DEL_KEYS
from test_object_schemas import (TEST_USER, TEST_STAFF, TEST_LEARNER,
                                TEST_ASSOCIATION_GROUP)


# ------------------------------ Scenario 01 -----------------------------------
"""
Fetch Coach details for a learner that is part of valid learner assocition group by giving valid learner uuid
"""
@behave.given("that a valid learner, coressponding user, valid coach exists and a valid AssociationGroup is present in the DB where the learner user and coach have already been added")
def step_impl1(context):

  # ADD COACH DETAILS
  coach = User.from_dict(TEST_USER)
  coach.user_type = "coach"
  coach.email = str(uuid4()) + ".coach@gmail.com"
  coach.user_id = ""
  coach.save()
  coach.user_id = coach.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.email = coach.email
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()
  context.staff_uuid = staff.uuid

  coach.user_type_ref = staff.id
  coach.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.email = str(uuid4()) + ".learner@gmail.com"
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.email = learner.email
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = TEST_ASSOCIATION_GROUP
  lag = AssociationGroup.from_dict(lag_body)
  lag.users = [{"user": learner_user.id, "status": "active"}] 
  lag.associations = {
      "coaches": [{"coach": coach.user_id, "status": "active"}],
      "instructors": []
    }
  lag.association_type = "learner"
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner.uuid}/coach"

@behave.when("API request is sent to fetch coach details by providing a valid learner id")
def step_impl2(context):
  coach_details = get_method(url=context.url)
  context.res_status = coach_details.status_code
  context.res_body = coach_details.json()


@behave.then("the details for coach present in the corresponding learner association group are fetched")
def step_impl3(context):
  assert context.res_status == 200
  assert context.res_body["success"] is True
  assert context.res_body["message"] == "Successfully fetched the coach"
  assert context.res_body["data"].get("coach_staff_id") == context.staff_uuid



# ------------------------------ Scenario 02 -----------------------------------
"""
Fetch Coach details by providing invalid learner uuid
"""
@behave.given("that all valid data exists and user corresponding to given learner uuid is part of learner assocaition group")
def step_impl1(context):
  # ADD COACH DETAILS
  coach = User.from_dict(TEST_USER)
  coach.user_type = "coach"
  coach.email = str(uuid4()) + ".coach@gmail.com"
  coach.user_id = ""
  coach.save()
  coach.user_id = coach.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.email = coach.email
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  coach.user_type_ref = staff.id
  coach.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.email = str(uuid4()) + ".learner@gmail.com"
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()

  learner_user = User.from_dict(TEST_USER)
  learner_user.email = learner.email
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = TEST_ASSOCIATION_GROUP
  lag = AssociationGroup.from_dict(lag_body)
  lag.users = [{"user": learner_user.id, "status": "active"}] 
  lag.associations = {
      "coaches": [{"coach": coach.user_id, "status": "active"}],
      "instructors": []
    }
  lag.association_type = "learner"
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  context.invalid_learner_id = "random_uuid"
  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.invalid_learner_id}/coach"

@behave.when("the endpoint is hit to fetch coach details with invalid learner ID")
def step_impl2(context):
  coach_details = get_method(url=context.url)
  context.res_status = coach_details.status_code
  context.res_body = coach_details.json()


@behave.then("endpoint throws ResourceNotFoundException for the given invalid learner ID")
def step_impl3(context):
  assert context.res_status == 404, f"Status Code = {context.res_status}"
  assert context.res_body["success"] is False
  assert context.res_body["message"] == \
      "Learner with uuid random_uuid not found"

# ------------------------------ Scenario 03 -----------------------------------
"""
Fetch Coach details by providing valid learner uuid which is not part of any learner association group
"""
@behave.given("that all valid data exists but user corresponding to given learner uuid is not part of any assocaition group")
def step_impl1(context):

  # ADD COACH DETAILS
  coach = User.from_dict(TEST_USER)
  coach.user_type = "coach"
  coach.email = str(uuid4()) + ".coach@gmail.com"
  coach.user_id = ""
  coach.save()
  coach.user_id = coach.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.email = coach.email
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()

  coach.user_type_ref = staff.id
  coach.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.email = str(uuid4()) + ".learner@gmail.com"
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_id = learner.uuid

  learner_user = User.from_dict(TEST_USER)
  learner_user.email = learner.email
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = TEST_ASSOCIATION_GROUP
  lag = AssociationGroup.from_dict(lag_body)
  # No learner user linked to the learner associaiton group
  lag.users = [] 
  lag.associations = {
      "coaches": [{"coach": coach.user_id, "status": "active"}],
      "instructors": []
    }
  lag.association_type = "learner"
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/coach"


@behave.when("the endpoint is hit to fetch coach details with learner uuid that is not associated in any group")
def step_impl2(context):
  coach_details = get_method(url=context.url)
  context.res_status = coach_details.status_code
  context.res_body = coach_details.json()


@behave.then("endpoint throws ValidationError stating that user corresponding to given learner uuid is not linked to any association group")
def step_impl3(context):
  assert context.res_status == 422
  assert context.res_body["success"] is False
  assert context.res_body["message"] == f"User for given learner_id {context.learner_id} is not associated in any Learner Association Group"



# ------------------------------ Scenario 04 -----------------------------------
"""
Fetch Coach details by providing valid learner uuid for which no active coach exists in any learner association group
"""
@behave.given("that all valid data exists but coach is not active in any learner assocaition group")
def step_impl1(context):

  # ADD COACH DETAILS
  coach = User.from_dict(TEST_USER)
  coach.user_type = "coach"
  coach.email = str(uuid4()) + ".coach@gmail.com"
  coach.user_id = ""
  coach.save()
  coach.user_id = coach.id

  staff = Staff.from_dict(TEST_STAFF)
  staff.email = coach.email
  staff.uuid = ""
  staff.save()
  staff.uuid = staff.id
  staff.update()
  context.staff_uuid = staff.uuid

  coach.user_type_ref = staff.id
  coach.update()

  # ADD Learner Details
  learner = Learner.from_dict(TEST_LEARNER)
  learner.email = str(uuid4()) + ".learner@gmail.com"
  learner.uuid = ""
  learner.save()
  learner.uuid = learner.id
  learner.update()
  context.learner_uuid = learner.uuid

  learner_user = User.from_dict(TEST_USER)
  learner_user.email = learner.email
  learner_user.user_type = "learner"
  learner_user.user_id = ""
  learner_user.user_type_ref = learner.id
  learner_user.save()
  learner_user.user_id = learner_user.id
  learner_user.update()

  # ADD LEARNER ASSOCIATION GROUP DETAILS
  lag_body = TEST_ASSOCIATION_GROUP
  lag = AssociationGroup.from_dict(lag_body)
  lag.users = [{"user": learner_user.id, "status": "active"}] 
  lag.associations = {
      "coaches": [],
      "instructors": []
    }
  lag.association_type = "learner"
  lag.uuid = ""
  lag.save()
  lag.uuid = lag.id
  lag.update()

  context.url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_uuid}/coach"

@behave.when("the endpoint is hit to fetch coach details with learner uuid for which no active coach exists in learner association group")
def step_impl2(context):
  coach_details = get_method(url=context.url)
  context.res_status = coach_details.status_code
  context.res_body = coach_details.json()


@behave.then("endpoint throws ValidationError stating that no active coach exists in learner assocition group corresponding to given learner uuid")
def step_impl3(context):
  assert context.res_status == 422
  assert context.res_body["success"] is False
  assert context.res_body["message"] == f"No active coach exists in Learner Association Group for user corresponding to given learner_id {context.learner_uuid}"
