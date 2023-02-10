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
from helper.bq_helper import insert_rows_to_bq
from helper.classroom_helper import get_user
from googleapiclient.errors import HttpError
from config import BQ_TABLE_DICT
# disabling for linting to pass
# pylint: disable = broad-except
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
    return insert_rows_to_bq(
        rows=rows, table_name=BQ_TABLE_DICT["BQ_LOG_RS_TABLE"]) & save_user(
        data["resourceId"]["userId"], data["message_id"], data["eventType"])
  except HttpError as ae:
    Logger.error(ae)
    return False
  except Exception as e:
    Logger.error(e)
    return False

def save_user(user_id,message_id,event_type):
  user=get_user(user_id)
  user["uuid"]=str(uuid.uuid4())
  user["message_id"]=message_id
  user["timestamp"] = datetime.datetime.utcnow()
  user["event_type"]=event_type
  return insert_rows_to_bq(rows=[user],
                           table_name=BQ_TABLE_DICT["BQ_COLL_USER_TABLE"])
