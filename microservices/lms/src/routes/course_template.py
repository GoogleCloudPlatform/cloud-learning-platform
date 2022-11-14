'''Course Template Endpoint'''
import datetime
from fastapi import APIRouter
from schemas.course_template import CourseTemplateModel, CourseTemplateListModel, CreateCourseTemplateResponseModel, InputCourseTemplateModel, DeleteCourseTemplateModel
from common.models import CourseTemplate
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import ResourceNotFound, InternalServerError
from services import classroom_crud
from schemas.error_schema import (InternalServerErrorResponseModel, NotFoundErrorResponseModel,
                                  ConflictResponseModel, ValidationErrorResponseModel)

router = APIRouter(prefix="/course_templates", tags=["CourseTemplate"], responses={
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


@router.get("/list", response_model=CourseTemplateListModel)
def get_course_template_list():
    """Get a list of Course Template endpoint
    
    Raises:
        HTTPException: 500 Internal Server Error if something fails.

    Returns:
        CourseTemplateListModel: object which contains list of course template object.
        InternalServerErrorResponseModel: if the get Course Template list raises an exception.
    """
    try:
        fetched_course_template_list = CourseTemplate.collection.filter(
            "is_deleted", "==", False).fetch()
        if fetched_course_template_list is None:
            return {"message": "Successfully get the course template list, but the list is empty.", "course_template_list": []}
        course_template_list = [i for i in fetched_course_template_list]
        return {"course_template_list": course_template_list}
    except ResourceNotFoundException as re:
        raise ResourceNotFound(str(re)) from re
    except Exception as e:
        print(e.message)
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
        InternalServerErrorResponseModel: if the get Course Template raises an exception
    """
    try:
        course_template = CourseTemplate.find_by_uuid(course_template_id)
        if course_template is None:
            raise ResourceNotFoundException(
                f'Course Template with uuid {course_template_id} is not found')
        return course_template
    except ResourceNotFoundException as re:
        raise ResourceNotFound(str(re)) from re
    except Exception as e:
        Logger.error(e)
        raise InternalServerError(str(e)) from e


@router.post("", response_model=CreateCourseTemplateResponseModel)
def create_course_template(input_course_template: InputCourseTemplateModel):
    """Create a Course Template endpoint

    Args:
        input_course_template (InputCourseTemplateModel): input course template to be inserted

    Raises:
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        CreateCourseTemplateResponseModel: Course Template Object
        InternalServerErrorResponseModel: if the Course Template creation raises an exception
  """
    try:
        course_template_dict = {**input_course_template.dict()}
        course_template = CourseTemplate()
        course_template = course_template.from_dict(course_template_dict)
        # creating course om classroom
        classroom = classroom_crud.create_course(
            name=course_template_dict["name"], section="master", description=course_template_dict["description"], owner_id=course_template_dict["admin"])
        # Adding instructional designer in the course on classroom
        classroom_crud.add_teacher(classroom.get(
            "id"), course_template_dict["instructional_designer"])
        # Storing classroom details
        course_template.classroom_id = classroom.get("id")
        course_template.classroom_code = classroom.get("enrollmentCode")
        # adding timestamp
        timestamp=datetime.datetime.utcnow()
        course_template.created_timestamp=timestamp
        course_template.last_updated_timestamp=timestamp
        course_template.save()
        course_template.uuid = course_template.id
        course_template.update()
        return {"course_template": course_template}
    except Exception as e:
        Logger.error(e)
        raise InternalServerError(str(e)) from e


@router.delete("/{course_template_id}", response_model=DeleteCourseTemplateModel)
def delete_course_template(course_template_id: str):
    """Delete a Course Template endpoint
    Args:
        course_template_id (str): unique id of the Course Template

    Raises:
        ResourceNotFoundException: If the Course Template does not exist
        HTTPException: 500 Internal Server Error if something fails

    Returns:
        DeleteCourseTemplateModel: if the Course Template is deleted,
        NotFoundErrorResponseModel: if the Course Template not found,
        InternalServerErrorResponseModel: if the Course Template deletion raises an exception
    """
    try:
        if CourseTemplate.archive_by_uuid(course_template_id):
            return {"message": f"Successfully deleted the course template with uuid {course_template_id}"}
        else:
            raise ResourceNotFoundException(
                f'Course Template with uuid {course_template_id} is not found')
    except ResourceNotFoundException as re:
        raise ResourceNotFound(str(re)) from re
    except Exception as e:
        Logger.error(e)
        raise InternalServerError(str(e)) from e
