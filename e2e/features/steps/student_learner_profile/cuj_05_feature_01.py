"""
Feature - Positive and Negative scenarios for Get APIs for Learning Progress in SLP
"""

import behave
import sys
from uuid import uuid4
from copy import deepcopy

sys.path.append("../")
from e2e.setup import post_method, get_method, put_method, set_cache, get_cache

from e2e.test_config import API_URL_LEARNER_PROFILE_SERVICE, \
  API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS
from e2e.test_object_schemas import (TEST_LEARNER, TEST_LEARNER_PROFILE,
                                 TEST_CURRICULUM_PATHWAY_2,
                                 TEST_LEARNER_PROFILE_PROGRESS_UPDATE,
                                 TEST_PROGRESS,
                                 TEST_LEARNING_OBJECT, TEST_LEARNING_EXPERIENCE,
                                 TEST_LEARNING_RESOURCE)

# ------------------------------ Scenario 01 -----------------------------------
"""
Fetch Learner progress with correct curriculum pathway uuid and learner uuid
"""


@behave.given(
  "that the learner, learner profile, curriculum pathway and the learner progress already exists")
def step_impl1(context):
  # add a learner
  post_learner_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  learner_payload = deepcopy(TEST_LEARNER)
  learner_payload["email_address"] = f"{uuid4()}@gmail.com"
  learner_post_res = post_method(url=post_learner_url,
                                 request_body=learner_payload,
                                 query_params=None
                                 )
  learner_post_res_dict = learner_post_res.json()
  context.learner_id = learner_post_res_dict["data"]["uuid"]

  # add a learner profile
  learner_uuid = context.learner_id
  post_learner_profile_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  learner_profile_payload = deepcopy(TEST_LEARNER_PROFILE)
  learner_profile_post_res = post_method(url=post_learner_profile_url,
                                         request_body=learner_profile_payload,
                                         query_params=None)
  learner_profile_post_res_dict = learner_profile_post_res.json()
  context.learner_profile_id = learner_profile_post_res_dict["data"]["uuid"]

  # add a curriculum pathway
  post_curriculum_pathway_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway"
  curriculum_pathway_payload = deepcopy(TEST_CURRICULUM_PATHWAY_2)

  for key in DEL_KEYS:
    if key in curriculum_pathway_payload:
      del curriculum_pathway_payload[key]

  curriculum_pathway_post_res = post_method(url=post_curriculum_pathway_url,
                                            request_body=curriculum_pathway_payload,
                                            query_params=None
                                            )

  curriculum_pathway_post_res_dict = curriculum_pathway_post_res.json()
  context.curriculum_pathway_id = curriculum_pathway_post_res_dict["data"][
    "uuid"]

  # update the learner profile with progress
  learner_profile_uuid = context.learner_profile_id
  put_learner_profile_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  update_learner_payload = deepcopy(TEST_LEARNER_PROFILE_PROGRESS_UPDATE)
  update_learner_payload["progress"]["curriculum_pathways"][
    context.curriculum_pathway_id] = TEST_PROGRESS
  update_learner_put_res = put_method(url=put_learner_profile_url,
                                      request_body=update_learner_payload,
                                      query_params=None
                                      )
  set_cache(key="learner_id", value=context.learner_id)
  set_cache(key="curriculum_pathway_id", value=context.curriculum_pathway_id)


@behave.when(
  "the curriculum pathway uuid and learner uuid is correctly passed to fetch learner progress")
def step_impl2(context):
  # get request to slp api
  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "curriculum_pathways",
                                          "node_id": context.curriculum_pathway_id
                                        }
                                        )
  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the learner progress for that currciculum pathway will be correctly fetched")
def step_impl3(context):
  # assert
  assert context.res_status == 200
  assert context.res_body["data"] is not None
  assert context.res_body["data"]["status"] == TEST_PROGRESS["status"]
  assert context.res_body["data"]["is_locked"] == TEST_PROGRESS["is_locked"]
  assert context.res_body["data"]["progress"] == TEST_PROGRESS["progress"]


# ------------------------------ Scenario 02 -----------------------------------
"""
Fetch Learner progress with incorrect curriculum pathway uuid and learner uuid
"""


@behave.given(
  "that the curriculum pathway uuid is incorrect and learner uuid is correct")
def step_impl1(context):
  context.dummy_cp = "abc"
  context.learner_id = get_cache(key="learner_id")


