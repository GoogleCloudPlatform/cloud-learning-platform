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
import uuid
from common.utils.logging_handler import Logger
from common.utils.bq_helper import insert_rows_to_bq
from helper.classroom_helper import get_user,get_course_by_id
from helper.json_helper import convert_dict_array_to_json
from googleapiclient.errors import HttpError
from config import BQ_TABLE_DICT,BQ_DATASET
# disabling for linting to pass
# pylint: disable = broad-except
role_dict={
  "students":"learner",
  "teachers":"faculty"
  }
def save_roster(data):
  """_summary_

  Args:
      data (_type_): _description_

  Returns:
      bool: _description_
  """
  try:
    rows = [{
      "message_id": data["message_id"], "collection": data["collection"],
      "event_type":data["eventType"], "resource":data["resourceId"],
      "publish_time":data["publish_time"],"timestamp":datetime.datetime.utcnow()
    }]
    log_flag = insert_rows_to_bq(rows=rows,
                                 dataset=BQ_DATASET,
                                 table_name=BQ_TABLE_DICT["BQ_LOG_RS_TABLE"])
    if data["eventType"] == "DELETED":
      return log_flag,None
    user_flag,notification_message=save_user(
        data["resourceId"]["userId"],
        data["resourceId"]["courseId"],
        data["message_id"],data["eventType"],
        data["collection"])
    return (log_flag & user_flag),notification_message
  except HttpError as ae:
    Logger.error(ae)
    return False,None
  except Exception as e:
    Logger.error(e)
    return False,None

def save_user(user_id,course_id,message_id,event_type,collection):
  """_summary_

  Args:
      user_id (_type_): _description_
      course_id (_type_): _description_
      message_id (_type_): _description_
      event_type (_type_): _description_
      collection (_type_): _description_

  Returns:
      _type_: _description_
  """
  user=get_user(user_id)
  notification_message=None
  if event_type == "CREATED":
    course=get_course_by_id(course_id)
    notification_message = {
        "type": "user",
        "email": user["emailAddress"],
        "name": user["name"],
        "gaia_id": user_id,
        "role": role_dict[collection.split(".")[1]],
        "classroom_id": course_id,
        "classroom_url":course["alternateLink"],
        "message": ("User is successfully enrolled in classroom "
                    + f"{course['name']}")
        }
  user["uuid"]=str(uuid.uuid4())
  user["message_id"]=message_id
  user["timestamp"] = datetime.datetime.utcnow()
  user["event_type"]=event_type
  user["permissions"] = convert_dict_array_to_json(user, "permissions")
  return insert_rows_to_bq(
    rows=[user],
    dataset=BQ_DATASET,
    table_name=BQ_TABLE_DICT["BQ_COLL_USER_TABLE"]),notification_message
