"""Line item  Endpoints"""
import traceback
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from config import ERROR_RESPONSES, LTI_ISSUER_DOMAIN
from common.models import LineItem, Result, Score, Tool, LTIContentItem
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 InvalidTokenError)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (InternalServerError, ResourceNotFound,
                                          Unauthenticated)
from schemas.line_item_schema import (LineItemModel, LineItemResponseModel,
                                      UpdateLineItemModel,
                                      UpdateLineItemUsingIdModel,
                                      DeleteLineItem, FullLineItemModel,
                                      BasicScoreModel, ResultResponseModel)
from schemas.error_schema import NotFoundErrorResponseModel
from services.line_item_service import (create_new_line_item,
                                        get_line_item_results,
                                        get_result_of_line_item)
from services.grade_service import grade_pass_back
from typing import List, Optional
from services.validate_service import validate_access, get_tool_info_using_token
# pylint: disable=unused-argument, use-maxsplit-arg, line-too-long

auth_scheme = HTTPBearer(auto_error=False)

router = APIRouter(tags=["Line item"], responses=ERROR_RESPONSES)


# TODO: Update the scope validation decorator using FastAPI dependencies
@router.get(
    "/{context_id}/line_items",
    name="Get all line items",
    response_model=List[FullLineItemModel],
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(allowed_scopes=[
    "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
    "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly"
])
def get_all_line_items(context_id: str,
                       resource_id: str = None,
                       resource_link_id: str = None,
                       tag: str = None,
                       skip: int = 0,
                       limit: int = 1000,
                       token: auth_scheme = Depends()):
  """The get line items endpoint will return an array of line items
  from firestore
  ### Args:
  skip: `int`
    Number of line items to be skipped <br/>
  limit: `int`
    Size of line items array to be returned <br/>
  resource_id: `str`
    Tool resource ID in a line item <br/>
  resource_link_id: `str`
    Platform's resource link ID in a line item <br/>
  tag: `str`
    Tag associated with the line item <br/>
  ### Raises:
  ValueError:
    Raised when input args are outside range. <br/>
  Exception:
    Internal Server Error Raised. Raised if something went wrong
  ### Returns:
  Array of line items: `FullLineItemModel`
  """
  try:

    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    collection_manager = LineItem.collection.filter("contextId", "==",
                                                    context_id)

    if resource_id:
      collection_manager = collection_manager.filter("resourceId", "==",
                                                     resource_id)
    if resource_link_id:
      collection_manager = collection_manager.filter("resourceLinkId", "==",
                                                     resource_link_id)
    if tag:
      collection_manager = collection_manager.filter("tag", "==", tag)

    line_items = collection_manager.order("-created_time").offset(skip).fetch(
        limit)

    line_items_list = []
    for i in line_items:
      line_item = i.get_fields(reformat_datetime=True)
      line_item[
          "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{i.id}"
      line_items_list.append(line_item)
    return line_items_list

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/{context_id}/line_items/{line_item_id}",
    name="Get a specific line item",
    response_model=LineItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(allowed_scopes=[
    "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem",
    "https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly"
])
def get_line_item(context_id: str,
                  line_item_id: str,
                  token: auth_scheme = Depends()):
  """The get line item endpoint will return the line item
  from firestore of which line_item_id is provided
  ### Args:
  line_item_id: `str`
    Unique identifier for line item
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  LineItem: `LineItemResponseModel`
  """
  try:
    line_item = LineItem.find_by_id(line_item_id)

    if line_item.contextId != context_id:
      raise ResourceNotFoundException(
          f"Line item with id {line_item_id} in {context_id} not found")

    line_item_fields = line_item.get_fields(reformat_datetime=True)
    line_item_fields[
        "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item.id}"

    return line_item_fields
  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/{context_id}/line_items",
    name="Add a Line item",
    response_model=LineItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(
    allowed_scopes=["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"])
def create_line_item(context_id: str,
                     input_line_item: LineItemModel,
                     token: auth_scheme = Depends(),
                     tool_details: dict = Depends(get_tool_info_using_token)):
  """The create line item endpoint will add a new line item to the firestore.
  ### Args:
  input_line_item: `LineItemModel`
    Input line item to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Line item Data: `LineItemResponseModel`
  """
  try:
    input_line_item_dict = {**input_line_item.dict()}
    input_line_item_dict["contextId"] = context_id

    lti_content_item = LTIContentItem.collection.filter(
        "context_id", "==", context_id).filter("tool_id", "==",
                                               tool_details.id).get()

    if not lti_content_item:
      raise Exception("No content item object found")

    lti_content_item_id = lti_content_item.id

    # This condition holds true when the line item is not created using content item return
    if not input_line_item_dict.get("resourceLinkId"):
      input_line_item_dict["resourceLinkId"] = lti_content_item_id

    line_item = create_new_line_item(input_line_item_dict)
    line_item_fields = line_item.get_fields(reformat_datetime=True)
    line_item_fields[
        "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item.id}"

    return line_item_fields
  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/{context_id}/line_items/{line_item_id}",
    response_model=LineItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(
    allowed_scopes=["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"])
def update_line_item(context_id: str,
                     line_item_id: str,
                     input_line_item: UpdateLineItemModel,
                     token: auth_scheme = Depends()):
  """Update a line item
  ### Args:
  line_item_id: `str`
    Unique identifier for line item
  input_line_item: `UpdateLineItemModel`
    Required body of the line item
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Updated line item: `LineItemResponseModel`
  """
  try:
    existing_line_item = LineItem.find_by_id(line_item_id)

    if existing_line_item.contextId != context_id:
      raise ResourceNotFoundException(
          f"Line item with id {line_item_id} in {context_id} not found")

    line_item_fields = existing_line_item.get_fields()

    input_line_item_dict = {**input_line_item.dict()}

    for key, value in input_line_item_dict.items():
      line_item_fields[key] = value
    for key, value in line_item_fields.items():
      setattr(existing_line_item, key, value)
    existing_line_item.update()
    line_item_fields = existing_line_item.get_fields(reformat_datetime=True)
    line_item_fields[
        "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}"

    return line_item_fields

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/{context_id}/line_items",
    response_model=LineItemResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(
    allowed_scopes=["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"])
def update_line_item_using_id(context_id: str,
                              input_line_item: UpdateLineItemUsingIdModel,
                              token: auth_scheme = Depends()):
  """Update a line item using the id in the request body
  ### Args:
  uuid: `str`
    Unique identifier for line item
  input_line_item: `UpdateLineItemUsingIdModel`
    Required body of the line item
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Updated line item: `LineItemResponseModel`
  """
  try:
    input_line_item_dict = {**input_line_item.dict(exclude_unset=True)}
    line_item_id = input_line_item_dict.get("id")
    line_item_id = line_item_id.split("/")[-1]

    existing_line_item = LineItem.find_by_id(line_item_id)

    if existing_line_item.contextId != context_id:
      raise ResourceNotFoundException(
          f"Line item with id {line_item_id} in {context_id} not found")

    line_item_fields = existing_line_item.get_fields()

    for key, value in input_line_item_dict.items():
      line_item_fields[key] = value
    for key, value in line_item_fields.items():
      setattr(existing_line_item, key, value)
    existing_line_item.update()
    line_item_fields = existing_line_item.get_fields(reformat_datetime=True)
    line_item_fields[
        "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}"

    return line_item_fields

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/{context_id}/line_items/{line_item_id}",
    response_model=DeleteLineItem,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(
    allowed_scopes=["https://purl.imsglobal.org/spec/lti-ags/scope/lineitem"])
def delete_line_item(context_id: str,
                     line_item_id: str,
                     token: auth_scheme = Depends()):
  """Delete a line item from firestore
  ### Args:
  line_item_id: `str`
    Unique ID of the line item
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Success/Fail Message: `JSON`
  """
  try:
    line_item = LineItem.find_by_id(line_item_id)

    if line_item.contextId != context_id:
      raise ResourceNotFoundException(
          f"Line item with id {line_item_id} in {context_id} not found")

    LineItem.delete_by_id(line_item_id)
    return {}

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/{context_id}/line_items/{line_item_id}/results",
    name="Get all the results of a specific line item",
    response_model=List[ResultResponseModel],
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(allowed_scopes=[
    "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly"
])
def get_results_of_line_item(context_id: str,
                             line_item_id: str,
                             skip: int = 0,
                             limit: int = 10,
                             user_id: Optional[str] = None,
                             token: auth_scheme = Depends()):
  """The get all results of a line item endpoint will return all the
  results of a line item from firestore
  ### Args:
  line_item_id: `str`
    Unique identifier for line item
  skip: `int`
    Number of results to be skipped <br/>
  limit: `int`
    Size of results array to be returned <br/>
  user_id: `str`
    Unique identifier of the user <br/>
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Result: `ResultResponseModel`
  """
  try:
    line_item = LineItem.find_by_id(line_item_id)

    if line_item.contextId != context_id:
      raise ResourceNotFoundException(
          f"Line item with id {line_item_id} in {context_id} not found")

    result_fields = get_line_item_results(
        context_id=context_id,
        line_item_id=line_item_id,
        user_id=user_id,
        skip=skip,
        limit=limit)

    return result_fields

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/{context_id}/line_items/{line_item_id}/results/{result_id}",
    name="Get the specific result of a line item",
    response_model=ResultResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(allowed_scopes=[
    "https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly"
])
def get_result(context_id: str,
               line_item_id: str,
               result_id: str,
               token: auth_scheme = Depends()):
  """The get result of a line item endpoint will return the specific result
  of a line item from firestore
  ### Args:
  line_item_id: `str`
    Unique identifier for line item
  result_id: `str`
    Unique identifier for result
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist. <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Result: `ResultResponseModel`
  """
  try:
    result_fields = get_result_of_line_item(
        context_id=context_id, line_item_id=line_item_id, result_id=result_id)

    return result_fields

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/{context_id}/line_items/{line_item_id}/scores",
    name="Add a score for a Line item",
    response_model=ResultResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
@validate_access(
    allowed_scopes=["https://purl.imsglobal.org/spec/lti-ags/scope/score"])
def create_score_for_line_item(context_id: str,
                               line_item_id: str,
                               input_score: BasicScoreModel,
                               token: auth_scheme = Depends()):
  """The create score for line item endpoint will add a score for a line item
  to the firestore.
  ### Args:
  input_score: `BasicScoreModel`
    Input line item to be inserted
  ### Raises:
  ResourceNotFoundException:
    If the line item does not exist <br/>
  Exception:
    Internal Server Error. Raised if something went wrong
  ### Returns:
  Result Data: `ResultResponseModel`
  """
  try:
    line_item = LineItem.find_by_id(line_item_id)

    if line_item.contextId != context_id:
      raise ResourceNotFoundException(
          f"Line item with id {line_item_id} in {context_id} not found")

    input_score_dict = {**input_score.dict()}

    if input_score_dict.get("scoreGiven") is not None:
      if input_score_dict.get("scoreMaximum") is not None:
        if input_score_dict["scoreGiven"] > input_score_dict["scoreMaximum"]:
          raise ValidationError(
              "Score maximum should not be greater than the given score")
        else:
          raise ValidationError("Score maximum should not be a null value")

    input_score_dict["lineItemId"] = line_item_id

    new_score = Score()
    new_score = new_score.from_dict(input_score_dict)
    new_score.save()
    line_item_url = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}"

    input_result_dict = {
        "userId": input_score_dict["userId"],
        "resultScore": input_score_dict["scoreGiven"],
        "resultMaximum": input_score_dict["scoreMaximum"],
        "comment": input_score_dict["comment"],
        "scoreOf": line_item_id,
        "lineItemId": line_item_id,
        "isGradeSyncCompleted": False
    }

    user_id = input_result_dict["userId"]
    result = Result.collection.filter("scoreOf", "==", line_item_id).filter(
        "userId", "==", input_score_dict["userId"]).get()

    if result:
      result_fields = result.get_fields()

      for key, value in input_result_dict.items():
        result_fields[key] = value
      for key, value in result_fields.items():
        setattr(result, key, value)
      result.update()
      result_fields = result.get_fields(reformat_datetime=True)
      result_fields["scoreOf"] = line_item_url
      result_fields[
          "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}/results/{result.id}"
    else:
      new_result = Result()
      new_result = new_result.from_dict(input_result_dict)
      new_result.save()
      result_fields = new_result.get_fields(reformat_datetime=True)
      result_fields["scoreOf"] = line_item_url
      result_fields[
          "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}/results/{new_result.id}"

    # Passing grades back to the LMS using shim service API
    if line_item.resourceLinkId:
      lti_content_item = LTIContentItem.find_by_id(line_item.resourceLinkId)
      tool = Tool.find_by_id(lti_content_item.tool_id)

      input_grade_dict = {
          "user_id": user_id,
          "comment": input_result_dict["comment"],
          "lti_content_item_id": line_item.resourceLinkId,
          "maximum_grade": input_result_dict["resultMaximum"],
          "assigned_grade": None,
          "draft_grade": None,
          "validate_title": tool.validate_title_for_grade_sync,
          "line_item_title": line_item.label
      }

      if input_score_dict["gradingProgress"] in ["Pending", "PendingManual"]:
        input_grade_dict["draft_grade"] = input_result_dict["resultScore"]

      if input_score_dict["gradingProgress"] == "FullyGraded":
        input_grade_dict["assigned_grade"] = input_result_dict["resultScore"]

      gpb_resp = grade_pass_back(input_grade_dict, user_id, line_item_id)
      if gpb_resp:
        result = Result.collection.filter("scoreOf", "==", line_item_id).filter(
            "userId", "==", input_score_dict["userId"]).get()
        result.isGradeSyncCompleted = True
        result.update()

    else:
      Logger.error(
          f"Content item id not found for given line item {line_item_id} to trigger grade passback"
      )

    return result_fields

  except InvalidTokenError as e:
    Logger.error(e)
    raise Unauthenticated(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
