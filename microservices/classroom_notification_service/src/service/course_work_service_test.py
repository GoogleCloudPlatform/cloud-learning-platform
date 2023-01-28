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
from service.course_work_service import save_course_work


def test_save_course_work_collection():
  data = {
      "message_id": "90000003344",
      "collection": "courses.courseWork",
      "eventType": "CREATED",
      "publish_time": "2014-10-02T15:01:23Z",
      "resourceId": {
          "id": "12345678900",
          "courseId": "550005555"
      }}
  with mock.patch("service.course_work_service.save_course_work_collection",
                  return_value=True):
    with mock.patch("service.course_work_service.insert_rows_to_bq",
                    return_value=True):
      result = save_course_work(data)
  assert result is True


def test_save_course_work_collection_negative():
  data = {
      "message_id": "90000003344",
      "collection": "courses.courseWork",
      "eventType": "CREATED",
      "publish_time": "2014-10-02T15:01:23Z",
      "resourceId": {
          "id": "12345678900",
          "courseId": "550005555"
      }}
  with mock.patch("service.course_work_service.save_course_work_collection",
                  return_value=False):
    with mock.patch("service.course_work_service.insert_rows_to_bq",
                    return_value=True):
      result_1 = save_course_work(data)
  with mock.patch("service.course_work_service.save_course_work_collection",
                  return_value=True):
    with mock.patch("service.course_work_service.insert_rows_to_bq",
                    return_value=False):
      result_2 = save_course_work(data)

  assert result_1 is False
  assert result_2 is False


def test_save_student_submission_collection():
  data = {
      "message_id": "90000003344",
      "collection": "courses.courseWork.studentSubmissions",
      "eventType": "CREATED",
      "publish_time": "2014-10-02T15:01:23Z",
      "resourceId": {
          "id": "AC56Vg722HC9U",
          "courseWorkId": "12345678900",
          "courseId": "550005555"
      }}
  with mock.patch("service.course_work_service.insert_rows_to_bq",
                  return_value=True):
    with mock.patch("service.course_work_service.save_student_submission",
                    return_value=True):
      result = save_course_work(data)
  assert result is True


def test_save_student_submission_collection_negative():
  data = {
      "message_id": "90000003344",
      "collection": "courses.courseWork.studentSubmissions",
      "eventType": "CREATED",
      "publish_time": "2014-10-02T15:01:23Z",
      "resourceId": {
          "id": "AC56Vg722HC9U",
          "courseWorkId": "12345678900",
          "courseId": "550005555"
      }}
  with mock.patch("service.course_work_service.save_student_submission",
                  return_value=False):
    with mock.patch("service.course_work_service.insert_rows_to_bq",
                    return_value=True):
      result_1 = save_course_work(data)
  with mock.patch("service.course_work_service.save_student_submission",
                  return_value=True):
    with mock.patch("service.course_work_service.insert_rows_to_bq",
                    return_value=False):
      result_2 = save_course_work(data)

  assert result_1 is False
  assert result_2 is False
