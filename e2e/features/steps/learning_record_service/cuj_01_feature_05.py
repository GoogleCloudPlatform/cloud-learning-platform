"""
Feature 05 - CRUD APIs for managing Statement data in Learning Record Service
"""
import behave
import sys
sys.path.append("../")
from uuid import uuid4
from e2e.setup import post_method, get_method, set_cache, get_cache, setup_rules_engine_data
from copy import deepcopy
from endpoint_proxy import get_baseurl
from e2e.test_object_schemas import TEST_ACTIVITY, TEST_AGENT, TEST_LEARNING_EXPERIENCE, TEST_VERB, TEST_XAPI_STATEMENT_1, TEST_XAPI_STATEMENT_2, TEST_SESSION
from e2e.test_config import API_URL_LEARNING_RECORD_SERVICE, API_URL_LEARNING_OBJECT_SERVICE, API_URL_USER_MANAGEMENT, DEL_KEYS


#-------------------------------CREATE STATEMENT-------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to Learning Record Service and needs to create xAPI Statements"
)
def step_impl_1(context):
  """
  I can access LRS APIs to create xAPI Statements
  Parameters
  ----------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  test_verb = deepcopy({**TEST_VERB})
  test_activity = deepcopy({**TEST_ACTIVITY})
  test_activity["name"] = f"{str(uuid4())}"
  context.user_id, context.learner_id, context.agent_id, context.verb_id, \
    context.activity_id = setup_rules_engine_data(test_verb, test_activity)

  context.learning_req_body = deepcopy(TEST_LEARNING_EXPERIENCE)
  for key in DEL_KEYS:
    if key in context.learning_req_body:
      del context.learning_req_body[key]
  create_learning_experience = post_method(
      url=f"{API_URL_LEARNING_OBJECT_SERVICE}/learning-experience",
      request_body=context.learning_req_body)
  created_learning_experience_data = create_learning_experience.json()
  context.learning_experience_id = created_learning_experience_data["data"][
      "uuid"]

  test_session = deepcopy({
      **TEST_SESSION, "user_id": context.user_id
  })
  create_session = post_method(
      url=f"{API_URL_USER_MANAGEMENT}/session",
      request_body=test_session)
  create_session_res = create_session.json()

  TEST_XAPI_STATEMENT_1["object"]["uuid"] = context.activity_id
  test_statement_1 = deepcopy({
      **TEST_XAPI_STATEMENT_1, "actor": deepcopy({**TEST_AGENT, "user_id": context.user_id, "uuid": context.agent_id}),
      "object": {
          **TEST_XAPI_STATEMENT_1["object"], "canonical_data": {
              "name": "activity test",
              "type": "learning_experiences",
              "uuid": context.learning_experience_id,
              "hierarchy": {}
          }
      },
      "session_id": create_session_res["data"]["session_id"],
      "verb": deepcopy({**TEST_VERB, "uuid": context.verb_id})

  })
  print("test_statement_1")
  print(test_statement_1)
  TEST_XAPI_STATEMENT_2["object"]["uuid"] = context.activity_id
  test_statement_2 = deepcopy({
      **TEST_XAPI_STATEMENT_2,  "actor": deepcopy({**TEST_AGENT, "user_id": context.user_id, "uuid": context.agent_id}),
      "object": {
          **TEST_XAPI_STATEMENT_2["object"], "canonical_data": {
              "name": "activity test",
              "type": "learning_experiences",
              "uuid": context.learning_experience_id,
              "hierarchy": {}
          }
      },
      "session_id": create_session_res["data"]["session_id"],
      "verb": deepcopy({**TEST_VERB, "uuid": context.verb_id})
  })
  print("test_statement_2")
  print(test_statement_2)
  context.statements = [test_statement_1, test_statement_2]
  access_url = get_baseurl("learning-record-service") + "/ping"
  access_res = get_method(url=access_url)
  access_res_data = access_res.json()
  print("access_res_data")
  print(access_res_data)
  assert access_res_data["message"] ==\
      "Successfully reached Learning Record Service"
  assert access_res_data["success"], "Cannot reach Learning Record Service"
  context.post_url = f"{API_URL_LEARNING_RECORD_SERVICE}/statements"


@behave.when(
    "API request is sent to create Statements with correct request payload")
def step_impl_2(context):
  context.post_res = post_method(
      url=context.post_url, request_body=context.statements)
  context.post_res_data = context.post_res.json()
  print("post_res_data")
  print(context.post_res_data)

@behave.then("The xAPI Statements will be created successfully")
def step_impl_3(context):
  assert context.post_res.status_code == 200, "Statement object creation failed"
  assert context.post_res_data["message"] ==\
      "Successfully added the given statement/s"


@behave.then("API request is sent to fetch the created Statements")
def step_impl_4(context):
  uuids = context.post_res_data["data"]
  set_cache(key="statement_ids", value=uuids)
  context.fetched_statements = []
  for uuid in uuids:
    get_url = f"{API_URL_LEARNING_RECORD_SERVICE}/statement/{uuid}"
    get_res = get_method(url=get_url)
    get_res_data = get_res.json()
    print("get_res_data")
    print(get_res_data)
    assert get_res_data["success"], "Cannot fetch xAPI Statement."
    assert get_res_data["message"] == "Successfully fetched the statement"
    fetched_statement = get_res_data["data"]
    del fetched_statement["stored"]
    del fetched_statement["timestamp"]
    del fetched_statement["uuid"]
    if fetched_statement["object"]["canonical_data"].get(
      "existing_document",""):
      del fetched_statement["object"]["canonical_data"]["existing_document"]
    context.fetched_statements.append(fetched_statement)

@behave.then("The fetched Statements are same as the created Statements")
def step_impl_4(context):
  assert len(context.statements)==len(context.fetched_statements), "Statement data not stored in BigQuery properly"

# --- Negative Scenario ---
@behave.given(
    "A user has access privileges to Learning Record Service and needs to create an xAPI Statement"
)
def step_impl_1(context):
  """
  I can access LRS APIs to create xAPI Statements
  Parameters
  ----------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  test_statement_1 = deepcopy(TEST_XAPI_STATEMENT_1)
  test_statement_2 = deepcopy(TEST_XAPI_STATEMENT_2)
  del test_statement_1["object_type"]
  del test_statement_2["actor"]
  context.statements = [test_statement_1, test_statement_2]

  access_url = get_baseurl("learning-record-service") + "/ping"
  access_res = get_method(url=access_url)
  access_res_data = access_res.json()
  assert access_res_data["message"] ==\
      "Successfully reached Learning Record Service"
  assert access_res_data["success"], "Cannot reach Learning Record Service"

  context.post_url = f"{API_URL_LEARNING_RECORD_SERVICE}/statements"


