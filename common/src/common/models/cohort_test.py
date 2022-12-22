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

'''
Unit test for cohort.py
'''
# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-import
# pylint: disable=unused-argument,redefined-outer-name
import pytest
from common.models import Cohort, CourseTemplate
from common.utils.errors import ResourceNotFoundException
from common.testing.example_objects import TEST_COHORT,TEST_COURSE_TEMPLATE
from common.testing.firestore_emulator import  firestore_emulator, clean_firestore


def test_new_cohort(clean_firestore):
  """Test for creating and loading of a new cohort"""
  new_cohort = Cohort.from_dict(TEST_COHORT)
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  new_cohort.course_template=course_template
  new_cohort.save()
  cohort=Cohort.find_by_id(new_cohort.id)
  assert cohort.name == TEST_COHORT["name"]
  assert cohort.max_students == TEST_COHORT["max_students"]


def test_delete_cohort(clean_firestore):
  '''test for soft delete method'''
  new_cohort = Cohort.from_dict(TEST_COHORT)
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  new_cohort.course_template = course_template
  new_cohort.save()
  assert Cohort.find_by_id(new_cohort.id) is not None
  Cohort.soft_delete_by_id(new_cohort.id)
  with pytest.raises(ResourceNotFoundException):
    Cohort.soft_delete_by_id(new_cohort.id)
  