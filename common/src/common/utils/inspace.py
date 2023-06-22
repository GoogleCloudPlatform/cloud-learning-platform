"""helper functions for Inspace operations"""
import os
import requests
import traceback

from google.cloud import secretmanager
from datetime import datetime, timedelta

from common.models.user import User
from common.utils.config import STAFF_USERS, EXTERNAL_USER_PROPERTY_PREFIX
from common.utils.logging_handler import Logger
from common.utils.jwt_token_generator import TokenGenerator

# pylint: disable = broad-exception-raised,broad-exception-caught

secrets = secretmanager.SecretManagerServiceClient()

GCP_PROJECT = os.environ.get("PROJECT_ID")
INSPACE_BASE_URL = os.getenv("INSPACE_BASE_URL", default=None)

if INSPACE_BASE_URL is not None:
  try:
    INSPACE_CLIENT_ID = secrets.access_secret_version(
      request={
        "name": "projects/" + GCP_PROJECT +
                "/secrets/inspace_client_id/versions/latest"
      }).payload.data.decode("utf-8")

    INSPACE_CLIENT_SECRET = secrets.access_secret_version(
      request={
        "name": "projects/" + GCP_PROJECT +
                "/secrets/inspace_client_secret/versions/latest"
      }).payload.data.decode("utf-8")

    INSPACE_AUTH_GROUP_ID = secrets.access_secret_version(
      request={
        "name": "projects/" + GCP_PROJECT +
                "/secrets/inspace_auth_group_id/versions/latest"
      }).payload.data.decode("utf-8")
  except Exception as e:
    Logger.info("Inspace API integration is not required for this Env")
else:
  Logger.info("Inspace API integration is not required for this Env")


def get_token_parameters() -> tuple:
  """Returns token parameters required for inspace JWT token"""
  jwt_payload = {
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(minutes=60),
  }

  jwt_headers = {
    "alg": "HS256",
    "authFlow": "ClientCredentials",
    "clientId": INSPACE_CLIENT_ID
  }

  return jwt_payload, jwt_headers, INSPACE_CLIENT_SECRET


def get_inspace_token(user_id):
  """Helper function for creating an Inspace token"""
  headers = get_inspace_headers()

  api_url = f"{INSPACE_BASE_URL}/auth/user/{user_id}/token" \
            f"/{int(INSPACE_AUTH_GROUP_ID)}"
  response = requests.get(api_url, headers=headers, timeout=30)

  return response


def get_inspace_headers():
  """
    Helper function to generate JWT token signed with
    inspace secrets
  """
  jwt_token = TokenGenerator.generate_jwt_token(*get_token_parameters())

  return {
    "Authorization": f"Bearer {jwt_token}",
    "Content-Type": "application/json"
  }


def create_inspace_user_helper(user) -> bool:
  """Helper function for creating an Inspace User"""
  if user.inspace_user.get("is_inspace_user"):

    headers = get_inspace_headers()

    if user.user_type in STAFF_USERS:
      inspace_user_type = "staffMember"
    else:
      inspace_user_type = "learner"

    user_payload = {
      "authGroupId": int(INSPACE_AUTH_GROUP_ID),
      "email": user.email,
      "firstName": user.first_name,
      "lastName": user.last_name,
      "userProperties": {
        f"{EXTERNAL_USER_PROPERTY_PREFIX}USER_ID": user.user_id,
        f"{EXTERNAL_USER_PROPERTY_PREFIX}USER_ROLE": inspace_user_type
      }
    }

    # api call for inspace user creation
    api_url = f"{INSPACE_BASE_URL}/auth/admin/user"
    response = requests.post(
      api_url, headers=headers, json=user_payload, timeout=30)

    inspace_user_res = response.json()

    if response.status_code == 200:
      user = User.find_by_user_id(user.user_id)

      inspace_user = {
        "is_inspace_user": True,
        "inspace_user_id": inspace_user_res["inspaceUser"]["id"],
      }

      user.inspace_user = inspace_user
      user.update()

      return True
    else:
      Logger.error(
        f"Error creating Inspace User: {user.user_id} :: {inspace_user_res}")
      Logger.error(traceback.print_exc())
      raise Exception("Error creating Inspace User:"
                      f"{user.user_id} :: {inspace_user_res.get('error')}")
  else:
    return False


