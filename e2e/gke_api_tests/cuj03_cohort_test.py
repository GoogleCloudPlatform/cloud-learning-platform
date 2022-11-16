"""Course template list and Course template CRUD API e2e tests"""
import datetime
from secrets_helper import get_required_emails_from_secret_manager
from xml.dom import NotFoundErr
import os
import pytest
import requests
import uuid
from endpoint_proxy import get_baseurl
from common.models import Cohort, CourseTemplate
from common.testing.example_objects import TEST_COHORT
from common.utils.errors import ResourceNotFoundException
DATABASE_PREFIX = os.environ.get("DATABASE_PREFIX")



course_template_uuid=None
@pytest.fixture(scope="session",autouse=True)
def create_course_template():
    "create a course template for reference"
    emails = get_required_emails_from_secret_manager()
    input_data = {
        "name": DATABASE_PREFIX+"test_course"+str(uuid.uuid4),
        "description": "Study Hall Test Course for Development purpose",
        "topic": "e2e test",
        "admin": emails["admin"],
        "instructional_designer": emails["instructional_designer"]
    }
    base_url = get_baseurl("lms")
    if not base_url:
        raise NotFoundErr("Unable to locate the service URL for lms")
    else:
        url = base_url + f"/lms/api/v1/course_templates"
        resp = requests.post(
            url=url, json=input_data)
        global course_template_uuid
        course_template_uuid = resp.json()["course_template"]["uuid"]


@pytest.fixture
def setup_cohort():
    """Fixture to create temprory data"""
    cohort = Cohort.from_dict(TEST_COHORT)
    course_template=CourseTemplate.find_by_uuid(course_template_uuid)
    cohort.course_template=course_template
    cohort.save()
    cohort.uuid = cohort.id
    cohort.update()
    return cohort




def test_create_cohort():
    """ 
    CUJ01 create a Cohort by providing a valid json object
    as a input using that json object creating a Cohort Model object using Third party tool.
    And also finding Course template object.
    Which is required for saving Cohort object in database.
    """
    base_url = get_baseurl("lms")
    if not base_url:
        raise ResourceNotFoundException(
            "Unable to locate the service URL for lms")
    else:
        url = base_url + f"/lms/api/v1/cohorts"
        input_data = {
            "name": DATABASE_PREFIX+"test_cohort"+str(uuid.uuid4),
            "description": "Study Hall Test Cohort for Development purpose",
            "start_date": "2022-10-14T00:00:00",
            "end_date": "2022-12-25T00:00:00",
            "registration_start_date": "2022-10-20T00:00:00",
            "registration_end_date": "2022-11-14T00:00:00",
            "max_student": 5000,
            "course_template_uuid": course_template_uuid
        }
        resp = requests.post(
            url=url, json=input_data)
        resp_json = resp.json()
        assert resp.status_code == 200, "Status 200"
        assert resp_json["success"] is True, "Check success"
        assert resp_json["cohort"]["start_date"].split("+")[0] == input_data["start_date"], "Check start_date of chort"
        assert resp_json["cohort"]["uuid"] not in [
            "", None], "Cohort Firebase check"


def test_create_cohort_negative_course_template():
    """ 
    CUJ02 create a Cohort by providing a valid json object but invalid course_template uuid
    as a input and calling create Cohort API.
    Which will return Resource not found exception.
    """
    base_url = get_baseurl("lms")
    if not base_url:
        raise ResourceNotFoundException(
            "Unable to locate the service URL for lms")
    else:
        url = base_url + f"/lms/api/v1/cohorts"
        input_data = {
            "name": DATABASE_PREFIX+"test_cohort"+str(uuid.uuid4),
            "description": "Study Hall Test Cohort for Development purpose",
            "start_date": "2022-10-14T00:00:00",
            "end_date": "2022-12-25T00:00:00",
            "registration_start_date": "2022-10-20T00:00:00",
            "registration_end_date": "2022-11-14T00:00:00",
            "max_student": 5000,
            "course_template_uuid": "fake-uuid"
        }
        resp = requests.post(
            url=url, json=input_data)
        resp_json = resp.json()
        assert resp.status_code == 404, "Status 404"
        assert resp_json["success"] is False, "Check success"

