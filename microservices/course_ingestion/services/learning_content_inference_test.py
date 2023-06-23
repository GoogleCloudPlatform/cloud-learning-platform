"""Test file for learning content inference"""
import pytest
# disabling as we need to append path for common
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
# pylint: disable=line-too-long
from config import PROJECT_ID
import sys

sys.path.append("../../common/src")
from utils.exception_handlers import LearningContentNotFound, \
  LearningContentIDMissing
from common.models import (LearningContentItem, LearningObjective, Competency)
from common.utils.errors import ResourceNotFoundException
from testing.example_objects import (TEST_LEARNING_CONTENT, TEST_COMPETENCY)
from testing.firestore_emulator import clean_firestore, firestore_emulator
from unittest.mock import MagicMock
from unittest import mock
with mock.patch("google.cloud.logging.Client",
side_effect = MagicMock()) as mok:
  from services import learning_content_inference

# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name
# pylint: disable=unspecified-encoding


@pytest.fixture(name="mocked_create_learning_content_collections")
def fixture_mocked_create_learning_content_collections():
  """mocks create_learning_content_collections"""
  return "sample_content_id"


@pytest.fixture(name="mocked_download_file_from_gcs")
def fixture_mocked_download_file_from_gcs():
  """mocks download_file_from_gcs"""
  return "testing/test.pdf"


@pytest.fixture(name="mocked_parse_content")
def fixture_mocked_parse_content():
  """mocks parse_content"""
  return ""


@pytest.fixture(name="mocked_create_recursive_topic_tree")
def fixture_mocked_create_recursive_topic_tree():
  """mocks create_recursive_topic_tree"""
  return [{"title": "Sample Title"}]


def test_clean_temp_folders():
  """tests clean_temp_folders"""
  learning_content_inference.clean_temp_folders()


