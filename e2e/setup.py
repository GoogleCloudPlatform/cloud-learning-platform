"""
E2E Test Basic Configuration
"""
import json
import redis
import requests
import os
import uuid
from copy import deepcopy
from e2e.test_object_schemas import (TEST_USER, TEST_LRS_COMPLETED_EVENT,
                                 TEST_LRS_STARTED_EVENT, TEST_VERB,
                                 VALID_VERBS, TEST_USER_GROUP)
from e2e.test_config import (API_URL_LEARNING_RECORD_SERVICE,
                         API_URL_USER_MANAGEMENT,
                         API_URL_AUTHENTICATION_SERVICE)
from common.models import User, Verb, Agent, UserGroup
from common.utils.collection_references import collection_references
from common.utils.gcs_adapter import (is_valid_path,
                                        delete_file_from_gcs)

GCP_BUCKET = os.environ.get("GCP_PROJECT")
CONTENT_SERVING_BUCKET = os.environ.get("CONTENT_SERVING_BUCKET",
                          "core-learning-services-dev-content-serving-bucket")

UUID = uuid.uuid4()

USER_EMAIL = f"behave-e2e-test-{UUID}@gmail.com"

USER_PASSWORD = f"{UUID}"

# Redis Configuration for testing
red_con = redis.StrictRedis(host="localhost", port=6379, db=0)

api_key = os.environ.get("FIREBASE_API_KEY")


def set_cache(key: str, value: any) -> object:
  """
  Function to cache the value using redis
  Parameters
  ----------
  key: str
  value: any
  Returns
  -------
  cache value
  """
  return red_con.set(name=key, value=json.dumps(value))


def get_cache(key: str) -> object:
  """
  Function to cache the value using redis
  Parameters
  ----------
  key: str
  Returns
  -------
  cache value
  """
  val = red_con.get(name=key)
  return json.loads(val) if val else None


def delete_user_from_db() -> bool:
  """
  Function to delete an user from the firestore collection
  """
  user = User.find_by_email(USER_EMAIL)
  User.collection.delete(user.key)
  return True


def user_login() -> None:
  """
  Function to do firebase login
  """
  input_user = {**TEST_USER, "email": USER_EMAIL}
  user = User.from_dict(input_user)
  user.user_id = ""
  user.user_type_ref = ""
  user.save()
  user.user_id = user.id
  user.update()

  if api_key is None:
    raise Exception(
      "Firebase api key not found. "
      "Please export FIREBASE_API_KEY as environment variable"
    )
  req_body = {
    "email": USER_EMAIL,
    "password": USER_PASSWORD
  }
  sign_up_req = requests.post(
    f"{API_URL_AUTHENTICATION_SERVICE}/sign-up/credentials", json=req_body)

  sign_up_res = sign_up_req.json()
  print(f"User with {USER_EMAIL} tried signing up", sign_up_req.text)

  if sign_up_req.status_code == 200:
    print(f"User with {USER_EMAIL} was created and signed up with "
            f"token {sign_up_req.json()['data']['idToken']}")
    set_cache(key="id_token", value=sign_up_res["data"]["idToken"])

  if sign_up_req.status_code == 422 and sign_up_res.get(
    "message") == "EMAIL_EXISTS":
    print(f"User with {USER_EMAIL} already exists. Trying log in")
    sign_in_req = requests.post(
      f"{API_URL_AUTHENTICATION_SERVICE}/sign-in/credentials", json=req_body)

    sign_in_res = sign_in_req.json()
    if sign_in_res is None or sign_in_res["data"] is None:
      print("User signed in fail", sign_in_req.text)
      raise Exception("User sign-in failed")

    print(f"User with {USER_EMAIL} was signed in with "
          f"token {sign_in_req.json()['data']['idToken']}")

    set_cache(key="id_token", value=sign_in_res["data"]["idToken"])


def delete_user():
  """
  Function to delete firebase user
  """
  token = get_cache(key="id_token")
  if token:
    req_body = {"idToken": token}
    requests.post(
      f"https://identitytoolkit.googleapis.com/v1/accounts"
      f":delete?key={api_key}", req_body)


