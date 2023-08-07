# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Save User Data to BQ Service
"""
import datetime
import json
import uuid
from common.utils.logging_handler import Logger
from common.utils.bq_helper import insert_rows_to_bq
from googleapiclient.errors import HttpError
from helper.classroom_helper import(get_course_work, get_student_submissions,
                                    get_course_work_material,get_user)
from helper.json_helper import convert_dict_array_to_json,convert_to_json
from config import BQ_TABLE_DICT,BQ_DATASET
# disabling for linting to pass
# pylint: disable = broad-except
event_based_message={
  "CREATED":"New Assignment is assigned",
  "MODIFIED":"Assignment got modified"
}
def get_message(event_type,course_work_type):
  if event_type == "CREATED":
    return f"New {course_work_type} is assigned"
  else:
    return f"Existing {course_work_type} is modified"

def save_course_work(data):
  """_summary_

  Args:
    data (_type_): _description_

  Returns:
    _type_: _description_
  """
  try:
    rows = [{
    "message_id": data["message_id"], "collection": data["collection"],
    "event_type":data["eventType"], "resource":json.dumps(data["resourceId"]),
    "publish_time":data["publish_time"],"timestamp":datetime.datetime.utcnow()
        }]
    log_flag = insert_rows_to_bq(rows=rows,
                                 dataset=BQ_DATASET,
                                 table_name=BQ_TABLE_DICT["BQ_LOG_CW_TABLE"])
    if data["eventType"] == "DELETED":
      return log_flag,None
    course_work_flag=False
    if len(data["collection"].split(".")) == 3:
      if data["collection"].split(".")[2] == "studentSubmissions":
        course_work_flag,notification_message =  save_student_submission(
                course_id=data["resourceId"]["courseId"],
                message_id=data["message_id"],
                course_work_id=data["resourceId"]["courseWorkId"],
                submissions_id=data["resourceId"]["id"],
                event_type=data["eventType"])
    else:
      course_work_flag,notification_message = save_course_work_collection(
            course_id=data["resourceId"]["courseId"],
            message_id=data["message_id"],
            course_work_id=data["resourceId"]["id"],
          event_type=data["eventType"])
    return (log_flag & course_work_flag),notification_message
  except HttpError as ae:
    Logger.error(ae)
    return False,None
  except Exception as e:
    Logger.error(e)
    return False,None



def save_course_work_collection(course_id,course_work_id,message_id,event_type):
  """_summary_

  Args:
    course_id (_type_): _description_
    course_work_id (_type_): _description_
    message_id (_type_): _description_

  Returns:
    _type_: _description_
  """
  try:
    course_work=get_course_work(
      course_id=course_id,course_work_id=course_work_id)
    course_work["uuid"] = str(uuid.uuid4())
    course_work["message_id"] = message_id
    course_work["assignment"] =convert_to_json(course_work,"assignment")
    course_work["multipleChoiceQuestion"] = convert_to_json(
        course_work, "multipleChoiceQuestion")
    course_work["individualStudentsOptions"] = convert_to_json(
        course_work, "individualStudentsOptions")
    course_work["gradeCategory"] = convert_to_json(course_work, "gradeCategory")
    course_work["materials"] = convert_dict_array_to_json(
      course_work,"materials")
    course_work["event_type"] = event_type
    course_work["timestamp"] = datetime.datetime.utcnow()
    return insert_rows_to_bq(
      rows=[course_work],
      dataset=BQ_DATASET,
      table_name=BQ_TABLE_DICT["BQ_COLL_CW_TABLE"]),{
        "type": "broadcast",
        "classroom_id": course_id,
        "course_work_id": course_work_id,
        "course_work_title": course_work["title"],
        "course_work_url": course_work["alternateLink"],
        "message": get_message(event_type, "Assignment")
    }
  except HttpError as hte:
    Logger.info(hte)
    if hte.status_code == 404:
      course_work_material=get_course_work_material(
        course_id,course_work_id)
      if course_work_material:
        notification_message = {
              "type": "broadcast",
              "classroom_id": course_id,
              "course_work_id": course_work_id,
              "course_work_title": course_work_material["title"],
              "course_work_url": course_work_material["alternateLink"],
              "message": get_message(event_type,"Material")
          }

        return True,notification_message
    else:
      raise HttpError(hte.resp,hte.content,hte.uri) from hte


def save_student_submission(course_id, course_work_id,
                            submissions_id, message_id,event_type):
  """method to save student submission in bq
    and also return filltered message.

  Args:
    course_id (string): unique classroom id
    course_work_id (string): unique course work id
    submissions_id (string): unique submission id
    message_id (string): unique message id for each message.

  Returns:
    bool: based on data insertion method returns a bool.
  """
  submission = get_student_submissions(
      course_id, course_work_id, submissions_id)
  submission_details=submission.copy()
  submission["uuid"] = str(uuid.uuid4())
  submission["message_id"]=message_id
  submission["assignmentSubmission"] = convert_to_json(
      submission, "assignmentSubmission")
  submission["submissionHistory"] =convert_dict_array_to_json( submission,
                    "submissionHistory")
  submission["shortAnswerSubmission"] = convert_to_json(
      submission, "shortAnswerSubmission")
  submission["multipleChoiceSubmission"] = convert_to_json(
      submission, "multipleChoiceSubmission")
  submission["event_type"] = event_type
  submission["timestamp"] = datetime.datetime.utcnow()
  return insert_rows_to_bq(
    rows=[submission],
    dataset=BQ_DATASET,
    table_name=BQ_TABLE_DICT["BQ_COLL_SCW_TABLE"]
    ),get_student_submission_message(
      submission_details)

def get_student_submission_message(submission):
  """get student submission message for lms notification

  Args:
    submission (dict): student submission object

  Returns:
    dict|None: lms notification message
  """
  notification_message=None
  list_of_assigned_datetime = [
      datetime.datetime.strptime(
        x["gradeHistory"]["gradeTimestamp"].split(".")[0],
                        "%Y-%m-%dT%H:%M:%S")
      for x in submission["submissionHistory"] if "gradeHistory" in x.keys()
      if x["gradeHistory"]["gradeChangeType"] ==
      "ASSIGNED_GRADE_POINTS_EARNED_CHANGE"
  ]

  if (datetime.datetime.strptime(
    submission["updateTime"].split(".")[0],
      "%Y-%m-%dT%H:%M:%S") == max(list_of_assigned_datetime)):
    course_work = get_course_work(submission["courseId"],
                                  submission["courseWorkId"])
    user = get_user(submission["userId"])
    notification_message = {
        "type": "user",
        "email": user["emailAddress"],
        "name": user["name"],
        "classroom_id": submission["courseId"],
        "course_work_id": submission["courseWorkId"],
        "course_work_title": course_work["title"],
        "course_work_url": course_work["alternateLink"],
        "assigned_grade": submission["assignedGrade"],
        "gaia_id": submission["userId"],
        "role": "learner",
        "message": "Teacher graded the assignment"
    }
  return notification_message
