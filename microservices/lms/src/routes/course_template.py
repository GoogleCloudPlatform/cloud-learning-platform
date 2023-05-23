'''Course Template Endpoint'''
from fastapi import APIRouter, Request
import datetime
import traceback
from googleapiclient.errors import HttpError
from common.models import CourseTemplate, Cohort, CourseTemplateEnrollmentMapping, User
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException, ValidationError
from common.utils.http_exceptions import (ResourceNotFound,
                                          InternalServerError, BadRequest,
                                          ClassroomHttpException, Conflict)
from common.utils import classroom_crud
from common.utils.bq_helper import insert_rows_to_bq
from config import (CLASSROOM_ADMIN_EMAIL, BQ_TABLE_DICT, BQ_DATASET)
from utils.helper import (convert_cohort_to_cohort_model)
from utils.user_helper import (
    course_template_enrollment_instructional_designer_model,
    check_instructional_designer_can_enroll, get_user_id)
from services import common_service
from schemas.cohort import CohortListResponseModel
from schemas.course_template import (
    CourseTemplateModel, CourseTemplateListModel,
    CreateCourseTemplateResponseModel, InputCourseTemplateModel,
    DeleteCourseTemplateModel, UpdateCourseTemplateModel,
    UpdateCourseTemplateResponseModel, AddInstructionalDesigner,
    EnrollmentResponseModel, DeleteInstructionalDesignerResponseModel)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ConflictResponseModel,
                                  ValidationErrorResponseModel)
# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/course_templates",
                   tags=["CourseTemplates"],
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
def get_course_template_list(skip: int = 0, limit: int = 10):
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
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")
    course_template_list = CourseTemplate.fetch_all(skip=skip, limit=limit)
    if course_template_list is None:
      return {
          "message":
          "Successfully get the course template list, but the list is empty.",
          "course_template_list": []
      }
    return {"course_template_list": list(course_template_list)}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
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
    course_template = CourseTemplate.find_by_id(course_template_id)
    return course_template
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.get("/{course_template_id}/cohorts",
            response_model=CohortListResponseModel)
def get_cohort_list_by_course_template_id(course_template_id: str,
                                          skip: int = 0,
                                          limit: int = 10):
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
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError\
        ("Invalid value passed to \"limit\" query parameter")
    course_template = CourseTemplate.find_by_id(course_template_id)
    fetched_cohort_list = Cohort.fetch_all_by_course_template(
        course_template_key=course_template.key, skip=skip, limit=limit)
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
        f" by Course template id {course_template_id}",
        "cohort_list": cohort_list
    }
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post("", response_model=CreateCourseTemplateResponseModel)
def create_course_template(input_course_template: InputCourseTemplateModel
                           # ,request: Request
                           ):
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
    # headers = {"Authorization": request.headers.get("Authorization")}
    course_template_dict = {**input_course_template.dict()}
    course_template = CourseTemplate()
    course_template = course_template.from_dict(course_template_dict)
    # creating course om classroom
    classroom = classroom_crud.create_course(
        name=course_template_dict["name"],
        section="template",
        description=course_template_dict["description"],
        owner_id="me")
    course_template.classroom_id = classroom.get("id")
    course_template.classroom_code = classroom.get("enrollmentCode")
    course_template.classroom_url = classroom.get("alternateLink")
    course_template.admin = CLASSROOM_ADMIN_EMAIL
    course_template_id = course_template.save().id
    rows = [{
        "courseTemplateId": course_template_id,
        "classroomId": course_template.classroom_id,
        "name": course_template.name,
        "description": course_template.description,
        "timestamp": datetime.datetime.utcnow(),
        "instructionalDesigners": []
    }]
    insert_rows_to_bq(rows=rows,
                      dataset=BQ_DATASET,
                      table_name=BQ_TABLE_DICT["BQ_COLL_COURSETEMPLATE_TABLE"])
    return {"course_template": course_template}
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                                 message=str(hte)) from hte
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.patch("/{course_template_id}",
              response_model=UpdateCourseTemplateResponseModel)
def update_course_template(
    course_template_id: str,
    update_course_template_model: UpdateCourseTemplateModel
    # ,request: Request
):
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
    course_template = CourseTemplate.find_by_id(course_template_id)
    update_course_template_dict = {**update_course_template_model.dict()}
    if not any(update_course_template_dict.values()):
      raise ValidationError(
          "Invalid request please provide some " +
          f"data to update the Course Template with id {course_template_id}")
    for key in update_course_template_dict:
      if update_course_template_dict[key] is not None:
        setattr(course_template, key, update_course_template_dict.get(key))
    classroom_crud.update_course(course_id=course_template.classroom_id,
                                 section_name="template",
                                 description=course_template.description,
                                 course_name=course_template.name)
    course_template.update()
    list_enrollment_mapping=CourseTemplateEnrollmentMapping\
      .fetch_all_by_course_template(course_template.key)
    list_instructional_designers = [
        i.user.email for i in list_enrollment_mapping
    ]
    rows = [{
        "courseTemplateId": course_template_id,
        "classroomId": course_template.classroom_id,
        "name": course_template.name,
        "description": course_template.description,
        "timestamp": datetime.datetime.utcnow(),
        "instructionalDesigners": [list_instructional_designers]
    }]
    insert_rows_to_bq(rows=rows,
                      dataset=BQ_DATASET,
                      table_name=BQ_TABLE_DICT["BQ_COLL_COURSETEMPLATE_TABLE"])
    return {
        "message": "Successfully Updated the " +
        f"Course Template with id {course_template_id}",
        "course_template": course_template
    }
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                                 message=str(hte)) from hte
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
    CourseTemplate.soft_delete_by_id(course_template_id)
    return {
        "message":
        "Successfully deleted the course template with" +
        f" id {course_template_id}"
    }
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.post("/{course_template_id}/instructional_designers",
             response_model=EnrollmentResponseModel)
