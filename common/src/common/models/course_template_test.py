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
Unit test for course_template.py
"""
# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-import
# pylint: disable=unused-argument,redefined-outer-name
from common.models import CourseTemplate
from common.testing.example_objects import TEST_COURSE_TEMPLATE
from common.testing.firestore_emulator import  firestore_emulator, clean_firestore


def test_new_course(clean_firestore):
  """Test for creating and loading a new course"""
  new_course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  new_course_template.save()
  new_course_template.uuid = new_course_template.id
  new_course_template.update()
  course_template=CourseTemplate.find_by_uuid(new_course_template.uuid)
  assert course_template.name==TEST_COURSE_TEMPLATE["name"]
  assert course_template.description == TEST_COURSE_TEMPLATE["description"]

def test_delete_course_template(clean_firestore):
  '''test for soft delete method'''
  new_course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  new_course_template.save()
  new_course_template.uuid = new_course_template.id
  new_course_template.update()
  assert CourseTemplate.archive_by_uuid(
      "fakeuuid") is False, "Course Template not found"
  assert CourseTemplate.archive_by_uuid(
      new_course_template.uuid) is True, "Course Template successfully deleted"
