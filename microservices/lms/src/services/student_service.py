"""Student API services"""
import re
from common.utils import classroom_crud

def get_section_with_minimum_student(sections):
  """Get section with minimum count of students
  Args:
  sections :list of section objects with same cohort
  Returns: sectioons object with minimum count of studnet

  """
  min_sections_count_mapping = None
  min_student = 0
  for i in sections:
    if min_sections_count_mapping is None:
      min_sections_count_mapping = i
      min_student =  i.enrolled_students_count
    else :
      if i.enrolled_students_count < min_student:
        min_student =i.enrolled_students_count
        min_sections_count_mapping = i
  return min_sections_count_mapping

def get_user_id(user,headers):
  regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
  if re.fullmatch(regex, user):
    return classroom_crud.get_user_details_by_email(
        user_email=user, headers=headers)["data"][0]["user_id"]
  return user
  