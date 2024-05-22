import fireo

fireo.connection(from_file="./prod_sa.json")

import os
import csv
import copy
import json
import asyncio
from pathlib import Path
from common.models import User, CourseEnrollmentMapping, LTIAssignment
from google.oauth2 import service_account
from googleapiclient.discovery import build
from concurrent.futures import ThreadPoolExecutor

CLASSROOM_ADMIN_EMAIL = "studyhallregistrar@asu.edu"
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
EMAILS_TO_BE_REPLACED = [{
    "zybooks_email": "simoneadgers@icloud.com",
    "clp_email": "moniesan715@gmail.com"
}, {
    "zybooks_email": "kaylamccloy@live.com",
    "clp_email": "kaylajmccloy@gmail.com"
}, {
    "zybooks_email": "loganash@outlook.com",
    "clp_email": "xioxio255@gmail.com"
}, {
    "zybooks_email": "bcamarda18@gmail.com",
    "clp_email": "katherineblocher93@gmail.com"
}, {
    "zybooks_email": "chloecampos15@yahoo.com",
    "clp_email": "chloecampos15@gmail.com"
}, {
    "zybooks_email": "imperfect.circle@yahoo.com",
    "clp_email": "imperfectcircle0@gmail.com"
}, {
    "zybooks_email": "psdragon4444@comcast.net",
    "clp_email": "dipasquap4444@gmail.com"
}, {
    "zybooks_email": "hbreannne00@gmail.com",
    "clp_email": "hbreanne00@gmail.com"
}, {
    "zybooks_email": "supremeezy@aim.com",
    "clp_email": "prich9600@gmail.com"
}, {
    "zybooks_email": "nr165@duke.edu",
    "clp_email": "nirvika98@gmail.com"
}, {
    "zybooks_email": "rehm.jeffrey@yahoo.com",
    "clp_email": "rehm.jeffrey@gmail.com"
}, {
    "zybooks_email": "robrenfrow911@gmail.com",
    "clp_email": "renfrowr88@gmail.com"
}, {
    "zybooks_email": "nyeerussell@icloud.com",
    "clp_email": "nyeerussell@gmail.com"
}, {
    "zybooks_email": "sandovalmichael003@yahoo.com",
    "clp_email": "msands0426@gmail.com"
}, {
    "zybooks_email": "nils@a-2.be",
    "clp_email": "nilssep04@gmail.com"
}, {
    "zybooks_email": "camsoz2000@yahoo.com",
    "clp_email": "cameronsozio@gmail.com"
}, {
    "zybooks_email": "vazquezgabriel425@yahoo.com",
    "clp_email": "igvasq21@gmail.com"
}]

