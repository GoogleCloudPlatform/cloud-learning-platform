"""Unit testing of LU inference"""
import sys
import pytest

# for firestore cleanup
# pylint: disable=unused-import
# disabling as we need to append path for common
# pylint: disable=wrong-import-position
sys.path.append("../../common/src")
from common.utils.errors import ResourceNotFoundException
from common.models import (Course, LearningObjective, Competency)
from testing.example_objects import (TEST_COMPETENCY, TEST_COURSE,
                                     TEST_LEARNING_OBJECTIVE,
                                     TEST_SUB_COMPETENCY)
from testing.firestore_emulator import clean_firestore, firestore_emulator
from unittest import mock
with mock.patch("google.cloud.logging.Client",
side_effect = mock.MagicMock()) as mok:
  from services.lo_inference import LearningObjectiveService

# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name


@pytest.fixture(name="get_lo_object")
def get_lo_object():
  """returns LO object"""
  lo_obj = LearningObjectiveService()
  return lo_obj


def test_create_learning_objective(clean_firestore, get_lo_object):
  """tests create_learning_objective"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  function_output = get_lo_object.create_learning_objective(
      sub_competency.id, TEST_LEARNING_OBJECTIVE)
  assert isinstance(function_output, dict)
  assert "id" in function_output


def test_get_learning_objective(clean_firestore, get_lo_object):
  """tests get_learning_objective"""
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
  function_output = get_lo_object.get_learning_objective(learning_objective.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == learning_objective.id


@pytest.mark.asyncio
async def test_update_learning_objective(clean_firestore, get_lo_object):
  """tests update_learning_objective"""
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
  updated_lo_fields = {
      "title": "Updated title",
      "parent_node": learning_objective.parent_node.ref.path
  }
  function_output = await get_lo_object.update_learning_objective(
      learning_objective.id, updated_lo_fields)
  assert isinstance(function_output, dict)
  assert function_output["id"] == learning_objective.id

  fetched_lo = LearningObjective.find_by_id(learning_objective.id)
  assert fetched_lo.title == updated_lo_fields["title"]


def test_delete_learning_objective(clean_firestore, get_lo_object):
  """tests delete_learning_objective"""
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
  function_output = get_lo_object.delete_learning_objective(
      learning_objective.id)
  assert function_output is None
  with pytest.raises(ResourceNotFoundException):
    LearningObjective.find_by_id(learning_objective.id)


def test_get_all_learning_objectives(clean_firestore, get_lo_object):
  """tests get_all_learning_objectives"""
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

  function_output = get_lo_object.get_all_learning_objectives(sub_competency.id)
  assert isinstance(function_output, list)
  assert len(function_output) == 1
