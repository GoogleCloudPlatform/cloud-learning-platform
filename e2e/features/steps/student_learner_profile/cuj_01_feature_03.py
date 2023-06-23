"""Behave Test for Learner achievements are updated
  as the user progresses through a learning pathway"""

from e2e.setup import post_method, get_method, delete_method, put_method
import behave
import sys
from uuid import uuid4
from copy import copy
sys.path.append("../")
from e2e.test_object_schemas import (LEARNER_OBJECT_TEMPLATE,
                                ACHIEVEMENT_OBJECT_TEMPLATE,
                                LEARNER_PROFILE_TEMPLATE)

from e2e.test_config import (API_URL_LEARNER_PROFILE_SERVICE,
                          API_URL_LEARNING_OBJECT_SERVICE)
from environment import (TEST_LEARNING_HIERARCHY_PATH)

API_URL = API_URL_LEARNER_PROFILE_SERVICE


# Scenario 1
@behave.given(
    "The learner completes competencies/credits and/or "
    "credentials (i.e.: 'achievements' associated with a learning pathway) "
    "as they progress through a learning pathway")
def step_1_1(context):
  """Defining the payload required for creating a Learner, Learner Profile and
      Achievement"""
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{str(uuid4())}@gmail.com"
  context.learner_url = f"{API_URL}/learner"
  learner_post_res = post_method(url=context.learner_url,
                                request_body=learner_dict)
  learner_post_res_data = learner_post_res.json()
  context.learner_id = learner_post_res_data["data"]["uuid"]
  assert learner_post_res.status_code == 200, "Status code not 200"

  context.learner_profile_dict = copy(LEARNER_PROFILE_TEMPLATE)
  context.learner_profile_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
  learner_profile_post_res = post_method(url=context.learner_profile_url,
                                    request_body=context.learner_profile_dict)
  learner_profile_post_res_data = learner_profile_post_res.json()
  context.learner_profile_id = learner_profile_post_res_data["data"]["uuid"]
  assert learner_profile_post_res.status_code == 200, "Status code not 200"

  achievement_dict = copy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_url = f"{API_URL}/achievement"
  achievement_post_res = post_method(url=achievement_url,
                                        request_body=achievement_dict)
  achievement_post_res_data = achievement_post_res.json()
  context.achievement_id = achievement_post_res_data["data"]["uuid"]
  assert achievement_post_res.status_code == 200, "Status code not 200"


@behave.when("Achievements are completed")
def step_1_2(context):
  """Updating the learner profile with uuid of completed achivement"""
  updated_learner_profile_dict = context.learner_profile_dict
  updated_learner_profile_dict["achievements"] = [context.achievement_id]
  del updated_learner_profile_dict["enrollment_information"]
  del updated_learner_profile_dict["is_archived"]
  update_achivement_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
  learner_profile_put_res = put_method(
      url=update_achivement_url, request_body=updated_learner_profile_dict)
  learner_profile_put_res_data = learner_profile_put_res.json()
  assert learner_profile_put_res.status_code == 200
  assert learner_profile_put_res_data["success"] is True



@behave.then("Achievement is logged in SLP so that the learner can view an up-to-date record of their achievements through the learner-facing profile interface")
def step_1_3(context):
  """fetching an achievement"""
  get_res = get_method(url=context.learner_profile_url)
  get_res_data = get_res.json()
  assert get_res.status_code == 200
  assert get_res_data["success"] is True
  assert get_res_data["data"]["learner_id"] == context.learner_id
  assert context.achievement_id in get_res_data["data"]["achievements"]

  # delete learner
  delete_method(url=context.learner_url + "/" + context.learner_id)


# Scenario 2
@behave.given(
    "The learner completes competencies/credits and/or "
    "credentials (i.e.: 'achievements' associated with a learning pathway) "
    "as they progress through a learning pathway (negative)")
def step_2_1(context):
  """Defining the payload required for creating a Learner, Learner Profile and
      Achievement"""
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{uuid4()}@gmail.com"
  context.learner_url = f"{API_URL}/learner"
  learner_post_res = post_method(url=context.learner_url,
                                request_body=learner_dict)
  learner_post_res_data = learner_post_res.json()
  context.learner_id = learner_post_res_data["data"]["uuid"]
  assert learner_post_res.status_code == 200, "Status code not 200"

  context.learner_profile_dict = copy(LEARNER_PROFILE_TEMPLATE)
  context.learner_profile_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
  learner_profile_post_res = post_method(url=context.learner_profile_url,
                                    request_body=context.learner_profile_dict)
  learner_profile_post_res_data = learner_profile_post_res.json()
  context.learner_profile_id = learner_profile_post_res_data["data"]["uuid"]
  assert learner_profile_post_res.status_code == 200, "Status code not 200"

  achievement_dict = copy(ACHIEVEMENT_OBJECT_TEMPLATE)
  achievement_url = f"{API_URL}/achievement"
  achievement_post_res = post_method(url=achievement_url,
                                        request_body=achievement_dict)
  achievement_post_res_data = achievement_post_res.json()
  context.achievement_id = achievement_post_res_data["data"]["uuid"]
  assert achievement_post_res.status_code == 200, "Status code not 200"


