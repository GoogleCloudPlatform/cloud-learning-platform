'''
Unit test for cohort.py
'''
from common.models import Cohort
from common.testing.example_objects import TEST_COHORT

def test_new_cohort():
  """Test for creating and loading of a new cohort"""
  cohort=Cohort.from_dict(TEST_COHORT)

  assert cohort.cohort_name == TEST_COHORT["cohort_name"]
  assert cohort.cohort_max_student == TEST_COHORT["cohort_max_student"]
  