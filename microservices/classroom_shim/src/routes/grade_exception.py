'''LTI Assignment Endpoints'''
from fastapi import APIRouter
from common.models import UserGradeException, User
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
    "/grade-exception-users",
    name="Get all grade exception user",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_all_exceptions(skip: int = 0, limit: int = 10):
  """The endpoint will return an array of grade-exception-users records from firestore
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    exception_records = UserGradeException.collection.order(
        "-created_time").offset(skip).fetch(limit)
    exception_records_list = []
    for i in exception_records:
      exception_data = i.get_fields(reformat_datetime=True)
      exception_data["id"] = i.id
      exception_records_list.append(exception_data)

    return {
        "success": True,
        "message": "Exception records have been fetched successfully",
        "data": exception_records_list
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/grade-exception-user/{doc_id}",
    name="Get a specific exception record",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_grade_exception(doc_id: str):
  """The get exception record endpoint will return the record
  from firestore of which doc_id is provided"""
  try:
    exception_record = UserGradeException.find_by_id(doc_id)
    exception_record_fields = exception_record.get_fields(
        reformat_datetime=True)
    exception_record_fields["id"] = exception_record.id
    return {
        "success":
            True,
        "message":
            f"Exception record with '{id}' has been fetched successfully",
        "data":
            exception_record_fields
    }
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/grade-exception-user",
    name="Add user to exception",
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def create_record(input_dict: GradeExceptionInputModel):
  """The grade_exception endpoint creates a new record in firestore if the
  email and tool id combination doesn't already exist.
  If it does, it updates the record for the allow selection field."""
  try:
    input_dict = {**input_dict.dict()}
    email_id = input_dict.get("email_id")
    tool_id = input_dict.get("tool_id")

    existing_data = UserGradeException.collection.filter(
        "email_id", "==", email_id).filter("tool_id", "==", tool_id).get()
    if existing_data:
      existing_data.allow_exception = input_dict.get("allow_exception")
      existing_data.update()
      user_fields = existing_data.get_fields(reformat_datetime=True)
      return {
          "success": True,
          "message": "User has been updated successfully",
          "data": {
              **user_fields
          }
      }
    else:
      user_details = User.find_by_email(email_id)
      if not user_details:
        raise Exception(f"User with email {email_id} not found")
      new_user = UserGradeException()
      new_user = new_user.from_dict(input_dict)
      new_user.user_id = user_details.get("user_id")
      new_user.save()
      user_fields = new_user.get_fields(reformat_datetime=True)
      user_fields["id"] = new_user.id
      return {
          "success": True,
          "message": "Exception record has been created successfully",
          "data": {
              **user_fields
          }
      }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
