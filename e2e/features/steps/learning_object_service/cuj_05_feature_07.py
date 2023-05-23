"""
Delete full Learning Hierarchy given ID
"""
import behave
import sys
import json

sys.path.append("../")
from e2e.setup import post_method, get_method, delete_method
from e2e.test_config import (API_URL_LEARNING_OBJECT_SERVICE, DEL_KEYS,
                        API_URL_LEARNER_PROFILE_SERVICE)
from environment import (TEST_LEARNING_HIERARCHY_PATH)

API_URL = API_URL_LEARNING_OBJECT_SERVICE

#LXE/CD ingest the full learning that is designed to be ingested via JSON----------------------------------------

@behave.given("that a LXE/CD has access to the content authoring tool and has a valid pathway ID that needs to be deleted with all of its components")
def step_impl_1(context):
  context.json_file = TEST_LEARNING_HIERARCHY_PATH
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json"

  # Create Learning Hierarchy
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.res = post_method(
      url=context.url,
      files={"json_file": hierarchy_data})
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.input_data = json.load(hierarchy_data)
  
  assert context.res.status_code == 200, "Hierarchy Ingestion Failed"
  context.created_hierarchy = context.res.json()
  context.hierarchy_id = context.created_hierarchy["data"][0]

  context.created_hierarchy = context.res.json()
  context.hierarchy_id = context.created_hierarchy["data"][0]
  context.get_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{context.hierarchy_id}"
  context.query_params = {
    "fetch_tree": True,
    "frontend_response": False
  }
  context.get_res = get_method(url = context.get_url,
                      query_params=context.query_params)
  assert context.get_res.status_code == 200, "Ingested Hierarchy not fetched"
  context.get_res_data = context.get_res.json()["data"]

  # Check Correct Program Details are inserted
  context.program = context.get_res_data
  context.input_program = context.input_data["curriculum_pathways"]

  # Check Correct Discipline Details are inserted
  context.discipline = context.program["child_nodes"]["curriculum_pathways"][0]
  context.input_discipline = context.input_program["child_nodes"]["curriculum_pathways"][0]

  # Check Correct Level Details are inserted
  context.level = context.discipline["child_nodes"]["curriculum_pathways"][0]
  context.input_level = context.input_discipline["child_nodes"]["curriculum_pathways"][0]

  # Check Correct Unit Details are inserted
  context.unit = context.level["child_nodes"]["curriculum_pathways"][0]
  context.input_unit = context.input_level["child_nodes"]["curriculum_pathways"][0]

  # Check Correct LE Details are inserted
  context.le = context.unit["child_nodes"]["learning_experiences"][0]
  context.input_le = context.input_unit["child_nodes"]["learning_experiences"][0]

  # Check Correct pretest Details are inserted
  context.pretest = context.le["child_nodes"]["learning_objects"][0]
  context.input_pretest = context.input_le["child_nodes"]["learning_objects"][0]

  # Check Correct PreTest Assessment Details are inserted
  context.pretest_assessment = context.pretest["child_nodes"]["assessments"][0]
  context.input_pretest_assessment = context.input_pretest["child_nodes"]["assessments"][0]
  
  # Check Correct Lesson Details are inserted
  context.lesson = context.le["child_nodes"]["learning_objects"][1]["child_nodes"]["learning_resources"][0]
  context.input_lesson = context.input_le["child_nodes"]["learning_objects"][1]["child_nodes"]["learning_resources"][0]

  # Check Correct Summative Assessment Details are inserted
  context.sa = context.le["child_nodes"]["learning_objects"][-1]["child_nodes"]["assessments"][0]
  context.input_sa = context.input_le["child_nodes"]["learning_objects"][-1]["child_nodes"]["assessments"][0]


@behave.when("they hit the endpoint with the valid pathway ID")
def step_impl_2(context):
  context.del_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-hierarchy/{context.hierarchy_id}"
  context.del_res = delete_method(url=context.del_url)
  context.del_res_data = context.del_res.json()

@behave.then("the full learning hierarchy is deleted")
def step_impl_3(context):
  assert context.del_res.status_code == 200, f"Status Code = {context.del_res.status_code}"


@behave.then("the achievements associated with node items in the hierarchy are deleted")
def step_impl_4(context):
  context.achievement_id = context.level["achievements"][0]["uuid"]
  context.achievement_url = f"{API_URL_LEARNER_PROFILE_SERVICE}/achievement/{context.achievement_id}"
  context.resp = get_method(url=context.achievement_url)
  context.resp_data = context.resp.json()
  assert context.resp.status_code == 404


# LXE/CD wants to delete the full learning that with an invalid pathway ID
@behave.given("that a LXE/CD has access to the content authoring tool and has a invalid pathway ID that needs to be deleted with all of its components")
def step_impl_1(context):
  context.hierarchy_id = "random_id"
  context.del_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-hierarchy/{context.hierarchy_id}"


@behave.when("they hit the endpoint with the invalid pathway ID")
def step_impl_2(context):
  context.del_res = delete_method(url=context.del_url)

@behave.then("the full learning hierarchy is not deleted and the endpoint throws 404 ResourceNotFound Error")
def step_impl_3(context):
  assert context.del_res.status_code == 404
