"""
Feature 09 - API Test Script For Data Sources Management
"""

import behave
import sys
sys.path.append("../")
from setup import post_method, set_cache, get_cache, get_method, put_method, delete_method


@behave.given("Format the API request url to insert data source using object type and source")
def step_impl1(context):
  context.req_body = {
    "type": "test_skill",
    "source": "emsi"
  }
  context.url = f"http://localhost:9012/skill-service/api/v1/sources"


@behave.when("API request is sent to upsert the new data source using object type and source")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will create a new document for given object type and source")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("type") == context.req_body["type"], "type is incorrect"
  assert context.req_body["source"] in context.res_data.get("data").get("source"), "source is incorrect" 



@behave.given("Format the API request url to add a new data source for already existing object type")
def step_impl1(context):
  context.req_body = {
    "type": "test_skill",
    "source": "updated_emsi"
  }
  context.url = f"http://localhost:9012/skill-service/api/v1/sources"


@behave.when("API request is sent to upsert the new data source for already existing object type")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will add the new data source to already existing document for given object type")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("type") == context.req_body["type"], "type is incorrect"
  assert context.req_body["source"] in context.res_data.get("data").get("source"), "source is incorrect"




@behave.given("Format the API request url to update the object type with no source")
def step_impl1(context):
  context.req_body = {
    "type": "test_skill"
  }
  context.url = f"http://localhost:9012/skill-service/api/v1/sources"


@behave.when("API request is sent to upsert data sources")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Skill Service will throw an error message while trying to upsert the data source document")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"




@behave.given("Format the API request url to fetch all data sources for given object type")
def step_impl1(context):
  context.params = {"type": "test_skill"}
  context.url = f"http://localhost:9012/skill-service/api/v1/sources"


@behave.when("API request is sent to fetch data sources for given object type")
def step_impl2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()


@behave.then("Skill Service will return data sources for given object type")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert len(context.res_data.get("data")) == 1, "Found more than one objects"  
  assert context.res_data.get("data")[0].get("type") == context.params["type"], "type did not match"
  assert set(context.res_data.get("data")[0].get("source")) >= set(["emsi", "updated_emsi"]), "source did not match"




@behave.given("Format the API request url to fetch data sources for all object types")
def step_impl1(context):
  context.url = f"http://localhost:9012/skill-service/api/v1/sources"


@behave.when("API request is sent to fetch data sources for all object types")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will return data sources for all object type")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert len(context.res_data.get("data")) >= 1, "Found more than one objects"




@behave.given("Format the API request url to fetch data sources for incorrect object type")
def step_impl1(context):
  context.params = {"type": "random"}
  context.url = f"http://localhost:9012/skill-service/api/v1/sources"


@behave.when("API request is sent to fetch data sources for incorrect object type")
def step_impl2(context):
  context.res = get_method(url=context.url, query_params=context.params)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an error message while trying to fetch the data sources")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"





@behave.given("Format the API request url to update given matching engine id for given data source and object type")
def step_impl1(context):
  context.req_body = {
      "type": "test_role",
      "source": "emsi",
      "matching_engine_index_id": "2564025931601543168"
  }
  context.url = f"http://localhost:9012/skill-service/api/v1/sources"


@behave.when("API request is sent to update matching engine id in corresponding data source")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Skill Service will update the given matching engine ID in corresponding data source")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("data").get("type") == context.req_body["type"], "type is incorrect"
  assert context.res_data.get("data").get("matching_engine_index_id").get(context.req_body["source"]) == \
      context.req_body["matching_engine_index_id"], "matching engine id not updated"





@behave.given("Format the API request url to update the data source without providing matching engine ID")
def step_impl1(context):
  context.req_body = {
      "type": "test_role",
      "source": "emsi"
  }
  context.url = f"http://localhost:9012/skill-service/api/v1/sources"


@behave.when("API request is sent to try updating matching engine id in corresponding data source")
def step_impl2(context):
  context.res = put_method(url=context.url, request_body=context.req_body)


@behave.then("Skill Service will throw an error message while trying to update the data source")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
