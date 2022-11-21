"""
  Tests for User endpoints
"""
import os
import json
import datetime
from routes import copy_course
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
# from common.testing.firestore_emulator import client_with_emulator, firestore_emulator, clean_firestore
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.testing.client_with_emulator import client_with_emulator

from common.models.section import Section
from common.models.course_template import CourseTemplate
from common.models.cohort import Cohort
import mock
from common.testing.example_objects import TEST_COHORT,TEST_COURSE_TEMPLATE


# assigning url
API_URL = "http://localhost/lms/api/v1"


os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}

def create_fake_data(course_template_id , cohort_id,section_id):
  TEST_COURSE_TEMPLATE = {
      "name": "test-name",
      "uuid":course_template_id,
      "description": "test-description",
      "admin": "test-admin@gmail.com",
      "instructional_designer": "IDesiner@gmail.com",
      "classroom_id": "fake-classroom-id",
      "classroom_code": "fake-classroom_code"
  }
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  
  TEST_COHORT = {
    "uuid":cohort_id,
    "name": "name",
    "description": "description",
    "course_template":course_template,
    "start_date": datetime.datetime(year=2022,month=10, day=14),
    "end_date": datetime.datetime(year=2022,month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022,month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022,month=11, day=14),
    "max_student": 0,
    "enrolled_student_count":0
  }
  cohort = Cohort.from_dict(TEST_COHORT)
  cohort.save()
  TEST_SECTION = {
    "uuid":"fake-section-id",
    "name" : "section_name",
    "section" : "section c",
    "description": "description",
    "classroom_id" :"cl_id",
    "classroom_code" :"cl_code",
    "course_template":course_template,
    "cohort":cohort,    
    "teachers_list":["teachera@gmail.com","teacherb@gmail.com"]
  }
  section = Section.from_dict(TEST_SECTION)
  section.save()
  return course_template , cohort,section
  

def test_get_user(client_with_emulator):
  url = API_URL + "/sections/get_courses/"
  with mock.patch("routes.copy_course.classroom_crud.get_course_list"):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200


def test_copy_course(client_with_emulator):
  url = API_URL + "/sections/copy_course/"
  course_details = {"course_id":"TEST123"}
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
      with mock.patch("routes.copy_course.classroom_crud.create_course"):
          with mock.patch("routes.copy_course.classroom_crud.get_topics"):
              with mock.patch("routes.copy_course.classroom_crud.create_topics"):
                with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
                    with mock.patch("routes.copy_course.classroom_crud.create_coursework"):
                        resp = client_with_emulator.post(url,json=course_details)
  json_response = json.loads(resp.text)
  assert resp.status_code == 200    


def test_copy_course_not_found(client_with_emulator):
  url = API_URL + "/sections/copy_course/"
  course_details = {"course_id":"TEST123"}
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id",return_value =None):
      with mock.patch("routes.copy_course.classroom_crud.create_course"):
          with mock.patch("routes.copy_course.classroom_crud.get_topics"):
              with mock.patch("routes.copy_course.classroom_crud.create_topics"):
                with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
                    with mock.patch("routes.copy_course.classroom_crud.create_coursework"):
                        resp = client_with_emulator.post(url,json=course_details)
  assert resp.status_code == 200

