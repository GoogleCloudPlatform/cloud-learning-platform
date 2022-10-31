from common.models import Section
from common.testing.example_objects import TEST_SECTION

def test_new_section():
  # a placeholder unit test so github actions runs until we add more
  section=Section.from_dict(TEST_SECTION)
  assert section.section_name == TEST_SECTION["section_name"]
  assert section.section_sec == TEST_SECTION["section_sec"]