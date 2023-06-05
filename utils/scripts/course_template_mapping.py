"""
  Script to create teacher course template enrollment mapping
  from  instructional designer
"""

# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common.models import CourseTemplateEnrollmentMapping, CourseTemplate, User
from common.utils.errors import ResourceNotFoundException

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")


def create_course_template_enrollment_mapping(teacher, course_template):
  """save course template enrollment mapping"""
  user = User.find_by_email(teacher.lower())
  if user:
    if not CourseTemplateEnrollmentMapping.find_enrolled_active_record(
        course_template.key, user.id):
      try:
        course_enrollment_mapping = CourseTemplateEnrollmentMapping()
        course_enrollment_mapping.course_template = course_template
        course_enrollment_mapping.role = "faculty"
        course_enrollment_mapping.user = User.find_by_user_id(user.user_id)
        course_enrollment_mapping.status = "active"
        course_enrollment_mapping.save()
        print(f"Instructional designer {teacher} is enrrolled in" +
              f" {course_template.id} course template using" +
              f" this {course_enrollment_mapping.id} mapping")
      except ResourceNotFoundException as re:
        print(str(re))
      except Exception as e:
        print(str(e))
    else:
      print("Mapping already exsists for this user" +
            f" {teacher} in this course template {course_template.id}")
  else:
    print(f"User not found by this {teacher} email." +
          f" Course Template {course_template.id}")


def main():
  print("Started Script")
  # Use a service account.
  cred = credentials.Certificate("service_creds.json")

  firebase_admin.initialize_app(cred)

  db = firestore.client()
  collection_name = CourseTemplate.collection_name
  enrollment_ref = db.collection(collection_name)
  docs = enrollment_ref.stream()
  for doc in docs:
    course_template_dict = doc.to_dict()
    if "instructional_designer" in course_template_dict.keys():
      course_template = CourseTemplate.find_by_id(doc.id)
      create_course_template_enrollment_mapping(
          course_template_dict["instructional_designer"], course_template)


if __name__ == "__main__":
  main()