def update_inspace_user_helper(user, new_user_payload):
  """
    Helper function for updating an Inspace User
    -------------------------------------------------
    Input:
      user: Firestore document of User model
      new_user_payload `dict`: a dict containing new data
            for the fields to be updated, empty otherwise
      eg: {
        "firstName": "some new data",
        "name": "",
        "lastName": "",
        "userProperties": {}
      }

      Notice that we have passed empty string and empty dict
      for the fields which do not require an update
  """

  headers = get_inspace_headers()

  status_code, inspace_user = get_inspace_user_helper(user)

  if status_code == 200:
    auth_group_id = int(INSPACE_AUTH_GROUP_ID)

    update_user_payload = {
      "userId": user.user_id,
      "firstName": new_user_payload.get("firstName", inspace_user[
        "inspaceUser"]["firstName"]),
      "name": new_user_payload.get("name", inspace_user["inspaceUser"]["name"]),
      "lastName": new_user_payload.get("lastName", inspace_user[
        "inspaceUser"]["lastName"]),
      "userProperties": new_user_payload.get("userProperties", {}),
      "authGroupId": auth_group_id
    }

    # api call for inspace user update
    api_url = f"{INSPACE_BASE_URL}/auth/admin/user"
    response = requests.patch(
      api_url, headers=headers, json=update_user_payload, timeout=30)

    inspace_user_res = response.json()

    if response.status_code == 200:
      return True
    else:
      Logger.error("Error updating Inspace User:"
                   f"{user.user_id} :: {inspace_user_res}")
      Logger.error(traceback.print_exc())
      Logger.error(inspace_user_res)
      raise Exception("Error updating Inspace User:"
                      f"{user.user_id} :: {inspace_user_res.get('error')}")
  else:
    return False


def get_inspace_user_helper(user):
  """
    Helper function to fetch Inspace User
    -------------------------------------------------
    Input:
      user: Firestore document of User model
  """
  headers = get_inspace_headers()

  # api call for getting inspace user
  api_url = f"{INSPACE_BASE_URL}/auth/admin/user/{user.user_id}" \
            f"/{int(INSPACE_AUTH_GROUP_ID)}"
  response = requests.get(
    api_url, headers=headers, timeout=30)

  if response.status_code in [200, 404]:
    return response.status_code, response.json()
  else:
    Logger.error("Error fetching Inspace User")
    Logger.error(traceback.print_exc())
    Logger.error(response.json())
    raise Exception("Error fetching Inspace User")


def delete_inspace_user_helper(user) -> bool:
  """
    Helper function for deleting an Inspace User
    -------------------------------------------------
    Input:
      user: Firestore document of User model
  """

  headers = get_inspace_headers()

  payload = {
    "userId": user.user_id,
    "authGroupId": int(INSPACE_AUTH_GROUP_ID)
  }

  # api call for inspace user deletion
  api_url = f"{INSPACE_BASE_URL}/auth/admin/user"
  response = requests.delete(
    api_url, headers=headers, json=payload, timeout=30)

  inspace_user_res = response.json()

  if response.status_code == 200:
    return True
  elif response.status_code == 404:
    return False
  else:
    Logger.error("Error deleting Inspace User"
                 f"{user.user_id} :: {inspace_user_res}")
    Logger.error(traceback.print_exc())
    Logger.error(inspace_user_res)
    raise Exception("Error deleting Inspace User:"
                    f"{user.user_id} :: {inspace_user_res.get('error')}")


def is_inspace_enabled(validate_param: bool = None) -> bool:
  """
  Function to validate the Inspace API Integration is required

  Parameters
  ----------
  validate_param: bool

  Returns
  -------
  bool
  """

  if validate_param is True and INSPACE_BASE_URL is None:
    return False
  elif validate_param is None and INSPACE_BASE_URL is None:
    return False
  return True
