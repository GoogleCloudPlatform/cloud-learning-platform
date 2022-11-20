import requests
from endpoint_proxy import get_baseurl
from common.utils.errors import ResourceNotFoundException

def test_get_progress_percentage():
  base_url = get_baseurl("lms")
  if not base_url:
    raise ResourceNotFoundException("Unable to locate the service URL for lms")
  res = requests.get(base_url + "/student/get_progress_percentage/?course_id=504551481098&student_email=test_user_1@dhodun.altostrat.com")
  result = res.json()
  assert res.status_code == 200
