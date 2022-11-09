"""
Unit test for course_template.py
"""
# pylint: disable=unused-import
from common.models import CourseTemplate
from common.testing.example_objects import TEST_COURSE_TEMPLATE
from common.testing.firestore_emulator import client_with_emulator, firestore_emulator, clean_firestore


def test_new_course(client_with_emulator):
  """Test for creating and loading a new course"""
  new_course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  new_course_template.save()
  new_course_template.uuid = new_course_template.id
  new_course_template.update()
  course_template=CourseTemplate.find_by_uuid(new_course_template.uuid)
  assert course_template.name==TEST_COURSE_TEMPLATE["name"]
  assert course_template.description == TEST_COURSE_TEMPLATE["description"]
  

def test_delete_course_template(client_with_emulator):
  '''test for soft delete method'''
  new_course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  new_course_template.save()
  new_course_template.uuid = new_course_template.id
  new_course_template.update()
  assert CourseTemplate.archive_by_uuid(
      "fakeuuid") is False, "Course Template not found"
  assert CourseTemplate.archive_by_uuid(
      new_course_template.uuid) is True, "Course Template successfully deleted"
