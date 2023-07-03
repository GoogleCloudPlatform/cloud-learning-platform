"""test for topic tree inference"""
import pytest
import json
import ast
import sys

sys.path.append("../../common/src")
#pylint: disable=unused-import
# disabling as we need to append path for common
#pylint: disable=wrong-import-position
# pylint: disable=unspecified-encoding
from unittest import mock
with mock.patch("google.cloud.logging.Client",
side_effect = mock.MagicMock()) as mok:
  from services import topic_tree_inference
from common.models import Course, Competency
from testing.firestore_emulator import clean_firestore, firestore_emulator
from testing.example_objects import (TEST_COMPETENCY, TEST_COURSE,
                                     TEST_LEARNING_OBJECTIVE,
                                     TEST_LEARNING_UNIT, TEST_SUB_COMPETENCY)
from unittest.mock import MagicMock


@pytest.fixture(name="mocked_create_recursive_topic_tree")
def fixture_mocked_create_recursive_topic_tree():
  """mocks create_recursive_topic_tree"""
  with open("testing/sample_clustering_output.json") as f:
    topic_tree = ast.literal_eval(json.load(f))
  return topic_tree


class AsyncMock(MagicMock):  #pylint: disable=invalid-overridden-method
  #pylint: disable=useless-super-delegation
  #pylint: disable=invalid-overridden-method
  async def __call__(self, *args, **kwargs):
    return super(AsyncMock, self).__call__(*args, **kwargs)  #pylint: disable=super-with-arguments


#pylint: disable=unused-argument
#pylint: disable=redefined-outer-name
#pylint: disable=protected-access
@pytest.mark.asyncio
@pytest.mark.parametrize("inputs", [({"level": "course", "text": [""]})])
async def test_create_hierarchy(mocker, clean_firestore, inputs,
                                mocked_create_recursive_topic_tree):
  """tests create hierarchy"""
  mocker.patch(
      "services.topic_tree_inference.create_recursive_topic_tree",
      new_callable=AsyncMock,
      return_value=mocked_create_recursive_topic_tree)
  mocker.patch(
      "services.topic_tree_inference.update_clustering_collections",
      new_callable=AsyncMock,
      return_value="mocking_create_recursive_topic_tree")
  course = Course.from_dict(TEST_COURSE)
  course.save()
  inputs["id"] = course.id
  mocker.patch(
      "services.topic_tree_inference.get_parent_node_from_id",
      return_value=course)
  response = await topic_tree_inference.create_hierarchy(inputs)
  assert response == {"response": "mocking_create_recursive_topic_tree"}


@pytest.mark.parametrize("data, output", [({
    "level": "course",
    "id": "dfhadkfakf"
}, {
    "title": "test course",
    "label": "test label",
    "id": "dfhadkfakf"
})])
def test_get_complete_tree(mocker, data, output):
  """tests get_complete tree"""
  mocker.patch(
      "services.topic_tree_inference.get_tree_data", return_value=output)
  mocker.patch(
      "services.topic_tree_inference.get_tree_from_cache",
      return_value=None)
  mocker.patch(
      "services.topic_tree_inference.cache_topic_tree",
      return_value=None)
  function_output = topic_tree_inference.get_complete_tree(data)
  assert function_output == output


def test_get_tree_data(clean_firestore):
  """test to get_tree_data"""
  competency = Competency()
  for key, value in TEST_COMPETENCY.items():
    setattr(competency, key, value)
  competency.save()
  course = Course()
  for key, value in TEST_COURSE.items():
    setattr(course, key, value)
  course.competency_ids = [competency.id]
  course.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  learning_unit = learning_objective.add_learning_unit_from_dict(
      TEST_LEARNING_UNIT)
  learning_unit.save()
  function_output = topic_tree_inference.get_tree_data("course", course.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == course.id
  assert len(function_output["competencies"]) == 1
  assert function_output["competencies"][0]["id"] == competency.id
  assert len(function_output["competencies"][0]["sub_competencies"]) == 1
  assert function_output["competencies"][0]["sub_competencies"][0]["id"]\
    == sub_competency.id
  assert len(function_output["competencies"][0]["sub_competencies"][0]\
    ["learning_objectives"]) == 1
  assert function_output["competencies"][0]["sub_competencies"][0]\
    ["learning_objectives"][0]["id"] == learning_objective.id
  assert len(function_output["competencies"][0]["sub_competencies"][0]\
    ["learning_objectives"][0]["learning_units"]) == 1
  assert function_output["competencies"][0]["sub_competencies"][0]\
    ["learning_objectives"][0]["learning_units"][0]["id"] == learning_unit.id