def add_instructional_designer(
    course_template_id: str, request: Request,
    instructional_designer: AddInstructionalDesigner):
  """_summary_

  Args:
      course_template_id (str): _description_
      request (Request): _description_
      instructional_designer (AddInstructionalDesigner): _description_

  Returns:
      _type_: _description_
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    course_template = CourseTemplate.find_by_id(course_template_id)
    instructional_designer = instructional_designer.email
    if not check_instructional_designer_can_enroll(instructional_designer,
                                                   headers, course_template):
      raise Conflict(
          f"Instructional Designer {instructional_designer} is already" +
          f" exists in this Course template {course_template.id}")
    invitation_object = classroom_crud.invite_user(
        course_template.classroom_id, instructional_designer, "TEACHER")
    try:
      classroom_crud.acceept_invite(invitation_object["id"],
                                    instructional_designer)
      user_profile = classroom_crud.\
          get_user_profile_information(instructional_designer)

      data = {
          "first_name": user_profile["name"]["givenName"],
          "last_name": user_profile["name"]["familyName"],
          "email": instructional_designer,
          "user_type": "faculty",
          "user_groups": [],
          "status": "active",
          "is_registered": True,
          "failed_login_attempts_count": 0,
          "access_api_docs": False,
          "gaia_id": user_profile["id"],
          "photo_url": user_profile["photoUrl"]
      }
      status = "active"
      invitation_id = ""
    except Exception as hte:
      Logger.info(hte)
      data = {
          "first_name": "first_name",
          "last_name": "last_name",
          "email": instructional_designer,
          "user_type": "faculty",
          "user_groups": [],
          "status": "active",
          "is_registered": True,
          "failed_login_attempts_count": 0,
          "access_api_docs": False,
          "gaia_id": "",
          "photo_url": ""
      }
      status = "invited"
      invitation_id = invitation_object["id"]
    user_dict = common_service.create_teacher(headers, data)
    course_template_enrollment = CourseTemplateEnrollmentMapping()
    course_template_enrollment.course_template = course_template
    course_template_enrollment.user = User.find_by_user_id(
        user_dict["user_id"])
    course_template_enrollment.status = status
    course_template_enrollment.invitation_id = invitation_id
    course_template_enrollment.role = "faculty"
    course_template_enrollment.save()
    list_enrollment_mapping=CourseTemplateEnrollmentMapping\
      .fetch_all_by_course_template(course_template.key)
    list_instructional_designers = [
        i.user.email for i in list_enrollment_mapping
    ]
    rows = [{
        "courseTemplateId": course_template_id,
        "classroomId": course_template.classroom_id,
        "name": course_template.name,
        "description": course_template.description,
        "timestamp": datetime.datetime.utcnow(),
        "instructionalDesigners": [list_instructional_designers]
    }]
    insert_rows_to_bq(rows=rows,
                      dataset=BQ_DATASET,
                      table_name=BQ_TABLE_DICT["BQ_COLL_COURSETEMPLATE_TABLE"])
    return {
        "message": ("Successfully Added the Instructional " +
                    f"Designer with email {instructional_designer}"),
        "data":
        course_template_enrollment_instructional_designer_model(
            course_template_enrollment)
    }
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                                 message=str(hte)) from hte
  except Conflict as conflict:
    Logger.error(conflict)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise Conflict(str(conflict)) from conflict
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e


@router.delete(
    "/{course_template_id}/instructional_designers/{instructional_designer}",
    response_model=DeleteInstructionalDesignerResponseModel)
def delete_instructional_designer(course_template_id: str,
                                  instructional_designer: str,
                                  request: Request):
  """_summary_

  Args:
      course_template_id (str): _description_
      request (Request): _description_
      instructional_designer (str): _description_

  Raises:
      ResourceNotFoundException: _description_
      ClassroomHttpException: _description_
      Conflict: _description_
      ResourceNotFound: _description_
      InternalServerError: _description_
  """
  try:
    headers = {"Authorization": request.headers.get("Authorization")}
    course_template = CourseTemplate.find_by_id(course_template_id)
    user_id = get_user_id(instructional_designer, headers)
    result = CourseTemplateEnrollmentMapping.find_enrolled_active_record(
        course_template.key, user_id)
    if result is None:
      raise ResourceNotFoundException(
          "Instructional Designer not found in this" +
          f" Course Template {course_template_id}")
    classroom_crud.delete_teacher(course_template.classroom_id,
                                  result.user.email)
    result.status = "inactive"
    result.update()
    list_enrollment_mapping=CourseTemplateEnrollmentMapping\
      .fetch_all_by_course_template(course_template.key)
    list_instructional_designers = [
        i.user.email for i in list_enrollment_mapping
    ]
    rows = [{
        "courseTemplateId": course_template_id,
        "classroomId": course_template.classroom_id,
        "name": course_template.name,
        "description": course_template.description,
        "timestamp": datetime.datetime.utcnow(),
        "instructionalDesigners": [list_instructional_designers]
    }]
    insert_rows_to_bq(rows=rows,
                      dataset=BQ_DATASET,
                      table_name=BQ_TABLE_DICT["BQ_COLL_COURSETEMPLATE_TABLE"])
    return {
        "message": ("Successfully delete teacher from section" +
                    f" {course_template_id} using {instructional_designer}")
    }
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                                 message=str(hte)) from hte
  except Conflict as conflict:
    Logger.error(conflict)
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise Conflict(str(conflict)) from conflict
  except ResourceNotFoundException as re:
    raise ResourceNotFound(str(re)) from re
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e
