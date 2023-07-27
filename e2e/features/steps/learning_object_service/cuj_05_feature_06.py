"""
Import full Learning Hierarchy from JSON
"""
import behave
import sys
import json

sys.path.append("../")
from e2e.setup import post_method, get_method
from e2e.test_config import API_URL_LEARNING_OBJECT_SERVICE
from environment import (TEST_LEARNING_HIERARCHY_PATH, TEST_INVALID_LEARNING_HIERARCHY_PATH)

API_URL = API_URL_LEARNING_OBJECT_SERVICE

#LXE/CD ingest the full learning that is designed to be ingested via JSON----------------------------------------

@behave.given("that a LXE/CD has access to the content authoring tool and has a valid JSON that needs to be ingested into the system")
def step_impl_1(context):
  context.json_file = TEST_LEARNING_HIERARCHY_PATH
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json"


@behave.when("they hit the endpoint with the valid JSON")
def step_impl_2(context):
  # Create Learning Hierarchy
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.res = post_method(
      url=context.url,
      files={"json_file": hierarchy_data})
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.input_data = json.load(hierarchy_data)

@behave.then("the full learning hierarchy is ingested")
def step_impl_3(context):
  assert context.res.status_code == 200, "Hierarchy Ingestion Failed"
  context.created_hierarchy = context.res.json()
  context.hierarchy_id = context.created_hierarchy["data"][0]
  context.get_url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/{context.hierarchy_id}"
  context.query_params = {
    "fetch_tree": True,
    "frontend_response": False,
    "achievements": True,
    "references":True
  }
  context.get_res = get_method(url = context.get_url,
                      query_params=context.query_params)
  assert context.get_res.status_code == 200, "Ingested Hierarchy not fetched"
  context.get_res_data = context.get_res.json()["data"]
  print(context.hierarchy_id)
  
  # Check Correct Program Details are inserted
  context.program = context.get_res_data
  context.input_program = context.input_data
  assert context.program["name"] == context.input_program["name"], "Wrong Program Name"
  assert context.program["alias"] == context.input_program["alias"], "Wrong Alias of the Program"
  assert context.program["uuid"] == context.program["root_version_uuid"], "Wrong Root Version UUID"

  # Check Correct level Details are inserted
  context.level = context.program["child_nodes"]["curriculum_pathways"][0]
  context.input_level = context.input_program["child_nodes"]["curriculum_pathways"][0]
  assert context.level["name"] == context.input_level["name"], "Wrong level Name"
  assert context.level["alias"] == context.input_level["alias"], "Wrong Alias of the level"
  assert context.level["uuid"] == context.level["root_version_uuid"], "Wrong Root Version UUID"

  # Check Correct discipline Details are inserted
  context.discipline = context.level["child_nodes"]["curriculum_pathways"][0]
  context.input_discipline = context.input_level["child_nodes"]["curriculum_pathways"][0]
  assert context.discipline["name"] == context.input_discipline["name"], "Wrong Level Name"
  assert context.discipline["alias"] == context.input_discipline["alias"], "Wrong Alias of the Level"
  assert context.discipline["uuid"] == context.discipline["root_version_uuid"], "Wrong Root Version UUID"

  # Check Correct Unit Details are inserted
  context.unit = context.discipline["child_nodes"]["curriculum_pathways"][0]
  context.input_unit = context.input_discipline["child_nodes"]["curriculum_pathways"][0]

  assert context.unit["name"] == context.input_unit["name"], "Wrong Level Name"
  assert context.unit["alias"] == context.input_unit["alias"], "Wrong Alias of the Level"
  assert context.unit["uuid"] == context.unit["root_version_uuid"], "Wrong Root Version UUID"

  # Check Correct LE Details are inserted
  context.le = context.unit["child_nodes"]["learning_experiences"][0]
  context.input_le = context.input_unit["child_nodes"]["learning_experiences"][0]
  assert context.le["name"] == context.input_le["name"], "Wrong Learning Experience Name"
  assert context.le["alias"] == context.input_le["alias"], "Wrong Alias of the Learning Experience"
  assert context.le["uuid"] == context.le["root_version_uuid"], "Wrong Root Version UUID"

  # Check Correct pretest Details are inserted
  context.pretest = context.le["child_nodes"]["learning_objects"][0]
  context.input_pretest = context.input_le["child_nodes"]["learning_objects"][0]
  assert context.pretest["name"] == context.input_pretest["name"], "Wrong Pretest Name"
  assert context.pretest["alias"] == context.input_pretest["alias"], "Wrong Alias of the Pretest"
  assert context.pretest["uuid"] == context.pretest["root_version_uuid"], "Wrong Root Version UUID"

  # Check Correct PreTest Assessment Details are inserted
  context.pretest_assessment = context.pretest["child_nodes"]["assessments"][0]
  context.input_pretest_assessment = context.input_pretest["child_nodes"]["assessments"][0]
  assert context.pretest_assessment["name"] == context.input_pretest_assessment["name"], \
    "Wrong Pretest Assessment Name"
  assert context.pretest_assessment["type"] == context.input_pretest_assessment["type"], \
    "Wrong Pretest Assessment Type"
  
  # Check Correct Lesson Details are inserted
  context.lesson = context.le["child_nodes"]["learning_objects"][1]["child_nodes"]["learning_resources"][0]
  context.input_lesson = context.input_le["child_nodes"]["learning_objects"][1]["child_nodes"]["learning_resources"][0]
  assert context.lesson["name"] == context.input_lesson["name"], "Wrong Lesson Name"
  assert context.lesson["type"] == context.input_lesson["type"], "Wrong Lesson Type"
  assert context.lesson["uuid"] == context.lesson["root_version_uuid"], "Wrong Root Version UUID"

  # Check Correct Summative Assessment Details are inserted
  context.sa = context.le["child_nodes"]["learning_objects"][-1]["child_nodes"]["assessments"][0]
  context.input_sa = context.le["child_nodes"]["learning_objects"][-1]["child_nodes"]["assessments"][0]
  assert context.sa["name"] == context.input_sa["name"], "Wrong Summative Assessment Name"
  assert context.sa["type"] == context.input_sa["type"], "Wrong Summative Assessment Type"


