"""
Feature 14 - API Test Script For Matching Engine Operations
"""

import behave
from time import sleep
import sys
import os
import json
sys.path.append("../")
from setup import post_method, set_cache, get_cache, get_method, put_method, delete_method
from test_config import API_URL_MATCHING_ENGINE, TESTING_OBJECTS_PATH
from test_object_schemas import E2E_SKILL_INDEX_ID, INDEX_ENDPOINT_ID

TEST_EMBEDDING_PATH = os.path.join(TESTING_OBJECTS_PATH, "test_query_embedding.json")
with open(TEST_EMBEDDING_PATH) as embedding_file:
  test_query_embedding_dict = json.load(embedding_file)

TEST_QUERY_EMBEDDING = test_query_embedding_dict["TEST_QUERY_EMBEDDING"]


#----------------------------- Scenario 01 --------------------------------

@behave.given("that there are indexes present in matching engine and user has access to fetch all indexes from matching engine")
def step_impl1(context):
  context.url = f"{API_URL_MATCHING_ENGINE}/index"


@behave.when("API to fetch all indexes is called by providing correct URL")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Matching Engine will retrieve and return all indexes stored in the matching engine")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("message") == "Successfully fetched all indexes"


#----------------------------- Scenario 02 --------------------------------

@behave.given("that there are indexes present in matching engine and user has access to fetch index from matching engine")
def step_impl1(context):
  context.url = f"{API_URL_MATCHING_ENGINE}/index/{E2E_SKILL_INDEX_ID}"


@behave.when("API to fetch index is called by providing an index id in the URL")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Matching Engine will retrieve and return the indexes stored in the matching engine corresponding to given index id")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("message") == "Successfully fetched the index"


#----------------------------- Scenario 03 --------------------------------

@behave.given("that there are indexes present in matching engine and user has privilege to fetch index from matching engine")
def step_impl1(context):
  invalid_index_id = "123456"
  context.url = f"{API_URL_MATCHING_ENGINE}/index/{invalid_index_id}"


@behave.when("API to fetch index is called by providing an invalid index id in the URL")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Matching Engine will throw an internal error as invalid index id was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not True"


#----------------------------- Scenario 04 --------------------------------

@behave.given("that there are index endpoints present in matching engine and user has access to fetch all index endpoints from matching engine")
def step_impl1(context):
  context.url = f"{API_URL_MATCHING_ENGINE}/index-endpoint"


@behave.when("API to fetch all index endpoints is called by providing correct URL")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Matching Engine will retrieve and return all index endpoints stored in the matching engine")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("message") == "Successfully fetched all index endpoints"

#----------------------------- Scenario 05 --------------------------------

@behave.given("that there are index endpoints present in matching engine and user has access to fetch index endpoint from matching engine")
def step_impl1(context):
  context.url = f"{API_URL_MATCHING_ENGINE}/index-endpoint/{INDEX_ENDPOINT_ID}"


@behave.when("API to fetch index endpoint is called by providing an index endpoint id in the URL")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Matching Engine will retrieve and return the index endpoint stored in the matching engine corresponding to given index endpoint id")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("message") == "Successfully fetched the index endpoint"


#----------------------------- Scenario 06 --------------------------------

@behave.given("that there are index endpoints present in matching engine and user has privilege to fetch index endpoint from matching engine")
def step_impl1(context):
  invalid_endpoint_id = "123456"
  context.url = f"{API_URL_MATCHING_ENGINE}/index-endpoint/{invalid_endpoint_id}"


@behave.when("API to fetch index endpoint is called by providing an invalid index endpoint id in the URL")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Matching Engine will throw an internal error as invalid index endpoint id was provided")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not True"


#----------------------------- Scenario 07 --------------------------------

