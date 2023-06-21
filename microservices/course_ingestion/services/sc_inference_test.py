"""Unit testing of Sub Competency inference"""
import sys
import pytest

# for firestore cleanup
# pylint: disable=unused-import
# disabling as we need to append path for common
# pylint: disable=wrong-import-position
sys.path.append("../../common/src")
from common.utils.errors import ResourceNotFoundException
from common.models import (Course, SubCompetency, Competency)
from testing.example_objects import (TEST_COMPETENCY, TEST_COURSE,
                                     TEST_SUB_COMPETENCY)
from testing.firestore_emulator import clean_firestore, firestore_emulator
from unittest import mock
with mock.patch("google.cloud.logging.Client",
  side_effect = mock.MagicMock()) as mok:
  from services.sc_inference import SubCompetencyService

# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name


@pytest.fixture(name="get_sc_object")
def get_sc_object():
  """returns SC object"""
  sc_obj = SubCompetencyService()
  return sc_obj


def test_create_sub_competency(clean_firestore, get_sc_object):
  """tests create_sub_competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  function_output = get_sc_object.create_sub_competency(competency.id,
                                                        TEST_SUB_COMPETENCY)
  assert isinstance(function_output, dict)
  assert "id" in function_output


def test_get_sub_competency(clean_firestore, get_sc_object):
  """tests get_sub_competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  function_output = get_sc_object.get_sub_competency(sub_competency.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == sub_competency.id
  function_output_with_text = get_sc_object.get_sub_competency(
    sub_competency.id, is_text_required = True)
  assert isinstance(function_output_with_text, dict)
  assert function_output_with_text["id"] == sub_competency.id
  assert "text" in function_output_with_text
  assert function_output_with_text["text"] == []

def test_update_sub_competency(clean_firestore, get_sc_object):
  """tests update_sub_competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  updated_sc_fields = {
      **TEST_SUB_COMPETENCY, "title": "Updated title",
      "parent_node": sub_competency.parent_node.ref.path
  }
  function_output = get_sc_object.update_sub_competency(sub_competency.id,
                                                        updated_sc_fields)
  assert isinstance(function_output, dict)
  assert function_output["id"] == sub_competency.id

  fetched_sc = SubCompetency.find_by_id(sub_competency.id)
  assert fetched_sc.title == updated_sc_fields["title"]


def test_delete_sub_competency(clean_firestore, get_sc_object):
  """tests delete_sub_competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  function_output = get_sc_object.delete_sub_competency(sub_competency.id)
  assert function_output is None
  with pytest.raises(ResourceNotFoundException):
    SubCompetency.find_by_id(sub_competency.id)


def test_get_all_sub_competencies(clean_firestore, get_sc_object):
  """tests get_all_sub_competencies"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  sub_competency = competency.add_sub_competency_from_dict(TEST_SUB_COMPETENCY)
  sub_competency.save()
  function_output = get_sc_object.get_all_sub_competencies(competency.id)
  assert isinstance(function_output, list)
  assert len(function_output) == 1