SKIP_EMAILS = [
    "sbdeshazo@gmail.com", "emmaleesadle@gmail.com", "jchasteen0117@gmail.com",
    "krymgonz@gmail.com", "lillywallace01@gmail.com", "eanvanvliet@gmail.com",
    "rancepledgerjr8801@gmail.com", "hernandeztifany364@gmail.com",
    "gabrielle.brett26@gmail.com", "lenapena7512@gmail.com",
    "mia.buer94@gmail.com", "nathanneu97@gmail.com",
    "angela.capistran@gmail.com", "bankyalade1@gmail.com",
    "chris.iannotti64@gmail.com", "samuel.ray@slr.family",
    "victorialovejo@gmail.com", "sadermin@gmail.com",
    "angeloruiz1012@gmail.com", "nathanielbman87@gmail.com",
    "katie.bunn996@gmail.com", "layton.and.natasha@gmail.com",
    "simon.school001@gmail.com", "jwfreeman99@gmail.com",
    "missjuliaberry@gmail.com", "natashamachado16@gmail.com",
    "cass.hemby@gmail.com", "heyitsrigo1@gmail.com", "heyitsrigo1@gmail.com",
    "rosawilliam602@gmail.com", "trarevol21@gmail.com",
    "nathanielcorson@gmail.com", "samuel.ray@slr.family",
    "ihaveapig11@gmail.com", "adreana.i.aquino5@gmail.com",
    "nguyennoah04@gmail.com", "clrowlett@gmail.com",
    "mario.robles.93@gmail.com", "harryhartono1997@gmail.com",
    "meredithspencer04@gmail.com", "bridgetdotjones@gmail.com",
    "jwimberly616@gmail.com", "jrmiller9559@gmail.com",
    "uhringanalise@gmail.com", "zarragama1@gmail.com",
    "pomaitollefsen@gmail.com", "cheyenneleelarson@gmail.com",
    "sharonchen200574@gmail.com", "dawn.hinerth@gmail.com",
    "plokommb@gmail.com", "spooky.tabor@gmail.com", "hayleybredt@gmail.com",
    "arielwhysper@gmail.com", "hernandeztifany364@gmail.com",
    "emryhrobinson@gmail.com", "arielwhysper@gmail.com", "hncasey7@gmail.com",
    "dvwhippl@gmail.com", "isabelag62702@gmail.com", "tylertodd6153@gmail.com",
    "seth.callis.e@gmail.com", "gcmaloney4@gmail.com",
    "hernandeztifany364@gmail.com", "menakeshishzadeh@gmail.com",
    "macyproctor98@gmail.com", "dianal.martin@yahoo.com",
    "cassiopeiafitzsimmons@gmail.com", "hoanghchristine@gmail.com",
    "kmbaldw2@asu.edu", "hannah.marie.mudge@gmail.com",
    "cynthiaamorette@gmail.com", "mitch.accounts@gmail.com",
    "owenfox066@gmail.com", "rosaamilee@gmail.com", "jenny.cas0206@gmail.com",
    "brycelcarpenter@gmail.com", "berg.c.09@gmail.com",
    "amberly.smith805@gmail.com", "siancmorris@gmail.com",
    "jcernoch25@gmail.com", "ajmassock@gmail.com", "naomirivera15@gmail.com",
    "sevillethorpe@gmail.com", "jjcm1994@gmail.com", "bgleason09@gmail.com",
    "melissa.hammon42@gmail.com", "wyatt.olson97@gmail.com",
    "dbenef25@gmail.com", "chris99thomson@gmail.com", "deleted@deleted.com",
    "elizabeth.zukowski@gmail.com", "gstridsigne915@gmail.com",
    "abbyhering45@gmail.com", "pomaitollefsen@gmail.com",
    "pomaitollefsen@gmail.com", "foleytho@gmail.com", "oapietrib@gmail.com",
    "oapietrib@gmail.com", "oapietrib@gmail.com", "charity.mcnally@gmail.com",
    "quillmccrory@gmail.com", "steviepenn@gmail.com", "alxrd6@gmail.com",
    "zforten1404@gmail.com", "m.raha1988m@gmail.com", "zforten1404@gmail.com",
    "emilyn111@icloud.com", "ramkc.1999@gmail.com", "themisterspider@gmail"
]

ASSIGNMENTS = [{
    "file_name": "Final_Exam_Proctoring_Report.csv",
    "lti_assignment_title": [
        " CSE 110 zyBook - Proctoring Practice",
        "CSE 110 zyBook - Proctoring Practice"
    ],
    "zybooks_max_grade_percentage": "5",
    "classroom_max_grade_percentage": "5"
}, {
    "file_name": "Final_Exam_Report.csv",
    "lti_assignment_title": [
        " CSE 110 zyBook - Final Exam", "CSE 110 zyBook - Final Exam"
    ],
    "zybooks_max_grade_percentage": "89",
    "classroom_max_grade_percentage": "94"
}]


def get_credentials():
  source_credentials = (
      service_account.Credentials.from_service_account_file(
          './prod_sa.json', scopes=SCOPES, subject=CLASSROOM_ADMIN_EMAIL))
  return source_credentials


CREDENTIALS = get_credentials()


