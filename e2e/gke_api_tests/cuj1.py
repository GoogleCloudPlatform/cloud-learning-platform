from xml.dom import NotFoundErr
import requests
from endpoint_proxy import get_baseurl
import mock
import os
# from microservices.lms.src import routes

def test_get_course_list():
  base_url = get_baseurl("lms")
  if not base_url:
    raise NotFoundErr("Unable to locate the service URL for lms")
  print("*****************************************",base_url+"/lms/api/v1/course/get_courses/")
#   print(base_url)
#   with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
  res = requests.get(base_url + "/lms/api/v1/course/get_courses/")

  result = res.json()
  assert type(result["result"]) == list
  assert res.status_code == 200

def test_create_course():
  base_url = get_baseurl("lms")
  if not base_url:
    raise NotFoundErr("Unable to locate the service URL for lms")
  print("********************SECRET KEY*********************", os.environ.get("GKE_POD_SA_KEY"))

#   print(base_url)
#   with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
  res = requests.post(base_url + "/lms/api/v1/course/create_course/")
  result = res.json()
  print(res.json)

  assert res.status_code == 200