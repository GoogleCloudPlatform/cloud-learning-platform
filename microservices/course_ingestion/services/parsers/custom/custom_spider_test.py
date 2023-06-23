"""Tests for the Custom course extraction."""

import json
import os
import pytest
from services.parsers.custom.custom_spider import CustomSpider

LOCAL_FILENAME = "index.html#/"
LOCAL_FOLDER = "test_data"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_TOC_FILE = "{}/{}/toc.jl".format(BASE_DIR, LOCAL_FOLDER)

# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name
# pylint: disable=unspecified-encoding


@pytest.fixture()
def create_temp_folder():
  """creates temp folder"""
  if not os.path.exists(".tmp"):
    os.makedirs(".tmp")


@pytest.fixture()
def extract_content(create_temp_folder):
  """Create a crawler for a local file and return
  the extract json for the course."""
  url = f"file://{BASE_DIR}/{LOCAL_FOLDER}/{LOCAL_FILENAME}"
  output_file = ".tmp/output.json"
  parser = CustomSpider(
      url=url, toc_file=TEST_TOC_FILE, output_filename=output_file)
  parser.parse_homepage()
  with open(output_file, "r") as f:
    course = json.load(f)
  return course


def test_toc_extraction(extract_content):  # pylint: disable=redefined-outer-name
  """tests toc_extraction"""
  assert len(extract_content) == 8
  assert extract_content[0]["subCompetency"]["learningObjectives"][
      "learningUnits"][0]["title"] == "Introduction"