@behave.when(
  "the incorrect currciculum pathway uuid and learner uuid is passed to fetch learner progress")
def step_impl2(context):
  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "curriculum_pathways",
                                          "node_id": context.dummy_cp
                                        }
                                        )

  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the api responds with 404 status and message as Curriculum Pathway not found, cannot fetch progress")
def step_impl3(context):
  assert context.res_status == 404
  assert f"id {context.dummy_cp} not found" in context.res_body["message"]


# ------------------------------ Scenario 03 -----------------------------------
"""
Fetch learner progress with correct curriculum pathway uuid and incorrect learner uuid
"""


@behave.given("that the curriculum pathway to fetch progress already exists")
def step_impl1(context):
  # post_curriculum_pathway_url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway"
  # curriculum_pathway_payload = deepcopy(TEST_CURRICULUM_PATHWAY_2)

  # for key in DEL_KEYS:
  #     if key in curriculum_pathway_payload :
  #         del curriculum_pathway_payload [key]

  # curriculum_pathway_post_res = post_method(url=post_curriculum_pathway_url,
  #                                 request_body=curriculum_pathway_payload,
  #                                 query_params=None
  #                             )

  # curriculum_pathway_post_res_dict = curriculum_pathway_post_res.json()
  # context.cp_id = curriculum_pathway_post_res_dict["data"]["uuid"]
  context.curriculum_pathway_id = get_cache(key="curriculum_pathway_id")


@behave.when(
  "the correct currciculum pathway uuid and invalid learner uuid is passed")
def step_impl2(context):
  context.dummy_learner_id = "def"

  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.dummy_learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "curriculum_pathways",
                                          "node_id": context.curriculum_pathway_id
                                        }
                                        )

  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the api responds with 404 status and message as Learner not found, cannot fetch progress")
def step_impl3(context):
  assert context.res_status == 404
  assert context.res_body[
           "message"] == f"Learner with uuid {context.dummy_learner_id} not found"


# ------------------------------ Scenario 04 -----------------------------------
"""
Fetch Learner progress with correct learning experience uuid and learner uuid
"""


@behave.given(
  "that the learner, learner profile, learning experience and the learner progress already exists")
def step_impl1(context):
  # add a learner
  post_learner_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  learner_payload = deepcopy(TEST_LEARNER)
  learner_payload["email_address"] = f"{uuid4()}@gmail.com"
  learner_post_res = post_method(url=post_learner_url,
                                 request_body=learner_payload,
                                 query_params=None
                                 )
  learner_post_res_dict = learner_post_res.json()
  context.learner_id = learner_post_res_dict["data"]["uuid"]

  # add a learner profile
  learner_uuid = context.learner_id
  post_learner_profile_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  learner_profile_payload = deepcopy(TEST_LEARNER_PROFILE)
  learner_profile_post_res = post_method(url=post_learner_profile_url,
                                         request_body=learner_profile_payload,
                                         query_params=None)
  learner_profile_post_res_dict = learner_profile_post_res.json()
  context.learner_profile_id = learner_profile_post_res_dict["data"]["uuid"]

  # add a learning experience
  post_le_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-experience"
  learning_experience_payload = deepcopy(TEST_LEARNING_EXPERIENCE)

  for key in DEL_KEYS:
    if key in learning_experience_payload:
      del learning_experience_payload[key]

  learning_experience_post_res = post_method(url=post_le_url,
                                             request_body=learning_experience_payload,
                                             query_params=None
                                             )

  learning_experience_post_res_dict = learning_experience_post_res.json()
  context.le_id = learning_experience_post_res_dict["data"]["uuid"]
  set_cache(key="learner_id", value=context.learner_id)
  set_cache(key="le_id", value=context.le_id)

  # update the learner profile with progress
  learner_profile_uuid = context.learner_profile_id
  put_learner_profile_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  update_learner_payload = deepcopy(TEST_LEARNER_PROFILE_PROGRESS_UPDATE)
  update_learner_payload["progress"]["learning_experiences"][
    context.le_id] = TEST_PROGRESS
  update_learner_put_res = put_method(url=put_learner_profile_url,
                                      request_body=update_learner_payload,
                                      query_params=None
                                      )


@behave.when(
  "the learning experience uuid and learner uuid is correctly passed to fetch learner progress")
