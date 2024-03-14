'''LTI Assignment Endpoints'''
import traceback
import datetime
from fastapi import APIRouter
from common.models import UserGradeException
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest)
from schemas.grade_exception_schema import GradeExceptionInputModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
# pylint: disable=line-too-long

router = APIRouter(
    tags=["Users for lti grade passback exception"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        404: {
            "model": NotFoundErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


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
def create_tool(input_dict: GradeExceptionInputModel):
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
    input_dict = {**input_dict.dict()}
    email_id = input_dict.get("email_id")
    tool_id = input_dict.get("tool_id")

    existing_data = UserGradeException.find_by_email_and_tool_id(
        email_id, tool_id)
    if existing_data:
      existing_data.allow_exception = input_dict.get("allow_exception")
      existing_data.update()
      user_fields = existing_data.get_fields()
      return {
        "success": True,
        "message": "User has been updated successfully",
        "data": {
            **tool_fields
        }
    }
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
