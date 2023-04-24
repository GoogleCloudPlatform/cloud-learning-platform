"""Requests Handler"""
import json
import requests
from config import auth_client


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
    token = auth_client.get_id_token()

  if token:
    headers = {"Authorization": f"Bearer {token}"}
  else:
    headers = {}

  return requests.get(
      url=f"{url}", params=query_params, headers=headers, timeout=60)
