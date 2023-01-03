'''Cohort Endpoint'''
import traceback
from fastapi import APIRouter
from common.models import Cohort, CourseTemplate
from common.models.section import Section
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import ResourceNotFound, InternalServerError, BadRequest
from schemas.cohort import (CohortListResponseModel, CohortModel,
                            CreateCohortResponseModel, InputCohortModel,
                            DeleteCohortResponseModel,
                            UpdateCohortResponseModel, UpdateCohortModel)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
from schemas.section import  SectionListResponseModel                                 
from utils.helper import (convert_cohort_to_cohort_model,convert_section_to_section_model)

router = APIRouter(prefix="/cohorts",
                   tags=["Cohort"],
                   responses={
                       500: {
                           "model": InternalServerErrorResponseModel
                       },
                       404: {
                           "model": NotFoundErrorResponseModel
                       },
                       409: {
                           "model": ConflictResponseModel
                       },
                       422: {
                           "model": ValidationErrorResponseModel
                       }
                   })


@router.get("", response_model=CohortListResponseModel)
def get_cohort_list():
  """Get a list of Cohort endpoint
    Raises:
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        CohortListModel: object which contains list of Cohort object.
        InternalServerErrorResponseModel:
            if the get cohort list raises an exception.
    """
  try:
    fetched_cohort_list = Cohort.fetch_all()
    if fetched_cohort_list is None:
      return {
          "message":
          "Successfully get the cohort list, but the list is empty.",
          "cohort_list": []
      }
    cohort_list = [
        convert_cohort_to_cohort_model(i) for i in fetched_cohort_list
    ]
    return {"cohort_list": cohort_list}
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    print(e.message)
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{cohort_id}", response_model=CohortModel)
def get_cohort(cohort_id: str):
  """Get a Cohort endpoint

    Args:
        cohort_id (str): unique id of the cohort

    Raises:
        ResourceNotFoundException: If the Cohort does not exist.
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        CohortModel: Cohort object for the provided id
        NotFoundErrorResponseModel: if the Cohort not found,
        InternalServerErrorResponseModel: if the get Cohort raises an exception
    """
  try:
    cohort = Cohort.find_by_id(cohort_id)
    loaded_cohort = convert_cohort_to_cohort_model(cohort)
    return loaded_cohort
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post("", response_model=CreateCohortResponseModel)
def create_cohort(input_cohort: InputCohortModel):
  """Create a Cohort endpoint

    Args:
        input_cohort (InputCohortModel): input Cohort to be inserted

    Raises:
        ResourceNotFoundException: If the Course Template does not exist.
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        CreateCohortResponseModel: Cohort Object,
        NotFoundErrorResponseModel: if the Course template not found,
        InternalServerErrorResponseModel:
            if the Cohort creation raises an exception
  """
  try:
    cohort_dict = {**input_cohort.dict()}
    course_template = CourseTemplate.find_by_id(
        cohort_dict["course_template_id"])
    cohort_dict.pop("course_template_id")
    cohort = Cohort.from_dict(cohort_dict)
    cohort.course_template = course_template
    cohort.save()
    return {"cohort": convert_cohort_to_cohort_model(cohort)}
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.patch("/{cohort_id}", response_model=UpdateCohortResponseModel)
def update_cohort(cohort_id: str, update_cohort_model: UpdateCohortModel):
  """Update Cohort API

    Args:
        update_cohort_model (UpdateCohortModel):
            pydantic model object which contains update details
    Raises:
        InternalServerError: 500 Internal Server Error if something fails
        ResourceNotFoundException :
          404 if cohort or course template id not found
    Returns:
        UpdateCohort: Returns Updated Cohort object,
        InternalServerErrorResponseModel:
            if the Cohort updation raises an exception
    """
  try:
    cohort_details = Cohort.find_by_id(cohort_id)
    update_cohort_dict = {**update_cohort_model.dict()}
    if not any(update_cohort_dict.values()):
      raise ValidationError("Invalid request please provide some data " +
                            f"to update the Cohort with id {cohort_id}")
    for key in update_cohort_dict:
      if update_cohort_dict[key] is not None:
        if key == "course_template":
          course_template = CourseTemplate.find_by_id(
              update_cohort_dict[key])
          setattr(cohort_details, key, course_template)
        else:
          setattr(cohort_details, key, update_cohort_dict[key])
    cohort_details.update()
    return {
        "message": f"Successfully Updated the Cohort with id {cohort_id}",
        "cohort": convert_cohort_to_cohort_model(cohort_details)
    }
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.delete("/{cohort_id}", response_model=DeleteCohortResponseModel)
def delete_cohort(cohort_id: str):
  """Delete a Cohort endpoint
    Args:
        cohort_id (str): unique id of the Cohort

    Raises:
        ResourceNotFoundException: If the Cohort does not exist
        HTTPException: 500 Internal Server Error if something fails

    Returns:
        DeleteCohortModel: if the Cohort is deleted,
        NotFoundErrorResponseModel: if the Cohort not found,
        InternalServerErrorResponseModel:
            if the Cohort deletion raises an exception
    """
  try:
    Cohort.soft_delete_by_id(cohort_id)
    return {
          "message": f"Successfully deleted the Cohort with id {cohort_id}"
      }
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.get("/{cohort_id}/sections",
            response_model=SectionListResponseModel)
def list_section(cohort_id: str):
  """ Get a list of sections of one cohort from db

  Args:
    cohort_id(str):cohort id from firestore db
  Raises:
    HTTPException: 500 Internal Server Error if something fails
    ResourceNotFound: 404 Resource not found exception
  Returns:
    {"status":"Success","data":{}}: Returns list of sections
    {'status': 'Failed',"data":null}
  """
  try:

    # Get cohort Id and create a reference of cohort object

    cohort = Cohort.find_by_id(cohort_id)
    # Using the cohort object reference key query sections model to get a list
    # of section of a perticular cohort
    result = Section.collection.filter("cohort", "==", cohort.key).fetch()
    sections_list = list(map(convert_section_to_section_model, result))
    return {"data": sections_list}
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except Exception as e:
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    raise InternalServerError(str(e)) from e
