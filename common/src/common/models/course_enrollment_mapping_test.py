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
Unit test for section.py
"""
# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-import
# pylint: disable=unused-argument,redefined-outer-name
import pytest
from common.models import Section, CourseTemplate, Cohort,CourseEnrollmentMapping
from common.utils.errors import ResourceNotFoundException
from common.testing.example_objects import TEST_SECTION, TEST_COURSE_TEMPLATE, TEST_COHORT
from common.testing.firestore_emulator import clean_firestore, firestore_emulator


def test_course_enrollment(clean_firestore):
  '''test for creating and loading a new section'''
  new_section = Section.from_dict(TEST_SECTION)
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  cohort = Cohort.from_dict(TEST_COHORT)
  cohort.course_template = course_template
  cohort.save()
  new_section.course_template = course_template
  new_section.cohort = cohort
  new_section.save()
  section = Section.find_by_id(new_section.id)
  course_enrollment = CourseEnrollmentMapping()
  course_enrollment.section = section
  course_enrollment.user ="test_user_id"
  course_enrollment.save()
  course_enrollment = CourseEnrollmentMapping.find_by_user("test_user_id")
  assert course_enrollment.user == "test_user_id"

