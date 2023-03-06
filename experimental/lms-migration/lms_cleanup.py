import os
import pandas as pd
from common.models import CourseTemplate,Cohort,Section
# from common.src.common.models import CourseTemplate,Section,Cohort
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
# SCOPES=["https://www.googleapis.com/auth/classroom.courses"]
# ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")
# creds = service_account.Credentials.from_service_account_file(
#     os.environ["SA_KEY"], scopes=SCOPES)
# creds = creds.with_subject(ADMIN_EMAIL)
# def delete_course(course_id):
#   service = build("classroom", "v1", credentials=creds)

#   try:
#     result=service.courses().delete(id=course_id)
#     print(f"Course deleted: {course_id}, {result}")
#   except HttpError as error:
#     print(f"An error occurred: {error}")
#     return error

def main():
  list_course_template=[
    "course_templates/T431YTn9twQfDPw9fgBe",
    "course_templates/mS2fVKuWkL9qZYlyRxG3",
    "course_templates/ti1j7NGGLeIbeKN5wobQ",
    "course_templates/srFHPXaxE4jV6d4EUdkV",
    "course_templates/6OPUslqDXCbZciZ5dBco"
  ]
  course_template_list=[]
  cohort_list=[]
  section_list=[]
  try:
    course_templates=list(CourseTemplate.collection.fetch())
    # print(len(course_templates))
    for course_template in course_templates:
      # print(course_template.key)
      if course_template.key not in list_course_template:
        cohorts = list(Cohort.collection.filter(
            "course_template", "==", course_template.key).fetch())
        sections = list(Section.collection.filter(
            "course_template", "==", course_template.key).fetch())
        for cohort in cohorts:
          # print(cohort.to_dict())
          cohort_list.append({"Name": cohort.name, "key": cohort.key,
                             "course_template_name": cohort.course_template.name,"course_template_key":cohort.course_template.key})
          # Cohort.collection.delete(cohort.key)
        print("\n-----------------------------------------\nSections:")
        for section in sections:
          section_list.append({"Name": section.name, "key": section.key,
                              "course_template_name": section.course_template.name, "course_template_key": section.course_template.key, "cohorts_name":section.cohort.name,"cohort_key": section.cohort.key})
          # delete_course(section.classroom_id)
          # Section.collection.delete(section.key)
        print("\n-----------------------------------------\nCourseTemplate:")
        course_template_list.append({"Name": course_template.name, "key": course_template.key})
        # delete_course(course_template.classroom_id)
        # CourseTemplate.collection.delete(course_template.key)
    df_course_template = pd.DataFrame(data=course_template_list)
    df_cohort = pd.DataFrame(data=cohort_list)
    df_section = pd.DataFrame(data=section_list)
    # convert into excel
    df_course_template.to_excel("course_template.xlsx", index=False)
    df_cohort.to_excel("cohort.xlsx", index=False)
    df_section.to_excel("section.xlsx", index=False)
    print("Dictionary converted into excel...")
  except Exception as e:
    print(f"Error occured: {e}")
main()