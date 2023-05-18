"""
Feature: User Deactivation flow
"""
import behave
import sys
from copy import deepcopy
from uuid import uuid4

sys.path.append("../")
from common.models import AssociationGroup
from test_object_schemas import TEST_USER, TEST_ASSOCIATION_GROUP, TEST_CURRICULUM_PATHWAY
from environment import TEST_USER_MANAGEMENT_PATH
from test_config import (API_URL_USER_MANAGEMENT as UM_API_URL, API_URL_LEARNING_OBJECT_SERVICE as LOS_API_URL)
from setup import post_method, get_method, put_method

# -----------------------------------------------------
# Scenario 1: User wants to upload a learning content file with sync api
# -----------------------------------------------------
@behave.given("A learner is part of a learner association group")
def step_impl_1(context):
  # Create Learner Association Grp
  lag_dict = {**TEST_ASSOCIATION_GROUP}
  lag_dict["name"] = f"Discipline Association Group - {uuid4()}"
  res = post_method(
            url=f"{UM_API_URL}/association-groups/learner-association",
            request_body=lag_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.lag_uuid = res_json["data"]["uuid"]

  # Create Learner
  user_dict = {**TEST_USER}
  user_dict["email"] = f"test-{uuid4()}@example.com"
  res = post_method(
            url=f"{UM_API_URL}/user",
            request_body=user_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.user_uuid = res_json["data"]["user_id"]

  # Add Learner to Learner Association Grp
  res = post_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}/users/add",
            request_body={
              "users": [context.user_uuid],
              "status": "active"
            }    
          )
  assert res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  assert len(res_json["data"]["users"]) == 1

@behave.when("A API request is sent to deactivate the learner")
def step_impl_2(context):
  context.res = put_method(
                  url=f"{UM_API_URL}/user/{context.user_uuid}/status",
                  request_body={
                    "status": "inactive"
                  }
                )
  context.res_json = context.res.json()

@behave.then("the learner is removed from learner association group")
def step_impl_3(context):
  assert context.res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  assert len(res_json["data"]["users"]) == 0

# -----------------------------------------------------
# Scenario 2: Coach is removed from Learner Association Group when deactivated
# -----------------------------------------------------
@behave.given("A coach is part of a learner association group")
def step_impl_1(context):
  # Create Learner Association Grp
  lag_dict = {**TEST_ASSOCIATION_GROUP}
  lag_dict["name"] = f"Learner Association Group - {uuid4()}"
  res = post_method(
            url=f"{UM_API_URL}/association-groups/learner-association",
            request_body=lag_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.lag_uuid = res_json["data"]["uuid"]

  # Create Coach
  user_dict = {**TEST_USER}
  user_dict["email"] = f"test-{uuid4()}@example.com"
  user_dict["user_type"] = "coach"
  res = post_method(
            url=f"{UM_API_URL}/user",
            request_body=user_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.user_uuid = res_json["data"]["user_id"]

  # Add Coach to Learner Association Grp
  res = post_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}/coaches/add",
            request_body={
              "coaches": [context.user_uuid],
              "status": "active"
            }    
          )
  assert res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  assert len(res_json["data"]["associations"]["coaches"]) == 1

@behave.when("A API request is sent to deactivate the coach")
def step_impl_2(context):
  context.res = put_method(
                  url=f"{UM_API_URL}/user/{context.user_uuid}/status",
                  request_body={
                    "status": "inactive"
                  }
                )
  context.res_json = context.res.json()

@behave.then("the coach is removed from learner association group")
def step_impl_3(context):
  assert context.res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  assert len(res_json["data"]["associations"]["coaches"]) == 0

