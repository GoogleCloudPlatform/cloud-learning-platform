"""
  Unit tests for skill search API
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import, line-too-long

import os
from grpc import services
import pytest
import numpy as np
from testing.testing_objects import TEST_SKILL_1, TEST_SKILL_2
from common.models import Skill
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from unittest import mock
with mock.patch("google.cloud.logging.Client",
  side_effect = mock.MagicMock()) as mok:
  from services.search.search import SearchSkillGraph

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

@pytest.fixture(name="get_search_skillgraph_object")
def get_search_skillgraph_object():
  search_skillgraph_object = SearchSkillGraph("skill", "snhu")
  return search_skillgraph_object


@pytest.fixture(name="add_skills")
def add_skills():
  test_skill_1 = Skill()
  test_skill_1 = test_skill_1.from_dict(TEST_SKILL_1)
  test_skill_1.save()
  test_skill_1.uuid = test_skill_1.id
  test_skill_1.update()

  test_skill_2 = Skill()
  test_skill_2 = test_skill_2.from_dict(TEST_SKILL_2)
  test_skill_2.save()
  test_skill_2.uuid = test_skill_2.id
  test_skill_2.update()
  return [test_skill_1.uuid, test_skill_2.uuid]


def test_prepare_text_for_embedding(clean_firestore, mocker,\
   get_search_skillgraph_object):
  skill_name = "IT Privacy & Protection"
  skill_statement = "Explain the impact of technology on privacy and the development of technology security measures to ensure information privacy and protection"

  expected_response = "IT Privacy & Protection. Explain the impact of technology on privacy and the development of technology security measures to ensure information privacy and protection"
  response = get_search_skillgraph_object.prepare_text_for_embedding(skill_name,
              skill_statement)
  assert expected_response == response,"Expected response not same"


def test_get_level_obj(clean_firestore, mocker, get_search_skillgraph_object):
  response = get_search_skillgraph_object.get_level_obj()
  expected_response = type(Skill)
  assert expected_response == type(response), "Expected response not same"


def test_align_query(clean_firestore, mocker, get_search_skillgraph_object,
                      add_skills):
  queries = "IT Services"
  top_k = 5

  expected_response = [{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.698584258556366}, {"name": "IT Security Framework", "id": add_skills[1], "score": 0.5785842537879944}]

  mocker.patch(
    "services.search.search.SearchSkillGraph.search_docs",
    return_value= [{"0": {"id": add_skills[0], "distance":0.6778147220611572}, "1": {"id": add_skills[1], "distance": 0.8778147220611572}}])

  mocker.patch(
    "services.search.search.SearchSkillGraph.rerank_docs",
    return_value= [np.float32(0.6985842704772949), np.float32(0.5785842704772949)])
  response = get_search_skillgraph_object.align_query(queries, top_k)
  assert response == expected_response, "Expected response not same"


def test_get_search_results(clean_firestore, mocker,\
   get_search_skillgraph_object, add_skills):
  queries = "IT Services"
  top_k = 5

  expected_response = [[{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.698584258556366}, {"name": "IT Security Framework", "id": add_skills[1], "score": 0.5785842537879944}]]

  mocker.patch(
    "services.search.search.SearchSkillGraph.check_index_exist",
    return_value= [True, ""])

  mocker.patch(
    "services.search.search.SearchSkillGraph.prepare_text_for_embedding",
    return_value= "IT Services")

  mocker.patch(
    "services.search.search.SearchSkillGraph.align_query",
    return_value= [[{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.698584258556366}, {"name": "IT Security Framework", "id": add_skills[1], "score": 0.5785842537879944}]])

  response = get_search_skillgraph_object.get_search_results(queries, top_k)
  assert expected_response == response, "Expected response not same"
