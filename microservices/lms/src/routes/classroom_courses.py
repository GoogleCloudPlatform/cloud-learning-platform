"""Classroom Courses endpoint"""
import traceback
from common.utils.errors import  ValidationError, ResourceNotFoundException
from common.utils.http_exceptions import (ClassroomHttpException,
                        InternalServerError,ResourceNotFound,
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
                          ClassroomCourseListResponseModel,
                          ClassroomResponseModel
                          )
from utils.helper import FEED_TYPES,convert_course_dict_to_classroom_model
# disabling for linting to pass
# pylint: disable = broad-except

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
    course_list = list(classroom_crud.get_course_list())[skip:limit+skip]
    data=[convert_course_dict_to_classroom_model(i) for i in course_list]
    return {"data": data}
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except Exception as e:
    Logger.error(e)
    error = traceback.format_exc().replace("\n", " ")
    Logger.error(error)
    raise InternalServerError(str(e)) from e


@router.get("/{course_id}",response_model=ClassroomResponseModel)
def get_course(course_id:str):
  """_summary_

  Args:
      course_id (str): unique course id

  Raises:
      BadRequest: _description_
      ClassroomHttpException: _description_
      InternalServerError: _description_
      InternalServerError: _description_

  Returns:
      ClassroomResponseModel: object which contains course details
  """
  try:
    course=classroom_crud.get_course_by_id(course_id)
    if course is None:
      raise ResourceNotFoundException(
          "Classroom course with id" +
          f" {course_id} is not found")
    data=convert_course_dict_to_classroom_model(course)
    return {
      "message":f"Successfully fetch course by this {course_id} id",
      "data":data
      }
  except ValidationError as ve:
    raise BadRequest(str(ve)) from ve
  except ResourceNotFoundException as err:
    Logger.error(err)
    raise ResourceNotFound(str(err)) from err
  except HttpError as hte:
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except InternalServerError as ie:
    raise InternalServerError(str(ie)) from ie
  except Exception as e:
    Logger.error(e)
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
    final_coursework =[]
    for coursework in coursework_list:
      try:
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
          url_mapping = classroom_crud.\
            get_edit_url_and_view_url_mapping_of_form()
          # Loop to check if a material in courssework has
          #  a google form attached to it
          # update the  view link to edit link and attach it as a form
          for material in coursework["materials"]:
            if "driveFile" in  material.keys():
              material = classroom_crud.copy_material(material,target_folder_id)
            if "form" in material.keys():
              if "title" not in material["form"].keys():
                raise ResourceNotFound("Form to be copied is deleted")
              result1 = classroom_crud.drive_copy(
                url_mapping[material["form"]["formUrl"]]["file_id"],
                      target_folder_id,material["form"]["title"])
              material["link"] = {
                  "title": material["form"]["title"],
                  "url": result1["webViewLink"]
              }
              # remove form from  material dict
              material.pop("form")
        final_coursework.append(coursework)
      except Exception as error:
        title = coursework["title"]
        Logger.error(f"Get coursework failed for {title}")
        error=traceback.format_exc().replace("\n", " ")
        Logger.error(error)
        continue

    # Create coursework in new course
    if final_coursework is not None:
      classroom_crud.create_coursework(new_course["id"], final_coursework)
    # Get the list of courseworkMaterial
    coursework_material_list = classroom_crud.get_coursework_material(
        course_id)
    final_coursework_material=[]
    for coursework_material in coursework_material_list:
      try:
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
          url_mapping = classroom_crud.\
            get_edit_url_and_view_url_mapping_of_form()
          # Loop to check if a material in courssework has a google
          # form attached to it
          # update the  view link to edit link and attach it as a form
          for material in coursework_material["materials"]:
            if "driveFile" in  material.keys():
              material = classroom_crud.copy_material(material,target_folder_id)
            if "form" in material.keys():
              if "title" not in material["form"].keys():
                raise ResourceNotFound("Form to be copied is deleted")
              new_copied_file_details = classroom_crud.drive_copy(
                url_mapping[material["form"]["formUrl"]]["file_id"],
                      target_folder_id,material["form"]["title"])
              material["link"] = {
                  "title": material["form"]["title"],
                  "url": new_copied_file_details["webViewLink"]
              }
              # remove form from  material dict
              material.pop("form")
        final_coursework_material.append(coursework_material)
      except Exception as error:
        title = coursework_material["title"]
        error=traceback.format_exc().replace("\n", " ")
        Logger.error(
          f"Get coursework material failed for {title}")
        Logger.error(error)
        continue
    # Create coursework in new course
    if final_coursework_material is not None:
      classroom_crud.create_coursework_material(new_course["id"],
                                                final_coursework_material)
    response={}
    response["new_course"] = new_course
    response["coursework_list"] = final_coursework
    response["coursework_material"]=final_coursework_material
    return {"data":response}
  except HttpError as hte:
    Logger.error(hte)
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
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
      ClassroomHttpException: raise error according to the HTTPError exception
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
    raise ClassroomHttpException(status_code=hte.resp.status,
                              message=str(hte)) from hte
  except InternalServerError as ie:
    raise InternalServerError(str(ie)) from ie
  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e