# -----------------------------------------------------
# Scenario 3: Assessor is removed from Discipline Association Group when deactivated
# -----------------------------------------------------
@behave.given("A assessor is part of a discipline association group")
def step_impl_1(context):
  # Create Discipline Association Grp
  lag_dict = {**TEST_ASSOCIATION_GROUP}
  lag_dict["name"] = f"Discipline Association Group - {uuid4()}"
  res = post_method(
            url=f"{UM_API_URL}/association-groups/discipline-association",
            request_body=lag_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.lag_uuid = res_json["data"]["uuid"]

  # Create Assessor
  user_dict = {**TEST_USER}
  user_dict["email"] = f"test-{uuid4()}@example.com"
  user_dict["user_type"] = "assessor"
  res = post_method(
            url=f"{UM_API_URL}/user",
            request_body=user_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.user_uuid = res_json["data"]["user_id"]

  # Add Assessor to Discipline Association Grp
  res = post_method(
            url=f"{UM_API_URL}/association-groups/discipline-association/{context.lag_uuid}/users/add",
            request_body={
              "users": [context.user_uuid],
              "status": "active"
            }    
          )
  assert res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/discipline-association/{context.lag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  assert len(res_json["data"]["users"]) == 1

@behave.when("A API request is sent to deactivate the assessor")
def step_impl_2(context):
  context.res = put_method(
                  url=f"{UM_API_URL}/user/{context.user_uuid}/status",
                  request_body={
                    "status": "inactive"
                  }
                )
  context.res_json = context.res.json()

@behave.then("the assessor is removed from discipline association group")
def step_impl_3(context):
  assert context.res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/discipline-association/{context.lag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  assert len(res_json["data"]["users"]) == 0

# -----------------------------------------------------
# Scenario 4: Instructor is removed from Learner Association Group and Discipline Association Group when deactivated
# -----------------------------------------------------
@behave.given("An instructor is part of a learner association group and discipline association group")
def step_impl_1(context):
  # Create Learner Association Grp
  lag_dict = {**TEST_ASSOCIATION_GROUP}
  lag_dict["name"] = f"Learner Association Group - {uuid4()}"
  res = post_method(
            url=f"{UM_API_URL}/association-groups/learner-association",
            request_body=lag_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.lag_uuid = res_json["data"]["uuid"]

  # Create Discipline Association Grp
  lag_dict = {**TEST_ASSOCIATION_GROUP}
  lag_dict["name"] = f"Discipline Association Group - {uuid4()}"
  res = post_method(
            url=f"{UM_API_URL}/association-groups/discipline-association",
            request_body=lag_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.dag_uuid = res_json["data"]["uuid"]

  # Create Instructor
  user_dict = {**TEST_USER}
  user_dict["email"] = f"test-{uuid4()}@example.com"
  user_dict["user_type"] = "instructor"
  res = post_method(
            url=f"{UM_API_URL}/user",
            request_body=user_dict
          )
  assert res.status_code == 200
  res_json = res.json()
  context.user_uuid = res_json["data"]["user_id"]

  # Create Program Pathway
  program_dict = {**TEST_CURRICULUM_PATHWAY}
  program_dict["alias"] = "program"
  program_dict["parent_nodes"] = {}
  res = post_method(
          url=f"{LOS_API_URL}/curriculum-pathway",
          request_body=program_dict
        )
  assert res.status_code == 200
  context.program_id = res.json()["data"]["uuid"]

  lag_doc = AssociationGroup.find_by_uuid(context.lag_uuid)
  lag_doc.associations = {
    "curriculum_pathway_id" : context.program_id,
    "coaches":[],
    "instructors":[]
  }
  lag_doc.update()

  # Create Level Pathway
  level_dict = {**TEST_CURRICULUM_PATHWAY}
  level_dict["alias"] = "level"
  level_dict["parent_nodes"] = {"curriculum_pathways":[context.program_id]}
  res = post_method(
          url=f"{LOS_API_URL}/curriculum-pathway",
          request_body=level_dict
        )
  assert res.status_code == 200
  context.level_id = res.json()["data"]["uuid"]

  # Create Discipline Pathway
  discipline_dict = {**TEST_CURRICULUM_PATHWAY}
  discipline_dict["alias"] = "discipline"
  discipline_dict["parent_nodes"] = {"curriculum_pathways":[context.level_id]}
  res = post_method(
          url=f"{LOS_API_URL}/curriculum-pathway",
          request_body=discipline_dict
        )
  assert res.status_code == 200
  context.discipline_id = res.json()["data"]["uuid"]

  dag_doc = AssociationGroup.find_by_uuid(context.dag_uuid)
  dag_doc.associations = {
    "curriculum_pathways" : [{"curriculum_pathway_id": context.discipline_id, "status": "active"}]
  }
  dag_doc.update()

  # Add Instructor to Discipline Association Grp
  res = post_method(
            url=f"{UM_API_URL}/association-groups/discipline-association/{context.dag_uuid}/users/add",
            request_body={
              "users": [context.user_uuid],
              "status": "active"
            }    
          )
  assert res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/discipline-association/{context.dag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  assert len(res_json["data"]["users"]) == 1

  # Add Instructor to Learner Association Grp
  res = post_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}/instructors/add",
            request_body={
              "instructors": [context.user_uuid],
              "curriculum_pathway_id": context.discipline_id,
              "status": "active"
            }    
          )
  assert res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  assert len(res_json["data"]["associations"]["instructors"]) == 1

@behave.when("A API request is sent to deactivate the instructor")
def step_impl_2(context):
  context.res = put_method(
                  url=f"{UM_API_URL}/user/{context.user_uuid}/status",
                  request_body={
                    "status": "inactive"
                  }
                )
  context.res_json = context.res.json()

@behave.then("the instructor is removed from learner association group and discipline association group")
def step_impl_3(context):
  assert context.res.status_code == 200

  res = get_method(
            url=f"{UM_API_URL}/association-groups/learner-association/{context.lag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  print(res_json)
  assert len(res_json["data"]["associations"]["instructors"]) == 0

  res = get_method(
            url=f"{UM_API_URL}/association-groups/discipline-association/{context.dag_uuid}"    
          )
  assert res.status_code == 200

  res_json = res.json()
  print(res_json)
  assert len(res_json["data"]["users"]) == 0
