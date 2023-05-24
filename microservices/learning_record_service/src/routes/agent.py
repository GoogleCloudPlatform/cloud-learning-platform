""" Agent endpoints """
import traceback
import math
from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Query
from common.models import Agent, User
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                ConflictError, PayloadTooLargeError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict,
                                          PayloadTooLarge)
from schemas.agent_schema import (BasicAgentModel, AgentModel, UpdateAgentModel,
                                  GetAgentModelResponse, PostAgentModelResponse,
                                  UpdateAgentModelResponse,
                                  AllAgentModelResponse, DeleteAgent,
                                  AgentSearchModelResponse,
                                  AgentImportJsonResponse)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  PayloadTooLargeResponseModel)
from services.json_import import json_import
from config import PAYLOAD_FILE_SIZE, ERROR_RESPONSES

router = APIRouter(tags=["Agent"])
router = APIRouter(
    tags=["Agent"],
    responses=ERROR_RESPONSES)


@router.get("/agent/search", response_model=AgentSearchModelResponse)
def search_agent(name: Optional[str] = None):
  """Search for agent based on the name
  ### Args:
  name: `str`
    Name of the agent. Defaults to None.
  ### Raises:
  ValueError:
    Raised when input angles are outside range. <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong.
  ### Returns:
  List of Agents: \
  `AgentSearchModelResponse`
  """
  result = []
  if name:
    # fetch agent that matches name
    agents = Agent.find_by_name(name)
    result = [agent.get_fields(reformat_datetime=True) for agent in agents]
    return {
        "success": True,
        "message": "Successfully fetched the agents",
        "data": result
    }
  else:
    raise BadRequest("Missing or invalid request parameters")


@router.get("/agents", response_model=AllAgentModelResponse)
def get_agents(user_id: str = None,
              skip: int = Query(0, ge=0, le=2000),
              limit: int = Query(10, ge=1, le=100)
):
  """The get agents endpoint will return an array agents from firestore

  Args:
      user_id(str): User Id for which sessions need to fetched
      skip (int): Number of objects to be skipped
      limit (int): Size of agents array to be returned
  Raises:
      Exception: 500 Internal Server Error if something went wrong
  Returns:
      AllAgentModelResponse: Array of AgentModel Object
  """
  try:
    if user_id is not None:
      agents = Agent.collection.filter(
        "user_id", "==", user_id).filter("is_deleted", "==", False).fetch()
    else:
      collection_manager = Agent.collection.filter(
        "is_deleted", "==", False).order("-created_time")
      agents = collection_manager.offset(skip).fetch(limit)
    agents = [i.get_fields(reformat_datetime=True) for i in agents if i.name]
    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": agents
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/agent/{uuid}",
    response_model=GetAgentModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_agent(uuid: str):
  """The get agent endpoint will return the agent from
  firestore of which uuid is provided

  Args:
      uuid (str): Unique identifier for Agent

  Raises:
      ResourceNotFoundException: If the Agent does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      GetAgentModelResponse: Agent Object
  """
  try:
    agent = Agent.find_by_uuid(uuid)
    agent = agent.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully fetched the agent",
        "data": agent
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/agent",
    response_model=PostAgentModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_agent(input_agent: AgentModel):
  """The create agentendpoint will add the agent to
  the firestore if it does not exist.If the agent exist then it
  will update the agent
  ### Args:
  input_agent: `AgentModel`
    Input agent to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the agent does not exist <br/>
  Exception 500:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  UUID: `str`
    Unique identifier for agnet
  """
  try:
    input_agent_dict = {**input_agent.dict()}
    if not Agent.find_by_user_id(input_agent_dict["user_id"]):
      user = User.find_by_uuid(input_agent_dict["user_id"])
      if user is not None:

        new_agent = Agent()

        new_agent = new_agent.from_dict(input_agent_dict)
        new_agent.uuid = ""

        new_agent.save()
        new_agent.uuid = new_agent.id
        new_agent.update()
        new_agent_fields = new_agent.get_fields(reformat_datetime=True)
        return {
            "success": True,
            "message": "Successfully created the agent",
            "data": new_agent_fields
        }
      else:
        raise ResourceNotFoundException(
            f"User with user_id {input_agent_dict['user_id']} not found")
    else:
      agent_user_id = input_agent_dict["user_id"]
      raise ConflictError(
        f"Agent with the given user_id {agent_user_id} already exists")

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/agent/{uuid}",
    response_model=UpdateAgentModelResponse,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_agent(uuid: str, input_agent: UpdateAgentModel):
  """Update the Agent with the uuid passed in the request body

  Args:
      input_agent (UpdateAgentModel): Required body of the
      agent

  Raises:
      ResourceNotFoundException: If the agent does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      UpdateAgentModelResponse: Agent Object
  """
  try:
    input_agent_dict = {**input_agent.dict(exclude_unset=True)}
    # Updating the original doc
    updated_doc_fields = \
        CommonAPIHandler.update_document(Agent,
                                         uuid,
                                         input_agent_dict)

    return {
        "success": True,
        "message": "Successfully updated the agent",
        "data": updated_doc_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/agent/{uuid}",
    response_model=DeleteAgent,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_agent(uuid: str):
  """Delete the agent with the given uuid from firestore

  Args:
      uuid (str): Unique id of the agent

  Raises:
      ResourceNotFoundException: If the agent does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      JSON: Success/Fail Message
  """
  try:
    agent = Agent.find_by_uuid(uuid)
    Agent.delete_by_uuid(agent.uuid)
    return {"success": True, "message": "Successfully deleted the agent"}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/agent/import/json",
    response_model=AgentImportJsonResponse,
    name="Import Agent from JSON file",
    responses={413: {
        "model": PayloadTooLargeResponseModel
    }})
