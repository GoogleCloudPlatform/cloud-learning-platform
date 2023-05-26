"""
  Script to create teacher course enrollment mapping from teacher list
"""

# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common.models import CourseEnrollmentMapping, Section, User
from common.utils.errors import ResourceNotFoundException


def create_teacher_course_enrollment_mapping(teacher, section):
  """save course enrollment mapping"""
  user = User.find_by_email(teacher.lower())
  if user:
    if not CourseEnrollmentMapping.check_enrollment_exists_section(
        section.key, user.id):
      try:
        course_enrollment_mapping = CourseEnrollmentMapping()
        course_enrollment_mapping.section = section
        course_enrollment_mapping.role = "faculty"
        course_enrollment_mapping.user = User.find_by_user_id(user.user_id)
        course_enrollment_mapping.status = "active"
        course_enrollment_mapping.save()
        print(f"Teacher {teacher} is enrrolled in {section.id}" +
              f" section using this {course_enrollment_mapping.id} mapping")
      except ResourceNotFoundException as re:
        print(str(re))
      except Exception as e:
        print(str(e))
    else:
      print("Mapping already exsists for this user" +
            f" {teacher} in this section {section.id}")
  else:
    print(f"User not found by this {teacher} email. Section {section.id}")


def main():
  print("Started Script")
  # Use a service account.
  cred = credentials.Certificate("service_creds.json")

  firebase_admin.initialize_app(cred)

  db = firestore.client()
  enrollment_ref = db.collection(Section.collection_name)
  docs = enrollment_ref.stream()
  for doc in docs:
    section_dict = doc.to_dict()
    if "teachers" in section_dict.keys():
      for teacher in section_dict["teachers"]:
        section = Section.find_by_id(doc.id)
        create_teacher_course_enrollment_mapping(teacher, section)


if __name__ == "__main__":
  main()
