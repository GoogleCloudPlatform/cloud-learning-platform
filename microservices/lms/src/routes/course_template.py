'''Course Endpoint'''
import datetime
import json
import logging
from fastapi import APIRouter, HTTPException,Response
from schemas.course_template import CourseTemplateModel, CourseTemplateListModel, CreateCourseTemplateResponseModel, InputCourseTemplateModel
from common.models import CourseTemplate
from common.utils.logging_handler import Logger

router = APIRouter(prefix="/course_templates", tags=["CourseTemplate"])

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = json.dumps({"status": "Failed"})

@router.get("/list",response_model=CourseTemplateListModel)
def get_course_list(response: Response):
    """Get a list of course template
    
    Raises:
        HTTPException: 500 Internal Server Error if something fails

    Returns:
        [course_template]: Array of course template object 
    """
    try:
        course_template_list=CourseTemplate.collection.fetch()
        if course_template_list is None:
            response.status_code=404
            response.body=json.dumps({"status":"Success","message":"Course Template not found"})
            return response
        courses_list_template=[i for i in course_template_list]
        return {"course_template_list":courses_list_template}
    except Exception as e:
        logging.error(e.message)
        response.status_code=500
        response.body=FAILED_RESPONSE
        return response

@router.get("/{course_template_id}",response_model=CourseTemplateModel)
def get_course(course_template_id:str,response:Response):
    """Get a course template

    Args:
        course_id (str): unique id of the course template

    Raises:
        HTTPException: 404 Not Found if course doesn't exist for the given id
        HTTPException: 500 Internal Server Error if something fails

    Returns:
        [course_template]: course template object for the provided id
    """
    try:
        course_template=CourseTemplate.find_by_id(course_template_id)
        logging.info(course_template.to_dict())
        if course_template is None:
            response.status_code=404
            response.body=json.dumps({"status":"Success","message":"Course Template not found"})
            return response
        return course_template
    # except HTTPException as e:
    #     return HTTPException(status_code=e.status_code,detail=e.detail)
    except Exception as e:
        response.status_code=500
        response.body=FAILED_RESPONSE
        return response


@router.post("",response_model=CreateCourseTemplateResponseModel)
def create_course(input_course_template:InputCourseTemplateModel,response:Response):
    """Create a course template endpoint

    Args:
        input_course_template (InputCourseTemplateModel): input course template to be inserted

    Raises:
        Exception: 500 Internal Server Error if something went wrong

    Returns:
        CreateCourseTemplateResponseModel: Course Template Object
  """
    try:
        course_template_dict={**input_course_template.dict()}
        course_template=CourseTemplate()
        course_template=course_template.from_dict(course_template_dict)
        timestamp = datetime.datetime.utcnow()
        course_template.created_timestamp = timestamp
        course_template.last_updated_timestamp = timestamp
        course_template.save()
        return {"course_template":course_template}
    except Exception as e:
        logging.info(e.message)
        response.status_code=500
        response.body=FAILED_RESPONSE
        return response



@router.delete("/{course_template_id}")
def delete_course(course_template_id:str,response:Response):
    '''
    
    '''
    try:
        course=CourseTemplate.find_by_id(course_template_id)
        if course is None:
            response.status_code=404
            response.body=json.dumps({"status":"Success","message":"Course Template not found"})
            return response
        CourseTemplate.delete_by_id(course_template_id)
        return SUCCESS_RESPONSE
    except Exception as e:
        response.status_code=500
        response.body=FAILED_RESPONSE
        return response




