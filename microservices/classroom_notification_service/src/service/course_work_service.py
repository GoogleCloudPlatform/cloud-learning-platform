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
from helper.bq_helper import insert_rows_to_bq
# from helper.classroom_helper import
from config import BQ_LOG_CW_TABLE


def save_course_work(data):
  rows = [{"message_id": data["message_id"], "collection": data[
      "collection"],
      "event_type":data["eventType"], "resource":json.dumps(
      data["resourceId"]), "timestamp":datetime.datetime.utcnow()}]
  return insert_rows_to_bq(
      rows=rows, table_name=BQ_LOG_CW_TABLE)