@behave.then("the achievements associated with node items in the hierarchy are ingested")
def step_impl_4(context):
  # Check Correct Achievements were associated with the node items"
  assert context.discipline["achievements"][0]["name"] == context.input_discipline["achievements"][0]["name"], "Wrong Achievement Name"
  assert context.discipline["achievements"][0]["type"] == context.input_discipline["achievements"][0]["type"], "Wrong Achievement Type"

@behave.then("the competencies associated with node items in the hierarchy are ingested")
def step_impl_5(context):
  pass
  # assert context.sa["references"]["competencies"][0]["name"] == context.input_sa["references"]["competencies"][0]["name"], "Wrong Competency Name"
  # assert context.sa["references"]["competencies"][0]["description"] == context.input_sa["references"]["competencies"][0]["description"], "Wrong Competency Description"


@behave.then("the skills associated with node items in the hierarchy are ingested")
def step_impl_6(context):
  assert context.pretest["references"]["skills"][0]["name"] == context.input_pretest["references"]["skills"][0]["name"], "Wrong Skill Name"
  assert context.pretest["references"]["skills"][0]["description"] == context.input_pretest["references"]["skills"][0]["description"], "Wrong Skill Description"

@behave.then("relationships established in the JSON are maintained")
def step_impl_7(context):
  context.get_module_url = f"""{API_URL_LEARNING_OBJECT_SERVICE}/learning-object/{context.pretest["uuid"]}"""
  context.get_module_res = get_method(url=context.get_module_url).json()
  context.get_le_url = f"""{API_URL_LEARNING_OBJECT_SERVICE}/learning-experience/{context.le["uuid"]}"""
  context.get_le_res = get_method(url=context.get_le_url).json()

  context.module = context.get_module_res["data"]
  context.le = context.get_le_res["data"]

  context.skills_list = []
  # for skills_id in context.sa["references"]["competencies"][0]["child_nodes"]["skills"]:
  #    context.skills_list.append(skills_id["uuid"])
  # assert context.pretest["references"]["skills"][0]["uuid"] in context.skills_list
  # assert context.pretest["references"]["skills"][0]["parent_nodes"]["competencies"][0] == context.sa["references"]["competencies"][0]["uuid"]
  # assert context.module["parent_nodes"]["learning_experiences"][0] == context.le["uuid"]
  # assert context.le["child_nodes"]["learning_objects"][0] == context.module["uuid"]

#LXE/CD ingest the full learning that is designed to be ingested via invalid JSON NEGATIVE
@behave.given("that a LXE/CD has access to the content authoring tool and has an invalid JSON that needs to be ingested into the system")
def step_impl_1(context):
  context.json_file = TEST_INVALID_LEARNING_HIERARCHY_PATH
  context.url = f"{API_URL_LEARNING_OBJECT_SERVICE}/curriculum-pathway/bulk-import/json"

@behave.when("they hit the endpoint with the invalid JSON")
def step_impl_2(context):
  with open(context.json_file, encoding="UTF-8") as hierarchy_data:
    context.res = post_method(
      url=context.url,
      files={"json_file": hierarchy_data})

@behave.then("the full learning hierarchy is not ingested and the endpoint throws 422 Validation Error")
def step_impl_3(context):
  assert context.res.status_code == 422
