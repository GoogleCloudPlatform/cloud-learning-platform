from xml.dom import NotFoundErr
import requests
from endpoint_proxy import get_baseurl
import mock
import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
# from microservices.lms.src import routes

def test_get_progress_percentage():
  base_url = get_baseurl("lms")
  if not base_url:
    raise NotFoundErr("Unable to locate the service URL for lms")
  res = requests.get(base_url + "/student/get_progress_percentage/?course_id=504551481098&student_email=saurav.minimi@gmail.com")
  result = res.json()
  assert res.status_code == 200
