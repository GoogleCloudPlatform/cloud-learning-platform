'''
Unit test for cohort.py
'''
from common.models import Cohort
from common.testing.example_objects import TEST_COHORT

def test_new_cohort():
  """Test for creating and loading of a new cohort"""
  cohort=Cohort.from_dict(TEST_COHORT)

  assert cohort.name == TEST_COHORT["name"]
  assert cohort.max_student == TEST_COHORT["max_student"]
  