"""Student Helper Functions"""


def convert_course_enrollment_course_enrollment_model(course_enrollment):
  """Convert Course Enrollment object to Course Enrollment Model"""
  course_enrollment_model = course_enrollment.to_dict()
  course_enrollment_model["course_enrollment_id"] = course_enrollment_model[
      "id"]
  section = course_enrollment_model.pop("section").to_dict()
  course_enrollment_model["section_id"] = section["id"]
  course_enrollment_model["classroom_url"] = section["classroom_url"]
  course_enrollment_model["classroom_id"] = section["classroom_id"]
  course_enrollment_model["cohort_id"] = section["cohort"].to_dict()["id"]
  user = course_enrollment_model.pop("user").to_dict()
  course_enrollment_model["enrollment_status"] = course_enrollment_model.pop(
      "status")
  course_enrollment_model.update(user)
  return course_enrollment_model