@behave.given("that nearest neighbors exist in matching engine and user has access to fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "index_id":E2E_SKILL_INDEX_ID,
      "query_embeddings": TEST_QUERY_EMBEDDING
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/result"


@behave.when("API to fetch nearest neighbors from matching engine is called by providing correct request payload")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Matching Engine will retrieve and return all nearest neighbors stored in the matching engine corresponding to index_id and query_embeddings given in request payload")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("message") == "Successfully fetched all nearest neighbors of given query", "Expected response not same"
  assert len(context.res_data.get("data")) == 10


#----------------------------- Scenario 08 --------------------------------

@behave.given("that nearest neighbors exist in matching engine and user can fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "index_id": "123456",
      "query_embeddings": TEST_QUERY_EMBEDDING
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/result"


@behave.when("API to fetch nearest neighbors from matching engine is called by providing invalid index id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Matching Engine will throw a validation error while trying to fetch neighbors as invalid index id was given")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"



#----------------------------- Scenario 09 --------------------------------

@behave.given("that nearest neighbors exist in matching engine and user has privilege to fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "index_id":E2E_SKILL_INDEX_ID,
      "query_embeddings": "random_embedding"
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/result"


@behave.when("API to fetch nearest neighbors from matching engine is called by providing invalid query_embeddings")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Matching Engine will throw a validation error while trying to fetch neighbors as invalid query_embeddings was given")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 10 --------------------------------

@behave.given("that nearest neighbors exist in matching engine and user can access functionality fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "query_embeddings": TEST_QUERY_EMBEDDING
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/result"


@behave.when("API to fetch nearest neighbors from matching engine is called with missing index id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Matching Engine will throw a validation error while trying to fetch neighbors as index id is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


# #----------------------------- Scenario 11 --------------------------------

@behave.given("that nearest neighbors exist in matching engine and user has ability to fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "index_id":E2E_SKILL_INDEX_ID
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/result"


@behave.when("API to fetch nearest neighbors from matching engine is called with missing query_embeddings")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Matching Engine will throw a validation error while trying to fetch neighbors as query_embeddings is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 12 --------------------------------

@behave.given("that nearest neighbors exist in matching engine and user has access to fetch nearest neighbors from matching engine by giving multiple queries")
def step_impl1(context):
  context.req_body = {
      "index_id":E2E_SKILL_INDEX_ID,
      "batch_query_embeddings": [TEST_QUERY_EMBEDDING]
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/batch-result"


@behave.when("API to fetch nearest neighbors from matching engine is called by providing correct request payload with multiple queries at once")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Matching Engine will retrieve and return all nearest neighbors stored in the matching engine corresponding to all queries given in request payload")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data["success"] is True, "Success is not True"
  assert context.res_data.get("message") == "Successfully fetched all nearest neighbors         of for all queries in the batch", "Expected response not same"
  assert len(context.res_data.get("data")) == 1
  assert len(context.res_data.get("data").get("0")) == 10

#----------------------------- Scenario 13 --------------------------------

@behave.given("that nearest neighbors exist in matching engine for multiple queries and user can fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "index_id": "123456",
      "batch_query_embeddings": [TEST_QUERY_EMBEDDING]
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/batch-result"


@behave.when("API to fetch nearest neighbors for multiple queries from matching engine is called by providing invalid index id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)
  context.res_data = context.res.json()


@behave.then("Matching Engine will throw a validation error while trying to fetch neighbors for multiple queries as invalid index id was given")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data["success"] is False, "Success is not False"


#----------------------------- Scenario 14 --------------------------------

@behave.given("that nearest neighbors exist in matching engine for multiple queries and user has privilege to fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "index_id":E2E_SKILL_INDEX_ID,
      "batch_query_embeddings": ["123456"]
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/batch-result"


@behave.when("API to fetch nearest neighbors for multiple queries from matching engine is called by providing invalid batch_query_embeddings")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Matching Engine will throw a validation error while trying to fetch neighbors for multiple queries as invalid batch_query_embeddings was given")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 15 --------------------------------

@behave.given("that nearest neighbors exist in matching engine for multiple queries and user can access functionality fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "batch_query_embeddings": [TEST_QUERY_EMBEDDING]
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/batch-result"


@behave.when("API to fetch nearest neighbors for multiple queries from matching engine is called with missing index id")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Matching Engine will throw a validation error while trying to fetch neighbors for multiple queries as index id is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"


#----------------------------- Scenario 16 --------------------------------

@behave.given("that nearest neighbors exist in matching engine for multiple queries and user has ability to fetch nearest neighbors from matching engine by giving query")
def step_impl1(context):
  context.req_body = {
      "index_id":E2E_SKILL_INDEX_ID
    }
  context.url = f"{API_URL_MATCHING_ENGINE}/query/batch-result"


@behave.when("API to fetch nearest neighbors for multiple queries from matching engine is called with missing batch_query_embeddings")
def step_impl2(context):
  context.res = post_method(url=context.url, request_body=context.req_body)


@behave.then("Matching Engine will throw a validation error while trying to fetch neighbors for multiple queries as batch_query_embeddings is missing")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"
