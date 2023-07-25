"""Unit testing of Sub Competency inference"""
import sys
import pytest
# disabling as we need to append path for common
# pylint: disable=unused-import
# pylint: disable=wrong-import-position
sys.path.append("../../common/src")
from common.utils.errors import ResourceNotFoundException
from common.models import (Competency, Course, LearningContentItem)
from testing.example_objects import (TEST_COMPETENCY, TEST_COURSE,
                                     TEST_LEARNING_CONTENT)
from testing.firestore_emulator import clean_firestore, firestore_emulator
from unittest import mock
with mock.patch("google.cloud.logging.Client",
  side_effect = mock.MagicMock()) as mok:
  from services.competency_inference import CompetencyService

# disabling these rules, as they cause issues with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name


@pytest.fixture(name="get_competency_object")
def get_competency_object():
  """returns SC object"""
  competency_obj = CompetencyService()
  return competency_obj


def test_create_competency(clean_firestore, get_competency_object):
  """tests create competency"""
  function_output = get_competency_object.create_competency(TEST_COMPETENCY)
  assert isinstance(function_output, dict)
  assert "id" in function_output
  assert function_output["title"] == TEST_COMPETENCY["title"]


def test_get_competency(clean_firestore, get_competency_object):
  """tests get competency"""

  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  function_output = get_competency_object.get_competency(competency.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == competency.id

def test_get_competency_with_text(clean_firestore, get_competency_object):
  """tests get competency"""

  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  function_output = get_competency_object.get_competency(competency.id,
  is_text_required = True)
  assert isinstance(function_output, dict)
  assert function_output["id"] == competency.id
  assert "text" in function_output
  assert function_output["text"] == []


def test_update_competency(clean_firestore, get_competency_object):
  """tests update competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  updated_competency_fields = {"title": "Updated title"}
  function_output = get_competency_object.update_competency(
      competency.id, updated_competency_fields)
  assert isinstance(function_output, dict)
  assert function_output["id"] == competency.id

  fetched_sc = Competency.find_by_id(competency.id)
  assert fetched_sc.title == updated_competency_fields["title"]


def test_delete_competency(clean_firestore, get_competency_object):
  """tests delete competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  function_output = get_competency_object.delete_competency(competency.id)
  assert function_output is None
  with pytest.raises(ResourceNotFoundException):
    assert Competency.find_by_id(competency.id)


def test_get_all_competencies(clean_firestore, get_competency_object):
  """tests get all competencies"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  function_output = get_competency_object.get_all_competencies()
  assert isinstance(function_output, list)
  assert len(function_output) == 1


# Course


def test_create_course_competency(clean_firestore, get_competency_object):
  """tests create competency"""
  course = Course.from_dict(TEST_COURSE)
  course.save()
  function_output = get_competency_object.create_course_competency(
      course.id, TEST_COMPETENCY)
  assert isinstance(function_output, dict)
  assert "id" in function_output
  assert function_output["title"] == TEST_COMPETENCY["title"]
  fetched_course = Course.find_by_id(course.id)
  assert len(fetched_course.competency_ids) == 1
  assert function_output["id"] in fetched_course.competency_ids


def test_get_course_competency(clean_firestore, get_competency_object):
  """tests get competency"""

  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  function_output = get_competency_object.get_course_competency(
      competency.id, course.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == competency.id


def test_update_course_competency(clean_firestore, get_competency_object):
  """tests update competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  updated_competency_fields = {"title": "Updated title"}
  function_output = get_competency_object.update_course_competency(
      competency.id, updated_competency_fields, course.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == competency.id

  fetched_sc = Competency.find_by_id(competency.id)
  assert fetched_sc.title == updated_competency_fields["title"]


def test_delete_course_competency(clean_firestore, get_competency_object):
  """tests delete competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  function_output = get_competency_object.delete_course_competency(
      competency.id, course.id)
  assert function_output is None
  assert Competency.find_by_id(competency.id) is not None
  fetched_course = Course.find_by_id(course.id)
  assert fetched_course.competency_ids == []


def test_get_course_all_competencies(clean_firestore, get_competency_object):
  """tests get all competencies"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  course = Course.from_dict(TEST_COURSE)
  course.competency_ids = [competency.id]
  course.save()
  function_output = get_competency_object.get_course_all_competencies(course.id)
  assert isinstance(function_output, list)
  assert len(function_output) == 1
  assert function_output[0]["id"] == competency.id


# Learning Content


def test_create_learning_content_competency(clean_firestore,
                                            get_competency_object):
  """tests create competency"""
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.save()
  function_output = get_competency_object.create_learning_content_competency(
      learning_content.id, TEST_COMPETENCY)
  assert isinstance(function_output, dict)
  assert "id" in function_output
  assert function_output["title"] == TEST_COMPETENCY["title"]
  fetched_learning_content = LearningContentItem.find_by_id(learning_content.id)
  assert len(fetched_learning_content.competency_ids) == 1
  assert function_output["id"] in fetched_learning_content.competency_ids


def test_get_learning_content_competency(clean_firestore,
                                         get_competency_object):
  """tests get competency"""

  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.competency_ids = [competency.id]
  learning_content.save()
  function_output = get_competency_object.get_learning_content_competency(
      competency.id, learning_content.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == competency.id


def test_update_learning_content_competency(clean_firestore,
                                            get_competency_object):
  """tests update competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.competency_ids = [competency.id]
  learning_content.save()
  updated_competency_fields = {"title": "Updated title"}
  function_output = get_competency_object.update_learning_content_competency(
      competency.id, updated_competency_fields, learning_content.id)
  assert isinstance(function_output, dict)
  assert function_output["id"] == competency.id

  fetched_sc = Competency.find_by_id(competency.id)
  assert fetched_sc.title == updated_competency_fields["title"]


def test_delete_learning_content_competency(clean_firestore,
                                            get_competency_object):
  """tests delete competency"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.competency_ids = [competency.id]
  learning_content.save()
  function_output = get_competency_object.delete_learning_content_competency(
      competency.id, learning_content.id)
  assert function_output is None
  assert Competency.find_by_id(competency.id) is not None
  fetched_learning_content = LearningContentItem.find_by_id(learning_content.id)
  assert fetched_learning_content.competency_ids == []


def test_get_learning_content_all_competencies(clean_firestore,
                                               get_competency_object):
  """tests get all competencies"""
  competency = Competency.from_dict(TEST_COMPETENCY)
  competency.save()
  learning_content = LearningContentItem.from_dict(TEST_LEARNING_CONTENT)
  learning_content.competency_ids = [competency.id]
  learning_content.save()
  function_output = get_competency_object.get_all_learning_content_competencies(
      learning_content.id)
  assert isinstance(function_output, list)
  assert len(function_output) == 1
  assert function_output[0]["id"] == competency.id
