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
Roster Service Unit Test
"""
import mock
from service.roster_service import save_roster
def test_save_roster():
  data = {
      "message_id": "90000003344",
      "collection": "courses.teachers",
      "eventType": "CREATED",
      "resourceId": {
          "userId": "12345678900",
          "courseId": "550005555"
      }}
  with mock.patch("service.roster_service.save_user",return_value=True):
    with mock.patch("service.roster_service.insert_rows_to_bq",
                    return_value=True):
      result=save_roster(data)
  assert result is True

def test_save_roster_negative():
  data = {
      "message_id": "90000003344",
      "collection": "courses.teachers",
      "eventType": "CREATED",
      "resourceId": {
          "userId": "12345678900",
          "courseId": "550005555"
      }}
  with mock.patch("service.roster_service.save_user", return_value=False):
    with mock.patch("service.roster_service.insert_rows_to_bq",
                    return_value=True):
      result_1 = save_roster(data)
  with mock.patch("service.roster_service.save_user", return_value=True):
    with mock.patch("service.roster_service.insert_rows_to_bq",
                    return_value=False):
      result_2 = save_roster(data)

  assert result_1 is False
  assert result_2 is False
