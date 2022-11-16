""" User endpoints """
import datetime
from re import I
from fastapi import APIRouter, HTTPException
from common.utils.logging_handler import Logger
from fastapi.encoders import jsonable_encoder
from google.api_core.exceptions import PermissionDenied
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from schemas.course_details import CourseDetails
from services import classroom_crud
import traceback
import os
# from config import CLASSROOM_KEY
import argparse
import requests
from config import CLASSROOM_ADMIN_EMAIL
# disabling for linting to pass
# pylint: disable = broad-except

router = APIRouter(prefix="/student", tags=["Course"])

SUCCESS_RESPONSE = {"status": "Success"}
FAILED_RESPONSE = {"status": "Failed"}

@router.get("/get_progress_percentage/")
def get_progress_percentage(course_id:int,student_email:str):
  """Get progress percentage

  Args:
    course_id : course_id of the course for which progress needs to be determined
    student_id : student_id of the student

  Raises:
    HTTPException: 500 Internal Server Error if something fails

  Returns:
    A number indicative of the percentage of the course colpleted by the student,
    {'status': 'Failed'} if any exception is raised
  """
  try:
    submitted_course_work_list=0 
    # course_work = classroom_crud.get_course_work_list(course_id)
    course_work_list = len(classroom_crud.get_course_work_list(course_id))
    submitted_course_work = classroom_crud.get_submitted_course_work_list(course_id,student_email)
    for x in submitted_course_work:
      if x['state']=="TURNED_IN":
        submitted_course_work_list = submitted_course_work_list+1

    print("total submitted",course_work_list,submitted_course_work_list)
    SUCCESS_RESPONSE["result"]= {"progress_percentage":round((submitted_course_work_list/course_work_list)*100,2)}
    return SUCCESS_RESPONSE

  except Exception as e:
    print("in error",e)
    Logger.error(e)
    err = traceback.format_exc().replace("\n", " ")
    raise HTTPException(status_code=500) from e