@behave.when(
    "API request is sent to create Statement with incorrect request payload")
def step_impl_2(context):
  context.post_res = post_method(
      url=context.post_url, request_body=context.statements)
  context.post_res_data = context.post_res.json()


@behave.then("The xAPI Statement object creation will fail")
def step_impl_3(context):
  assert context.post_res.status_code == 422, "xAPI Statement object created"
  assert context.post_res_data["message"] == "Validation Failed"
  assert not context.post_res_data["success"]


#-------------------------------GET STATEMENT-------------------------------
# --- Negative Scenario ---
@behave.given(
    "A user has access to Learning Record Service and needs to fetch an xAPI Statement"
)
def step_impl_1(context):
  """
  I can access LRS APIs to create xAPI Statements
  Parameters
  ----------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.uuid = "wrong_id"

  access_url = get_baseurl("learning-record-service") + "/ping"
  access_res = get_method(url=access_url)
  access_res_data = access_res.json()
  assert access_res_data["message"] ==\
      "Successfully reached Learning Record Service"
  assert access_res_data["success"], "Cannot reach Learning Record Service"

  context.get_url = f"{API_URL_LEARNING_RECORD_SERVICE}/statement/{context.uuid}"


@behave.when(
    "API request is sent to fetch the xAPI Statement with incorrect Statement uuid"
)
def step_impl_2(context):
  context.get_res = get_method(url=context.get_url)
  context.get_res_data = context.get_res.json()
  print("context.get_res")
  print(context.get_res)
  print("context.get_res_data")
  print(context.get_res_data)


@behave.then(
    "The xAPI Statement will not be fetched and Learning Record Service will throw ResourceNotFound error"
)
def step_impl_3(context):
  print("context.get_res_data")
  print(context.get_res.status_code)
  assert context.get_res.status_code == 404
  assert not context.get_res_data["success"], "Fetched xAPI Statement."


#------------------------------GET ALL STATEMENTS-------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to Learning Record Service and needs to fetch all xAPI Statements"
)
def step_impl_1(context):
  """
  I can access LRS APIs to fetch xAPI Statements
  Parameters
  ----------
  context: behave.runner.Context

  Returns
  -------
  None
  """
  context.uuids = get_cache(key="statement_ids")

  access_url = get_baseurl("learning-record-service") + "/ping"
  access_res = get_method(url=access_url)
  access_res_data = access_res.json()
  assert access_res_data["message"] ==\
      "Successfully reached Learning Record Service"
  assert access_res_data["success"], "Cannot reach Learning Record Service"

  context.get_url = f"{API_URL_LEARNING_RECORD_SERVICE}/statements"


@behave.when(
    "API request is sent to fetch all the xAPI Statements with correct request parameters"
)
def step_impl_2(context):
  query_params = {"skip": 0, "limit": 1}
  context.get_res = get_method(url=context.get_url, query_params=query_params)
  context.get_res_data = context.get_res.json()


@behave.then("the Learning Record Service will serve up all the xAPI Statements"
            )
def step_impl_3(context):
  temp = context.uuids[::-1]
  assert context.get_res.status_code == 200, "xAPI Statements cannot be fetched"
  assert context.get_res_data["success"]
  assert context.get_res_data["message"] ==\
      "Successfully fetched the statements"
  assert temp[0] in [statement["uuid"] for statement in context.get_res_data["data"]] 


#------------------------------GET ALL STATEMENTS-------------------------------
# --- Negative Scenario ---
@behave.given(
    "A user has access privileges to Learning Record Service and needs to fetch all xAPI Statements"
)
def step_impl_1(context):
  """
  I can access LRS APIs to create xAPI Statements
  Parameters
  ----------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  access_url = get_baseurl("learning-record-service") + "/ping"
  access_res = get_method(url=access_url)
  access_res_data = access_res.json()
  assert access_res_data["message"] ==\
      "Successfully reached Learning Record Service"
  assert access_res_data["success"], "Cannot reach Learning Record Service"

  context.get_url = f"{API_URL_LEARNING_RECORD_SERVICE}/statements"


