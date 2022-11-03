"""
Unit test for section.py
"""
from common.models import Section
from common.testing.example_objects import TEST_SECTION

def test_new_section():
  '''test for creating and loading a new section'''
  section=Section.from_dict(TEST_SECTION)

  assert section.name == TEST_SECTION["name"]
  assert section.section == TEST_SECTION["section"]
