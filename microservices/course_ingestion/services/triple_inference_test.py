"""Unit testing of Triple inference"""
import sys
import pytest

# for firestore cleanup
# pylint: disable=unused-import
# disabling as we need to append path for common
# pylint: disable=wrong-import-position
sys.path.append("../../common/src")
from common.utils.errors import ResourceNotFoundException
from common.models import (Competency, LearningUnit, Triple)
from testing.example_objects import (TEST_COMPETENCY, TEST_LEARNING_OBJECTIVE,
                                     TEST_LEARNING_UNIT, TEST_SUB_COMPETENCY,
                                     TEST_TRIPLE)
from testing.firestore_emulator import clean_firestore, firestore_emulator
from unittest import mock
with mock.patch("google.cloud.logging.Client",
side_effect = mock.MagicMock()) as mok:
  from services.triple_inference import TripleService

# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name


@pytest.fixture(name="get_triple_object")
def get_triple_object():
  """returns triple object"""
  triple_obj = TripleService()
  return triple_obj


def test_create_triple(clean_firestore, get_triple_object):
  """tests create_triple"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  learning_unit = learning_objective.add_learning_unit_from_dict(
      TEST_LEARNING_UNIT)
  learning_unit.save()
  function_output = get_triple_object.create_triple(learning_unit.id,
                                                    TEST_TRIPLE)
  assert isinstance(function_output, dict)
  assert "id" in function_output


def test_get_triple(clean_firestore, get_triple_object):
  """tests get_triple"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  learning_unit = learning_objective.add_learning_unit_from_dict(
      TEST_LEARNING_UNIT)
  learning_unit.save()
  triple = learning_unit.add_triple_from_dict(TEST_TRIPLE)
  triple.save()
  function_output = get_triple_object.get_triple(triple.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == triple.id


def test_update_triple(clean_firestore, get_triple_object):
  """tests update_triple"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  learning_unit = learning_objective.add_learning_unit_from_dict(
      TEST_LEARNING_UNIT)
  learning_unit.save()
  triple = learning_unit.add_triple_from_dict(TEST_TRIPLE)
  triple.save()
  updated_fields = {"subject": "updated subject", "object": "updated object"}
  function_output = get_triple_object.update_triple(triple.id, updated_fields)
  assert isinstance(function_output, dict)
  assert function_output["id"] == triple.id

  fetched_triple = Triple.find_by_id(triple.id)
  assert fetched_triple.subject == "updated subject"
  assert fetched_triple.object == "updated object"


def test_delete_triple(clean_firestore, get_triple_object):
  """tests delete_triple"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  learning_unit = learning_objective.add_learning_unit_from_dict(
      TEST_LEARNING_UNIT)
  learning_unit.save()
  triple = learning_unit.add_triple_from_dict(TEST_TRIPLE)
  triple.save()
  function_output = get_triple_object.delete_triple(triple.id)
  assert function_output is None
  with pytest.raises(ResourceNotFoundException):
    Triple.find_by_id(triple.id)


def test_get_all_triples(clean_firestore, get_triple_object):
  """tests get_all_triples"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  learning_unit = learning_objective.add_learning_unit_from_dict(
      TEST_LEARNING_UNIT)
  learning_unit.save()
  triple = learning_unit.add_triple_from_dict(TEST_TRIPLE)
  triple.save()

  function_output = get_triple_object.get_all_triples(learning_unit.id)
  assert isinstance(function_output, list)
  assert len(function_output) == 1


def test_generate_triples(mocker, get_triple_object):
  mocker.patch(
      "services.triple_inference.TripleService._extract_triples_from_text",
      return_value=[[{
          "sentence": "dummy sentence",
          "triples": [TEST_TRIPLE]
      }]])
  output = get_triple_object.generate_triples(["dummy lu text"])
  assert isinstance(output, list)


def test_create_triples_from_lu(mocker, get_triple_object):
  """tests create triples from lu"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  learning_objective = sub_competency.add_learning_objective_from_dict(
      TEST_LEARNING_OBJECTIVE)
  learning_objective.save()
  learning_unit = learning_objective.add_learning_unit_from_dict(
      TEST_LEARNING_UNIT)
  learning_unit.save()
  triple = learning_unit.add_triple_from_dict(TEST_TRIPLE)
  triple.save()
  dummy_triple = triple.get_fields()
  dummy_triple["id"] = triple.id
  mocker.patch(
      "services.triple_inference.TripleService.generate_triples",
      return_value=[[dummy_triple]])
  function_output = get_triple_object.\
  create_triples_from_lu(learning_unit.id)
  assert isinstance(function_output, list)
  assert Triple.find_by_id(triple.id).id == function_output[0]["id"]
