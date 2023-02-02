"""Student API services"""

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