def post_method(url: str,
                request_body=None,
                query_params=None,
                data=None,
                files=None,
                token=None) -> json:
  """
  Function for API test POST method
  Parameters
  ----------
  url: str
  request_body: dict
  query_params: dict
  data: dict
  files: File
  token: token
  Returns
  -------
  JSON Object
  """

  if token is None:
    token = get_cache(key="id_token")
  headers = {"Authorization": f"Bearer {token}"}
  return requests.post(
    url=f"{url}",
    json=request_body,
    params=query_params,
    data=data,
    files=files,
    headers=headers)


def get_method(url: str, query_params=None, token=None) -> json:
  """
  Function for API test GET method
  Parameters
  ----------
  url: str
  query_params: dict
  token: token
  Returns
  -------
  JSON Object
  """

  if token is None:
    token = get_cache(key="id_token")
  headers = {"Authorization": f"Bearer {token}"}
  return requests.get(url=f"{url}", params=query_params, headers=headers,
                      allow_redirects=False)


def put_method(url: str,
               request_body: dict,
               query_params=None,
               token=None) -> json:
  """
  Function for API test PUT method
  Parameters
  ----------
  url: str
  request_body: dict
  query_params: dict
  token: token
  Returns
  -------
  JSON Object
  """

  if token is None:
    token = get_cache(key="id_token")
  headers = {"Authorization": f"Bearer {token}"}
  return requests.put(
    url=f"{url}", json=request_body, params=query_params, headers=headers)


def delete_method(url: str, query_params=None, token=None) -> json:
  """
  Function for API test DELETE method
  Parameters
  ----------
  url: str
  query_params: dict
  token: token
  Returns
  -------
  JSON Object
  """

  if token is None:
    token = get_cache(key="id_token")
  headers = {"Authorization": f"Bearer {token}"}
  return requests.delete(url=f"{url}", params=query_params, headers=headers)


def create_user(user_data=None):
  """
  Function to add an user to the firestore collection
  """
  user_id, agent_id, learner_id = None, None, None
  # Create User Group
  group_dict = {**TEST_USER_GROUP, "name": "learner"}
  post_group = post_method(url=f"{API_URL_USER_MANAGEMENT}/user-group/immutable", \
                           request_body=group_dict)
  assert post_group.status_code in [200, 409]
  learner_group_id = None
  if post_group.status_code == 200:
    learner_group_id = post_group.json()["data"]["uuid"]
  if post_group.status_code == 409:
    post_group = UserGroup.find_by_name(group_dict["name"])
    post_group.is_immutable = True
    post_group.update()
    learner_group_id = post_group.id

  # Create User
  if user_data is None:
    user_data = deepcopy(
      {**TEST_USER, "email": f"{str(uuid.uuid4())}@gmail.com",
      "user_groups": [learner_group_id], "user_type": "learner"}
      )

  created_user = post_method(
    url=f"{API_URL_USER_MANAGEMENT}/user",
    request_body=user_data
  )
  assert created_user.status_code == 200, f"User Creation Failed {created_user.json()}"
  created_user = created_user.json()["data"]
  user_id = created_user["user_id"]

  #create verbs required for rules engine
  valid_verbs = VALID_VERBS + ["progressed", "not_attempted",
  "evaluation_pending"]
  for verb_name in valid_verbs:
    test_verb = Verb()
    test_verb_dict = deepcopy(TEST_VERB)
    test_verb_dict["name"] = verb_name
    test_verb = test_verb.from_dict(test_verb_dict)
    test_verb.uuid = ""
    test_verb.save()
    test_verb.uuid = test_verb.id
    test_verb.update()

  # find agent
  agent = Agent.find_by_user_id(user_id)
  if agent:
    agent_id = agent.id
  else:
    agent_id = ""

  # find learner
  if created_user.get("user_type", "").lower() == "learner":
    learner_id = created_user["user_type_ref"]

  return user_id, learner_id, agent_id