def write_log(log_message, log_file_name, mode='a'):
  output_file_path = os.path.join(OUTPUT_DIR, log_file_name)
  with open(output_file_path, mode) as log_file:
    log_file.write("\n" + log_message)


def get_submitted_course_work_list(classroom_id,
                                   user_email,
                                   course_work_id="-"):
  service = build("classroom", "v1", credentials=get_credentials())

  submitted_course_work_list = service.courses().courseWork(
  ).studentSubmissions().list(
      courseId=classroom_id, courseWorkId=course_work_id,
      userId=user_email).execute()
  if submitted_course_work_list:
    submitted_course_work_list = submitted_course_work_list[
        "studentSubmissions"]
  return submitted_course_work_list


def post_grade_of_the_user(classroom_id,
                           course_work_id: str,
                           submission_id: str,
                           assigned_grade: float = None,
                           draft_grade: float = None):
  service = build("classroom", "v1", credentials=get_credentials())

  student_submission = {}

  if assigned_grade is not None:
    student_submission["assignedGrade"] = assigned_grade

  if draft_grade is not None:
    student_submission["draftGrade"] = draft_grade

  output = service.courses().courseWork().studentSubmissions().patch(
      courseId=classroom_id,
      courseWorkId=course_work_id,
      id=submission_id,
      updateMask="assignedGrade,draftGrade",
      body=student_submission).execute()

  return output


FINAL_JSON = []


def main(user_email, final_grade_percentage):
  print("user_email", user_email)
  for email in EMAILS_TO_BE_REPLACED:
    if email.get("zybooks_email") == user_email:
      write_log(
          f"replaced zybooks email {user_email} with clp email {email.get('clp_email')}",
          "data_collection_changes.txt")
      user_email = email.get("clp_email")

  if user_email in SKIP_EMAILS:
    write_log(f"skipping inactive student with {user_email}",
              "data_collection_changes.txt")
    return

  # get user id using email
  user_data = User.find_by_email(user_email)
  if not user_data:
    write_log(f"user with email not found {user_email}",
              "data_collection_errors.txt")
    return

  # query course enrollment to get section id, classroom id
  all_user_course_details = CourseEnrollmentMapping.find_by_user(
      user_data.user_id)
  user_course_details = None
  # # handle for multiple sections
  if len(all_user_course_details) > 1:
    for course in all_user_course_details:
      if "CSE110" in course.section.name:
        user_course_details = course
        break
  else:
    if all_user_course_details and "CSE110" in all_user_course_details[
        0].section.name:
      user_course_details = all_user_course_details[0]
    else:
      write_log(f"something wrong for student with email {user_email}",
                "data_collection_errors.txt")
      return

  if not user_course_details:
    return
  section_id = user_course_details.section.id
  # fetch lti assignment using the lti assignment title and context id/section id
  all_lti_assignments = LTIAssignment.collection.filter("context_id", "==",
                                                        section_id).fetch()

  lti_assignment = None
  for assignment in list(all_lti_assignments):
    # all_assignments.append(assignment)
    if assignment.lti_assignment_title in LTI_ASSIGNMENT_TITLE:
      lti_assignment = assignment
      break

  if lti_assignment is None:
    write_log(f"user found in section {user_course_details.section.name}",
              "data_collection_errors.txt")
  # send student submissions using course work id, grades and email

  lti_assignment_max_points = None
  if lti_assignment:
    lti_assignment_max_points = lti_assignment.max_points

  course_work_id = None
  if lti_assignment:
    course_work_id = lti_assignment.course_work_id
  data_to_append = {
      "user_id": user_data.user_id,
      "user_email": user_email,
      "section_id": section_id,
      "section_name": user_course_details.section.name,
      "lti_assignment_title": LTI_ASSIGNMENT_TITLE,
      "lti_max_points": lti_assignment_max_points,
      "course_work_id": course_work_id,
      "final_grade_percentage": final_grade_percentage,
      "classroom_id": user_course_details.section.classroom_id
  }

  FINAL_JSON.append(data_to_append)


