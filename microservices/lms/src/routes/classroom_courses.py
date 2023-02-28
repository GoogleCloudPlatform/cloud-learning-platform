"""Classroom Courses endpoint"""
import traceback
from common.utils.errors import  ValidationError
from common.utils.http_exceptions import (CustomHTTPException,
                                          InternalServerError,
                                          BadRequest)
from common.utils import classroom_crud
from common.utils.logging_handler import Logger
from fastapi import APIRouter
from googleapiclient.errors import HttpError
from schemas.error_schema import (ConflictResponseModel,
                                  InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from schemas.classroom_courses import (
                          CourseDetails,
                          EnableNotificationsResponse,
                          CopyCourseResponse,
                          ClassroomCourseListResponseModel
                          )
from utils.helper import FEED_TYPES

router = APIRouter(prefix="/classroom_courses",
                   tags=["ClassroomCourses"],
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

@router.get("", response_model=ClassroomCourseListResponseModel)
def get_courses(skip: int = 0, limit: int = 10):
  """Get courses list
  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    List of courses in classroom ,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")
    if limit < 1:
      raise ValidationError(
          "Invalid value passed to \"limit\" query parameter")
    course_list = classroom_crud.get_course_list()
    return {"data": list(course_list)[skip:limit]}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except HttpError as hte:
    Logger.error(hte)
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
  except Exception as e:
    Logger.error(e)
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    raise InternalServerError(str(e)) from e


@router.post("/copy_course",response_model=CopyCourseResponse)
def copy_courses(course_details: CourseDetails):
  """Copy course  API

  Args:
    course_id (Course): Course_id of a course that needs to copied

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    {"status":"Success","new_course":{}}: Returns new course details,
    {'status': 'Failed'} if the user creation raises an exception
  """
  try:
    input_course_details_dict = {**course_details.dict()}
    course_id = input_course_details_dict["course_id"]
    # Get course by course id
    current_course = classroom_crud.get_course_by_id(course_id)
    if current_course is None:
      return "No course found "
    # Create a new course
    new_course = classroom_crud.create_course(current_course["name"],
                                              current_course["description"],
                                              current_course["section"],
                                              current_course["ownerId"]
                                              )

    target_folder_id = new_course["teacherFolder"]["id"]
    # Get topics of current course
    topics = classroom_crud.get_topics(course_id)
    # If topics are present in course create topics returns a dict
    # with keys a current topicID and new topic id as values
    if topics is not None:
      topic_id_map = classroom_crud.create_topics(new_course["id"], topics)
    # Get coursework of current course and create a new course
    coursework_list = classroom_crud.get_coursework(course_id)
    for coursework in coursework_list:
      # Check if a coursework is linked to
      #  a topic if yes then
      # replace the old topic id to new
      # topic id using topic_id_map
      if "topicId" in coursework.keys():
        coursework["topicId"] = topic_id_map[coursework["topicId"]]
      # Check if a material is present in coursework
      if "materials" in coursework.keys():
        # Calling function to get edit_url and view url of google
        #  form which returns
        # a dictionary of view_links as keys and edit likns as
        # values of google form
        url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in courssework has
        #  a google form attached to it
        # update the  view link to edit link and attach it as a form
        for material in coursework["materials"]:
          if "driveFile" in  material.keys():
            material = classroom_crud.copy_material(material,target_folder_id)
          print("_____________NEW MATERIAL__________________")
          print(material)
          if "form" in material.keys():
            print("In form Loop ",url_mapping[material["form"]["formUrl"]])
            result1 = classroom_crud.drive_copy(url_mapping[material["form"]["formUrl"]]["file_id"],
                                          target_folder_id,material["form"]["title"])
            material["link"] = {
                "title": material["form"]["title"],
                "url": result1["webViewLink"]
            }
            # remove form from  material dict
            material.pop("form")

    # Create coursework in new course
    if coursework_list is not None:
      classroom_crud.create_coursework(new_course["id"], coursework_list)
    # Get the list of courseworkMaterial
    coursework_material_list = classroom_crud.get_coursework_material(
        course_id)
    for coursework_material in coursework_material_list:
      # Check if a coursework material is linked to a topic if yes then
      # replace the old topic id to new topic id using topic_id_map
      if "topicId" in coursework_material.keys():
        coursework_material["topicId"] = topic_id_map[
            coursework_material["topicId"]]
      # Check if a material is present in coursework
      if "materials" in coursework_material.keys():
        # Calling function to get edit_url and view url of
        # google form which returns
        # a dictionary of view_links as keys and edit
        #  likns as values of google form
        url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in courssework has a google
        # form attached to it
        # update the  view link to edit link and attach it as a form
        for material in coursework_material["materials"]:
          if "driveFile" in  material.keys():
            material = classroom_crud.copy_material(material,target_folder_id)
            print(material)
          if "form" in material.keys():
            print("In form Loop ",url_mapping[material["form"]["formUrl"]])
            new_copied_file_details = classroom_crud.drive_copy(url_mapping[material["form"]["formUrl"]]["file_id"],
                                          target_folder_id,material["form"]["title"])
            material["link"] = {
                "title": material["form"]["title"],
                "url": new_copied_file_details["webViewLink"]
            }
            # remove form from  material dict
            material.pop("form")
    # Create coursework in new course
    if coursework_material_list is not None:
      classroom_crud.create_coursework_material(new_course["id"],
                                                coursework_material_list)
    response={}
    response["new_course"] = new_course
    response["coursework_list"] = coursework_list
    return {"data":response}
  except HttpError as hte:
    Logger.error(hte)
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@router.post("/{course_id}/enable_notifications",
             response_model=EnableNotificationsResponse)
def classroom_enable_notifications_pub_sub(course_id:str):
  """Resgister course with a pub/sub topic

  Args:
      course_id (str): unique course id
  Raises:
      InternalServerError: 500 Internal Server Error if something fails
      CustomHTTPException: raise error according to the HTTPError exception
  Returns:
      _type_: _description_
  """
  try:
    responses = [classroom_crud.enable_notifications(course_id,
              i) for i in FEED_TYPES
      ]
    return {
        "message":
        "Successfully enable the notifications of the course using " +
        f"{course_id} id",
        "data": responses
    }
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except HttpError as hte:
    raise CustomHTTPException(status_code=hte.resp.status,
                              success=False,
                              message=str(hte),
                              data=None) from hte
  except InternalServerError as ie:
    raise InternalServerError(str(ie)) from ie
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e
