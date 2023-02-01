def get_section_with_minimum_student(sections):
  """Get section with minimum count of students 
  Args:
  sections :list of section objects with same cohort 
  Returns: sectioons object with minimum count of studnet

  """ 
  print("INSIDE GET MIN STUDNET SECTIOn",sections)
  min_sections_count_mapping = {}
  min_student = 0
  for i in sections:
    print("------------------")
    print(i.id , i.count)
    print("------------------------")
    if min_sections_count_mapping =={}:
      min_sections_count_mapping = i
      min_student =  i.count
    else :
      if i.count < min_student:
          print("In  IF UPDATE " ,i.count , min_student)
          min_student =i.count
          min_sections_count_mapping = i
  return min_sections_count_mapping