@behave.when("Achievements are completed and incorrect achievement is tried to be updated in learner profile")
def step_2_2(context):
  """Updating the learner profile with invalid achivement uuid"""
  updated_learner_profile_dict = context.learner_profile_dict
  updated_learner_profile_dict["achievements"] = ["random_achivement_id"]
  del updated_learner_profile_dict["enrollment_information"]
  del updated_learner_profile_dict["is_archived"]
  update_achivement_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
  context.learner_profile_put_res = put_method(
      url=update_achivement_url, request_body=updated_learner_profile_dict)
  context.learner_profile_put_res_data = context.learner_profile_put_res.json()


@behave.then("SLP will throw a resource not found error as incorrect achievement was given")
def step_2_3(context):
  """Creating an Achievement"""
  assert context.learner_profile_put_res.status_code == 404
  assert context.learner_profile_put_res_data["success"] is False
  assert context.learner_profile_put_res_data["message"] == "Achievement with uuid random_achivement_id not found"

# Scenario 3
@behave.given(
    "The learner with an existing learner profile enrolled into a valid curriculum pathway program")
def step_3_1(context):
  """Defining the payload required for creating a Learner, Learner Profile and
      curriculum hierarchy"""
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{str(uuid4())}@gmail.com"
  context.learner_url = f"{API_URL}/learner"
  learner_post_res = post_method(url=context.learner_url,
                                request_body=learner_dict)
  learner_post_res_data = learner_post_res.json()
  context.learner_id = learner_post_res_data["data"]["uuid"]
  assert learner_post_res.status_code == 200, "Status code not 200"

  context.learner_profile_dict = copy(LEARNER_PROFILE_TEMPLATE)
  context.learner_profile_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
  learner_profile_post_res = post_method(url=context.learner_profile_url,
                                    request_body=context.learner_profile_dict)
  learner_profile_post_res_data = learner_profile_post_res.json()
  context.learner_profile_id = learner_profile_post_res_data["data"]["uuid"]

  # Create Learning Hierarchy
  with open(TEST_LEARNING_HIERARCHY_PATH, encoding="UTF-8") as hierarchy_data:
    created_hierarchy = post_method(
    url=f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json",
      files={"json_file": hierarchy_data})
    assert created_hierarchy.status_code == 200, "Hierarchy Ingestion Failed"
    created_hierarchy = created_hierarchy.json()
  context.hierarchy_id = created_hierarchy["data"][0]

@behave.when("Learner fetches achievements for a valid program")
def step_3_2(context):
  """Fetching learner achievements ifor a program"""
  learner_url = f"{API_URL}/learner/{context.learner_id}/achievements"
  get_learner_pathway_achievements_res = get_method(url=learner_url,
                                            query_params={
                                      "program_pathway_id":context.hierarchy_id
                                            }
                                        )
  context.res_status = get_learner_pathway_achievements_res.status_code
  context.res_body = get_learner_pathway_achievements_res.json()

@behave.then("SLP will return all achievements for the program along with the status of learner for each achievement")
def step_3_3(context):
  assert context.res_status == 200
  assert context.res_body["data"] is not None

# Scenario 4
@behave.given(
    "The learner with valid learner profile try to fetch learner achievements for an invalid Program")
def step_4_1(context):
  """Defining the payload required for creating a Learner, Learner Profile"""
  learner_dict = copy(LEARNER_OBJECT_TEMPLATE)
  learner_dict["email_address"] = f"{str(uuid4())}@gmail.com"
  context.learner_url = f"{API_URL}/learner"
  learner_post_res = post_method(url=context.learner_url,
                                request_body=learner_dict)
  learner_post_res_data = learner_post_res.json()
  context.learner_id = learner_post_res_data["data"]["uuid"]
  assert learner_post_res.status_code == 200, "Status code not 200"

  context.learner_profile_dict = copy(LEARNER_PROFILE_TEMPLATE)
  context.learner_profile_url = f"{API_URL}/learner/{context.learner_id}/learner-profile"
  learner_profile_post_res = post_method(url=context.learner_profile_url,
                                    request_body=context.learner_profile_dict)
  learner_profile_post_res_data = learner_profile_post_res.json()
  context.learner_profile_id = learner_profile_post_res_data["data"]["uuid"]

@behave.when("Learner fetches achievements for an invalid program")
def step_4_2(context):
  """Fetching learner achievements for an invalid program"""
  learner_url = f"{API_URL}/learner/{context.learner_id}/achievements"
  get_learner_pathway_achievements_res = get_method(url=learner_url,
                                            query_params={
                                      "program_pathway_id":"dummy_program"
                                            }
                                        )
  context.response = get_learner_pathway_achievements_res

@behave.then("SLP will throw a resource not found error as incorrect program curriculum pathway was given")
def step_4_3(context):
  assert context.response.status_code == 404
