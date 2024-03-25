"""
  Unit tests for skill similarity service
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import, line-too-long
import os
import pytest
from skill_similarity import SkillSimilarity
from unittest.mock import Mock
from testing.testing_objects import TEST_SKILL_1, TEST_SKILL_2
from common.models import Skill
from common.testing.firestore_emulator import (firestore_emulator,
                                              clean_firestore)

@pytest.mark.parametrize("idx", [0,1,2])
def test_get_skill_data(clean_firestore, mocker, idx):
  skill_similarity_object = SkillSimilarity()

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

  source = "snhu"

  skill_id_1, skill_id_2, source, expected_response = [
    (
      test_skill_1.uuid, test_skill_2.uuid, source,
      ("IT Privacy & Protection. Explain the impact of technology on privacy and the development of technology security measures to ensure information privacy and protection",
      "IT Security Framework. Use an information technology security framework to inform the security plan and support governance and compliance")
    ),
    (test_skill_1.uuid, "JQHbpPkSY9RpMo8VXEc2", source, Exception),
    (test_skill_1.uuid, test_skill_2.uuid, "fake-source", Exception)
  ][idx]

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = skill_similarity_object.get_skill_data(skill_id_1, skill_id_2, source)
      if idx == 1:
        assert "Skill with the given id does not exist" == str(exc.value)
      else:
        assert "Invalid data source." == str(exc.value)
  else:
    response = skill_similarity_object.get_skill_data(skill_id_1, skill_id_2, source)
    assert expected_response == response, "Expected response not same"


@pytest.mark.parametrize("text1,text2,expected_response",
[
  ("Team Building", "Team Work", 0.203),
  ("Team Building", 123, Exception)
])
def test_get_skill_similarity(clean_firestore, mocker, text1, text2, expected_response):
  skill_similarity_object = SkillSimilarity()

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = skill_similarity_object.get_skill_similarity(text1, text2)
      assert "Couldn't retieve similarity score" == str(exc.value)
  else:
    response = skill_similarity_object.get_skill_similarity(text1, text2)
    assert isinstance(response, float)
    assert expected_response == response, "Expected response not same"
