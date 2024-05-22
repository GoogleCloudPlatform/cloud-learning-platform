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
    "emilyn111@icloud.com"
]

ASSIGNMENTS = [{
    "file_name": "Individual_Assignments_01_report.csv",
    "lti_assignment_title": '💡 1.3 Apply (Zybooks 1.17 "Hello, World!" In Java)'
}, {
    "file_name":
        "Individual_Assignments_02_report.csv",
    "lti_assignment_title":
        "💡 2.5 Apply (Zybooks - 2.20, 2.21, 2.22 Individual Assignments)"
}, {
    "file_name": "Individual_Assignments_03_report.csv",
    "lti_assignment_title": "💡 3.5 Apply (Zybooks - 3.19 - 3.24)"
}, {
    "file_name": "Individual_Assignments_04_report.csv",
    "lti_assignment_title": "💡 4.5 Apply (Zybooks 4.6 - 4.11 & 5.8 - 5.12)"
}, {
    "file_name": "Individual_Assignments_05_report.csv",
    "lti_assignment_title": "💡 5.5 Apply (Zybooks - 6.24 - 6.32)"
}, {
    "file_name": "Individual_Assignments_06_report.csv",
    "lti_assignment_title": "💡 6.5 Apply (Zybooks - 7.8 - 7.14)"
}, {
    "file_name": "Individual_Assignments_07_report.csv",
    "lti_assignment_title": "💡 7.5 Apply (Zybooks - 8.16 - 8.25)"
}, {
    "file_name": "Individual_Assignments_08_report.csv",
    "lti_assignment_title": "💡 9.5 Apply (Zybooks - 9.24 - 9.32)"
}, {
    "file_name": "Individual_Assignments_09_report.csv",
    "lti_assignment_title": "💡10.4 Apply (Zybooks 10.31 - 10.39)"
}, {
    "file_name":
        "Individual_Assignments_10_report.csv",
    "lti_assignment_title":
        "💡 11.5 Apply (Zybooks - 11.12 - 11.17 & 12.8 - 12.13)"
}, {
    "file_name": "Individual_Assignments_11_report.csv",
    "lti_assignment_title": "💡 12.5 Apply (Zybooks - 13.22 - 13.28)"
}, {
    "file_name":
        "Individual_Assignments_12_report.csv",
    "lti_assignment_title":
        "💡 13.3 Apply (Zybooks - 14.11 Verde Valley Volleyball)"
}, {
    "file_name": "Individual_Assignments_13_report.csv",
    "lti_assignment_title": "💡 14.3 Apply (Zybooks - 15.6 Climate Data)"
}, {
    "file_name":
        "Lab_Challenge_01_report.csv",
    "lti_assignment_title":
        "🏗️ 2.4 Code (Zybooks - 2.19 Lab 01 - Properties of a Circle)"
}, {
    "file_name":
        "Lab_Challenge_02_report.csv",
    "lti_assignment_title":
        "🏗️ 3.4 Code (Zybooks - 3.18 Lab 02 - Painting a Wall)"
}, {
    "file_name":
        "Lab_Challenge_03_report.csv",
    "lti_assignment_title":
        "🏗️ 4.4 Code (Zybooks 5.7 Lab 03 - Truckloads of Asphalt)"
}, {
    "file_name":
        "Lab_Challenge_04_report.csv",
    "lti_assignment_title":
        "🏗️ 5.4 Code (Zybooks - 6.23 Lab 04 - Interstate Highway)"
}, {
    "file_name": "Lab_Challenge_05_report.csv",
    "lti_assignment_title": "🏗️ 6.4 Code (Zybooks - Lab 05 - 7.7 Proper Name)"
}, {
    "file_name": "Lab_Challenge_06_report.csv",
    "lti_assignment_title": "🏗️ 7.4 Code (Zybooks - 8.15 Lab 06 - Patty's Cakes"
}, {
    "file_name":
        "Lab_Challenge_07_report.csv",
    "lti_assignment_title":
        "🏗️ 9.4 Code (Zybooks - 9.19 - 9.23 Lab 07 (Parts 1-4) Rosie's Road Co.)"
}, {
    "file_name":
        "Lab_Challenge_08_report.csv",
    "lti_assignment_title":
        "🏗️ 10.3 Code (Zybooks - 10.26-10.30 Lab 08, Parts 1-5 - Arrays)"
}, {
    "file_name":
        "Lab_Challenge_09_report.csv",
    "lti_assignment_title":
        "🏗️ 11.4 Code (Zybooks - 12.7 Lab 09 - Normalize a Data File)"
}, {
    "file_name":
        "Lab_Challenge_10_report.csv",
    "lti_assignment_title":
        "🏗️ 12.4 Code (Zybooks - 13.21 Lab 10 - Kitty Class)"
}, {
    "file_name":
        "Reading_Activities_01_report.csv",
    "lti_assignment_title":
        "💻 1.2 Lesson  (Zybooks Chapter 1: What is Computer Science? )"
}, {
    "file_name":
        "Reading_Activities_02_report.csv",
    "lti_assignment_title":
        "💻 2.2 Lesson (Zybooks - Chapter 2: Data Types, Expressions & Variables  - Part 1)"
}, {
    "file_name":
        "Reading_Activities_03_report.csv",
    "lti_assignment_title":
        "💻 3.2 Lesson (Zybooks - Chapter 3: Data Types, Expressions & Variables - Part 2)"
}, {
    "file_name":
        "Reading_Activities_04_report.csv",
    "lti_assignment_title":
        "💻 4.2 Lesson (Zybooks Chapter 4: Console Input and Output & Chapter 5: Sequence)"
}, {
    "file_name":
        "Reading_Activities_05_report.csv",
    "lti_assignment_title":
        "💻 5.2 Lesson (Zybooks - Chapter 6 - Branches/Decisions)"
}, {
    "file_name":
        "Reading_Activities_06_report.csv",
    "lti_assignment_title":
        "💻 6.2 Lesson (Zybooks - Chapter 7 - Methods - Part 1)"
}, {
    "file_name":
        "Reading_Activities_07_report.csv",
    "lti_assignment_title":
        "💻 7.2 Lesson (Zybooks - Chapter 8 - Loops - Repetition)"
}, {
    "file_name":
        "Reading_Activities_08_report.csv",
    "lti_assignment_title":
        "💻 9.2 Lesson (Zybooks - Chapter 9: Methods - Part 2)"
}, {
    "file_name": "Reading_Activities_09_report.csv",
    "lti_assignment_title": "💻 10.1 Lesson (Zybooks - Chapter 10: Arrays)"
}, {
    "file_name":
        "Reading_Activities_10_report.csv",
    "lti_assignment_title":
        "💻 11.2 Lesson (Zybooks - Chapter 11 - Array Lists & Chapter 12 - File Input and Output)"
}, {
    "file_name":
        "Reading_Activities_11_report.csv",
    "lti_assignment_title":
        "💻 12.2 Lesson (Zybooks - Chapter 13 - Object Oriented Programming - Part 1)"
}, {
    "file_name":
        "Reading_Activities_12_report.csv",
    "lti_assignment_title":
        "💻 13.2 Lesson (Zybooks - Chapter 14 - Object Oriented Programming - Part 2)"
}, {
    "file_name":
        "Reading_Activities_13_report.csv",
    "lti_assignment_title":
        " 💻 14.2 Lesson (Zybooks - Chapter 15 - The End of the Beginning)"
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
    if assignment.lti_assignment_title == LTI_ASSIGNMENT_TITLE:
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
    assigned_grade = draft_grade = (float(final_grade_percentage) /
                                    100) * lti_max_points
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
    email_col = header.index('Primary email')
    grade_col = header.index('Percent grade')

    # Convert the CSV data to a list of dictionaries
    data = []
    for row in csv_reader:
      data.append({
          'user_email': row[email_col],
          'final_grade_percentage': row[grade_col]
      })
  output_file_path = os.path.join(OUTPUT_DIR, 'output.json')
  # Open a JSON file for writing
  with open(output_file_path, 'w') as json_file:
    # Write the data to the JSON file
    json.dump(data, json_file, indent=4)


# ______________________________________________________________________________
for assignment in ASSIGNMENTS:

  CSV_FILE_NAME = assignment.get("file_name")
  LTI_ASSIGNMENT_TITLE = assignment.get("lti_assignment_title")

  OUTPUT_DIR = Path(CSV_FILE_NAME.split(".")[0])
  OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
  FINAL_JSON = []
  FAILED_SUBMISSIONS = []
  print("loading csv", CSV_FILE_NAME)
  csv_operations()

  print("fetching data from firestore")
  with open(os.path.join(OUTPUT_DIR, 'output.json')) as f:
    data = json.load(f)
    async_fetch_data(data)

  grade_push_json_path = os.path.join(OUTPUT_DIR, 'data_for_grade_push.json')
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
