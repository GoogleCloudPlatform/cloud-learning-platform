"""
  Unit tests for skill parsing service
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long

import os
import pytest
import numpy as np
from testing.testing_objects import TEST_SKILL_1, TEST_SKILL_2, TEST_ROLE
from common.models import Skill
from common.models import EmploymentRole
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)
from unittest import mock

with mock.patch("google.cloud.logging.Client",
  side_effect = mock.MagicMock()) as mok:
  from services.skill_parsing.skill_parsing import SkillParser

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.fixture(name="get_skill_parsing_object")
def get_skill_parsing_object():
  skill_parser_object = SkillParser("snhu", "skill_snhu")
  return skill_parser_object

@pytest.fixture(name="add_skills", scope="module")
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

@pytest.fixture(name="add_role", scope="module")
def add_role():
  test_role = EmploymentRole()
  test_role = test_role.from_dict(TEST_ROLE)
  test_role.save()
  test_role.uuid = test_role.id
  test_role.update()
  return test_role.uuid


def test_create_reranker_input(clean_firestore, mocker, get_skill_parsing_object):
  query = "Sample string"
  passages = ["Sample list element 1", "Sample list element 2", "Sample list element 3" ]

  expected_response = [["Sample string", "Sample list element 1"], ["Sample string", "Sample list element 2"],
  ["Sample string", "Sample list element 3"]]
  response = get_skill_parsing_object.create_reranker_input(query, passages)
  assert expected_response == response, "Expected response not same"


def test_filter_docs(clean_firestore, mocker, get_skill_parsing_object):
  docs = [{"name": "Operating System", "id": "1234" , "desc": "", "score":0.18},
  {"name": "System Software", "id": "4567" , "desc": "", "score": 0.76}]

  expected_response = [{"name": "System Software", "id": "4567" , "desc": "", "score": 0.76}]
  response = get_skill_parsing_object.filter_docs(docs)
  assert expected_response == response, "Expected response not same"


def test_create_response(clean_firestore, mocker, get_skill_parsing_object):
  skill =  {"name": "System Software", "id": "4567" , "desc": "", "score": 0.76}

  expected_response = {"name": "System Software", "id": "4567", "score": 0.76}
  response = get_skill_parsing_object.create_response(skill)
  assert expected_response == response, "Expected response not same"


@pytest.mark.parametrize("idx", [0,1,2])
def test_get_relevant_skills(clean_firestore, mocker, get_skill_parsing_object, add_skills, idx):

  req_body, expected_response = [
    (
      {"name" : "", "description": "Explain Operating Systems", "top_k": 5, "alignment_sources": ["snhu"]},
      [{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.699}, {"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}]
    ),
    (
      {"name" : "", "description": "", "top_k": 5, "alignment_sources": ["snhu"]},
      Exception
    ),
    (
      {"name" : "Operating System", "description": "Explain Operating Systems", "top_k": 5, "alignment_sources": ["snhu"]},
      [{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.699}, {"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}]
    )
    ][idx]

  mocker.patch(
    "services.skill_parsing.skill_parsing.SkillParser.search_docs",
    return_value = [{"0": {"id": add_skills[0], "distance": 0.677}, "1": {"id": add_skills[1], "distance": 0.877}}])
  mocker.patch(
    "services.skill_parsing.skill_parsing.SkillParser.rerank_docs",
    return_value = [np.float32(0.699), np.float32(0.579)])

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_parsing_object.get_relevant_skills(req_body)
      assert "Both name and description cannot be empty." == str(exc.value)
  else:
    response = get_skill_parsing_object.get_relevant_skills(req_body)
    assert expected_response == response, "Expected response not same"


@pytest.mark.parametrize("update_skills", [False, True])
def test_update_aligned_skills(clean_firestore, mocker, get_skill_parsing_object, add_skills, add_role, update_skills):

  input_object_list = [EmploymentRole.find_by_id(add_role)]
  aligned_skills_list = [
    [{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.699},
     {"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}]
  ]

  expected_response = {"snhu": {"aligned": [], "suggested": [{"score": 0.699, "name": "IT Privacy & Protection", "id": add_skills[0]}, {"name": "IT Security Framework", "score": 0.579, "id": add_skills[1]}]}}
  _ = get_skill_parsing_object.update_aligned_skills(input_object_list, aligned_skills_list, update_skills)
  firestore_response = EmploymentRole.find_by_id(add_role).to_dict()["alignments"]["skill_alignment"]
  assert sorted(expected_response) == sorted(firestore_response), "Expected response not same"


@pytest.mark.parametrize("idx", [0,1,2])
def test_parse_skills_by_role_ids(clean_firestore, mocker, get_skill_parsing_object, add_skills, add_role, idx):
  update_flag = False

  request_body, expected_response = [
    (
      {"ids": [add_role], "top_k": 5, "skill_alignment_sources" : ["snhu"]},
      {add_role:[
        {"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.699},
        {"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}]}
    ),
    (
      {"source_name": ["snhu"], "top_k": 5, "skill_alignment_sources" : ["snhu"]},
      {add_role:[
        {"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.699},
        {"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}
      ]}
    ),
    (
      {"top_k": 5, "skill_alignment_sources" : ["snhu"]},
      Exception
    )
  ][idx]

  mocker.patch(
    "services.skill_parsing.skill_parsing.SkillParser.get_relevant_skills",
    return_value = [
      {"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.699},
      {"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}
    ])

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_parsing_object.parse_skills_by_role_ids(request_body, update_flag)
      assert "Both EmploymentRole IDs and Source name cannot be empty." == str(exc.value)
  else:
    response = get_skill_parsing_object.parse_skills_by_role_ids(request_body, update_flag)

    assert expected_response == response, "Expected response not same"
