# pylint: disable=unspecified-encoding,missing-module-docstring,broad-exception-raised,broad-exception-caught,invalid-name,unused-variable,
# pylint: disable=consider-using-dict-items,consider-iterating-dictionary
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import asyncio

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses",
    "https://www.googleapis.com/auth/classroom.rosters",
    "https://www.googleapis.com/auth/classroom.topics",
    "https://www.googleapis.com/auth/classroom.coursework.students",
    "https://www.googleapis.com/auth/classroom.coursework.me",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/classroom.profile.photos",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials",
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
    "https://www.googleapis.com/auth/classroom.push-notifications",
    "https://www.googleapis.com/auth/classroom.student-submissions." +
    "students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly"
]

CLASSROOM_ADMIN_EMAIL = "studyhallregistrar@asu.edu"
csv_file_name = "Lab Participation 02 - Painting a Wall.csv"


def get_credentials():
  source_credentials = (
      service_account.Credentials.from_service_account_file(
          "asu-prod-key.json", scopes=SCOPES, subject=CLASSROOM_ADMIN_EMAIL))
  # print("Get credentials worked",source_credentials)
  return source_credentials


STUDENT_JSON = {}

STUDENT_ARRAY = []


def prepare_json():

  print("In prepare JSON CSV file name is", csv_file_name)
  csvFile = pd.read_csv(csv_file_name)
  print(type(csvFile))
  for d in csvFile:
    print(d)

  print("----------------------------------")

  for index, row in csvFile.iterrows():
    if STUDENT_JSON.get(row["Email"], None):
      if STUDENT_JSON[row["Email"]]["score"] <= row["Score"]:
        STUDENT_JSON[row["Email"]] = {
            "email": row["Email"],
            "score": row["Score"],
            "section_id": row["SectionId"],
            "classroom_id": row["CourseId"],
            "coursework_id": row["AssignmentId"],
            "section_name": row["SectionName"]
        }
        # This array is getting duplicatly added
        # STUDENT_ARRAY.append({
        #     "email": row["Email"],
        #     "score": row["Score"],
        #     "section_id": row["SectionId"],
        #     "classroom_id": row["CourseId"],
        #     "coursework_id": row["AssignmentId"],
        #     "section_name": row["SectionName"]
        # })

    else:
      STUDENT_JSON[row["Email"]] = {
          "email": row["Email"],
          "score": row["Score"],
          "section_id": row["SectionId"],
          "classroom_id": row["CourseId"],
          "coursework_id": row["AssignmentId"],
          "section_name": row["SectionName"]
      }
      # STUDENT_ARRAY.append({
      #     "email": row["Email"],
      #     "score": row["Score"],
      #     "section_id": row["SectionId"],
      #     "classroom_id": row["CourseId"],
      #     "coursework_id": row["AssignmentId"],
      #     "section_name": row["SectionName"]
      # })

    # print(row)
  for key in STUDENT_JSON.keys():
    STUDENT_ARRAY.append(STUDENT_JSON[key])
  with open("student_json_" + csv_file_name, "w") as file:
    file.write(str(STUDENT_JSON))
  print("Length of Student JSON is ----------------", len(STUDENT_JSON))
  print("Length of Student Array is -----------------", len(STUDENT_ARRAY))


# Make student JSON
prepare_json()


def list_coursework_submissions_user(classroomId, courseworkId, email):
  service = build("classroom", "v1", credentials=get_credentials())
  submissions = []
  page_token = None
  while True:
    coursework = service.courses().courseWork()
    response = coursework.studentSubmissions().list(
        pageToken=page_token,
        courseId=classroomId,
        courseWorkId=courseworkId,
        userId=email).execute()
    submissions.extend(response.get("studentSubmissions", []))
    page_token = response.get("nextPageToken", None)
    if not page_token:
      break
  return submissions


def patch_student_submission(course_id, coursework_id, student_submission_id,
                             assigned_grade, draft_grade):
  """Get  list of coursework from classroom

  Args: course_id
  Returns:
    returns list of coursework of given course in classroom
    """ ""
  service = build("classroom", "v1", credentials=get_credentials())
  student_submission = {
      "assignedGrade": assigned_grade,
      "draftGrade": draft_grade
  }
  patch_result = service.courses().courseWork().studentSubmissions().patch(
      courseId=course_id,
      courseWorkId=coursework_id,
      id=student_submission_id,
      updateMask="assignedGrade,draftGrade",
      body=student_submission).execute()

  return patch_result


def push_grade(email, classroom_id, coursework_id, draft_grade, assigned_grade):
  submissions = list_coursework_submissions_user(classroom_id, coursework_id,
                                                 email)

  if submissions:
    try:
      result = patch_student_submission(classroom_id, coursework_id,
                                        submissions[0]["id"], draft_grade,
                                        assigned_grade)
      with open("Success_logs" + csv_file_name, "a") as fa:
        fa.write(f"\nGrade import successful for {email} {assigned_grade}")
      print("Grade imported for", email)
    except Exception as e:
      with open("error_logs" + csv_file_name, "a") as file:
        file.write(f"\nStudent DATA-{email}")

        file.write(f"Error is {e}")

  else:
    print("Student not found in given course", email)
    with open("Student_not_found" + csv_file_name, "a") as fa:
      fa.write(f"\nStudent_not_found for {email}")


# def import_form_grade_from_JSON():
#     print("Inside Import form grade function")
#     print("Length of student JSON is ", len(STUDENT_JSON))
#     for key, values in STUDENT_JSON.items():
#         push_grade(STUDENT_JSON[key]["email"],
#                    STUDENT_JSON[key]["classroom_id"],
#                    STUDENT_JSON[key]["coursework_id"],
#                    STUDENT_JSON[key]["score"], STUDENT_JSON[key]["score"])


async def initiate_grade_push(data_list):

  with ThreadPoolExecutor(max_workers=15) as executor:
    loop = asyncio.get_event_loop()
    tasks = []
    for data in data_list:
      runner = loop.run_in_executor(
          executor, push_grade,
          *(data.get("email"), data.get("classroom_id"),
            data.get("coursework_id"), data.get("score"), data.get("score")))
      tasks.append(runner)

    for response in await asyncio.gather(*tasks):  # pylint: disable=unused-variable
      pass


def async_push_grades(data_list):
  loop = asyncio.get_event_loop()
  future = asyncio.ensure_future(initiate_grade_push(data_list))
  loop.run_until_complete(future)


# FOr Loop
# Prepare array
async_push_grades(STUDENT_ARRAY)
