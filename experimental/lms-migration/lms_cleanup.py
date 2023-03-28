"""
Lms cleanup script
"""
# disabling for linting to pass
# pylint: disable = broad-except
import os
import json
# import pandas as pd
from common.models import CourseTemplate,Cohort,Section
# from common.src.common.models import CourseTemplate,Section,Cohort
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
SCOPES=[
  "https://www.googleapis.com/auth/classroom.courses",
  "https://www.googleapis.com/auth/drive"
        ]
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")
creds = service_account.Credentials.from_service_account_info(
    json.loads(os.environ["SA_KEY"]), scopes=SCOPES)
creds = creds.with_subject(ADMIN_EMAIL)
def get_course(course_id):
  service = build("classroom", "v1", credentials=creds)
  try:
    return service.courses().get(id=course_id)
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error
def delete_course(course_id):
  service = build("classroom", "v1", credentials=creds)

  try:
    result=service.courses().delete(id=course_id)
    print(f"Course deleted: {course_id}, {result}")
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

def delete_drive_folder(folder_id):
  service= build("drive", "v3", credentials=creds)
  try:
    result=service.files().delete(fileId=folder_id).execute()
    print(f"Delete drive folder initiated {result}")
  except HttpError as error:
    print(f"An error occured: {error}")
    return error

def initiate_delete_classroom(classroom_id):
  try:
    course=get_course(classroom_id)
    delete_drive_folder(course["teacherFolder"]["id"])
    delete_course(course["id"])
  except HttpError as error:
    print(f"An error occured: {error}")

def main():
  list_course_template=[
  ]

  # for excel sheet
  # course_template_list=[]
  # cohort_list=[]
  # section_list=[]
  try:
    course_templates=list(CourseTemplate.collection.fetch())
    for course_template in course_templates:
      if course_template.key not in list_course_template:
        cohorts = list(Cohort.collection.filter(
            "course_template", "==", course_template.key).fetch())
        sections = list(Section.collection.filter(
            "course_template", "==", course_template.key).fetch())
        for cohort in cohorts:
          # for excel
          # cohort_list.append({
          # "Name": cohort.name,
          # "key": cohort.key,
          # "course_template_name": cohort.course_template.name,
          # "course_template_key":cohort.course_template.key
          # })
          Cohort.collection.delete(cohort.key)
        print("Deleted all cohort inside this course template:"+
              f" {course_template.id}")
        for section in sections:
          # section_list.append(
          #   {
          #     "Name": section.name, "key": section.key,
          #     "course_template_name": section.course_template.name,
          #     "course_template_key": section.course_template.key,
          #     "cohorts_name":section.cohort.name,
          #     "cohort_key": section.cohort.key
          #   }
          #   )
          initiate_delete_classroom(section.classroom_id)
          Section.collection.delete(section.key)
        print("Deleted all sections and classroom inside this course template:"+
          f" {course_template.id}")
        # for excel sheet
        # course_template_list.append(
        #   {"Name": course_template.name,
        #   "key": course_template.key})
        initiate_delete_classroom(course_template.classroom_id)
        CourseTemplate.collection.delete(course_template.key)
        print(f"Deleted Course template: {course_template.id}")
    # for excel sheet
    # df_course_template = pd.DataFrame(data=course_template_list)
    # df_cohort = pd.DataFrame(data=cohort_list)
    # df_section = pd.DataFrame(data=section_list)
    # # convert into excel
    # df_course_template.to_excel("course_template.xlsx", index=False)
    # df_cohort.to_excel("cohort.xlsx", index=False)
    # df_section.to_excel("section.xlsx", index=False)
    # print("Dictionary converted into excel...")
  except HttpError as hte:
    print(f"Error occured: {hte}")
  except Exception as e:
    print(f"Error occured: {e}")

if __name__=="__main__":
  main()
