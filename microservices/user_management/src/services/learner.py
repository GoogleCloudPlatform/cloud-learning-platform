"""service file to create learner and learner profile"""
#pylint: disable=broad-exception-raised,redefined-builtin,unused-argument
from common.utils.rest_method import post_method, delete_method, put_method
from config import SLP_BASE_URL
#pylint: disable=broad-exception-raised


# pylint: disable = broad-exception-raised

def create_learner(headers: dict = None,
                   learner_dict: dict = None):
  """Post request to student learner profile service to create learner"""
  api_url = f"{SLP_BASE_URL}/learner"
  response = post_method(url=api_url,
                         request_body=learner_dict,
                         token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to create learner")
  learner_id = response.json().get("data").get("uuid")
  return learner_id


def create_learner_profile(headers: dict = None,
                           learner_id: str = None,
                           learner_profile_dict: dict = None):
  """Post request to student learner profile service to create learner
  profile"""
  api_url = f"{SLP_BASE_URL}/learner/{learner_id}/learner-profile"
  if learner_profile_dict is None:
    learner_profile_dict = {}
  response = post_method(url=api_url,
                         request_body=learner_profile_dict,
                         token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to create learner profile")


def delete_learner(headers: dict = None,
                   learner_id: str = None):
  """Delete request to student learner profile service to delete learner"""
  api_url = f"{SLP_BASE_URL}/learner/{learner_id}"
  response = delete_method(url=api_url,
                         token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to delete learner")


def delete_learner_profile(headers: dict = None,
                           learner_id: str = None):
  """Delete request to student learner profile service to delete learner
  profile"""
  api_url = f"{SLP_BASE_URL}/learner/{learner_id}/learner-profile"
  response = delete_method(url=api_url,
                         token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to delete learner profile")


def update_learner(headers: dict = None,
                   learner_id: str = None,
                   learner_dict: dict = None):
  """PUT request to student-learner-profile service to update learner"""
  api_url = f"{SLP_BASE_URL}/learner/{learner_id}"
  response = put_method(url=api_url,
                        request_body=learner_dict,
                        token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to update learner")
