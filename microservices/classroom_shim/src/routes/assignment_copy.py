'''LTI Assignment Endpoints'''
import traceback
import requests
from fastapi import APIRouter
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError,
                                          CustomHTTPException)
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
from schemas.lti_assignment_schema import InputLTIAssignmentModel, UpdateLTIAssignmentModel
from routes.lti_assignment import get_lti_assignment, update_lti_assignment, create_lti_assignment
from common.utils.secrets import get_backend_robot_id_token
from common.utils import classroom_crud
from pydantic import BaseModel
from googleapiclient.errors import HttpError
# pylint: disable=line-too-long

router = APIRouter(
    tags=["LTI Assignments Copy"],
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


class CourseDetails(BaseModel):
  """Course Detail model"""
  course_id: str


@router.post("/copy_course")
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
                                              current_course["ownerId"])
    saved_lti_assignments_in_coursework = []
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
      lti_assignment_ids = []
      # Check if a coursework is linked to a topic
      # if yes then replace the old topic id to new
      # topic id using topic_id_map
      if "topicId" in coursework.keys():
        coursework["topicId"] = topic_id_map[coursework["topicId"]]
      # Check if a material is present in coursework
      if "materials" in coursework.keys():
        # Calling function to get edit_url and view url of google
        #  form which returns
        # a dictionary of view_links as keys and edit links as
        # values of google form
        url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in coursework has
        #  a google form attached to it
        # update the  view link to edit link and attach it as a form
        for material in coursework["materials"]:
          if "driveFile" in material.keys():
            material = classroom_crud.copy_material(material, target_folder_id)
          if "form" in material.keys():
            result1 = classroom_crud.drive_copy(
                url_mapping[material["form"]["formUrl"]]["file_id"],
                target_folder_id, material["form"]["title"])
            material["link"] = {
                "title": material["form"]["title"],
                "url": result1["webViewLink"]
            }
            # remove form from  material dict
            material.pop("form")
          ## Update lti assignment with the course work details
          if "link" in material.keys():
            link = material["link"]
            if "classroom_shim/api/v1?lti_assignment=" in link["url"]:
              split_url = link["url"].split(
                  "classroom_shim/api/v1?lti_assignment=")
              lti_assignment_id = split_url[-1]
              copy_assignment = copy_lti_assignment({
                  "lti_assignment_id": lti_assignment_id,
                  "context_id": new_course["id"]
              })
              material["link"] = link.replace(
                  lti_assignment_id,
                  copy_assignment.get("data").get("id"))

      # create coursework
      coursework_data = classroom_crud.create_single_coursework(
          new_course["id"], coursework)
      print("\n\n***coursework_data from classroom", coursework_data)
      for assignment_id in lti_assignment_ids:
        coursework_id = coursework_data.get("id")
        # get assignment
        lti_assignment = get_lti_assignment(assignment_id)
        lti_assignment["data"]["coursework_id"] = coursework_id
        # patch assignment
        update_lti_assignment(
            assignment_id,
            UpdateLTIAssignmentModel.parse_obj(lti_assignment["data"]))
      # update the lti assignment with the course work details

    # Create coursework in new course
    # if coursework_list is not None:
    #   classroom_crud.create_coursework(new_course["id"], coursework_list)
    # Get the list of courseworkMaterial
    coursework_material_list = classroom_crud.get_coursework_material(course_id)
    for coursework_material in coursework_material_list:
      # Check if a coursework material is linked to a topic if yes then
      # replace the old topic id to new topic id using topic_id_map
      if "topicId" in coursework_material.keys():
        coursework_material["topicId"] = topic_id_map[
            coursework_material["topicId"]]
      # Check if a material is present in coursework
      if "materials" in coursework_material.keys():
        # Calling function to get edit_url and view url of google form which
        # returns a dictionary of view_links as keys and edit links as values
        # of google form
        url_mapping = classroom_crud.get_edit_url_and_view_url_mapping_of_form()
        # Loop to check if a material in coursework has a google form attached to it
        # update the view link to edit link and attach it as a form
        for material in coursework_material["materials"]:
          if "driveFile" in material.keys():
            material = classroom_crud.copy_material(material, target_folder_id)
          if "form" in material.keys():
            new_copied_file_details = classroom_crud.drive_copy(
                url_mapping[material["form"]["formUrl"]]["file_id"],
                target_folder_id, material["form"]["title"])
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
    response = {}
    response["new_course"] = new_course
    response["coursework_list"] = coursework_list
    return {"data": response}
  except HttpError as hte:
    Logger.error(hte)
    raise CustomHTTPException(
        status_code=hte.resp.status, success=False, message=str(hte),
        data=None) from hte
  except Exception as e:
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    raise InternalServerError(str(e)) from e


@router.post("/lti-assignment/copy")
def copy_lti_assignment(data: dict):
  """
  input data format: {
    lti_assignment_id: "123",
    context_id: "123"
  }
  """
  try:
    # fetch content_item and related line_items
    assignment_data = get_lti_assignment(data.get("lti_assignment_id"))
    content_item_id = assignment_data.get("data").get("lti_content_item_id")
    tool_id = assignment_data.get("data").get("tool_id")

    content_item_req = requests.get(
        f"http://lti/lti/api/v1/content-item/{content_item_id}",
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        timeout=60)
    content_item_data = content_item_req.json().get("data")

    # create a copy of above content item
    content_item_data["context_id"] = data.get("context_id")
    del content_item_data["id"]
    del content_item_data["created_time"]
    del content_item_data["last_modified_time"]
    copy_content_item_req = requests.post(
        "http://lti/lti/api/v1/content-item",
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        json=content_item_data,
        timeout=60)

    copy_content_item_data = copy_content_item_req.json().get("data")
    copy_content_item_id = copy_content_item_data.get("id")

    new_lti_assignment_data = {
        **assignment_data, "section_id": data.get("context_id"),
        "lti_content_item_id": copy_content_item_data.get("id"),
        "course_work_id": None
    }
    new_lti_assignment_item = create_lti_assignment(
        InputLTIAssignmentModel.parse_obj(new_lti_assignment_data))
    return new_lti_assignment_item

  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
