"""
  Unit tests for skill to lu file
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import, line-too-long

import os
from grpc import services
import pytest
import numpy as np
from testing.testing_objects import TEST_LEARNING_UNIT_1
from common.models import KnowledgeServiceLearningUnit
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

from unittest import mock
from collections import defaultdict
with mock.patch("google.cloud.logging.Client",
  side_effect = mock.MagicMock()) as mok:
  from services.skill_to_knowledge.skill_to_node_data import Skill_LU, Skill_Passage

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

@pytest.fixture(name="get_objects")
def get_objects():
  test_learning_unit_1 = KnowledgeServiceLearningUnit()
  test_learning_unit_1 = test_learning_unit_1.from_dict(TEST_LEARNING_UNIT_1)
  test_learning_unit_1.save()

  passage_id = str(test_learning_unit_1.id) +"##0"
  passage_title = str(test_learning_unit_1.title) + "_##Passage_0"
  metadata = {"passage_text": "test passage", "skill_description": "test description" }

  skill_passage_object = Skill_Passage(passage_id,passage_title, metadata)
  skill_lu_object = Skill_LU(test_learning_unit_1.id, test_learning_unit_1.title, [skill_passage_object])
  return skill_lu_object, skill_passage_object

def test_calculate_length(clean_firestore, mocker, get_objects):
  metadata = [get_objects[1]]

  expected_response = 2
  response = get_objects[0].calculate_length(metadata)
  assert expected_response == response, "Expected response not same"


def test_calculate_score(clean_firestore, mocker, get_objects):
  metadata = [get_objects[1]]

  expected_response = 0.011
  response = get_objects[0].calculate_score(metadata)
  assert expected_response == response, "Expected response not same"

def test_check_mapping(clean_firestore, mocker, get_objects):
  metadata = [get_objects[1]]

  expected_response = False
  response = get_objects[0].check_mapping(metadata)
  assert expected_response == response, "Expected response not same"
