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
    EnrollmentResponseModel, DeleteInstructionalDesignerResponseModel,
    GetInstructionalDesigner, ListInstructionalDesigner)
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
@router.get("",response_model=CourseTemplateListModel)
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
			raise ValidationError(
				"Invalid value passed to \"limit\" query parameter")
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