def test_get_learning_content(clean_firestore):
  """tests get_learning_content"""
  with pytest.raises(ResourceNotFoundException):
    learning_content_inference.get_learning_content("test_id")

  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.save()
  function_output = learning_content_inference.get_learning_content(
      learning_content.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == learning_content.id
  with pytest.raises(ResourceNotFoundException):
    (learning_content_inference.get_learning_content("temp_learning_content_id")
    )


def test_get_all_learning_contents(clean_firestore):
  """tests get all learning_contents"""
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.save()
  function_output = learning_content_inference.get_all_learning_contents()
  assert isinstance(function_output, list)
  assert len(function_output) == 1


def test_delete_learning_content(clean_firestore):
  """tests delete_learning_content"""
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.save()
  # pylint: disable=assignment-from-no-return
  function_output = learning_content_inference.delete_learning_content(
      learning_content.id)
  assert function_output is None
  with pytest.raises(ResourceNotFoundException):
    LearningObjective.find_by_id(learning_content.id)


def test_update_learning_content(clean_firestore):
  """tests update_learning_content"""
  with pytest.raises(ResourceNotFoundException):
    learning_content_inference.update_learning_content("test_id", [])
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.save()
  with pytest.raises(Exception):
    learning_content_inference.update_learning_content(learning_content.id, [])
  updated_learning_content_fields = {
      **TEST_LEARNING_CONTENT, "title": "Updated title"
  }
  function_output = learning_content_inference.update_learning_content(
      learning_content.id, updated_learning_content_fields)
  assert isinstance(function_output, dict)
  assert function_output["id"] == learning_content.id


class AsyncMock(MagicMock):  #pylint: disable=invalid-overridden-method
  #pylint: disable=useless-super-delegation
  #pylint: disable=invalid-overridden-method
  async def __call__(self, *args, **kwargs):
    return super(AsyncMock, self).__call__(*args, **kwargs)  #pylint: disable=super-with-arguments


@pytest.mark.asyncio
@pytest.mark.parametrize("inputs", [({
    "title":
        "Research Design test 2",
    "gcs_path":
        "gs://{}/learning_content-resources/Research Design "
          "The Scholar-Practitioner’s Guide to Research "
            "Design.pdf".format(PROJECT_ID),
    "doc_type":
        "custom",
    "format":
        "pdf",
    "start_page": 1,
    "end_page": 2
})])
async def test_create_learning_content_using_clustering(
    mocker, clean_firestore, inputs, mocked_create_learning_content_collections,
    mocked_download_file_from_gcs, mocked_create_recursive_topic_tree):
  """tests create learning_content using clustering"""
  mocker.patch(
      "services.learning_content_inference.create_recursive_topic_tree",
      new_callable=AsyncMock,
      return_value=mocked_create_recursive_topic_tree)
  mocker.patch(
      "services.learning_content_inference.download_file_from_gcs",
      return_value=mocked_download_file_from_gcs)
  mocker.patch(
      "services.learning_content_inference"
        ".create_clustering_learning_content_collections",
      return_value=mocked_create_learning_content_collections)
  mocker.patch(
      "services.learning_content_inference.get_learning_content",
      return_value={"learning_content id": str("sample_learning_content_id")})
  result = await learning_content_inference \
    .create_learning_content_using_clustering(
      inputs)
  assert result == {"learning_content id": str("sample_learning_content_id")}


@pytest.mark.parametrize("inputs", [({
    "title":
        "Research Design test 2",
    "gcs_path":
        "gs://{}/learning_content-resources/Research "
          "Design/The Scholar-Practitioner’s Guide to Research Design.pdf" \
            .format(PROJECT_ID),
    "doc_type":
        "custom",
    "format":
        "pdf",
    "start_page": 1,
    "end_page": 2
})])
def test_create_learning_content_using_parser(
    mocker, clean_firestore, inputs, mocked_create_learning_content_collections,
    mocked_download_file_from_gcs, mocked_parse_content):
  """tests for creating learning_content using parser"""
  mocker.patch(
      "services.learning_content_inference.create_learning_content_collections",
      return_value=mocked_create_learning_content_collections)
  mocker.patch(
      "services.learning_content_inference.download_file_from_gcs",
      return_value=mocked_download_file_from_gcs)

  mocker.patch(
      "services.learning_content_inference.parse_content",
      return_value=mocked_parse_content)
  mocker.patch(
      "services.learning_content_inference.get_learning_content",
      return_value={"learning_content id": str("sample_learning_content_id")})
  result = learning_content_inference.create_learning_content_using_parser(
      inputs)
  assert result == {"learning_content id": str("sample_learning_content_id")}
  input_3 = {
      "title":
          "Research Design test 2",
      "gcs_path":
          "gs://{}/learning_content-resources/Research Design/"
          "The Scholar-Practitioner’s Guide to Research Design.pdf" \
              .format(PROJECT_ID),
      "doc_type":
          "others",
      "format":
          "pdf"
  }
  input_4 = {
      "title":
          "Research Design test 2",
      "gcs_path":
          "https://openstax.org/books/concepts-biology/"
            "pages/1-1-themes-and-concepts-of-biology",
      "doc_type":
          "others",
      "format":
          "html"
  }
  with pytest.raises(Exception):
    learning_content_inference.create_learning_content_using_parser(input_3)
    learning_content_inference.create_learning_content_using_parser(input_4)
  assert result == {"learning_content id": str("sample_learning_content_id")}


def test_add_competencies(clean_firestore):
  """tests add_competencies"""
  with pytest.raises(ResourceNotFoundException):
    learning_content_inference.add_competencies("test_id", [])
  lc = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  lc.save()
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  with pytest.raises(Exception):
    learning_content_inference.add_competencies(lc.id, None)
  function_output = learning_content_inference.add_competencies(
      lc.id, {"competency_ids": [competency.id]})
  assert isinstance(function_output, dict)
  assert function_output["id"] == lc.id
  assert function_output["competencies"][0]["id"] == competency.id
