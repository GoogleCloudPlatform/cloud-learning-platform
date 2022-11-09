'''
Unit test for cohort.py
'''
from common.models import Cohort,CourseTemplate
from common.testing.example_objects import TEST_COHORT,TEST_COURSE_TEMPLATE
from common.testing.firestore_emulator import client_with_emulator, firestore_emulator, clean_firestore

def test_new_cohort(client_with_emulator):
  """Test for creating and loading of a new cohort"""
  new_cohort = Cohort.from_dict(TEST_COHORT)
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  new_cohort.course_template=course_template
  new_cohort.save()
  new_cohort.uuid = new_cohort.id
  new_cohort.update()
  cohort=Cohort.find_by_uuid(new_cohort.uuid)
  assert cohort.name == TEST_COHORT["name"]
  assert cohort.max_student == TEST_COHORT["max_student"]

def test_delete_cohort(client_with_emulator):
  '''test for soft delete method'''
  new_cohort = Cohort.from_dict(TEST_COHORT)
  course_template = CourseTemplate.from_dict(TEST_COURSE_TEMPLATE)
  course_template.save()
  new_cohort.course_template = course_template
  new_cohort.save()
  new_cohort.uuid = new_cohort.id
  new_cohort.update()
  assert Cohort.archive_by_uuid("fakeuuid") == False, "Cohort not found"
  assert Cohort.archive_by_uuid(
      new_cohort.uuid) == True, "Cohort successfully deleted"
  