async def import_agents(json_file: UploadFile = File(...)):
  """Create agents from json file
  ### Args:
  json_file: `UploadFile`
    Upload json file consisting of agents.
  ### Raises:
  Exception 500:
    Internal Server Error. Raised if something fails
  ### Returns:
    Agent UUID: `AgentImportJsonResponse`
  """
  try:
    if len(await json_file.read()) > PAYLOAD_FILE_SIZE:
      raise PayloadTooLargeError(
        f"File size is too large: {json_file.filename}"
      )
    await json_file.seek(0)
    final_output = json_import(
        json_file=json_file,
        json_schema=BasicAgentModel,
        model_obj=Agent,
        object_name="agents")
    return final_output
  except PayloadTooLargeError as e:
    raise PayloadTooLarge(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/agent/add-is-deleted", include_in_schema=False)
def update_agent_documents():
  """This endpoint will add the is_deleted field in Agent documents where it
      doesn't exist.

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong
  """
  try:
    agents = list(Agent.collection.order("-created_time").fetch())

    # list of agent documents which are updated with the is_deleted field
    updated_agents = []

    # total count of all agent records
    agent_count = 0
    for i in enumerate(agents):
      agent_count+=1

    # calculate number of workers required (100 docs per worker)
    workers = math.ceil(agent_count / 100)

    # function to update the document
    def update_field(agent_list):
      for agent in agent_list:
        if agent.is_deleted is None:
          agent.is_deleted = False
          agent.update()
          Logger.info(f"Updated {agent.uuid}: is_deleted={agent.is_deleted}")
          updated_agents.append(agent.uuid)
        else:
          Logger.info(f"{agent.uuid}: is_deleted={agent.is_deleted}")

    # initialize executor
    executor = ThreadPoolExecutor(max_workers=workers)

    for i in range(workers):
      executor.submit(update_field, agents[i*100:(i+1)*100])

    executor.shutdown(wait=True)

    return {
      "success": True,
      "message": "Successfully added the is_deleted field for following agents",
      "data": {
        "updated_agents": updated_agents
      }
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
