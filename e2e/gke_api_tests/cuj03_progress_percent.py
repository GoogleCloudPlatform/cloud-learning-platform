from testing_objects.test_config import API_URL
from testing_objects.login_fixture import user_login_fixture
from setup import get_method


def test_get_progress_percentage():
  res = get_method(
      API_URL +
      "/student/get_progress_percentage/?course_id=504551481098&student_email=test_user_1@dhodun.altostrat.com"
  )
  result = res.json()
  assert res.status_code == 200
