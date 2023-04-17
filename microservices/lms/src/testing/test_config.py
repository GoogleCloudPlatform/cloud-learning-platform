"""Test config File"""
import datetime

BASE_URL = "http://localhost/lms/api/v1"

# TEST DATA
COURSE_TEMPLATE_LIST_TEST_DATA = [{
    "name":
    "test-name_1",
    "description":
    "test-description_1",
    "admin":
    "test-admin_1@gmail.com",
    "instructional_designer":
    "IDesiner_1@gmail.com",
    "classroom_id":
    "fake-classroom_id_1",
    "classroom_code":
    "fake-classroom_code_1",
    "classroom_url":
    "https://classroom.google.com/1"
}, {
    "name":
    "test-name_2",
    "description":
    "test-description_2",
    "admin":
    "test-admin_2@gmail.com",
    "instructional_designer":
    "IDesiner_2@gmail.com",
    "classroom_id":
    "fake-classroom_id_2",
    "classroom_code":
    "fake-classroom_code_2",
    "classroom_url":
    "https://classroom.google.com/2"
}, {
    "name":
    "test-name_3",
    "description":
    "test-description_3",
    "admin":
    "test-admin@gmail.com_3",
    "instructional_designer":
    "IDesiner_3@gmail.com",
    "classroom_id":
    "fake-classroom_id_3",
    "classroom_code":
    "fake-classroom_code_3",
    "classroom_url":
    "https://classroom.google.com/3"
}]

COHORT_LIST_TEST_DATA = [{
    "name":
    "name-1",
    "description":
    "description-1",
    "start_date":
    datetime.datetime(year=2022, month=10, day=14),
    "end_date":
    datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date":
    datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date":
    datetime.datetime(year=2022, month=11, day=14),
    "max_students":
    100,
    "enrolled_students_count":
    0
}, {
    "name":
    "name-2",
    "description":
    "description-2",
    "start_date":
    datetime.datetime(year=2022, month=10, day=14),
    "end_date":
    datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date":
    datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date":
    datetime.datetime(year=2022, month=11, day=14),
    "max_students":
    100,
    "enrolled_students_count":
    0
}, {
    "name":
    "name-3",
    "description":
    "description-3",
    "start_date":
    datetime.datetime(year=2022, month=10, day=14),
    "end_date":
    datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date":
    datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date":
    datetime.datetime(year=2022, month=11, day=14),
    "max_students":
    100,
    "enrolled_students_count":
    0
}]

INPUT_COHORT_TEST_DATA = {
    "name": "name",
    "description": "description",
    "start_date": "2022-10-14T00:00:00",
    "end_date": "2022-12-25T00:00:00",
    "registration_start_date": "2022-10-20T00:00:00",
    "registration_end_date": "2022-11-14T00:00:00",
    "max_students": 100
}
GET_COURSEWORK_DATA = {
  "courseId": "604063268646",
  "id": "553046445746",
  "title": "youtube coursewok",
  "materials": [
    {
      "youtubeVideo": {
        "id": "pl-tBjAM9g4",
        "title": "How to Use Google Classroom - Tutorial for Beginners",
        "alternateLink": "https://www.youtube.com/watch?v=pl-tBjAM9g4",
        "thumbnailUrl": "https://i.ytimg.com/vi/pl-tBjAM9g4/default.jpg"
      }
    },
    {
      "form": {
        "formUrl": "https://docs.google.com/forms/d/e/1FAIpQL",
        "title": "e2e_form1",
        "thumbnailUrl": "https://lh6.googleusercontent.com/E7m"
      }
    }
  ],
  "state": "PUBLISHED"}

FORM_RESPONSE_LIST = {"responses":
    [{"respondentEmail":"clplmstestuser1@gmail.com","totalScore":5}]
    }

LIST_COURSEWORK_SUBMISSION_USER=[{"state":"TURNED_IN",
                                  "courseWorkId":"553046445746",
                                  "courseId":"604063268646",
                                  "userId":"107386744676889596754",
                                  "id":"Cg4IubuS9uwQELKdjKGMEA",
                                  "courseWorkType":"ASSIGNMENT"}]

EDIT_VIEW_URL_FILE_ID_MAPPING_FORM ={
    "https://docs.google.com/forms/d/e/1FAIpQL":
    {"file_id":"test123",
    "webViewLink":"https://docs.google.com/forms/d/e/1FAIpQL/edit"}}
