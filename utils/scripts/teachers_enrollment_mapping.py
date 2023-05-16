"""
  Script to create teacher course enrollment mapping from teacher list
"""

# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except
from common.models import CourseEnrollmentMapping,TempUser,Section,User
from common.utils.errors import ResourceNotFoundException

def create_teacher_course_enrollment_mapping(teacher,section):
  """save course enrollment mapping"""
  user=TempUser.find_by_email(teacher.lower())
  if user:
    if not CourseEnrollmentMapping.check_enrollment_exists_section(
      section.key,user.id):
      try:
        course_enrollment_mapping=CourseEnrollmentMapping()
        course_enrollment_mapping.section=section
        course_enrollment_mapping.role=user.user_type
        course_enrollment_mapping.user=User.find_by_user_id(user.user_id)
        course_enrollment_mapping.status="active"
        course_enrollment_mapping.save()
        print(f"Teacher {teacher} is enrrolled in {section.id}"+
              f" section using this {course_enrollment_mapping.id} mapping")
      except ResourceNotFoundException as re:
        print(str(re))
      except Exception as e:
        print(str(e))
    else:
      print("Mapping already exsists for this user"+
            f" {teacher} in this section {section.id}")
  else:
    print(f"User not found by this {teacher} email. Section {section.id}")

def main():
  print("Started Script")
  sections=Section.fetch_all()
  for section in sections:
    for teacher in section.teachers:
      create_teacher_course_enrollment_mapping(teacher,section)

if __name__=="__main__":
  # main()
  print(CourseEnrollmentMapping.find_by_id("oYmRtuZqwvmhwyt0herC").to_dict())
