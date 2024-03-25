"""
  Unit test cases for skill alignment service
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
  from services.skill_alignment.skill_alignment import SkillAlignment

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

@pytest.fixture(name="get_skill_alignment_object")
def get_skill_alignment_object():
  skill_alignment_object = SkillAlignment("snhu", "skill_snhu")
  return skill_alignment_object

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


@pytest.mark.parametrize("idx", [0,1,2,3])
def test_prepare_text_for_embedding(clean_firestore, get_skill_alignment_object, idx):

  skill_name, skill_statement, expected_response = [
    (
    "IT Privacy & Protection",
    "Explain the impact of technology on privacy and the development of technology security measures to ensure information privacy and protection",
    "IT Privacy & Protection. Explain the impact of technology on privacy and the development of technology security measures to ensure information privacy and protection"
    ),
    ("",
    "Explain the impact of technology on privacy and the development of technology security measures to ensure information privacy and protection",
    "Explain the impact of technology on privacy and the development of technology security measures to ensure information privacy and protection"
    ),
    (
    "IT Privacy & Protection", "", "IT Privacy & Protection"
    ),
    (
    "", "", Exception
    )
    ][idx]

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_alignment_object.prepare_text_for_embedding(skill_name, skill_statement)
      assert "For embedding input alteast one out of skill_name and skill_statement should be present." == str(exc.value)
  else:
    response = get_skill_alignment_object.prepare_text_for_embedding(skill_name, skill_statement)
    assert expected_response == response, "Expected response not same"


def test_align_skills(clean_firestore, mocker, get_skill_alignment_object, add_skills):
  queries = ["IT Services"]
  top_k = 5

  expected_response = [[{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.699}, {"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}]]

  mocker.patch(
    "services.skill_alignment.skill_alignment.SkillAlignment.search_docs",
    return_value= [{"0": {"id": add_skills[0], "distance":0.678}, "1": {"id": add_skills[1], "distance": 0.878}}])

  mocker.patch(
    "services.skill_alignment.skill_alignment.SkillAlignment.rerank_docs",
    return_value= [0.699, 0.579])
  response = get_skill_alignment_object.align_skills(queries, top_k)
  assert expected_response == response, "Expected response not same"


@pytest.mark.parametrize("idx", [0,1,2])
def test_align_skills_by_ids(clean_firestore, mocker, get_skill_alignment_object, add_skills, idx):
  update_flag = False

  request_body, mocker_response, expected_response = [
    (
      {"ids": [add_skills[0]], "top_k": 5, "skill_alignment_sources" : ["snhu"]},
      [[{"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}]],
      [[{"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}]]
    ),
    (
      {"source_name": ["snhu"], "top_k": 5, "skill_alignment_sources" : ["snhu"]},
      [[{"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}], [{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.678}]],
      [[{"name": "IT Security Framework", "id": add_skills[1], "score": 0.579}], [{"name": "IT Privacy & Protection", "id": add_skills[0], "score": 0.678}]]
    ),
    (
      {"top_k": 5, "skill_alignment_sources" : ["snhu"]},
      None,
      Exception
    )
  ][idx]

  mocker.patch(
    "services.skill_alignment.skill_alignment.SkillAlignment.align_skills",
    return_value = mocker_response)

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_alignment_object.align_skills_by_ids(request_body, update_flag)
      assert "Both Skill IDs and Source name cannot be empty." == str(exc.value)
  else:
    response = get_skill_alignment_object.align_skills_by_ids(request_body, update_flag)
    assert expected_response == response, "Expected response not same"


@pytest.mark.parametrize(
  "skill_name, skill_statement, expected_response",
  [
  ("Operating System", "", [[{"name": "Operating Systems and Solutions", "id": "1aLY6zQK89BPenEYrzDv", "score": 0.999}, {"name": "Operating Systems and Services", "id": "IdRLaUn0Gp7mvQQONS4r", "score": 0.999}]]),
  ("", "", Exception)
  ])
def test_align_skills_by_query(clean_firestore, mocker, get_skill_alignment_object, skill_name, skill_statement, expected_response):
  top_k = 5

  mocker.patch(
    "services.skill_alignment.skill_alignment.SkillAlignment.align_skills",
    return_value= [[{"name": "Operating Systems and Solutions", "id": "1aLY6zQK89BPenEYrzDv", "score": 0.999}, {"name": "Operating Systems and Services", "id":"IdRLaUn0Gp7mvQQONS4r", "score": 0.999}]])

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_alignment_object.align_skills_by_query(skill_name, skill_statement, top_k)
      assert "Atleast one param out of skill_name or skill_statement should be present." == str(exc.value)
  else:
    response = get_skill_alignment_object.align_skills_by_query(skill_name, skill_statement, top_k)
    assert expected_response == response, "Expected response not same"


@pytest.mark.parametrize("update_skills", [False, True])
def test_update_aligned_skill(clean_firestore, mocker,get_skill_alignment_object, add_skills, update_skills):
  internal_skills = [Skill.find_by_uuid(add_skills[0])]
  aligned_skills_list = [[{"name": "IT Security Framework","id": add_skills[1], "score": 0.579}]]

  expected_response = {"snhu": {"suggested": [{"name": "IT Security Framework", "score": 0.579, "id": add_skills[1]}], "aligned": []}}
  _ = get_skill_alignment_object.update_aligned_skill(internal_skills, aligned_skills_list, update_skills)
  firestore_response = Skill.find_by_uuid(add_skills[0]).to_dict()["alignments"]["skill_alignment"]
  assert sorted(expected_response) == sorted(firestore_response), "Expected response not same"
