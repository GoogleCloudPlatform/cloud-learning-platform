""" Helper Functions"""

def convert_cohort_to_cohort_model(cohort):
  """Convert Cohort Object to Cohort Model Object

  Args:
    cohort (Cohort): Cohort Object.
  Returns:
    return a dict in the cohort model format.
  """ ""
  loaded_cohort = cohort.to_dict()
  course_template = loaded_cohort.pop("course_template").to_dict()
  loaded_cohort["course_template"] = course_template["key"]
  loaded_cohort["course_template_name"] = course_template["name"]
  return loaded_cohort


def convert_section_to_section_model(section):
  """Convert Section Object to Section Model Object

  Args:
    section (Section): Section Object.
  Returns:
    return a dict in the section model format.
  """ ""
  loaded_section = section.to_dict()
  course_template = loaded_section.pop("course_template").to_dict()
  loaded_section["course_template"] = course_template["key"]
  cohort = loaded_section.pop("cohort").to_dict()
  loaded_section["cohort"] = cohort["key"]
  return loaded_section