FAILED_SUBMISSIONS = []


def push_grades(
    user_email,
    final_grade_percentage,
    lti_max_points,
    classroom_id,
    course_work_id,
):
  try:
    print(f"pushing grade for {user_email}")
    assigned_grade = draft_grade = (float(final_grade_percentage) *
                                    float(CLASSROOM_MAX_GRADE_PERCENTAGE)
                                   ) / float(ZYBOOKS_MAX_GRADE_PERCENTAGE)
    submissions = get_submitted_course_work_list(classroom_id, user_email,
                                                 course_work_id)
    if submissions:
      submission_id = submissions[0].get("id")
      output = post_grade_of_the_user(classroom_id, course_work_id,
                                      submission_id, assigned_grade,
                                      draft_grade)
      if not output:
        raise Exception("Output None")
      else:
        print(f"successfully pushed grade for {user_email}")
        message = f"submission completed for {user_email} with grades {assigned_grade}"
        write_log(message, "successful_submissions.txt")
  except Exception as e:
    print(f"failed to push grade for {user_email}")
    message = f"submission failed for {user_email} with error {e}"
    write_log(message, "unsuccessful_submissions.txt")
    FAILED_SUBMISSIONS.append({
        "user_email": user_email,
        "final_grade_percentage": str(final_grade_percentage),
        "lti_max_points": lti_max_points,
        "classroom_id": classroom_id,
        "course_work_id": course_work_id
    })


async def initiate_grade_push_process(data_list):
  with ThreadPoolExecutor(max_workers=150) as executor:
    # Set any session parameters here before calling `insert_claim`
    loop = asyncio.get_event_loop()
    tasks = []
    for grade_data in data_list:
      runner = loop.run_in_executor(
          executor, push_grades,
          *(grade_data.get("user_email"),
            grade_data.get("final_grade_percentage"),
            grade_data.get("lti_max_points"), grade_data.get("classroom_id"),
            grade_data.get("course_work_id")))
      tasks.append(runner)

    for response in await asyncio.gather(*tasks):  # pylint: disable=unused-variable
      pass


def async_push_grades(data_list):
  loop = asyncio.get_event_loop()
  future = asyncio.ensure_future(initiate_grade_push_process(data_list))
  loop.run_until_complete(future)


async def initiate_data_collection_process(data_list):
  with ThreadPoolExecutor(max_workers=200) as executor:
    loop = asyncio.get_event_loop()
    tasks = []
    for data in data_list:
      runner = loop.run_in_executor(
          executor, main,
          *(data.get("user_email"), data.get("final_grade_percentage")))
      tasks.append(runner)

    for response in await asyncio.gather(*tasks):  # pylint: disable=unused-variable
      pass


def async_fetch_data(data_list):
  loop = asyncio.get_event_loop()
  future = asyncio.ensure_future(initiate_data_collection_process(data_list))
  loop.run_until_complete(future)


