import requests
from testing_objects.test_config import API_URL
from testing_objects.token_fixture import get_token


def test_get_progress_percentage(get_token):
  res = requests.get(
      API_URL +
      "/student/get_progress_percentage/?course_id=504551481098&student_email=test_user_1@dhodun.altostrat.com",headers=get_token
  )
  result = res.json()
  assert res.status_code == 200
