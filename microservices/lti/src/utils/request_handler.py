"""Requests Handler"""
import json
import requests
from common.utils.secrets import get_backend_robot_id_token


def post_method(url: str,
                request_body=None,
                query_params=None,
                data=None,
                files=None,
                use_bot_account=None,
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
  use_bot_account: bool
  token: token
  Returns
  -------
  JSON Object
  """

  if use_bot_account:
    token = get_backend_robot_id_token()

  if token:
    headers = {"Authorization": f"Bearer {token}"}
  else:
    headers = {}

  resp = requests.post(
      url=url,
      json=request_body,
      params=query_params,
      data=data,
      files=files,
      headers=headers,
      timeout=60)

  if resp.status_code == 200:
    resp_data = resp.json().get("data")
  else:
    raise Exception("Internal error from the API")

  return resp_data


def get_method(url: str,
               query_params=None,
               use_bot_account=None,
               token=None) -> json:
  """
  Function for API test GET method
  Parameters
  ----------
  url: str
  query_params: dict
  use_bot_account: bool
  token: token
  Returns
  -------
  JSON Object
  """

  if use_bot_account:
    token = get_backend_robot_id_token()

  if token:
    headers = {"Authorization": f"Bearer {token}"}
  else:
    headers = {}

  return requests.get(
      url=f"{url}", params=query_params, headers=headers, timeout=60)
