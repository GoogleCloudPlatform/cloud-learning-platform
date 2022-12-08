'''Course Template Endpoint'''
import datetime
from fastapi import APIRouter
from common.models import CourseTemplate, Cohort
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import ResourceNotFound, InternalServerError, BadRequest
from services import classroom_crud
from utils.helper import convert_cohort_to_cohort_model
from schemas.cohort import CohortListResponseModel
from schemas.course_template import CourseTemplateModel, CourseTemplateListModel, CreateCourseTemplateResponseModel, InputCourseTemplateModel, DeleteCourseTemplateModel,UpdateCourseTemplateModel,UpdateCourseTemplateResponseModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)

router = APIRouter(prefix="/course_templates",
                   tags=["CourseTemplate"],
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


@router.get("", response_model=CourseTemplateListModel)
def get_course_template_list():
  """Get a list of Course Template endpoint
    Raises:
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        CourseTemplateListModel:
            object which contains list of course template object.
        InternalServerErrorResponseModel:
            if the get Course Template list raises an exception.
    """
  try:
    course_template_list = CourseTemplate.collection.filter(
        "is_deleted", "==", False).fetch()
    if course_template_list is None:
      return {
          "message":
          "Successfully get the course template list, but the list is empty.",
          "course_template_list": []
      }
    return {"course_template_list": list(course_template_list)}
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{course_template_id}", response_model=CourseTemplateModel)
def get_course_template(course_template_id: str):
  """Get a Course Template endpoint

    Args:
        course_template_id (str): unique id of the course template

    Raises:
        ResourceNotFoundException: If the Course Template does not exist.
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        CourseTemplateModel: course template object for the provided id
        NotFoundErrorResponseModel: if the Course Template not found,
        InternalServerErrorResponseModel:
            if the get Course Template raises an exception
    """
  try:
    course_template = CourseTemplate.find_by_uuid(course_template_id)
    if course_template is None:
      raise ResourceNotFoundException(
          f"Course Template with uuid {course_template_id} is not found")
    return course_template
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{course_template_id}/cohorts",
            response_model=CohortListResponseModel)
def get_cohort_list_by_course_template_id(course_template_id: str):
  """Get list of cohorts inside a course template endpoint

    Args:
        course_template_id (str): unique id of the course template

    Raises:
        ResourceNotFoundException: If the Course Template does not exist.
        InternalServerError: Internal Server Error if something fails.

    Returns:
        CohortListResponseModel:
          object which contains list of cohort inside cousre template
        NotFoundErrorResponseModel: if the Course Template not found,
        InternalServerErrorResponseModel:
          if the get cohort list raises an exception
    """
  try:
    course_template = CourseTemplate.find_by_uuid(course_template_id)
    if course_template is None:
      raise ResourceNotFoundException(
          f"Course Template with uuid {course_template_id} is not found")
    fetched_cohort_list = Cohort.collection.filter(
        "course_template", "==", course_template.key).fetch()
    if fetched_cohort_list is None:
      return {
          "message":
          "Successfully get the cohorts list, but the list is empty.",
          "cohort_list": []
      }
    cohort_list = [
        convert_cohort_to_cohort_model(i) for i in fetched_cohort_list
    ]
    return {
        "message": "Successfully get the Cohort list" +
        f" by Course template uuid {course_template_id}",
        "cohort_list": cohort_list
    }
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post("", response_model=CreateCourseTemplateResponseModel)
def create_course_template(input_course_template: InputCourseTemplateModel):
  """Create a Course Template endpoint

    Args:
        input_course_template (InputCourseTemplateModel):
            input course template to be inserted

    Raises:
        InternalServerError: Internal Server Error if something went wrong

    Returns:
        CreateCourseTemplateResponseModel: Course Template Object
        InternalServerErrorResponseModel:
            if the Course Template creation raises an exception
  """
  try:
    course_template_dict = {**input_course_template.dict()}
    course_template = CourseTemplate()
    course_template = course_template.from_dict(course_template_dict)
    # creating course om classroom
    classroom = classroom_crud.create_course(
        name=course_template_dict["name"],
        section="master",
        description=course_template_dict["description"],
        owner_id=course_template_dict["admin"])
    # Adding instructional designer in the course on classroom
    classroom_crud.add_teacher(classroom.get("id"),
                               course_template_dict["instructional_designer"])
    # Storing classroom details
    course_template.classroom_id = classroom.get("id")
    course_template.classroom_code = classroom.get("enrollmentCode")
    # adding timestamp
    timestamp = datetime.datetime.utcnow()
    course_template.created_timestamp = timestamp
    course_template.last_updated_timestamp = timestamp
    course_template.save()
    course_template.uuid = course_template.id
    course_template.update()
    return {"course_template": course_template}
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.patch("/{course_template_id}",
              response_model=UpdateCourseTemplateResponseModel)
def update_course_template(course_template_id:str,
                  update_course_template_model: UpdateCourseTemplateModel):
  """Update Course Template Api

  Args:
      course_template_id (str): Unique id of course template
      update_course_template_model (UpdateCourseTemplateModel):
        pydantic model object which contains update details

  Raises:
      ResourceNotFoundException: If the Course Template does not exist
      InternalServerError: Internal Server Error if something went wrong

  Returns:
      UpdateCourseTemplateResponseModel:
          object which contains update success, message
            and updated course template record.
      NotFoundErrorResponseModel: if the Course Template not found,
      InternalServerErrorResponseModel:
          If the update course template raises an exception
  """
  try:
    course_template = CourseTemplate.find_by_uuid(course_template_id)
    if course_template is None:
      raise ResourceNotFoundException(
          f"Course Template with uuid {course_template_id} is not found")
    update_course_template_dict={**update_course_template_model.dict()}
    if not any(update_course_template_dict.values()):
      raise ValidationError("Invalid request please provide some " +
          f"data to update the Course Template with uuid {course_template_id}")
      # return {"message": "Please provide some data to update the" +
      #         f" Course Template with uuid {course_template_id}",
      #         "course_template": course_template}
    for key in update_course_template_dict:
      if update_course_template_dict[key] is not None:
        setattr(course_template,key,update_course_template_dict.get(key))
    course_template.last_updated_timestamp=datetime.datetime.utcnow()
    course_template.update()
    return {"message": "Successfully Updated the "+
            f"Course Template with uuid {course_template_id}",
            "course_template":course_template}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e

@router.delete("/{course_template_id}",
               response_model=DeleteCourseTemplateModel)
def delete_course_template(course_template_id: str):
  """Delete a Course Template endpoint
    Args:
        course_template_id (str): unique id of the Course Template

    Raises:
        ResourceNotFoundException: If the Course Template does not exist
        InternalServerError: 500 Internal Server Error if something fails

    Returns:
        DeleteCourseTemplateModel: if the Course Template is deleted,
        NotFoundErrorResponseModel: if the Course Template not found,
        InternalServerErrorResponseModel:
            if the Course Template deletion raises an exception
    """
  try:
    if CourseTemplate.archive_by_uuid(course_template_id):
      return {
          "message":
          "Successfully deleted the course template with" +
          f" uuid {course_template_id}"
      }
    else:
      raise ResourceNotFoundException(
          f"Course Template with uuid {course_template_id} is not found")
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e