def test_create_cohort_validation():
    """ 
    CUJ03 create a cohort by providing a invalid json object
    as a input using that json object used in calling create cohort API.
    Which will return a validation error response.
    """
    base_url = get_baseurl("lms")
    if not base_url:
        raise ResourceNotFoundException(
            "Unable to locate the service URL for lms")
    else:
        url = base_url + f"/lms/api/v1/cohorts"
        resp = requests.post(
            url=url, json={"name": DATABASE_PREFIX+"e2e_test_cases",
                           "description": "Study Hall Test Course for Development purpose"})
        assert resp.status_code == 422, "Status 422"
        assert resp.json()["success"] is False


def test_get_cohort(setup_cohort):
    """ 
    CUJ04 get a Cohort by providing a valid uuid
    as a path variable and calling get cohort API.
    Which will return a Cohort object.
    """
    base_url = get_baseurl("lms")
    if not base_url:
        raise ResourceNotFoundException(
            "Unable to locate the service URL for lms")
    else:
        url = base_url + \
            f"/lms/api/v1/cohorts/{setup_cohort.id}"
        resp = requests.get(url=url)
        data = TEST_COHORT
        data["uuid"] = setup_cohort.uuid
        data["course_template"] = CourseTemplate.find_by_uuid(
            course_template_uuid).key
        response_cohort = resp.json()
        response_cohort["start_date"] = datetime.datetime.strptime(
        response_cohort.pop("start_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
        response_cohort["end_date"] = datetime.datetime.strptime(
        response_cohort.pop("end_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
        response_cohort["registration_start_date"] = datetime.datetime.strptime(
        response_cohort.pop("registration_start_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
        response_cohort["registration_end_date"] = datetime.datetime.strptime(
        response_cohort.pop("registration_end_date").split("+")[0], '%Y-%m-%dT%H:%M:%S')
        print(data)
        print(response_cohort)
        assert resp.status_code == 200, "Status 200"
        assert response_cohort == data, "Data doesn't Match"


def test_get_cohort_negative():
    """ 
    CUJ05 get a Cohort by providing a invalid uuid
    as a path variable and calling get cohort api.
    Which will return a not found error response.
    """
    base_url = get_baseurl("lms")
    if not base_url:
        raise ResourceNotFoundException(
            "Unable to locate the service URL for lms")
    else:
        url = base_url + \
            f"/lms/api/v1/cohorts/fake-uuid"
        resp = requests.get(url=url)
        resp_json = resp.json()
        assert resp.status_code == 404, "Status 404"
        assert resp_json["success"] is False, "Data doesn't Match"


def test_delete_chort(setup_cohort):
    """ 
    CUJ05 delete a cohort by providing a valid uuid
    as a path variable and calling delete cohort api.
    Which will return a DeleteCohortModel object as a response.
    """
    base_url = get_baseurl("lms")
    if not base_url:
        raise ResourceNotFoundException(
            "Unable to locate the service URL for lms")
    else:
        url = base_url + \
            f"/lms/api/v1/cohorts/{setup_cohort.id}"
        resp = requests.delete(url=url)
        resp_json = resp.json()
        assert resp.status_code == 200, "Status 200"
        assert resp_json["success"] is True, "Check success"


def test_delete_cohort_negative():
    """ 
    CUJ06 delete a cohort by providing a invalid uuid
    as a path variable and calling delete cohort api.
    Which will return a not found error response.
    """
    base_url = get_baseurl("lms")
    if not base_url:
        raise ResourceNotFoundException(
            "Unable to locate the service URL for lms")
    else:
        url = base_url + \
            f"/lms/api/v1/cohorts/fake-uuid"
        resp = requests.delete(url=url)
        resp_json = resp.json()
        assert resp.status_code == 404, "Status 404"
        assert resp_json["success"] is False, "Data doesn't Match"


def test_get_list_cohort():
    """ 
    CUJ07 get a cohort list by calling get cohort list api.
    Which will return a CohortList object.
    """
    base_url = get_baseurl("lms")
    if not base_url:
        raise ResourceNotFoundException(
            "Unable to locate the service URL for lms")
    else:
        url = base_url + "/lms/api/v1/cohorts"
        resp = requests.get(url=url)
        resp_json = resp.json()
        assert resp.status_code == 200, "Status 200"
        assert resp_json["success"] is True, "Check success"
