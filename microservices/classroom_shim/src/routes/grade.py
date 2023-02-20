''' Grade APIs '''
import requests
from fastapi import APIRouter
from common.models import LTIAssignment
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError
from common.utils.classroom_crud import (get_credentials,
                                         post_grade_of_the_user,
                                         get_submitted_course_work_list)
from common.utils.secrets import get_backend_robot_id_token
from schemas.grade_schema import PostGradeModel
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)

# pylint: disable=line-too-long

router = APIRouter(
    tags=["Grade"],
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

creds = get_credentials()


@router.post("/grade")
def update_classroom_grade(input_grade: PostGradeModel):
  """Post/Updates the student grade in the classroom for a given course
   work in a course"""

  try:
    input_grade_dict = {**input_grade.dict()}

    # TODO: Need to check where the comment can be added in the classroom
    if input_grade_dict["comment"]:
      pass

    lti_assignment = LTIAssignment.collection.filter(
        "lti_content_item_id", "==",
        input_grade_dict["lti_content_item_id"]).get()

    get_section_url = f"http://lms/lms/api/v1/sections/{lti_assignment.section_id}"

    section_res = requests.get(
        url=get_section_url,
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        timeout=60)

    if section_res.status_code == 200:
      section_data = section_res.json().get("data")
    else:
      raise Exception("Internal server error from lms API")

    course_id = section_data.get("classroom_id")

    lti_assignment_max_points = lti_assignment.max_points
    course_work_id = lti_assignment.course_work_id

    assigned_grade = input_grade_dict["assigned_grade"]
    draft_grade = input_grade_dict["assigned_grade"]

    if assigned_grade:
      assigned_grade = (assigned_grade / input_grade_dict["maximum_grade"]
                       ) * lti_assignment_max_points

    if draft_grade:
      draft_grade = (draft_grade / input_grade_dict["maximum_grade"]
                    ) * lti_assignment_max_points

    user_id = input_grade_dict["user_id"]
    get_user_url = f"http://user-management/user-management/api/v1/user/{user_id}"

    user_res = requests.get(
        url=get_user_url,
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        timeout=60)

    if user_res.status_code == 200:
      user_data = user_res.json().get("data")
    else:
      raise Exception("Internal server error from lms API")

    user_email = user_data.get("email")
    submissions = get_submitted_course_work_list(course_id, user_email,
                                                 course_work_id)

    if submissions:
      submission_id = submissions[0].get("id")
      post_grade_of_the_user(course_id, course_work_id, submission_id,
                             assigned_grade, draft_grade)
    else:
      raise Exception("Submission not found for the user")

    return {"success": True}

  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e
