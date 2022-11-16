"""
  Tests for Course Template endpoints
"""
import os
import json
import datetime

import pytest

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.testing.client_with_emulator import client_with_emulator
from common.models import CourseTemplate,Cohort
import mock

# assigning url
API_URL = "http://localhost/lms/api/v1/cohorts"
TEST_COURSE_TEMPLATE = {
    "name": "test-name",
    "description": "test-description",
    "admin": "test-admin@gmail.com",
    "instructional_designer": "IDesiner@gmail.com",
    "classroom_id": "fake-classroom_id",
    "classroom_code": "fake-classroom_code"
}
TEST_COHORT_LIST = [
    {
        "name": "name-1",
        "description": "description-1",
        "start_date": datetime.datetime(year=2022,
                                        month=10, day=14),
        "end_date": datetime.datetime(year=2022,
                                      month=12, day=25),
        "registration_start_date": datetime.datetime(year=2022,
                                                     month=10, day=20),
        "registration_end_date": datetime.datetime(year=2022,
                                                   month=11, day=14),
        "max_student": 0,
        "enrolled_student_count": 0
    },
    {
        "name": "name-2",
        "description": "description-2",
        "start_date": datetime.datetime(year=2022,
                                        month=10, day=14),
        "end_date": datetime.datetime(year=2022,
                                      month=12, day=25),
        "registration_start_date": datetime.datetime(year=2022,
                                                     month=10, day=20),
        "registration_end_date": datetime.datetime(year=2022,
                                                   month=11, day=14),
        "max_student": 0,
        "enrolled_student_count": 0
    },
    {
        "uuid": "fake-cohort-id-3",
        "name": "name-3",
        "description": "description-3",
        "start_date": datetime.datetime(year=2022,
                                        month=10, day=14),
        "end_date": datetime.datetime(year=2022,
                                      month=12, day=25),
        "registration_start_date": datetime.datetime(year=2022,
                                                     month=10, day=20),
        "registration_end_date": datetime.datetime(year=2022,
                                                   month=11, day=14),
        "max_student": 0,
        "enrolled_student_count": 0
    }
]

TEST_COHORT={
    "uuid": "fake-cohort-id",
    "name": "name",
    "description": "description",
    "start_date": datetime.datetime(year=2022,
                                    month=10, day=14),
    "end_date": datetime.datetime(year=2022,
                                  month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022,
                                                 month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022,
                                               month=11, day=14),
    "max_student": 0,
    "enrolled_student_count": 0
}
TEST_INPUT_COHORT = {
    "name": "name", 
    "description": "description", 
    "start_date": "2022-10-14T00:00:00", 
    "end_date": "2022-12-25T00:00:00",
    "registration_start_date": "2022-10-20T00:00:00",
    "registration_end_date": "2022-11-14T00:00:00",
    "max_student": 0
    }

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

@pytest.fixture
def create_course_template(client_with_emulator):
    course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
    course_template.save()
    course_template.uuid = course_template.id
    course_template.update()
    return course_template

def test_get_cohort_list(client_with_emulator,create_course_template):
    
    for i in TEST_COHORT_LIST:
        cohort = Cohort.from_dict(i)
        cohort.course_template=create_course_template
        cohort.save()
        cohort.uuid = cohort.id
        cohort.update()
    data = {
        "success": True,
        "message": "Successfully get the Cohort list"
    }
    # mock logger
    with mock.patch("routes.cohort.Logger"):
        response = client_with_emulator.get(API_URL)
    response_json = response.json()
    assert response.status_code == 200, "Status 200"
    assert len(response_json["cohort_list"]) == len(
        TEST_COHORT_LIST), "Return data list len doesn't match."
    response_json.pop("cohort_list")
    assert response_json == data, "Return data doesn't match."


def test_get_cohort(client_with_emulator, create_course_template):
    cohort = Cohort.from_dict(TEST_COHORT)
    cohort.course_template = create_course_template
    cohort.save()
    cohort.uuid = cohort.id
    cohort.update()

    url = API_URL+f'/{cohort.uuid}'
    data = TEST_COHORT
    data["uuid"] = cohort.uuid
    data["course_template"]=create_course_template.key
    with mock.patch("routes.cohort.Logger"):
        response = client_with_emulator.get(url)
    response_cohort = json.loads(response.text)
    response_cohort["start_date"] = datetime.datetime.strptime(response_cohort.pop("start_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
    response_cohort["end_date"] = datetime.datetime.strptime(response_cohort.pop("end_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
    response_cohort["registration_start_date"] = datetime.datetime.strptime(
        response_cohort.pop("registration_start_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
    response_cohort["registration_end_date"] = datetime.datetime.strptime(
        response_cohort.pop("registration_end_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
    assert response.status_code == 200, "Status 200"
    assert response_cohort == data, "Return data doesn't match."


def test_create_course_template(client_with_emulator, create_course_template):
    TEST_INPUT_COHORT[ "course_template_uuid"]=create_course_template.uuid
    with mock.patch("routes.cohort.Logger"):
        response = client_with_emulator.post(
            API_URL, json=TEST_INPUT_COHORT)
    response_json = json.loads(response.text)
    assert response.status_code == 200, "Status 200"
    assert response_json["success"] == True, "Response Success"
    assert response_json["cohort"]["name"] == TEST_INPUT_COHORT["name"], "Check the response cohort name"
    assert response_json["cohort"]["course_template"] == create_course_template.key, "Check the response cohort name"


def test_get_nonexist_cohort(client_with_emulator):
    uuid = "non_exist_uuid"
    url = API_URL + f"/{uuid}"
    data = {
        "success": False,
        "message": f"Cohort with uuid {uuid} is not found",
        "data": None
    }
    with mock.patch("routes.cohort.Logger"):
        response = client_with_emulator.get(url)
    assert response.status_code == 404, "Status 404"
    assert response.json() == data, "Return data doesn't match."

def test_delete_cohort(client_with_emulator,create_course_template):
    cohort = Cohort.from_dict(TEST_COHORT)
    cohort.course_template = create_course_template
    cohort.save()
    cohort.uuid = cohort.id
    cohort.update()

    uuid = cohort.uuid
    url = API_URL+f'/{uuid}'
    data = {
        "success": True,
        "message": f"Successfully deleted the Cohort with uuid {uuid}",
        "data": None
    }
    with mock.patch("routes.cohort.Logger"):
        response = client_with_emulator.delete(url)
    response_cohort = response.json()
    assert response.status_code == 200, "Status 200"
    assert response_cohort == data, "Return data doesn't match."


def test_delete_nonexist_cohort(client_with_emulator):
    uuid = "non_exist_uuid"
    url = API_URL + f"/{uuid}"
    data = {
        "success": False,
        "message": f"Cohort with uuid {uuid} is not found",
        "data": None
    }
    with mock.patch("routes.cohort.Logger"):
        response = client_with_emulator.delete(url)
    assert response.status_code == 404, "Status 404"
    assert response.json() == data, "Return data doesn't match."
