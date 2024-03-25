"""
Feature 08 - API Test Script For Batch Job Management
"""

import behave
import sys
sys.path.append("../")
from setup import post_method, set_cache, get_cache, get_method, put_method, delete_method
sys.path.append("../../")
from test_object_schemas  import DUMMY_BATCH_JOB_NAMES


@behave.given("Format the API request url to fetch batch job using correct job type and incorrect job name")
def step_impl1(context):
  job_type = "e2e_test"
  context.url = f"http://localhost:9012/skill-service/api/v1/jobs/{job_type}/123456789"


@behave.when("API request is sent to get the batch job")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an error message while trying to get the batch job")
def step_impl3(context):
  assert context.res.status_code != 200, "Status is 200"
  assert context.res_data["success"] is False


@behave.given("Format the API request url to fetch batch job using correct job name without job type")
def step_impl1(context):
  context.url = f"http://localhost:9012/skill-service/api/v1/jobs/123456789"


@behave.when("API request is sent to fetch the batch job")
def step_impl2(context):
  context.res = get_method(url=context.url)


@behave.then("Skill Service will throw an error message while trying to fetch the batch job")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"



@behave.given("Format the correct API request url to get all the jobs using correct job type")
def step_impl1(context):
  job_type = "e2e_test"
  context.url = f"http://localhost:9012/skill-service/api/v1/jobs/{job_type}"


@behave.when("API request is sent to get all batch jobs")
def step_impl2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will fetch all batch jobs")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data.get("success") is True, "Success not true"
  assert len(context.res_data.get("data")) >= len(DUMMY_BATCH_JOB_NAMES),\
        "All expected batch jobs are not present"



@behave.given("Format the correct API request url to get all the jobs using incorrect job type")
def step_impl1(context):
  job_type = "random_job_type"
  context.url = f"http://localhost:9012/skill-service/api/v1/jobs/{job_type}"


@behave.when("API request is sent to fetch all batch jobs")
def step_impl2(context):
  context.res = get_method(url=context.url)


@behave.then("Skill Service will throw an error message while trying to get the batch jobs")
def step_impl3(context):
  assert context.res.status_code == 422, "Status is not 422"



@behave.given("Format the correct API request url to delete the batch job using correct job name")
def step_impl1(context):
  job_type = "e2e_test"
  context.url = f"http://localhost:9012/skill-service/api/v1/jobs/{job_type}/{DUMMY_BATCH_JOB_NAMES[0]}"


@behave.when("API request is sent to delete the batch job")
def step_impl2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will successfully delete the requested batch job")
def step_impl3(context):
  assert context.res.status_code == 200, "Status is not 200"
  assert context.res_data.get("success") is True, "Success not true"


@behave.given("Format the correct API request url to delete the batch job using incorrect job name")
def step_impl1(context):
  job_type = "e2e_test"
  context.url = f"http://localhost:9012/skill-service/api/v1/jobs/{job_type}/random_job_name"


@behave.when("API request is sent to delete the batch job with incorrect name")
def step_impl2(context):
  context.res = delete_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an error message while trying to delete the batch job")
def step_impl3(context):
  assert context.res.status_code == 404, "Status is not 404"
  assert context.res_data.get("success") is False, "Success not False"
  assert context.res_data.get("message") == "Invalid BatchJobModel name: random_job_name"
