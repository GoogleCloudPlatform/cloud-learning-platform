"""Tests for the custom Toc extraction."""

import json
import os
import shutil
import pytest
from services.parsers.custom.toc_spider import CustomTOCSpider

LOCAL_FILENAME = "index.html"
LOCAL_FOLDER = "test_data"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument
# pylint: disable=unspecified-encoding



@pytest.fixture(scope="session", autouse=True)
def extract_toc():
  """Create a crawler for a local file and return
  the extract json for the table of contents."""
  url = f"file://{BASE_DIR}/{LOCAL_FOLDER}/{LOCAL_FILENAME}"
  output_file = ".tmp/toc.jl"
  parser = CustomTOCSpider(url=url, output_filename=output_file)
  parser.get_toc()
  with open(".tmp/toc.jl", "r") as f:
    toc = json.load(f)
  return toc


@pytest.fixture()
def cleanup(request):
  """Cleanup a testing directory once we are finished."""

  def remove_test_dir():
    shutil.rmtree(".tmp")

  request.addfinalizer(remove_test_dir)


def test_toc_extraction(extract_toc, cleanup):  # pylint: disable=redefined-outer-name
  """tests toc_extraction"""
  assert extract_toc["1"]["comptency"] == ""
  assert extract_toc["1"]["sub_comptency"] ==\
     "Foundations of Sociology Introduction"