def setup_rules_engine_data(verb_data,
                            activity_data,
                            user_data=None):
  """
  Function to setup the data for Rules Engine testing
  Args:
    verb_data: Dict
    activity_data: Dict
    user_data: Dict
  Returns:
    Generated UUIDs that are stored in the DB
    user_id, learner_id, cp_id, agent_id, verb_id, activity_id
  """
  user_id, learner_id, agent_id = create_user(user_data)

  # Create verb
  try:
    created_verb = post_method(
      url=f"{API_URL_LEARNING_RECORD_SERVICE}/verb",
      request_body=verb_data)
    print(created_verb)
    print(created_verb.json())
    assert created_verb.status_code == 200, "Verb Creation Failed"
    created_verb = created_verb.json()
    verb_id = created_verb["data"]["uuid"]
  except AssertionError:
    created_verb = Verb.find_by_name(verb_data["name"])
    verb_id = created_verb.id

  # Create Activity
  created_activity = post_method(
    url=f"{API_URL_LEARNING_RECORD_SERVICE}/activity",
    request_body=activity_data)
  assert created_activity.status_code == 200, "Activity Creation Failed"
  created_activity = created_activity.json()
  activity_id = created_activity["data"]["uuid"]

  return user_id, learner_id, agent_id, verb_id, activity_id


def update_prereqs(uuid, collection_type, prereq):
  """Function to update the Prerequisites of a Learning Hierarchy Item"""
  node_item = collection_references[collection_type].find_by_id(uuid)
  node_item.prerequisites = prereq
  node_item.update()


def create_required_lrs_event(agent_id=None,
                              email=None,
                              user_id=None,
                              verb_id=None,
                              verb_name=None,
                              node_id=None,
                              node_name=None,
                              node_type=None,
                              session_id=None):
  """Function to create the required LRS event for E2E"""
  lrs_event = {}
  if verb_name == "started":
    lrs_event = deepcopy(TEST_LRS_STARTED_EVENT)
  elif verb_name == "completed":
    lrs_event = deepcopy(TEST_LRS_COMPLETED_EVENT)

  if agent_id is not None:
    lrs_event["actor"]["uuid"] = agent_id
  if email is not None:
    lrs_event["actor"]["mbox"] = f"mailto:{email}"
  if user_id is not None:
    lrs_event["actor"]["user_id"] = user_id
  if verb_id is not None:
    lrs_event["verb"]["uuid"] = verb_id
  if verb_name is not None:
    lrs_event["verb"]["name"] = verb_name
  if node_id is not None:
    lrs_event["object"]["uuid"] = node_id
    lrs_event["object"]["canonical_data"]["uuid"] = node_id
  if node_name is not None:
    lrs_event["object"]["canonical_data"]["name"] = node_name
  if node_type is not None:
    lrs_event["object"]["canonical_data"]["type"] = node_type
  if session_id is not None:
    lrs_event["session_id"] = session_id
  return lrs_event


def setup_verb_data(verb_data):
  # Create verb
  try:
    created_verb = post_method(
      url=f"{API_URL_LEARNING_RECORD_SERVICE}/verb",
      request_body=verb_data)
    assert created_verb.status_code == 200, "Verb Creation Failed"
    created_verb = created_verb.json()
    verb_id = created_verb["data"]["uuid"]
  except AssertionError as e:
    created_verb = Verb.find_by_name(verb_data["name"])
    verb_id = created_verb.id

    return verb_id
  
def create_immutable_user_groups(user_group_name):
  get_user_group = get_method(url=f"{API_URL_USER_MANAGEMENT}/user-group/search",query_params={"name": user_group_name})
  assert get_user_group.status_code == 200
  user_group_resp = get_user_group.json()["data"]
  user_group_id = user_group_resp[0]["uuid"] if user_group_resp else None
  if not user_group_id:    
    req_body = {
      "name": user_group_name,
      "description": f"immutable group for {user_group_name}'s"
    }
    immutable_group_res = post_method(f"{API_URL_USER_MANAGEMENT}/user-group/immutable",request_body=req_body)
    assert immutable_group_res.status_code == 200, "Immutable user group Failed"
    immutable_group = immutable_group_res.json()["data"]
    assert immutable_group.get("is_immutable") is True
    user_group_id = immutable_group.get("uuid")
  return user_group_id


def delete_test_files_from_gcs(files_to_delete):
  for file_path in files_to_delete:
    if is_valid_path(f"gs://{CONTENT_SERVING_BUCKET}/{file_path}"):
      delete_file_from_gcs(
        bucket_name=CONTENT_SERVING_BUCKET,
        src_path=file_path)
    else:
      print(f"file {file_path} was not found. Hence cannot be deleted")
