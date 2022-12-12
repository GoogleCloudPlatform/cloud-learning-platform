"""
E2E Test Basic Configuration
"""
import json
import redis
import requests
from testing_objects.test_config import API_URL_AUTHENTICATION_SERVICE
from e2e.gke_api_tests.secrets_helper import get_user_email_and_password_for_e2e

USER_EMAIL, USER_PASSWORD = get_user_email_and_password_for_e2e()

# Redis Configuration for testing
red_con = redis.StrictRedis(host="localhost", port=6379, db=0)

# api_key = os.environ.get("FIREBASE_API_KEY")


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
  return json.loads(red_con.get(name=key))


def user_login() -> None:
  """
  Function to do firebase login
  """

  req_body = {"email": USER_EMAIL, "password": USER_PASSWORD}
  #   req = requests.post(
  #       f"{API_URL_AUTHENTICATION_SERVICE}/sign-up/credentials",
  # json=req_body)
  #   if req.status_code == 422 and req.json().get(
  #       "message") == "EMAIL_EXISTS":
  #     req = requests.post(
  #         f"{API_URL_AUTHENTICATION_SERVICE}/sign-in/credentials",
  # json=req_body)
  req = requests.post(f"{API_URL_AUTHENTICATION_SERVICE}/sign-in/credentials",
                      json=req_body,
                      timeout=60)
  res = req.json()
  if res is None or res["data"] is None:
    raise Exception("User sign-in failed")
  print(f"User with {USER_EMAIL} was logged in with "
        f"token {req.json()['data']['idToken']}")
  set_cache(key="id_token", value=req.json()["data"]["idToken"])


# def delete_user():
#   """
#   Function to delete firebase user
#   """
#   token = get_cache(key="id_token")
#   if token:
#     req_body = {"idToken": token}
#     requests.post(
#         f"https://identitytoolkit.googleapis.com/v1/accounts"
#         f":delete?key={api_key}", req_body)


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
  return requests.post(url=f"{url}",
                       json=request_body,
                       params=query_params,
                       data=data,
                       files=files,
                       headers=headers,
                       timeout=60)


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
  return requests.get(url=f"{url}",
                      params=query_params,
                      headers=headers,
                      allow_redirects=False,
                      timeout=60)


def patch_method(url: str,
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
  return requests.patch(url=f"{url}",
                        json=request_body,
                        params=query_params,
                        headers=headers,
                        timeout=60)


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
  return requests.delete(url=f"{url}",
                         params=query_params,
                         headers=headers,
                         timeout=60)
