"""Tool Registration Endpoints"""
from uuid import uuid4
from typing import Optional
from fastapi import APIRouter
from config import ERROR_RESPONSES
from common.models import Tool
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError)
from common.utils.http_exceptions import (InternalServerError, BadRequest,
                                          ResourceNotFound, Conflict)
from schemas.tool_schema import (ToolModel, ToolResponseModel, UpdateToolModel,
                                 DeleteTool, ToolSearchResponseModel,
                                 AllToolsResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel

router = APIRouter(
    tags=["Tool Registration Endpoints"], responses=ERROR_RESPONSES)


@router.get("/tool/search", response_model=ToolSearchResponseModel)
def search_tool(client_id: str):
  """Search for Tool based on the client_id
  ### Args:
  client_id: `str`
    client_id of the Tool.
  ### Raises:
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  List of Tool: `ToolSearchResponseModel`
  """
  result = []
  try:
    # fetch tool that matches client_id
    tool = Tool.find_by_client_id(client_id)
    if tool:
      result = [tool.get_fields(reformat_datetime=True)]
    return {
        "success": True,
        "message": "Successfully fetched the tools",
        "data": result
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/tools",
    name="Get all tools",
    response_model=AllToolsResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_tools(skip: int = 0,
                  limit: int = 10,
                  fetch_archive: Optional[bool] = None):
  """The get tools endpoint will return an array of tools from firestore
  ### Args:
  skip: `int`
    Number of tools to be skipped <br/>
  limit: `int`
    Size of tools array to be returned <br/>
  ### Raises:
  ValueError:
    Raised when input args are outside range. <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Array of Tools: `AllToolsResponseModel`
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    collection_manager = Tool.collection.filter("is_deleted", "==", False)
    if fetch_archive is not None:
      collection_manager = collection_manager\
                            .filter("is_archived", "==", fetch_archive)

    tools = collection_manager.order("-created_time").offset(skip).fetch(limit)
    tools = [i.get_fields(reformat_datetime=True) for i in tools]

    return {
        "success": True,
        "message": "Tools has been fetched successfully",
        "data": tools
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/tool/{uuid}",
    name="Get a specific tool",
    response_model=ToolResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_tool(uuid: str):
  """The get tool endpoint will return the tool
  from firestore of which uuid is provided
  ### Args:
  uuid: `str`
    Unique identifier for tool
  ### Raises:
  ResourceNotFoundException:
    If the tool with given uuid does not exist. <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Tool: `ToolResponseModel`
  """
  try:
    tool = Tool.find_by_uuid(uuid)
    tool_fields = tool.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": f"Tool with '{uuid}' has been fetched successfully",
        "data": tool_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/tool",
    name="Register a Tool",
    response_model=ToolResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_tool(input_tool: ToolModel):
  """The create tool endpoint will add the tool to the firestore if it does not
  exist.If the tool exist then it will update the tool
  ### Args:
  input_tool: `ToolModel`
    Input tool to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the tool with given uuid does not exist <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Tool Data: `ToolResponseModel`
  """
  try:
    input_tool_dict = {**input_tool.dict()}

    client_id = str(uuid4())
    deployment_id = str(uuid4())

    existing_tool = Tool.find_by_tool_url(input_tool_dict["tool_url"])
    if existing_tool:
      raise ConflictError(
          "Tool with the provided tool url {} already exists".format(
              input_tool_dict["tool_url"]))

    if not input_tool_dict.get("tool_public_key") and not input_tool_dict.get(
        "tool_keyset_url"):
      return {"success": False, "message": "Public key is missing", "data": []}

    input_tool_dict["client_id"] = client_id
    input_tool_dict["deployment_id"] = deployment_id
    new_tool = Tool()
    new_tool = new_tool.from_dict(input_tool_dict)
    new_tool.uuid = ""
    new_tool.save()
    new_tool.uuid = new_tool.id
    new_tool.update()
    tool_fields = new_tool.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Tool has been created successfully",
        "data": {
            **tool_fields
        }
    }
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/tool/{uuid}",
    response_model=ToolResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_tool(uuid: str, input_tool: UpdateToolModel):
  """Update a tool
  ### Args:
  uuid: `str`
    Unique identifier for tool
  input_tool: `UpdateToolModel`
    Required body of the tool
  ### Raises:
  ResourceNotFoundException:
    If the tool with given uuid does not exist <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Updated Tool: `ToolResponseModel`
  """
  try:
    existing_tool = Tool.find_by_uuid(uuid)
    tool_fields = existing_tool.get_fields()

    input_tool_dict = {**input_tool.dict()}

    if not input_tool_dict.get("tool_public_key") and not input_tool_dict.get(
        "tool_keyset_url"):
      return {"success": False, "message": "Public key is missing", "data": []}

    for key, value in input_tool_dict.items():
      tool_fields[key] = value
    for key, value in tool_fields.items():
      setattr(existing_tool, key, value)
    existing_tool.update()
    tool_fields = existing_tool.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully updated the tool",
        "data": tool_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/tool/{uuid}",
    response_model=DeleteTool,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_tool(uuid: str):
  """Delete a tool with given uuid from firestore
  ### Args:
  uuid: `str`
    Unique ID of the tool
  ### Raises:
  ResourceNotFoundException:
    If the tool with given uuid does not exist. <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    Tool.delete_by_uuid(uuid)
    return {}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
