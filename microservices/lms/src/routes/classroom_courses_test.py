"""
  Tests for Classroom Courses endpoints
"""
import os
import mock
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from testing.test_config import BASE_URL
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"
SUCCESS_RESPONSE = {"status": "Success"}

course_dict={
  "id": "456789",
  "name": "course_name",
  "section": "section",
  "description": "desc",
  "ownerId": "1234567888887654",
  "creationTime": "2023-04-20T10:44:05.896Z",
  "updateTime": "2023-04-20T10:44:05.896Z",
  "enrollmentCode": "ry7ui2z",
  "courseState": "ACTIVE",
  "alternateLink": "https://classroom.google.com/c/xcvbn",
  "teacherGroupEmail": "course_name_section_teachers_678fg@google.com",
  "courseGroupEmail": "course_name_section_hj678@google.com",
  "teacherFolder": {
    "id": "234567xdcfgyhu345678",
    "title": "course name section",
    "alternateLink":
      "https://drive.google.com/drive/folders/234567xdcfgyhu345678"
  },
  "guardiansEnabled": False,
  "calendarId": "dfghj56789@group.calendar.google.com",
  "gradebookSettings": {
    "calculationType": "TOTAL_POINTS",
    "displaySetting": "HIDE_OVERALL_GRADE"
  }
}

def test_get_courses(client_with_emulator):
  url = BASE_URL + "/classroom_courses"
  with mock.patch("routes.classroom_courses.classroom_crud.get_course_list",
                  return_value=[course_dict]):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200

def test_get_course(client_with_emulator):
  url = BASE_URL + f"/classroom_courses/{course_dict['id']}"
  with mock.patch("routes.classroom_courses.classroom_crud.get_course_by_id",
                  return_value=course_dict):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 200, "Status 200"
  assert resp.json()["data"]["name"]==course_dict["name"], "check data"
  assert resp.json()["data"]["owner_id"]==course_dict["ownerId"],"check data"

def test_negative_get_course(client_with_emulator):
  url = BASE_URL + "/classroom_courses/12345678"
  with mock.patch("routes.classroom_courses.classroom_crud.get_course_by_id",
                  return_value=None):
    resp = client_with_emulator.get(url)
  assert resp.status_code == 404,"Status 404"

def test_copy_course(client_with_emulator):
  url = BASE_URL + "/classroom_courses/copy_course"
  course_details = {"course_id": "TEST123"}
  with mock.patch("routes.classroom_courses.classroom_crud.get_course_by_id"):
    with mock.patch("routes.classroom_courses.classroom_crud.create_course"):
      with mock.patch("routes.classroom_courses.classroom_crud.get_topics"):
        with mock.patch(
          "routes.classroom_courses.classroom_crud.create_topics"):
          with mock.patch(
            "routes.classroom_courses.classroom_crud.get_coursework_list"):
            with mock.patch(
              "routes.classroom_courses.classroom_crud.create_coursework"):
              with mock.patch(
              "routes.classroom_courses.classroom_crud.get_coursework_material_list"
              ):
                with mock.patch(
            "routes.classroom_courses.classroom_crud.create_coursework_material"
                ):
                  with mock.patch(
              "routes.classroom_courses.classroom_crud.drive_copy"):
                    with mock.patch(
              "routes.classroom_courses.classroom_crud.copy_material"):
                      resp = client_with_emulator.post(url, json=course_details)
  assert resp.status_code == 200


def test_copy_course_not_found(client_with_emulator):
  url = BASE_URL + "/classroom_courses/copy_course"
  course_details = {"course_id": "TEST123"}
  with mock.patch("routes.classroom_courses.classroom_crud.get_course_by_id",
                  return_value=None):
    with mock.patch("routes.classroom_courses.classroom_crud.create_course"):
      with mock.patch("routes.classroom_courses.classroom_crud.get_topics"):
        with mock.patch(
          "routes.classroom_courses.classroom_crud.create_topics"):
          with mock.patch(
            "routes.classroom_courses.classroom_crud.get_coursework_list"):
            with mock.patch(
              "routes.classroom_courses.classroom_crud.create_coursework"):
              with mock.patch(
            "routes.classroom_courses.classroom_crud.create_coursework_material"
            ):
                with mock.patch(
              "routes.classroom_courses.classroom_crud.get_coursework_material_list"
                  ):
                  with mock.patch(
              "routes.classroom_courses.classroom_crud.drive_copy"):
                    with mock.patch(
              "routes.classroom_courses.classroom_crud.copy_material"):
                      resp = client_with_emulator.post(url, json=course_details)
  assert resp.status_code == 200


def test_enable_notifications_using_course_id(client_with_emulator):
  course_id = "57690009090"
  url = f"{BASE_URL}/classroom_courses/{course_id}/enable_notifications"
  data = {
      "success": True,
      "message":
      "Successfully enable the notifications of the course using " +
      f"{course_id} id",
      "data": {
          "registrationId": "2345667",
          "feed": {
              "feedType": "COURSE_ROSTER_CHANGES",
              "courseRosterChangesInfo": {
                  "courseId": course_id
              }
          },
          "expiryTime": "20xx-0x-x0T1x:xx:0x.x1xZ"
      }
  }
  with mock.patch(
    "routes.classroom_courses.classroom_crud.enable_notifications",
              return_value=data["data"]):
    with mock.patch("routes.classroom_courses.Logger"):
      resp = client_with_emulator.post(url)
  assert resp.status_code == 200, "Status 200"
  assert resp.json()["success"] is True, "Data doesn't Match"
  assert resp.json()["data"][0] == data["data"], "Data doesn't Match"
