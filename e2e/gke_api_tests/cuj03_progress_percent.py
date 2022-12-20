from testing_objects.test_config import API_URL
from testing_objects.session_fixture import get_session,user_login


def test_get_progress_percentage(get_session):
  res = get_session.get(
      API_URL +
      "/student/get_progress_percentage/?course_id=504551481098&student_email=test_user_1@dhodun.altostrat.com"
  )
  result = res.json()
  assert res.status_code == 200
