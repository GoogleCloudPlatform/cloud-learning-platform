"""
  Tests for Course Template endpoints
"""
import os
import json
import datetime

# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import

from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from common.testing.client_with_emulator import client_with_emulator
from common.models import CourseTemplate
import mock

# assigning url
API_URL = "http://localhost/lms/api/v1/course_templates"
TEST_COURSE_TEMPLATE = {
    "name": "test-name",
    "description": "test-description",
    "admin": "test-admin@gmail.com",
    "instructional_designer": "IDesiner@gmail.com",
    "classroom_id": "fake-classroom_id",
    "classroom_code": "fake-classroom_code"
}
TEST_COURSE_TEMPLATE_LIST = [
    {
        "uuid": "",
        "name": "test-name_1",
        "description": "test-description_1",
        "admin": "test-admin_1@gmail.com",
        "instructional_designer": "IDesiner_1@gmail.com",
        "classroom_id": "fake-classroom_id_1",
        "classroom_code": "fake-classroom_code_1"
    },
    {
        "uuid": "",
        "name": "test-name_2",
        "description": "test-description_2",
        "admin": "test-admin_2@gmail.com",
        "instructional_designer": "IDesiner_2@gmail.com",
        "classroom_id": "fake-classroom_id_2",
        "classroom_code": "fake-classroom_code_2"
    },
    {
        "uuid": "",
        "name": "test-name_3",
        "description": "test-description_3",
        "admin": "test-admin@gmail.com_3",
        "instructional_designer": "IDesiner_3@gmail.com",
        "classroom_id": "fake-classroom_id_3",
        "classroom_code": "fake-classroom_code_3"
    }
]
TEST_INPUT_COURSE_TEMPLATE = {
    "name": "test-name",
    "description": "test-description",
    "admin": "test-admin@gmail.com",
    "instructional_designer": "IDesiner@gmail.com"
}

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_get_course_template_list(client_with_emulator):
    for i in TEST_COURSE_TEMPLATE_LIST:
        course_template = CourseTemplate.from_dict(i)
        course_template.save()
        course_template.uuid = course_template.id
        course_template.update()
    url = API_URL+'/list'
    data = {
        "success": True,
        "message": "Successfully get the course template list"
    }
    # mock logger
    with mock.patch("routes.course_template.Logger"):
        response = client_with_emulator.get(url)
    response_json = response.json()
    assert response.status_code == 200, "Status 200"
    assert len(response_json["course_template_list"]) == len(
        TEST_COURSE_TEMPLATE_LIST), "Return data list len doesn't match."
    response_json.pop("course_template_list")
    assert response_json == data, "Return data doesn't match."

def test_get_course_template(client_with_emulator):
    course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
    course_template.save()
    course_template.uuid = course_template.id
    course_template.update()

    url = API_URL+f'/{course_template.uuid}'
    data = TEST_COURSE_TEMPLATE
    data["uuid"] = course_template.uuid
    with mock.patch("routes.course_template.Logger"):
        response = client_with_emulator.get(url)
    response_course_template = response.json()
    assert response.status_code == 200, "Status 200"
    assert response_course_template == data, "Return data doesn't match."


def test_create_course_template(client_with_emulator):
    with mock.patch("routes.course_template.Logger"):
        with mock.patch("routes.course_template.classroom_crud.create_course", return_value={"id": "classroom_id", "enrollmentCode": "classroomcode"}):
            with mock.patch("routes.course_template.classroom_crud.add_teacher"):
                response = client_with_emulator.post(
                    API_URL, json=TEST_INPUT_COURSE_TEMPLATE)
    response_json = response.json()
    assert response.status_code == 200, "Status 200"
    assert response_json["success"] == True, "Response Success"
    assert response_json["course_template"]["name"] == TEST_INPUT_COURSE_TEMPLATE["name"], "Check the response course template name"


def test_get_nonexist_course_template(client_with_emulator):
    uuid = "non_exist_uuid"
    url = API_URL + f"/{uuid}"
    data = {
        "success": False,
        "message": f"Course Template with uuid {uuid} is not found",
        "data": None
    }
    with mock.patch("routes.course_template.Logger"):
        response = client_with_emulator.get(url)
    assert response.status_code == 404, "Status 404"
    assert response.json() == data, "Return data doesn't match."

def test_delete_course_template(client_with_emulator):
    course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
    course_template.save()
    course_template.uuid = course_template.id
    course_template.update()

    uuid = course_template.uuid
    url = API_URL+f'/{uuid}'
    data = {
        "success": True,
        "message": f"Successfully deleted the course template with uuid {uuid}",
        "data": None
    }
    with mock.patch("routes.course_template.Logger"):
        response = client_with_emulator.delete(url)
    response_course_template = response.json()
    assert response.status_code == 200, "Status 200"
    assert response_course_template == data, "Return data doesn't match."


def test_delete_nonexist_course_template(client_with_emulator):
    uuid = "non_exist_uuid"
    url = API_URL + f"/{uuid}"
    data = {
        "success": False,
        "message": f"Course Template with uuid {uuid} is not found",
        "data": None
    }
    with mock.patch("routes.course_template.Logger"):
        response = client_with_emulator.delete(url)
    assert response.status_code == 404, "Status 404"
    assert response.json() == data, "Return data doesn't match."
