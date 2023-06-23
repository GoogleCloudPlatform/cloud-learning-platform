# pylint: disable=line-too-long
# disabling as we need to append path for common
# pylint: disable=wrong-import-position
"""Test file for import learning_content"""

import pytest
import sys

sys.path.append("../../common/src")
from unittest import mock
with mock.patch("google.cloud.logging.Client",
side_effect = mock.MagicMock()) as mok:
  from services import import_learning_content
# for firestore cleanup
# pylint: disable=unused-import
from common.models import (LearningContentItem, Competency, SubCompetency,
                           LearningObjective, LearningUnit)
from testing.firestore_emulator import clean_firestore, firestore_emulator
from testing.example_objects import (TEST_COMPETENCY, TEST_LEARNING_CONTENT,
                                     TEST_LEARNING_OBJECTIVE,
                                     TEST_LEARNING_UNIT, TEST_SUB_COMPETENCY)
from unittest.mock import MagicMock
from config import GCP_PROJECT


# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name
@pytest.fixture(name="mocked_get_topics")
def fixture_mocked_get_topics():
  """mocks get_topics"""
  return [["sample_topic", 0.912334]]


class AsyncMock(MagicMock):  #pylint: disable=invalid-overridden-method
  #pylint: disable=useless-super-delegation
  #pylint: disable=invalid-overridden-method
  async def __call__(self, *args, **kwargs):
    return super(AsyncMock, self).__call__(*args, **kwargs)  #pylint: disable=super-with-arguments


@pytest.mark.parametrize(
    "learning_content_title,gcs_path,learning_content_label, \
    start_page,end_page,parsed_output_json",
    [("test_learning_content", "gs://" + GCP_PROJECT + "/abc", "test_label",1, 2, "testing/test_output.json")])
def test_create_learning_content_collections(clean_firestore,
                                             learning_content_title,
                                             gcs_path,
                                             learning_content_label,
                                             start_page,
                                             end_page,
                                             parsed_output_json):
  """Unit tests for creating learning_content collections"""
  result = import_learning_content.create_learning_content_collections(
      learning_content_title, gcs_path, learning_content_label, \
      start_page, end_page, parsed_output_json)
  assert result.isalnum()


@pytest.mark.parametrize(
    "learning_content_title, gcs_path, learning_content_label, \
    start_page, end_page, parsed_output_json",
    [("test_learning_content", "gs://" + GCP_PROJECT + "/abc", "test_label",
      1, 2, "testing/sample_clustering_output.json")])
def test_create_clustering_learning_content_collections(clean_firestore,
                                                        learning_content_title,
                                                        learning_content_label,
                                                        gcs_path,
                                                        start_page,
                                                        end_page,
                                                        parsed_output_json):
  """Unit tests for creating learning_content collections using clustering"""
  result = import_learning_content.create_clustering_learning_content_collections(
      learning_content_title, learning_content_label, gcs_path, \
      start_page, end_page, learning_content_label, parsed_output_json)
  assert result.isalnum()


@pytest.mark.asyncio
@pytest.mark.parametrize("level,items", [("learning_objective", [{
    "title": "New LU",
    "text": "This is a sample paragraph",
    "triples": []
}])])
async def test_update_clustering_collections(mocker, clean_firestore, level,
                                             items, mocked_get_topics):
  """Unit tests for updating learning_content collections"""
  mocker.patch(
      "services.import_learning_content.get_topics",
      return_value=mocked_get_topics)
  mocker.patch(
      "services.import_learning_content.compress_text_for_title_generation",
      new_callable=AsyncMock,
      return_value="summarised text")
  mocker.patch(
      "services.import_learning_content.get_blooms_titles",
      return_value=[["updated title"]])

  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.competency_ids = [competency.id]
  learning_content.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  learning_unit = learning_objective.add_learning_unit_from_dict(
      TEST_LEARNING_UNIT)
  learning_unit.save()
  result = await import_learning_content.update_clustering_collections(
      level, learning_objective.id, items)
  assert result == "successfully updated learning objective child nodes"
