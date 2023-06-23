# pylint: disable=unused-argument
"""Test cases for custom html paragraph parser"""

import pytest
import json
import os
from services.parsers.custom.custom_html_paragraph_parser import CustomHtmlParser

LOCAL_FILENAME = "index.html#/"
LOCAL_FOLDER = "test_data"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_OUTPUT_FILE = "{}/{}/output_para.json".format(BASE_DIR, LOCAL_FOLDER)


#pylint: disable=redefined-outer-name
# pylint: disable=unspecified-encoding

@pytest.fixture()
def create_temp_folder():
  if not os.path.exists(".tmp"):
    os.makedirs(".tmp")


@pytest.fixture()
def parser_object(create_temp_folder):
  """Create a crawler"""
  url = f"file://{BASE_DIR}/{LOCAL_FOLDER}/{LOCAL_FILENAME}"
  url += "lessons/3qBQkPVgfNYvkcQ0jqF5J4LC4gu0nYM4"
  output_filename = ".tmp/output.json"
  obj = CustomHtmlParser(url, output_filename)
  return obj


@pytest.mark.parametrize("text, output",
                         [("This is title", ""),
                          ("This is sentence one. This is sentence two",
                           "This is sentence one. This is sentence two")])
def test_remove_heading(text, output, parser_object):
  function_output = parser_object.remove_heading(text)
  assert function_output == output


@pytest.mark.parametrize("text, output, mocked_remove_heading_output",
                         [("**test**", "", ""),
                          ("This is sentence one. This is sentence **two**",
                           ("This is sentence one. This is sentence two"),
                           ("This is sentence one. This is sentence two"))])
def test_clean_paragraphs(mocker, text, output, mocked_remove_heading_output,
                          parser_object):
  mocker.patch(
      "services.parsers.custom.custom_html_paragraph_parser."
      "CustomHtmlParser.remove_heading",
      return_value=mocked_remove_heading_output)
  function_output = parser_object.clean_paragraphs(text)
  assert function_output == output


def test_paragraph_extraction(parser_object):
  """extract from the content"""
  parser_object.get_paragraphs()
  with open(TEST_OUTPUT_FILE, "r") as f:
    test_paragraphs = json.load(f)
  assert isinstance(parser_object.paragraphs, list)
  assert test_paragraphs["paragraphs"] == parser_object.paragraphs
