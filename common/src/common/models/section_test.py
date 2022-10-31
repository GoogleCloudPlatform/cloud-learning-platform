"""
Unit test for section.py
"""
from common.models import Section
from common.testing.example_objects import TEST_SECTION

def test_new_section():
  '''test for creating and loading a new section'''
  section=Section.from_dict(TEST_SECTION)

  assert section.section_name == TEST_SECTION["section_name"]
  assert section.section_sec == TEST_SECTION["section_sec"]