@behave.when(
    "API request is sent to fetch all the xAPI Statements with incorrect request parameters"
)
def step_impl_2(context):
  incorrect_agent = uuid4()
  query_params = {"agent": incorrect_agent, "skip": -1, "limit": 1}
  context.get_res = get_method(url=context.get_url, query_params=query_params)
  context.get_res_data = context.get_res.json()


@behave.then(
    "The xAPI Statements will not be fetched and Learning Record Service will throw validation error"
)
def step_impl_3(context):
  assert context.get_res.status_code == 422
  assert not context.get_res_data["success"], "Fetched xAPI Statement."


#-------------------------------GET LRS DETAILS-------------------------------
# --- Positive Scenario ---
@behave.given(
    "A user has access to Learning Record Service and needs to fetch its details"
)
def step_impl_1(context):
  """
  I can access LRS APIs to create xAPI Statements
  Parameters
  ----------
  context: behave.runner.Context

  Returns
  -------
  None
  """

  access_url = get_baseurl("learning-record-service") + "/ping"
  access_res = get_method(url=access_url)
  access_res_data = access_res.json()
  assert access_res_data["message"] ==\
      "Successfully reached Learning Record Service"
  assert access_res_data["success"], "Cannot reach Learning Record Service"

  context.get_url = f"{API_URL_LEARNING_RECORD_SERVICE}/about"


@behave.when(
    "API request is sent to fetch the details of Learning Record Service")
def step_impl_2(context):
  context.get_res = get_method(url=context.get_url)
  context.get_res_data = context.get_res.json()


@behave.then("The Learning Record Service will return its details")
def step_impl_3(context):
  assert context.get_res.status_code == 200, "LRS details cannot be fetched"
  assert context.get_res_data["success"]
  assert context.get_res_data["message"] ==\
      "Successfully fetched the details about LRS"