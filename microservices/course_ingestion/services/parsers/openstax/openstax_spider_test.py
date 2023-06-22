"""Tests for the OpenStax Spider crawler extraction."""

import json
import os
import shutil
import pytest
from .openstax_spider import parse_content

# pylint: disable=unspecified-encoding

TESTING_DIR = "testing_dir"
TEST_FILE = "bio101_competencties.json"
TEST_FILE_PATH = "{}/{}".format(TESTING_DIR, TEST_FILE)
LOCAL_FILENAME = "1-1-themes-and-concepts-of-biology.html"
LOCAL_FOLDER = "test_data"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_TOC_FILE = "{}/toc.jl".format(LOCAL_FOLDER)


@pytest.fixture(scope="session", autouse=True)
def competencies():
  """Create a crawler for a local file and return
  the extract json and table of contents."""
  parse_content(
      url=f"file://{BASE_DIR}/{LOCAL_FOLDER}/{LOCAL_FILENAME}",
      toc_file=".tmp/toc.jl",
      output_file=".tmp/output.json")
  with open(".tmp/output.json", "r") as f:
    competences_json = json.load(f)
  return competences_json


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
  """Cleanup a testing directory once we are finished."""

  def remove_test_dir():
    shutil.rmtree(".tmp")

  request.addfinalizer(remove_test_dir)


def test_competency_extraction(competencies):  # pylint: disable=redefined-outer-name
  """tests crawler output json"""
  assert len(competencies) == 1
  assert competencies[0]["competency"] == "The Cellular Foundation of Life"
  assert competencies[0]["subCompetency"]["title"] == "Introduction to Biology"
  assert competencies[0]["subCompetency"]["learningObjectives"][
      "title"] == "Themes and Concepts of Biology"