def step_impl2(context):
  # get request to slp api
  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "learning_experiences",
                                          "node_id": context.le_id
                                        }
                                        )
  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the learner progress for that learning experience will be correctly fetched")
def step_impl3(context):
  assert context.res_status == 200
  assert context.res_body["data"] is not None
  assert context.res_body["data"]["status"] == TEST_PROGRESS["status"]
  assert context.res_body["data"]["is_locked"] == TEST_PROGRESS["is_locked"]
  assert context.res_body["data"]["progress"] == TEST_PROGRESS["progress"]


# ------------------------------ Scenario 05 -----------------------------------
"""
Fetch Learner progress with incorrect learning experience uuid and learner uuid
"""


@behave.given("that the learning experience uuid is incorrect")
def step_impl1(context):
  context.dummy_le = "abc"
  context.learner_id = get_cache(key="learner_id")


@behave.when(
  "the incorrect learning experience uuid and learner uuid is passed")
def step_impl2(context):
  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "learning_experiences",
                                          "node_id": context.dummy_le
                                        }
                                        )

  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the api responds with 404 status and message as Learning Experience not found")
def step_impl3(context):
  assert context.res_status == 404
  assert context.res_body[
           "message"] == f"Learning Experience with uuid {context.dummy_le} not found"


# ------------------------------ Scenario 06 -----------------------------------
"""
Fetch Learner progress with correct learning object uuid and learner uuid
"""


@behave.given(
  "that the learner, learner profile, learning object and the learner progress already exists")
def step_impl1(context):
  # add a learner
  post_learner_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  learner_payload = deepcopy(TEST_LEARNER)
  learner_payload["email_address"] = f"{uuid4()}@gmail.com"
  learner_post_res = post_method(url=post_learner_url,
                                 request_body=learner_payload,
                                 query_params=None
                                 )
  learner_post_res_dict = learner_post_res.json()
  context.learner_id = learner_post_res_dict["data"]["uuid"]

  # add a learner profile
  learner_uuid = context.learner_id
  post_learner_profile_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  learner_profile_payload = deepcopy(TEST_LEARNER_PROFILE)
  learner_profile_post_res = post_method(url=post_learner_profile_url,
                                         request_body=learner_profile_payload,
                                         query_params=None)
  learner_profile_post_res_dict = learner_profile_post_res.json()
  context.learner_profile_id = learner_profile_post_res_dict["data"]["uuid"]

  # add a learning object
  post_lo_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-object"
  learning_object_payload = deepcopy(TEST_LEARNING_OBJECT)

  for key in DEL_KEYS:
    if key in learning_object_payload:
      del learning_object_payload[key]

  learning_object_post_res = post_method(url=post_lo_url,
                                         request_body=learning_object_payload,
                                         query_params=None
                                         )

  learning_object_post_res_dict = learning_object_post_res.json()
  context.lo_id = learning_object_post_res_dict["data"]["uuid"]

  # update the learner profile with progress
  learner_profile_uuid = context.learner_profile_id
  put_learner_profile_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  update_learner_payload = deepcopy(TEST_LEARNER_PROFILE_PROGRESS_UPDATE)
  update_learner_payload["progress"]["learning_objects"][
    context.lo_id] = TEST_PROGRESS
  update_learner_put_res = put_method(url=put_learner_profile_url,
                                      request_body=update_learner_payload,
                                      query_params=None
                                      )
  set_cache(key="learner_id", value=context.learner_id)
  set_cache(key="lo_id", value=context.lo_id)


@behave.when(
  "the learning object uuid and learner uuid is correctly passed to fetch learner progress")
def step_impl2(context):
  # get request to slp api
  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "learning_objects",
                                          "node_id": context.lo_id
                                        }
                                        )
  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the learner progress for that learning object will be correctly fetched")
def step_impl3(context):
  assert context.res_status == 200
  assert context.res_body["data"] is not None
  assert context.res_body["data"]["status"] == TEST_PROGRESS["status"]
  assert context.res_body["data"]["is_locked"] == TEST_PROGRESS["is_locked"]
  assert context.res_body["data"]["progress"] == TEST_PROGRESS["progress"]


# ------------------------------ Scenario 07 -----------------------------------
"""
Fetch Learner progress with incorrect learning object uuid and learner uuid
"""


@behave.given("that the learning object uuid is incorrect")
def step_impl1(context):
  context.dummy_lo = "abc"
  context.learner_id = get_cache(key="learner_id")


