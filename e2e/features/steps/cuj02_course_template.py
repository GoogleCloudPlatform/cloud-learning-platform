import behave
import requests
from testing_objects.test_config import API_URL
from testing_objects.course_template import COURSE_TEMPLATE_INPUT_DATA

# -------------------------------CREATE Course Template-------------------------------------
# ----Positive Scenario-----
@behave.given("A user has access privileges and needs to create a Course Template Record")
def step_impl_1(context):
    context.url = f'{API_URL}/course_templates'
    context.payload=COURSE_TEMPLATE_INPUT_DATA

@behave.when("API request is sent to create Course Template Record with correct request payload")
def step_impl_2(context):
    resp=requests.post(context.url,json=context.payload)
    context.status=resp.status_code
    context.response=resp.json()


@behave.then("Course Template Record will be created in a third party tool and classroom master course will be create with provided payload and all metadata will be ingested and stored in Cousre Template service and uuid for learning experiences will be stored in Cousre Template service")
def step_impl_3(context):
    assert context.status == 200, "Status 200"
    assert context.response["success"] is True, "Check success"
    assert context.response["course_template"]["classroom_code"] not in [
        "", None], "Course Template classroom check"
    assert context.response["course_template"]["uuid"] not in [
        "", None], "Course Template Firebase check"

# ----Negative Scenario-----


@behave.given("A user has access to admin portal and wants to create a Course Template Record")
def step_impl_4(context):
    context.url = f'{API_URL}/course_templates'
    context.payload = {"name": "e2e_test_cases",
                       "description": "description"}
@behave.when("API request is sent to create Course Template Record with incorrect request payload")
def step_impl_5(context):
    resp = requests.post(context.url, json=context.payload)
    context.status = resp.status_code
    context.response = resp.json()
@behave.then("Course Template Record Record will not be created and Course Template API will throw a validation error")
def step_impl_6(context):
    assert context.status == 422, "Status 422"
    assert context.response["success"] is False, "Check success"

# -------------------------------Retrieve Course Template-------------------------------------
# ----Positive Scenario-----
@behave.given("A user has access privileges and needs to retrieve a Course Template Record")
def setp_impl_7(context):
    COURSE_TEMPLATE_INPUT_DATA["uuid"] = context.course_template.uuid
    COURSE_TEMPLATE_INPUT_DATA["classroom_id"] = context.course_template.classroom_id
    COURSE_TEMPLATE_INPUT_DATA["classroom_code"] = context.course_template.classroom_code
    context.test_data=COURSE_TEMPLATE_INPUT_DATA
    context.url = f'{API_URL}/course_templates/{context.course_template.uuid}'
@behave.when("API request is sent to retrieve Course Template Record by providing correct uuid")
def step_impl_8(context):
    resp = requests.get(context.url)
    context.status = resp.status_code
    context.response = resp.json()


@behave.then("Course Template Record corresponding to given uuid will be returned successfully")
def step_impl_9(context):
    assert context.status == 200, "Status 200"
    assert context.response == context.test_data, "Data doesn't Match"

# ----Negative Scenario-----


@behave.given("A user has access to admin portal and wants to retrieve a Course Template Record")
def setp_impl_10(context):
    context.url = f'{API_URL}/course_templates/fake_non_exist_uuid'
@behave.when("API request is sent to retrieve Course Template Record by providing invalid uuid")
def step_impl_11(context):
    resp = requests.get(context.url)
    context.status = resp.status_code
    context.response = resp.json()
@behave.then("Course Template Record will not be returned and API will throw a resource not found error")
def step_impl_12(context):
    assert context.status == 404, "Status 404"
    assert context.response["success"] is False, "Check success"

# -------------------------------Delete Course Template-------------------------------------
# ----Positive Scenario-----
@behave.given("A user has access privileges and needs to delete a Course Template Record")
def setp_impl_13(context):
    context.url = f'{API_URL}/course_templates/{context.course_template.uuid}'
@behave.when("API request is sent to delete Course Template Record by providing correct uuid")
def step_impl_14(context):
    resp = requests.delete(context.url)
    context.status = resp.status_code
    context.response = resp.json()
@behave.then("Course Template Record will be deleted successfully")
def step_impl_12(context):
    assert context.status == 200, "Status 200"
    assert context.response["success"] is True, "Check success"

# ----Negative Scenario-----


@behave.given("A user has access to admin portal and wants to delete a Course Template Record")
def setp_impl_10(context):
    context.url = f'{API_URL}/course_templates/fake_non_exist_uuid'
@behave.when("API request is sent to delete Course Template Record by providing invalid uuid")
def step_impl_11(context):
    resp = requests.delete(context.url)
    context.status = resp.status_code
    context.response = resp.json()
@behave.then("Course Template Record will not be deleted and API will throw a resource not found error")
def step_impl_12(context):
    assert context.status == 404, "Status 404"
    assert context.response["success"] is False, "Check success"

# -------------------------------Fetch All Course Templates-------------------------------------

@behave.given("A user has access privileges and needs to fetch all Course Template Records")
def step_impl_1(context):
    context.url = f'{API_URL}/course_templates'

@behave.when("API request is sent to fetch all Course Template Records")
def step_impl_2(context):
    resp = requests.get(context.url)
    context.status = resp.status_code
    context.response = resp.json()

@behave.then("Course Template API will return all existing Course Template Records successfully")
def step_impl_3(context):
    assert context.status == 200, "Status 200"
    assert context.response["success"] is True, "Check success"
