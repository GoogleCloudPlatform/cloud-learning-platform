"""
Unit test for course_template.py
"""
from common.models import CourseTemplate
from common.testing.example_objects import TEST_COURSE

def test_new_course():
  """Test for creating and loading a new course"""
  course = CourseTemplate.from_dict(TEST_COURSE)
  # course.save()
  assert course.name==TEST_COURSE["name"]
