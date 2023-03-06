"""Tool Registration Endpoints"""
from uuid import uuid4
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
      tool_data = tool.get_fields(reformat_datetime=True)
      tool_data["id"] = tool.id
      result = [tool_data]
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
def get_all_tools(skip: int = 0, limit: int = 10):
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

    collection_manager = Tool.collection.filter("deleted_at_timestamp", "==",
                                                None)

    tools = collection_manager.order("-created_time").offset(skip).fetch(limit)
    tools_list = []
    for i in tools:
      tool_data = i.get_fields(reformat_datetime=True)
      tool_data["id"] = i.id
      tools_list.append(tool_data)

    return {
        "success": True,
        "message": "Tools has been fetched successfully",
        "data": tools_list
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/tool/{tool_id}",
    name="Get a specific tool",
    response_model=ToolResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_tool(tool_id: str):
  """The get tool endpoint will return the tool
  from firestore of which tool_id is provided
  ### Args:
  tool_id: `str`
    Unique identifier for tool
  ### Raises:
  ResourceNotFoundException:
    If the tool with given tool_id does not exist. <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Tool: `ToolResponseModel`
  """
  try:
    tool = Tool.find_by_id(tool_id)
    tool_fields = tool.get_fields(reformat_datetime=True)
    tool_fields["id"] = tool.id
    return {
        "success": True,
        "message": f"Tool with '{tool_id}' has been fetched successfully",
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

    tool_url = input_tool_dict["tool_url"]
    existing_tool = Tool.find_by_tool_url(tool_url)
    if existing_tool:
      error_msg = f"Tool with the provided tool url {tool_url} already exists"
      raise ConflictError(error_msg)

    if not input_tool_dict.get("tool_public_key") and not input_tool_dict.get(
        "tool_keyset_url"):
      raise ValidationError("Public key is missing")

    input_tool_dict["client_id"] = client_id
    input_tool_dict["deployment_id"] = deployment_id
    new_tool = Tool()
    new_tool = new_tool.from_dict(input_tool_dict)
    new_tool.save()
    tool_fields = new_tool.get_fields(reformat_datetime=True)
    tool_fields["id"] = new_tool.id
    return {
        "success": True,
        "message": "Tool has been created successfully",
        "data": {
            **tool_fields
        }
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/tool/{tool_id}",
    response_model=ToolResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_tool(tool_id: str, input_tool: UpdateToolModel):
  """Update a tool
  ### Args:
  tool_id: `str`
    Unique identifier for tool
  input_tool: `UpdateToolModel`
    Required body of the tool
  ### Raises:
  ResourceNotFoundException:
    If the tool with given tool_id does not exist <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Updated Tool: `ToolResponseModel`
  """
  try:
    existing_tool = Tool.find_by_id(tool_id)
    tool_fields = existing_tool.get_fields()

    input_tool_dict = {**input_tool.dict()}

    if not input_tool_dict.get("tool_public_key") and not input_tool_dict.get(
        "tool_keyset_url"):
      return ValidationError("Public key is missing")

    for key, value in input_tool_dict.items():
      tool_fields[key] = value
    for key, value in tool_fields.items():
      setattr(existing_tool, key, value)
    existing_tool.update()
    tool_fields = existing_tool.get_fields(reformat_datetime=True)
    tool_fields["id"] = existing_tool.id
    return {
        "success": True,
        "message": "Successfully updated the tool",
        "data": tool_fields
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/tool/{tool_id}",
    response_model=DeleteTool,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_tool(tool_id: str):
  """Delete a tool with given tool_id from firestore
  ### Args:
  tool_id: `str`
    Unique ID of the tool
  ### Raises:
  ResourceNotFoundException:
    If the tool with given tool_id does not exist. <br/>
  Internal Server Error:
    Raised if something went wrong.
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    Tool.find_by_id(tool_id)
    Tool.delete_by_id(tool_id)
    return {}
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