def csv_operations():
  # Open the CSV file
  with open(CSV_FILE_NAME, 'r') as csv_file:
    # Create a CSV reader object
    csv_reader = csv.reader(csv_file)

    # Get the header row
    header = next(csv_reader)

    # Find the indices of the desired columns
    email_col = header.index('Primary Email')
    possible_grade_col = header.index('Possible Score')
    student_grade_col = header.index('Student Score')
    state = header.index('State')
    csv_data = []
    for row in csv_reader:
      csv_data.append({
          'email_col': row[email_col],
          'possible_grade_col': row[possible_grade_col],
          'student_grade_col': row[student_grade_col]
      })
    # Convert the CSV data to a list of dictionaries
    temp_dict = {}
    student_data = []
    for row in csv_data:
      found_in_iteration = False
      for iteration in csv_data:
        print(iteration["email_col"])
        if iteration["email_col"] == row["email_col"]:
          found_in_iteration = True
          if temp_dict.get(iteration["email_col"]):
            if temp_dict[
                iteration["email_col"]] < iteration["student_grade_col"]:
              temp_dict[iteration["email_col"]] = iteration["student_grade_col"]
          else:
            temp_dict[iteration["email_col"]] = iteration["student_grade_col"]
      if not found_in_iteration:
        temp_dict[row["email_col"]] = row["student_grade_col"]
    print("temp_dict", temp_dict)

    added_emails = []
    for row in csv_data:
      if row["email_col"] not in added_emails:
        added_emails.append(row["email_col"])
        largest_score_data = {
            'user_email': row["email_col"],
            'max_grade_percentage': row["possible_grade_col"],
            'final_grade_percentage': temp_dict[row["email_col"]]
        }
        student_data.append(largest_score_data)

  print(len(student_data))

  output_file_path = os.path.join(OUTPUT_DIR, 'output.json')
  with open(output_file_path, 'w') as json_file:
    json.dump(student_data, json_file, indent=4)


def add_remaining_students():
  with open("all_students_list.json") as f:
    all_students = json.load(f)
  output_file_path = os.path.join(OUTPUT_DIR, 'output.json')

  with open(output_file_path) as f:
    data = json.load(f)

  final_json = []
  for student_email in all_students:
    student_email_found = False
    for record in data:
      if record.get("user_email") == student_email:
        student_email_found = True
        final_json.append(record)

    if not student_email_found:
      final_json.append({
          'user_email': student_email,
          'max_grade_percentage': ZYBOOKS_MAX_GRADE_PERCENTAGE,
          'final_grade_percentage': "0"
      })
  print(len(final_json))
  with open(output_file_path, 'w') as json_file:
    # Write the data to the JSON file
    json.dump(final_json, json_file, indent=4)


# ______________________________________________________________________________
for assignment in ASSIGNMENTS:

  CSV_FILE_NAME = assignment.get("file_name")
  LTI_ASSIGNMENT_TITLE = assignment.get("lti_assignment_title")
  ZYBOOKS_MAX_GRADE_PERCENTAGE = assignment.get("zybooks_max_grade_percentage")
  CLASSROOM_MAX_GRADE_PERCENTAGE = assignment.get(
      "classroom_max_grade_percentage")
  OUTPUT_DIR = Path(CSV_FILE_NAME.split(".")[0])
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  FINAL_JSON = []
  FAILED_SUBMISSIONS = []
  grade_push_json_path = os.path.join(OUTPUT_DIR, 'data_for_grade_push.json')
  print("loading csv", CSV_FILE_NAME)
  csv_operations()

  add_remaining_students()

  print("fetching data from firestore")
  with open(os.path.join(OUTPUT_DIR, 'output.json')) as f:
    data = json.load(f)
    async_fetch_data(data)

  with open(grade_push_json_path, 'w', encoding='utf-8') as f:
    print(f"count of grades to be pushed for {LTI_ASSIGNMENT_TITLE}",
          len(FINAL_JSON))
    json.dump(FINAL_JSON, f, ensure_ascii=False, indent=4)

  print("pushing data to classroom")
  with open(grade_push_json_path) as f:
    data = json.load(f)
    async_push_grades(data)

    i = 0
    while i < 20:
      print("looping through failed submissions", i, len(FAILED_SUBMISSIONS))
      if len(FAILED_SUBMISSIONS) == 0 or len(FAILED_SUBMISSIONS) < 5:
        break
      data_to_push = copy.deepcopy(FAILED_SUBMISSIONS)
      FAILED_SUBMISSIONS = []
      async_push_grades(data_to_push)
      i += 1

    if len(FAILED_SUBMISSIONS) > 0:
      for submission in FAILED_SUBMISSIONS:
        push_grades(
            submission.get("user_email"),
            submission.get("final_grade_percentage"),
            submission.get("lti_max_points"), submission.get("classroom_id"),
            submission.get("course_work_id"))
