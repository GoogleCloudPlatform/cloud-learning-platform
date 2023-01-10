import behave
import requests
from testing_objects.test_config import API_URL
from e2e.gke_api_tests.secrets_helper import get_student_email_and_token

# -------------------------------Enroll student to Section-------------------------------------
# ----Positive Scenario-----


@behave.given("A user has access privileges and wants to enroll a student into a section")
def step_impl_1(context):
    context.url = f'{API_URL}/sections/{context.sections.id}/students'
    print("-PAYLOAD FOR student enroll---")
    print(get_student_email_and_token())
    context.payload = get_student_email_and_token()
    context.header = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNlOWI4ODBmODE4MmRkYTU1N2Y3YzcwZTIwZTRlMzcwZTNkMTI3NDciLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vY29yZS1sZWFybmluZy1zZXJ2aWNlcy1kZXYiLCJhdWQiOiJjb3JlLWxlYXJuaW5nLXNlcnZpY2VzLWRldiIsImF1dGhfdGltZSI6MTY3MzM3MzE3MSwidXNlcl9pZCI6Ik1GcEFPUm8ybnNPVjZpN0l0N2JOWktGS0FGYzIiLCJzdWIiOiJNRnBBT1JvMm5zT1Y2aTdJdDdiTlpLRktBRmMyIiwiaWF0IjoxNjczMzczMTcxLCJleHAiOjE2NzMzNzY3NzEsImVtYWlsIjoiZTJlXzcxMTJmNzczXzFhNTNfZW1haWxAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImUyZV83MTEyZjc3M18xYTUzX2VtYWlsQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.Eb8-H-JMr3pK3aL1lZl99l5dwqjahMdMVMgvkb0yD-EeQFIfw-ulhVgKWAs5dW43RwV9xSBjkE1bef2xFnonICdMgLzly74nlRhMwXo_EBJgRmNtncnxoR-vGsWK9Kt-10bLCe5x3v4ihJDpLxfIMUxAltPBO8TWD2_LMZJtKsSnvyTbYbjfhHuawC9943LLm_rYmpDzVmEiCBJJz9uv5n94jSXDcqABmxO8w8VEEUzAYWytxhZoc3Cw4LH9xEaAivCeKvlsVm5LhrVc_PUL-M__6EosVkVVXbuiFA_rmetGL3ZiHK4ycDa3VhOgCUCzguSkfBbrIKDdhmzMdTE8Dw"



@behave.when("API request is sent to enroll student to a section with correct request payload and valid section id")
def step_impl_2(context):
    resp = requests.post(context.url, json=context.payload,headers=context.header)
    print("-----------Step imp2--------")
    print("resp.status",resp.status_code)
    print("resp.response",resp.json())
    context.status = resp.status_code
    context.response = resp.json()


@behave.then("Section will be fetch using the given id and student is enrolled using student credentials and a response model object will be return")
def step_impl_3(context):

    print("-----------Step imp3--------")
    assert context.status == 200, "Status 200"
    assert context.response["success"] is True, "Check success"

# -----Negative Scenario-----


@behave.given("A user has access to portal and needs to enroll a student into a section")
def setp_impl_4(context):
    context.url = f'{API_URL}/sections/fake_id_data/students'
    context.payload = get_student_email_and_token()


@behave.when("API request is sent to enroll student to a section with correct request payload and invalid section id")
def step_impl_5(context):
    resp = requests.post(context.url, json=context.payload,headers=context.header)
    context.status = resp.status_code
    context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a resource not found error")
def step_impl_6(context):
    assert context.status == 404, "Status 404"
    assert context.response["success"] is False, "Check success"


@behave.given("A user has access to the portal and wants to enroll a student into a section")
def step_impl_7(context):
    context.url = f'{API_URL}/sections/{context.sections.id}/students'
    context.payload ={"email":"email@gmail.com","credentials":{"token":"token"}}
    

@behave.when("API request is sent to enroll student to a section with incorrect request payload and valid section id")
def step_impl_8(context):
    resp = requests.post(context.url, json=context.payload,headers=context.header)
    context.status = resp.status_code
    context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a validation error")
def step_impl_9(context):
    assert context.status == 422, "Status 422"
    assert context.response["success"] is False, "Check success"