def test_create_section(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  url = API_URL + "/sections"
  section_details = {
  "name": "section_20",
  "description": "This is description",
  "course_template":"fake-classroom-id",
  "cohort": "fake-cohort-id",
  "teachers_list": [
    os.environ.get("CLASSROOM_ADMIN_EMAIL")
  ]
}
  mock_return_course = {
    "id":"57690009090",
    "enrollmentCode":"as3rr",
    "name":"Jhjiuiui"
  }
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
      with mock.patch("routes.copy_course.classroom_crud.create_course",return_value=mock_return_course):
          with mock.patch("routes.copy_course.classroom_crud.get_topics"):
              with mock.patch("routes.copy_course.classroom_crud.create_topics"):
                with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
                    with mock.patch("routes.copy_course.classroom_crud.create_coursework"):
                      with mock.patch("routes.copy_course.classroom_crud.add_teacher"):
                        resp = client_with_emulator.post(url,json=section_details)
  json_response = json.loads(resp.text)
  assert resp.status_code == 200   

def test_create_section_course_template_not_found(client_with_emulator):

  # create_fake_data()
  url = API_URL + "/section"
  section_details = {
  "name": "section_20",
  "description": "This is description",
  "course_template":"fake-classroom-id_new",
  "cohort": "7888888",
  "teachers_list": [
    "string"
  ]

}
  mock_return_course = {
    "id":"57690009090",
    "enrollmentCode":"as3rr",
    "name":"Jhjiuiui"
  }
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
      with mock.patch("routes.copy_course.classroom_crud.create_course",return_value=mock_return_course):
          with mock.patch("routes.copy_course.classroom_crud.get_topics"):
              with mock.patch("routes.copy_course.classroom_crud.create_topics"):
                with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
                    with mock.patch("routes.copy_course.classroom_crud.create_coursework"):
                        resp = client_with_emulator.post(url,json=section_details)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404   


  # create_fake_data()
  url = API_URL + "/sections"
  section_details = {
  "name": "section_20",
  "description": "This is description",
  "course_template":"fake-classroom-id_new",
  "cohort": "7888888",
  "teachers_list": [
    "string"
  ]

}
  mock_return_course = {
    "id":"57690009090",
    "enrollmentCode":"as3rr",
    "name":"Jhjiuiui"
  }
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
      with mock.patch("routes.copy_course.classroom_crud.create_course",return_value=mock_return_course):
          with mock.patch("routes.copy_course.classroom_crud.get_topics"):
              with mock.patch("routes.copy_course.classroom_crud.create_topics"):
                with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
                    with mock.patch("routes.copy_course.classroom_crud.create_coursework"):
                        resp = client_with_emulator.post(url,json=section_details)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404   

def test_create_section_cohort_not_found(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  url = API_URL + "/sections"
  section_details = {
  "name": "section_20",
  "description": "This is description",
  "course_template":"fake-classroom-id",
  "cohort": "fake-cohort-id-new",
  "teachers_list": [
    "string"
  ]
}
  mock_return_course = {
    "id":"57690009090",
    "enrollmentCode":"as3rr",
    "name":"Jhjiuiui"
  }
  with mock.patch("routes.copy_course.classroom_crud.get_course_by_id"):
      with mock.patch("routes.copy_course.classroom_crud.create_course",return_value=mock_return_course):
          with mock.patch("routes.copy_course.classroom_crud.get_topics"):
              with mock.patch("routes.copy_course.classroom_crud.create_topics"):
                with mock.patch("routes.copy_course.classroom_crud.get_coursework"):
                    with mock.patch("routes.copy_course.classroom_crud.create_coursework"):
                        resp = client_with_emulator.post(url,json=section_details)
  json_response = json.loads(resp.text)
  assert resp.status_code == 404  

def test_list_section_for_one_cohort(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  url = API_URL + "/sections/cohort/fake-cohort-id/sections"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200 

def test_list_section(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  url = API_URL + "/sections"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200 

def test_list_section_cohort_not_found(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  url = API_URL + "/sections/cohort/fake-cohort-id22/sections"

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  
  assert resp.status_code == 404 

def test_get_section(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  url = API_URL + f"/sections/{fake_data_result[2].uuid}"

  resp = client_with_emulator.get(url)
  json_response = resp.json()
  assert resp.status_code == 200 

def test_get_section_not_found(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  url = API_URL + f"/sections/test_case_id_does_not_exists"
  resp = client_with_emulator.get(url)
  json_response = resp.json()
  
  assert resp.status_code == 404 

def test_update_section(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  data = {
  "uuid": "fake-section-id",
  "course_id": "561822649300",
  "section_name": "tsection",
  "description": "tdescription",
  "course_state": "ACTIVEu"
}
  url = API_URL + f"/sections" 
  with mock.patch("routes.copy_course.classroom_crud.update_course"):
    resp = client_with_emulator.patch(url,json=data)
  json_response = resp.json()
  assert resp.status_code == 200 

def test_update_section_section_id_not_found(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  
  data = {
  "uuid": "fake-section-id_new",
  "course_id": "561822649300",
  "section_name": "tsection",
  "description": "tdescription",
  "course_state": "ACTIVEu"
}
  url = API_URL + f"/sections"

  with mock.patch("routes.copy_course.classroom_crud.update_course"):
    resp = client_with_emulator.patch(url,json=data)
  json_response = resp.json()
  assert resp.status_code == 404

def test_update_section_course_id_not_found(client_with_emulator):

  fake_data_result =create_fake_data("fake-classroom-id","fake-cohort-id","fake-section-id")
  data = {
  "uuid": "fake-section-id_new",
  "course_id": "561822649300",
  "section_name": "tsection",
  "description": "tdescription",
  "course_state": "ACTIVEu"
}
  url = API_URL + f"/sections"
  with mock.patch("routes.copy_course.classroom_crud.update_course",return_value=None):
    resp = client_with_emulator.patch(url,json=data)
  json_response = resp.json()
  assert resp.status_code == 404 
