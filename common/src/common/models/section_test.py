"""
Unit test for section.py
"""
from common.models import Section,CourseTemplate,Cohort
from common.testing.example_objects import TEST_SECTION,TEST_COURSE_TEMPLATE,TEST_COHORT
from common.testing.firestore_emulator import clean_firestore,client_with_emulator,firestore_emulator

def test_new_section(client_with_emulator):
  '''test for creating and loading a new section'''
  new_section = Section.from_dict(TEST_SECTION)
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  cohort = Cohort.from_dict(TEST_COHORT)
  cohort.course_template=course_template
  cohort.save()
  new_section.course_template = course_template
  new_section.cohort = cohort
  new_section.save()
  new_section.uuid = new_section.id
  new_section.update()
  section=Section.find_by_uuid(new_section.uuid)
  assert section.name == TEST_SECTION["name"]
  assert section.section == TEST_SECTION["section"]
  

def test_delete_section(client_with_emulator):
  '''test for soft delete method'''
  new_section = Section.from_dict(TEST_SECTION)
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  cohort=Cohort.from_dict(TEST_COHORT)
  cohort.course_template = course_template
  cohort.save()
  new_section.course_template=course_template
  new_section.cohort=cohort
  new_section.save()
  new_section.uuid = new_section.id
  new_section.update()
  assert Section.archive_by_uuid("fakeuuid") == False, "Section not found"
  assert Section.archive_by_uuid(
      new_section.uuid) == True, "Section successfully deleted"
