""" User endpoints """
import traceback
from fastapi import APIRouter, HTTPException
from services import classroom_crud
from common.utils.logging_handler import Logger
# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/student", tags=["Student"])

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}


@router.get("/get_progress_percentage/")
def get_progress_percentage(course_id: int, student_email: str):
  """Get progress percentage

  Args:
    course_id :
      course_id of the course for which progress needs to be determined
    student_email : student_email of the student

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    A number indicative of the percentage of the course completed
    by the student,
    {'status': 'Failed'} if any exception is raised
  """
  try:
    submitted_course_work_list = 0
    course_work_list = len(classroom_crud.get_course_work_list(course_id))
    submitted_course_work = classroom_crud.get_submitted_course_work_list(
        course_id, student_email)
    for x in submitted_course_work:
      if x["state"] == "TURNED_IN":
        submitted_course_work_list = submitted_course_work_list + 1

    SUCCESS_RESPONSE["result"] = {
        "progress_percentage":
        round((submitted_course_work_list / course_work_list) * 100, 2)
    }
    return SUCCESS_RESPONSE

  except Exception as e:
    Logger.error(e)
    traceback.format_exc().replace("\n", " ")
    raise HTTPException(status_code=500) from e