@behave.when("the incorrect learning object uuid and learner uuid is passed")
def step_impl2(context):
  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "learning_objects",
                                          "node_id": context.dummy_lo
                                        }
                                        )

  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the api responds with 404 status and message as Learning Object not found")
def step_impl3(context):
  assert context.res_status == 404
  assert f"id {context.dummy_lo} not found" in context.res_body["message"]


# ------------------------------ Scenario 07 -----------------------------------
"""
Fetch Learner progress with correct learning resource uuid and learner uuid
"""


@behave.given(
  "that the learner, learner profile, learning resource and the learner progress already exists")
def step_impl1(context):
  # add a learner
  post_learner_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner"
  learner_payload = deepcopy(TEST_LEARNER)
  learner_payload["email_address"] = f"{uuid4()}@gmail.com"
  learner_post_res = post_method(url=post_learner_url,
                                 request_body=learner_payload,
                                 query_params=None
                                 )
  learner_post_res_dict = learner_post_res.json()
  context.learner_id = learner_post_res_dict["data"]["uuid"]

  # add a learner profile
  learner_uuid = context.learner_id
  post_learner_profile_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  learner_profile_payload = deepcopy(TEST_LEARNER_PROFILE)
  learner_profile_post_res = post_method(url=post_learner_profile_url,
                                         request_body=learner_profile_payload,
                                         query_params=None)
  learner_profile_post_res_dict = learner_profile_post_res.json()
  context.learner_profile_id = learner_profile_post_res_dict["data"]["uuid"]

  # add a learning resource
  post_lr_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-resource"
  learning_resource_payload = deepcopy(TEST_LEARNING_RESOURCE)
  lo_id = get_cache(key="lo_id")
  learning_resource_payload["parent_nodes"]["learning_objects"] = [lo_id]

  for key in DEL_KEYS:
    if key in learning_resource_payload:
      del learning_resource_payload[key]

  learning_resource_post_res = post_method(url=post_lr_url,
                                           request_body=learning_resource_payload,
                                           query_params=None
                                           )

  learning_resource_post_res_dict = learning_resource_post_res.json()
  context.lr_id = learning_resource_post_res_dict["data"]["uuid"]

  # update the learner profile with progress
  learner_profile_uuid = context.learner_profile_id
  put_learner_profile_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{learner_uuid}/learner-profile"
  update_learner_payload = deepcopy(TEST_LEARNER_PROFILE_PROGRESS_UPDATE)
  update_learner_payload["progress"]["learning_resources"][
    context.lr_id] = TEST_PROGRESS
  update_learner_put_res = put_method(url=put_learner_profile_url,
                                      request_body=update_learner_payload,
                                      query_params=None
                                      )
  set_cache(key="learner_id", value=context.learner_id)


@behave.when(
  "the learning resource uuid and learner uuid is correctly passed to fetch learner progress")
def step_impl2(context):
  # get request to slp api
  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "learning_resources",
                                          "node_id": context.lr_id
                                        }
                                        )
  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the learner progress for that learning resource will be correctly fetched")
def step_impl3(context):
  assert context.res_status == 200
  assert context.res_body["data"] is not None
  assert context.res_body["data"]["status"] == TEST_PROGRESS["status"]
  assert context.res_body["data"]["is_locked"] == TEST_PROGRESS["is_locked"]
  assert context.res_body["data"]["progress"] == TEST_PROGRESS["progress"]


# ------------------------------ Scenario 07 -----------------------------------
"""
Fetch Learner progress with incorrect learning resource uuid and learner uuid
"""


@behave.given("that the learning resource uuid is incorrect")
def step_impl1(context):
  context.dummy_lr = "abc"
  context.learner_id = get_cache(key="learner_id")


@behave.when("the incorrect learning resource uuid and learner uuid is passed")
def step_impl2(context):
  get_learner_progress_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/learner/{context.learner_id}/progress"

  get_learner_progress_res = get_method(url=get_learner_progress_url,
                                        query_params={
                                          "node_type": "learning_resources",
                                          "node_id": context.dummy_lr
                                        }
                                        )

  context.res_status = get_learner_progress_res.status_code
  context.res_body = get_learner_progress_res.json()


@behave.then(
  "the api responds with 404 status and message as Learning Resource not found")
def step_impl3(context):
  assert context.res_status == 404
  assert f"id {context.dummy_lr} not found" in context.res_body["message"]
