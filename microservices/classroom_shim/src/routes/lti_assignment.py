'''LTI Assignment Endpoints'''
import traceback
from fastapi import APIRouter
from common.models import LTIAssignment
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          BadRequest)
from schemas.lti_assignment_schema import (
    LTIAssignmentListResponseModel, GetLTIAssignmentResponseModel,
    CreateLTIAssignmentResponseModel, InputLTIAssignmentModel,
    DeleteLTIAssignmentResponseModel, UpdateLTIAssignmentResponseModel,
    UpdateLTIAssignmentModel)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
# pylint: disable=line-too-long

router = APIRouter(
    tags=["LTI Assignments"],
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


@router.get("/lti-assignments", response_model=LTIAssignmentListResponseModel)
def get_lti_assignments_list(skip: int = 0, limit: int = 10):
  """Get a list of LTI Assignments endpoint
    Raises:
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        LTIAssignmentListModel: object which contains list of LTI Assignment object.
        InternalServerErrorResponseModel:
            if the get LTI Assignment list raises an exception.
    """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")
    lti_assignment_list = LTIAssignment.fetch_all(skip=skip, limit=limit)

    return {
        "success": True,
        "message": "Data fetched successfully",
        "data": lti_assignment_list
    }
  except ValidationError as e:
    Logger.error(e)
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/lti-assignment/{lti_assignment_id}",
    response_model=GetLTIAssignmentResponseModel)
def get_lti_assignment(lti_assignment_id: str):
  """Get a LTI Assignment endpoint

    Args:
        lti_assignment_id (str): unique id of the LTI Assignment

    Raises:
        ResourceNotFoundException: If the LTI Assignment does not exist.
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        LTIAssignmentModel: LTI Assignment object for the provided id
        NotFoundErrorResponseModel: if the LTI Assignment not found,
        InternalServerErrorResponseModel: if the get LTI Assignment raises an exception
    """
  try:

    lti_assignment = LTIAssignment.find_by_id(lti_assignment_id)
    lti_assignment_data = lti_assignment.to_dict()

    return {
        "success": True,
        "message": "Successfully fetched assignment",
        "data": lti_assignment_data
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/lti-assignment", response_model=CreateLTIAssignmentResponseModel)
def create_lti_assignment(input_lti_assignment: InputLTIAssignmentModel):
  """Create a LTI Assignment endpoint

    Args:
        input_lti_assignment (InputLTIAssignmentModel): input LTI Assignment to be inserted

    Raises:
        ResourceNotFoundException: If the Course Template does not exist.
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        CreateLTIAssignmentResponseModel: LTI Assignment Object,
        NotFoundErrorResponseModel: if the Course template not found,
        InternalServerErrorResponseModel:
            if the LTI Assignment creation raises an exception
  """
  try:

    lti_assignment_dict = {**input_lti_assignment.dict()}
    lti_assignment = LTIAssignment.from_dict(lti_assignment_dict)
    lti_assignment.save()
    lti_assignment_data = lti_assignment.to_dict()

    return {"data": lti_assignment_data}

  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.patch(
    "/lti-assignment/{lti_assignment_id}",
    response_model=UpdateLTIAssignmentResponseModel)
def update_lti_assignment(
    lti_assignment_id: str,
    update_lti_assignment_model: UpdateLTIAssignmentModel):
  """Update LTI Assignment API

    Args:
        update_lti_assignment_model (UpdateLTIAssignmentModel):
            Pydantic model object which contains update details
    Raises:
        InternalServerError: 500 Internal Server Error if something fails
        ResourceNotFoundException :
          404 if LTI Assignment not found
    Returns:
        UpdateLTIAssignment: Returns Updated LTI Assignment object
        InternalServerErrorResponseModel:
            If the LTI Assignment update raises an exception
    """
  try:
    lti_assignment_details = LTIAssignment.find_by_id(lti_assignment_id)
    update_lti_assignment_dict = {**update_lti_assignment_model.dict()}

    if not any(update_lti_assignment_dict.values()):
      raise ValidationError(
          "Invalid request please provide some data " +
          f"to update the LTI Assignment with id {lti_assignment_id}")

    for key in update_lti_assignment_dict:
      if update_lti_assignment_dict[key] is not None:
        setattr(lti_assignment_details, key, update_lti_assignment_dict[key])
    lti_assignment_details.update()
    lti_assignment_data = lti_assignment_details.to_dict()

    return {
        "message":
            f"Successfully updated the LTI Assignment with id {lti_assignment_id}",
        "data":
            lti_assignment_data
    }
  except ValidationError as e:
    Logger.error(e)
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/lti-assignment/{lti_assignment_id}",
    response_model=DeleteLTIAssignmentResponseModel)
def delete_lti_assignment(lti_assignment_id: str):
  """Delete a LTI Assignment endpoint
    Args:
        lti_assignment_id (str): unique id of the LTI Assignment

    Raises:
        ResourceNotFoundException: If the LTI Assignment does not exist
        HTTPException: 500 Internal Server Error if something fails

    Returns:
        DeleteLTIAssignmentResponseModel: if the LTI Assignment is deleted
        NotFoundErrorResponseModel: if the LTI Assignment not found
        InternalServerErrorResponseModel:
            if the LTI Assignment deletion raises an exception
    """
  try:
    LTIAssignment.soft_delete_by_id(lti_assignment_id)
    return {
        "message":
            f"Successfully deleted the LTI Assignment with id {lti_assignment_id}"
    }
  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
