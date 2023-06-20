import behave
import requests
import time
import datetime
from datetime import timedelta
from common.models import Section
from testing_objects.test_config import API_URL,e2e_google_form_id,e2e_drive_folder_id
from testing_objects.course_template import emails
from e2e.gke_api_tests.secrets_helper import (get_student_email_and_token,
  get_workspace_student_email_and_token)
from e2e.gke_api_tests.classroom_e2e_helper import(
create_coursework_submission,
list_coursework_submission_user,insert_file_into_folder)

# -------------------------------Enroll student to cohort-------------------------------------
# ----Positive Scenario-----


@behave.given("A user has access privileges and wants to enroll a student into a cohort")
def step_impl_1(context):
  # context.url = f'{API_URL}/sections/{context.sections.id}/students'
  context.url = f'{API_URL}/cohorts/{context.cohort.id}/students'
  context.payload = get_student_email_and_token()



@behave.when("API request is sent to enroll student to a section with correct request payload and valid cohort id")
def step_impl_2(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Section will be fetch using the given id and student is enrolled using student credentials and a response model object will be return")
def step_impl_3(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -----Negative Scenario-----


@behave.given("A user has access to portal and needs to enroll a student into a cohort")
def setp_impl_4(context):
  context.url = f'{API_URL}/cohorts/fake_id_data/students'
  context.payload = get_student_email_and_token()


@behave.when("API request is sent to enroll student to a section with correct request payload and invalid cohort id")
def step_impl_5(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a resource not found error")
def step_impl_6(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

# ----

@behave.given("A user has access to the portal and wants to enroll a student into a cohort")
def step_impl_7(context):
  context.url = f'{API_URL}/cohorts/{context.cohort.id}/students'
  context.payload ={"email":"email@gmail.com","credentials":{"token":"token"}}


@behave.when("API request is sent to enroll student to a section with incorrect request payload and valid cohort id")
def step_impl_8(context):
  resp = requests.post(context.url, json=context.payload,headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Student will not be enrolled and API will throw a validation error")
def step_impl_9(context):
  assert context.status == 422, "Status 422"
  assert context.response["success"] is False, "Check success"

# -----Positive Scenario--------


@behave.given("A user has access privileges and wants to enroll a student using his/her workspace email into a cohort")
def step_impl_10(context):
  context.url = f'{API_URL}/cohorts/{context.cohort.id}/students'
  context.payload = get_workspace_student_email_and_token()


@behave.when("API request is sent to enroll workspace email as a student to a cohort with correct request payload and valid cohort id")
def step_impl_11(context):
  resp = requests.post(context.url, json=context.payload,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then("Section will be fetch using the given id and student is enrolled using student access token and his workspace email and a response model object will be return")
def step_impl_12(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -------------------------------enable notification to a course-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access privileges and wants to enable notifications for a section"
)
def step_impl_13(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/enable_notifications'

@behave.when(
    "API request is sent to enable notifications for a section using valid section id"
)
def step_impl_14(context):
  resp = requests.post(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will be enabled using unique section id and a response model object will be return"
)
def step_impl_15(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -----Negative Scenario-----

@behave.given(
    "A user has access to portal and needs to enable notifications for a section"
)
def step_impl_16(context):
  context.url = f'{API_URL}/sections/fake_section_id/enable_notifications'

@behave.when(
    "API request is sent to enable notifications for a section using invalid section id"
)
def step_impl_17(context):
  resp = requests.post(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Notifications will not be enabled and API will throw a resource not found error"
)
def step_impl_18(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"


# -------------------------------Retrieve assignment-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access to portal and needs to retrieve a assignment using section id and assignment id"
)
def step_impl_19(context):
  context.url = f'{API_URL}/sections/{context.assignment["section_id"]}/assignments/{context.assignment["id"]}'


@behave.when(
    "API request is sent to retrieve assignment details of a section with correct section id and assignment id"
)
def step_impl_20(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Assignment Record corresponding to given assignment id will be returned successfully"
)
def step_impl_21(context):
  assert context.status == 200, "Status 200"
  assert context.response["id"] == context.assignment["id"], "Data id doesn't Match"
  assert context.response["classroom_id"] == context.assignment["courseId"], "Data classroom id doesn't Match"
  assert context.response["title"] == context.assignment["title"], "Data title doesn't Match"

#----Negative scenario-------


@behave.given(
    "A user has access to admin portal and wants to retrieve a assignment using assignment id and section id"
)
def setp_impl_22(context):
  context.url = f'{API_URL}/sections/fake_section_id/assignments/fake_assignment_id'


@behave.when(
    "API request is sent to retrieve assignment details by providing invalid section id"
)
def step_impl_23(context):
  resp = requests.get(context.url, headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Assignment details will not be returned and API will throw a resource not found error"
)
def step_impl_24(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

# -------------------------------List teachers in section-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access to admin portal and needs to retrieve the list of teachers with vailid section id"
)
def step_impl_31(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/teachers'


@behave.when(
    "API request is sent which contains valid section id"
)
def step_impl_32(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "List of teachers will be given with there details"
)
def step_impl_33(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] == True, "Success status doesn't match"
  assert context.response["data"][0]["user_type"] == "faculty", "User type faculty doesn't match"

# -------------------------------List teachers in section negative -------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access to admin portal and needs to retrieve the list of teachers with invailid section id"
)
def step_impl_34(context):
  context.url = f'{API_URL}/sections/invalid_id/teachers'


@behave.when(
    "API request is sent which contains invalid section id"
)
def step_impl_35(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Section not found error is sent in response"
)
def step_impl_36(context):
  assert context.status == 404, "Status 404"

# -------------------------------Get teachers in section Positive-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access to admin portal and needs to retrieve the details teacher with valid section id and teacher_email"
)
def step_impl_37(context):
  context.url = f'{API_URL}/sections/{context.enrollment_mapping.section.id}/teachers/{context.enrollment_mapping.user.email}'


@behave.when(
    "Get request is sent which contains valid section id and teacher email"
)
def step_impl_38(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then(
    "Get the details of teacher from user collection"
)
def step_impl_39(context):
  assert context.status == 200, "Status 200"
  assert context.response["data"]["email"] == context.enrollment_mapping.user.email,"Check data"
  assert context.response["data"]["user_id"] == context.enrollment_mapping.user.user_id,"Check data"

#---negative scenario

@behave.given(
    "A user has access privileges wants to retrieve the details teacher with valid section id and invalid teacher_email"
)
def step_impl_40(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/teachers/12345678'


@behave.when(
    "API request is sent which contains valid section id and invalid teacher email"
)
def step_impl_41(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then(
    "Get teacher API will throw teacher not found error"
)
def step_impl_42(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check Data"

#-----------------------------------Delete teacher from section--------------------------------------
#---Positive scenario

@behave.given(
    "A user has access to admin portal and needs to delete the teacher with valid section id and teacher_email"
)
def step_impl_43(context):
  context.url = f'{API_URL}/sections/{context.enrollment_mapping.section.id}/teachers/{context.enrollment_mapping.user.email}'


@behave.when(
    "Delete request is sent which contains valid section id and teacher email"
)
def step_impl_44(context):
  resp = requests.delete(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then(
    "Set inactive teacher from enrollment mapping collection"
)
def step_impl_45(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "check data"

#---negative scenario

@behave.given(
    "A user has access privileges wants to delete teacher with valid section id and invalid teacher id"
)
def step_impl_46(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/teachers/12345678'


@behave.when(
    "API request is sent which contains valid section id and invalid teacher id to delete teacher"
)
def step_impl_47(context):
  resp = requests.get(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then(
    "Delete teacher API throw teacher not found error"
)
def step_impl_48(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check Data"

#---------------------------------Enroll teacher in a section-------------
@behave.given(
    "A user has access privileges wants to enroll the teacher using valid section id and teacher_email"
)
def step_impl_49(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/teachers'
  context.payload = {"email":emails["teacher"]}


@behave.when(
    "Post request is sent which contains valid section id and payload which contains valid teacher email"
)
def step_impl_50(context):
  resp = requests.post(context.url,
                       headers=context.header,json=context.payload)
  context.status = resp.status_code
  context.response = resp.json()

@behave.then(
    "The teacher enrolled in classroom and a enrollment mapping is created and return user details with enrollment details"
)
def step_impl_51(context):
  print(f"--------------------json: {context.payload}-----------------------")
  print(f"------------------Status: {context.status}------------------------")
  print(f"------------------data: {context.response}------------------------")
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check Data"

# -----------------------------------Import grade coursework- Positive-------------------------------

@behave.given(
    "A teacher has access to portal and wants to  update grades of student for a coursework with form quize of a section"
)
def step_impl_52(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/coursework/{context.coursework_id}'
  print("CONTEXT URL for import grade",context.url)

@behave.when(
    "API request is sent which has valid section_id and coursework_id"
)
def step_impl_53(context):
  resp = requests.patch(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()
  print("Response of Import grade api not turn in ",context.response)

@behave.then(
    "Student grades are not updated in classroom"
)
def step_impl_54(context):
  time.sleep(6)
  assert context.status == 202, "Status 202"
  result = list_coursework_submission_user(context.access_token,
                                  context.classroom_id,
                                  context.coursework["id"],"me")
  # insert_file_into_folder(e2e_drive_folder_id,e2e_google_form_id)
  print("This is result after list coursework submission Before turn in",result)
  assert "assignedGrade" not in result[0].keys()


@behave.given(
    "A teacher wants to update grades of student for a coursework with for turnIn  assignment with google form"
)
def step_impl_55(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/coursework/{context.coursework_id}'
  print("CONTEXT URL for import grade",context.url)

@behave.when(
    "API request is sent which has valid input"
)
def step_impl_56(context):
  submission =list_coursework_submission_user(context.access_token,
                                              context.classroom_id,
                                              context.coursework["id"],"me")
  print("get Coursework submission of user",context.student_email,
        context.access_token,submission)

  create_coursework_submission(context.access_token,context.classroom_id,
                               context.coursework["id"],submission[0]["id"])
  resp = requests.patch(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()
  print("Response of Import grade api turn in",context.response)

@behave.then(
    "Student grades are  updated in classroom ans student_email is present in api response"
)
def step_impl_57(context):
  time.sleep(15)
  # insert_file_into_folder(e2e_drive_folder_id,e2e_google_form_id)
  print("After inser to origin folder")
  result = list_coursework_submission_user(context.access_token,
                                  context.classroom_id,
                                  context.coursework["id"],"me")
  print("This is result after Turn in list coursework submission",result)
  assert context.status == 202, "Status 202"
  assert context.response["success"] is True,"success status not matching"

# -------------------------------update classroom code of a section-------------------------------------
# ----Positive Scenario-----

@behave.given(
    "A user has access privileges and wants to update classroom code for a section"
)
def step_impl_58(context):
  context.url = f'{API_URL}/sections/{context.sections.id}/update_classroom_code'

@behave.when(
    "API request is sent to update classroom code for a section using valid section id"
)
def step_impl_59(context):
  resp = requests.patch(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Code will be updated using unique section id and a response model object will be return"
)
def step_impl_60(context):
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"

# -----Negative Scenario-----

@behave.given(
    "A user has access to portal and needs to update classroom code for a section"
)
def step_impl_61(context):
  context.url = f'{API_URL}/sections/fake_section_id/update_classroom_code'

@behave.when(
    "API request is sent to update classroom code for a section using invalid section id"
)
def step_impl_62(context):
  resp = requests.patch(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Code will not be updated and API will throw a resource not found error"
)
def step_impl_63(context):
  assert context.status == 404, "Status 404"
  assert context.response["success"] is False, "Check success"

#--------------------Delete section cronjob----------------------------------
# positive scenario

@behave.given(
    "A cronjob is accessing this API daily"
)
def step_impl_64(context):
  print("-----------------------------------------------------------")
  print(f"Section with id {context.sections.id}")
  section = Section.find_by_id(context.sections.id)
  section.status = "FAILED_TO_PROVISION"
  section.created_time = datetime.datetime.utcnow() - timedelta(days=8)
  section.update()
  print("Section details updated in firestore with details",section.id ,section.status,section.created_time)
  print("------------------------------------------------")
  context.url = f'{API_URL}/sections/cronjob/delete_failed_to_provision_section'

@behave.when(
    "A section with FAILED_TO_PROVISION status is present in db with section creation date 7 days before"
)
def step_impl_65(context):
  resp = requests.delete(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Then section is deleted from db and google classroom with ddrive folder is deleted"
)
def step_impl_66(context):
  print("Response of delete 1 section API",context.response)
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"
  assert context.response["data"] ==1 ,"count of deleted section"

@behave.given(
    "A cronjob is accessing this API daily to delete section"
)
def step_impl_67(context):
  print("-------------------------------------------")
  print(f"Section with id {context.sections.id}")
  section = Section.find_by_id(context.sections.id)
  section.status = "ACTIVE"
  section.created_time = datetime.datetime.utcnow() - timedelta(days=5)
  section.update()
  print("Section details updated in firestore with details",section.id ,section.status,section.created_time)
  print("------------------------------------------------")
  context.url = f'{API_URL}/sections/cronjob/delete_failed_to_provision_section'

@behave.when(
    "A section with FAILED_TO_PROVISION status is present in db with ACTIVE status"
)
def step_impl_68(context):
  resp = requests.delete(context.url,
                       headers=context.header)
  context.status = resp.status_code
  context.response = resp.json()


@behave.then(
    "Then section is not deleted from db and google classroom"
)
def step_impl_69(context):
  print("Response of delete 1 section API",context.response)
  assert context.status == 200, "Status 200"
  assert context.response["success"] is True, "Check success"
  assert context.response["data"] ==0 ,"count of deleted section"