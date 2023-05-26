"""service file to create agent"""
#pylint: disable=broad-exception-raised,redefined-builtin,unused-argument
from common.utils.rest_method import (post_method, delete_method, put_method,
                           get_method)
from config import LRS_BASE_URL

# pylint: disable = broad-exception-raised
def create_agent(headers: dict = None,
                 agent_dict: dict = None):
  """Post request to learner record service to create agent"""
  api_url = f"{LRS_BASE_URL}/agent"
  response = post_method(url=api_url,
                         request_body=agent_dict,
                         token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to create agent")


def delete_agent(headers: dict = None,
                 agent_id: str = None):
  """Delete request to learner record service to delete agent"""
  api_url = f"{LRS_BASE_URL}/agent/{agent_id}"
  response = delete_method(url=api_url,
                         token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to delete agent")


def get_agent(headers: dict = None,
              user_id: str = None):
  """Get agent for the given user"""
  api_url = f"{LRS_BASE_URL}/agents"
  params = {"user_id": user_id}
  response = get_method(url=api_url,
                        query_params=params,
                        token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to fetch agent for the given user")
  agent_id = response.json().get("data")[0].get("uuid")
  return agent_id


def update_agent(headers: dict = None,
                 agent_id: str = None,
                 agent_dict: dict = None):
  """PUT request to learner record service to update agent"""
  api_url = f"{LRS_BASE_URL}/agent/{agent_id}"
  response = put_method(url=api_url,
                        request_body=agent_dict,
                        token=headers.get("Authorization"))
  if response.status_code != 200:
    raise Exception("Failed to update agent")
