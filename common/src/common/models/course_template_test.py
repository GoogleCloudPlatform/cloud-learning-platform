from common.models import CourseTemplate
from common.testing.example_objects import TEST_COURSE

def test_new_course():
  # a placeholder unit test so github actions runs until we add more
  course = CourseTemplate.from_dict(TEST_COURSE)
  # course.save()
  assert course.course_name==TEST_COURSE["course_name"]