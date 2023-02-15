''' Grade APIs '''
from fastapi import APIRouter
from common.models import LTIAssignment
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (InternalServerError)
from common.utils.classroom_crud import (get_credentials, create_course,
                                         post_user_grade,
                                         get_submitted_course_work_list)
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
def update_classroom_grade(user_id: str,
                           assigned_grade: float,
                           comment: str,
                           lti_content_item_id: str,
                           maximum_grade: float = None,
                           draft_grade: float = None):
  """Post/Updates the student grade in the classroom for a given course
   work in a course"""
  # TODO: Get the course id and course work id using the lti content item id
  # from the lti assignment document
  # Need to check where the comment can be added in the classroom
  try:
    lti_assignment = LTIAssignment.filter("lti_content_item_id", "==",
                                          lti_content_item_id).get()

    lti_assignment_max_points = lti_assignment.max_points
    assigned_grade = (assigned_grade /
                      maximum_grade) * lti_assignment_max_points

    course_id = lti_assignment.section_id
    course_work_id = lti_assignment.course_work_id

    # TODO: Get the user email/gaia id using the firestore user_id

    #   userId="ltitesting001@gmail.com"
    submissions = get_submitted_course_work_list(course_id, user_id,
                                                 course_work_id)

    if submissions:
      submission_id = submissions[0].get("id")
      post_user_grade(course_id, course_work_id, submission_id, assigned_grade,
                      draft_grade)
    else:
      raise Exception("Submission not found for the user")

    return {"success": True}

  except Exception as e:
    Logger.error(e)
    raise InternalServerError(str(e)) from e
