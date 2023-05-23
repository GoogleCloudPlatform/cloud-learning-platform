"""service file to create agent"""
#pylint: disable=broad-exception-raised,redefined-builtin,unused-argument
from common.models import Agent, User
from common.utils.common_api_handler import CommonAPIHandler
# from common.utils.rest_method import (post_method, delete_method, put_method,
#                           get_method)
#from config import LRS_BASE_URL

# pylint: disable = broad-exception-raised
def create_agent(headers: dict = None,
                 agent_dict: dict = None):
  """Post request to learner record service to create agent"""
  # TODO: Enable API call to LRS service after LRS is moved to CLP
  # api_url = f"{LRS_BASE_URL}/agent"
  # response = post_method(url=api_url,
  #                        request_body=agent_dict,
  #                        token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to create agent")
  if not Agent.find_by_uuid(agent_dict["user_id"]):
    user = User.find_by_user_id(agent_dict["user_id"])
    if user is not None:
      new_agent = Agent()
      new_agent = new_agent.from_dict(agent_dict)
      new_agent.uuid = ""
      new_agent.save()
      new_agent.uuid = new_agent.id
      new_agent.update()


def delete_agent(headers: dict = None,
                 agent_id: str = None):
  """Delete request to learner record service to delete agent"""
  # TODO: Enable API call to LRS service after LRS is moved to CLP
  # api_url = f"{LRS_BASE_URL}/agent/{agent_id}"
  # response = delete_method(url=api_url,
  #                        token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to delete agent")
  agent = Agent.find_by_uuid(agent_id)
  Agent.delete_by_uuid(agent.uuid)


def get_agent(headers: dict = None,
              user_id: str = None):
  """Get agent for the given user"""
  # TODO: Enable API call to LRS service after LRS is moved to CLP
  # api_url = f"{LRS_BASE_URL}/agents"
  # params = {"user_id": user_id}
  # response = get_method(url=api_url,
  #                       query_params=params,
  #                       token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to fetch agent for the given user")
  # agent_id = response.json().get("data")[0].get("uuid")
  # return agent_id
  agents = Agent.collection.filter(
      "user_id", "==", user_id).filter("is_deleted", "==", False).fetch()
  agents = [i.get_fields(reformat_datetime=True) for i in agents if i.name]
  agent_id = agents[0].uuid
  return agent_id


def update_agent(headers: dict = None,
                 agent_id: str = None,
                 agent_dict: dict = None):
  """PUT request to learner record service to update agent"""
  # TODO: Enable API call to LRS service after LRS is moved to CLP
  # api_url = f"{LRS_BASE_URL}/agent/{agent_id}"
  # response = put_method(url=api_url,
  #                       request_body=agent_dict,
  #                       token=headers.get("Authorization"))
  # if response.status_code != 200:
  #   raise Exception("Failed to update agent")
  # Updating the original doc
  _ = CommonAPIHandler.update_document(Agent,
                                       agent_id,
                                       agent_dict)
