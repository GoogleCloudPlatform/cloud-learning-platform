"""Unit testing of LU inference"""
import sys
import pytest

# for firestore cleanup
# pylint: disable=unused-import
# disabling as we need to append path for common
# pylint: disable=wrong-import-position
sys.path.append("../../common/src")
from common.utils.errors import ResourceNotFoundException
from common.models import (Course, Competency, LearningUnit)
from testing.example_objects import (TEST_COMPETENCY, TEST_COURSE,
                                     TEST_LEARNING_OBJECTIVE,
                                     TEST_LEARNING_UNIT, TEST_SUB_COMPETENCY)
from testing.firestore_emulator import clean_firestore, firestore_emulator
from unittest import mock
with mock.patch("google.cloud.logging.Client",
side_effect = mock.MagicMock()) as mok:
  from services.lu_inference import LearningUnitService
from unittest.mock import MagicMock

# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name


@pytest.fixture(name="get_lu_object")
def get_lu_object():
  """returns LU object"""
  lu_obj = LearningUnitService()
  return lu_obj


def test_create_learning_unit(mocker, clean_firestore, get_lu_object):
  """tests create_learning_unit"""
  mocker.patch(
      "services.lu_inference.TripleService.generate_triples", return_value=[[]])
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  function_output = get_lu_object.create_learning_unit(learning_objective.id,
                                                       TEST_LEARNING_UNIT)
  assert isinstance(function_output, dict)
  assert "id" in function_output


def test_get_learning_unit(mocker, clean_firestore, get_lu_object):
  """tests get_learning_unit"""
  mocker.patch(
      "services.lu_inference.TripleService.generate_triples", return_value=[[]])
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
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
  function_output = get_lu_object.get_learning_unit(learning_unit.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == learning_unit.id


class AsyncMock(MagicMock):  #pylint: disable=invalid-overridden-method
  #pylint: disable=useless-super-delegation
  #pylint: disable=invalid-overridden-method
  async def __call__(self, *args, **kwargs):
    return super(AsyncMock, self).__call__(*args, **kwargs)  #pylint: disable=super-with-arguments


@pytest.mark.asyncio
async def test_update_learning_unit(clean_firestore, mocker, get_lu_object):
  """tests update_learning_unit"""
  mocker.patch(
      "services.lu_inference.get_blooms_titles",
      return_value=[["updated title"]])
  mocker.patch(
      "services.lu_inference.TripleService.generate_triples", return_value=[[]])
  mocker.patch(
      "services.lu_inference.compress_text_for_title_generation",
      new_callable=AsyncMock,
      return_value="compressed text")
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
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
  updated_lu_fields = {"label": "updated title", "text": ["updated text"]}
  function_output = await get_lu_object.update_learning_unit(
      learning_unit.id, updated_lu_fields)
  assert isinstance(function_output, dict)
  assert function_output["id"] == learning_unit.id

  fetched_lu = LearningUnit.find_by_id(learning_unit.id)
  assert fetched_lu.title == "updated title"
  assert fetched_lu.text == updated_lu_fields["text"][0]


def test_delete_learning_unit(clean_firestore, get_lu_object):
  """tests delete_learning_unit"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
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
  function_output = get_lu_object.delete_learning_unit(learning_unit.id)
  assert function_output is None
  with pytest.raises(ResourceNotFoundException):
    LearningUnit.find_by_id(learning_unit.id)


def test_get_all_learning_units(clean_firestore, get_lu_object):
  """tests get_all_learning_units"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
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

  function_output = get_lu_object.get_all_learning_units(learning_objective.id)
  assert isinstance(function_output, list)
  assert len(function_output) == 1


@pytest.mark.asyncio
async def test_create_lu_from_lo(mocker, get_lu_object):
  """tests create lu from lo"""
  mocker.patch(
      "services.lu_inference.LearningUnitService.add_triples", return_value=[])
  mocker.patch(
      "services.lu_inference.update_clustering_collections",
      new_callable=AsyncMock)
  mocker.patch(
      "services.lu_inference.create_recursive_topic_tree",
      new_callable=AsyncMock,
      return_value=[])
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  function_output = await get_lu_object.\
  create_lu_from_lo(learning_objective.id, {})
  assert isinstance(function_output, dict)
  assert "response" in function_output
