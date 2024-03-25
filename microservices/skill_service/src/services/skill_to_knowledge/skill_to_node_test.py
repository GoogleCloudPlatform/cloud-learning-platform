"""
  Unit tests for skill to node service
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long,wrong-import-position

import os
from grpc import services
import pytest
from testing.testing_objects import TEST_SKILL_5, TEST_LEARNING_RESOURCE_1, \
                                    TEST_CONCEPT, TEST_SUBCONCEPT, TEST_LEARNING_OBJECTIVE, \
                                    TEST_LEARNING_UNIT_1, TEST_LEARNING_UNIT_2, TEST_LEARNING_UNIT_3
from common.models import (Skill, KnowledgeServiceLearningContent, Concept,
                          SubConcept, KnowledgeServiceLearningObjective,
                          KnowledgeServiceLearningUnit)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

from unittest import mock
with mock.patch(
    "google.cloud.logging.Client", side_effect=mock.MagicMock()) as mok:
  from services.skill_to_knowledge.skill_to_node_data import Skill_Passage
  from services.skill_to_knowledge.skill_to_node import SkillNodeAlignment

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


@pytest.fixture(name="add_data", scope="module")
def add_data():
  #add test learning resource
  test_learning_resource = KnowledgeServiceLearningContent()
  test_learning_resource = test_learning_resource.from_dict(TEST_LEARNING_RESOURCE_1)
  test_learning_resource.save()
  test_learning_resource.uuid = test_learning_resource.id
  test_learning_resource.update()

  #add test concept
  test_concept = Concept.from_dict(TEST_CONCEPT)
  test_concept.parent_nodes["learning_resource"] = [test_learning_resource.uuid]
  test_concept.save()
  test_concept.uuid = test_concept.id
  test_concept.update()

  test_learning_resource.child_nodes["concepts"] = [test_concept.id]
  test_learning_resource.update()

  #add test sub-concept
  test_subconcept = SubConcept.from_dict(TEST_SUBCONCEPT)
  test_subconcept.parent_nodes["concepts"] = [test_concept.id]
  test_subconcept.save()
  test_subconcept.uuid = test_subconcept.id
  test_subconcept.update()

  test_concept.child_nodes["sub_concepts"] = [test_subconcept.uuid]
  test_concept.update()

  #add test learning objective
  test_learning_objective = KnowledgeServiceLearningObjective.from_dict(TEST_LEARNING_OBJECTIVE)
  test_learning_objective.parent_nodes["sub_concepts"] = [test_subconcept.id]
  test_learning_objective.save()
  test_learning_objective.uuid = test_learning_objective.id
  test_learning_objective.update()

  test_subconcept.child_nodes["learning_objectives"] = [test_learning_objective.uuid]
  test_subconcept.update()

  #add test learning units
  test_learning_unit_1 = KnowledgeServiceLearningUnit.from_dict(TEST_LEARNING_UNIT_1)
  test_learning_unit_1.parent_nodes["learning_objectives"] = [test_learning_objective.id]
  test_learning_unit_1.save()
  test_learning_unit_1.uuid = test_learning_unit_1.id
  test_learning_unit_1.update()

  test_learning_unit_2 = KnowledgeServiceLearningUnit.from_dict(TEST_LEARNING_UNIT_2)
  test_learning_unit_2.parent_nodes["learning_objectives"] = [test_learning_objective.id]
  test_learning_unit_2.save()
  test_learning_unit_2.uuid = test_learning_unit_2.id
  test_learning_unit_2.update()

  test_learning_unit_3 = KnowledgeServiceLearningUnit.from_dict(TEST_LEARNING_UNIT_3)
  test_learning_unit_3.parent_nodes["learning_objectives"] = [test_learning_objective.id]
  test_learning_unit_3.save()
  test_learning_unit_3.uuid = test_learning_unit_3.id
  test_learning_unit_3.update()

  test_learning_objective.child_nodes["learning_units"] = [test_learning_unit_1.uuid,
    test_learning_unit_2.uuid, test_learning_unit_3.uuid]
  test_learning_objective.update()

  return [
      test_learning_resource, test_learning_unit_1, test_learning_unit_2,
      test_learning_unit_3, test_concept, test_subconcept,
      test_learning_objective
  ]


@pytest.fixture(name="get_skill_node_alignment_object")
def get_skill_node_alignment_object():
  skill_node_alignment_object = SkillNodeAlignment()
  return skill_node_alignment_object


@pytest.fixture(name="add_skill", scope="module")
def add_skill():
  test_skill = Skill()
  test_skill = test_skill.from_dict(TEST_SKILL_5)
  test_skill.save()
  test_skill.uuid = test_skill.id
  test_skill.update()
  return test_skill


@pytest.fixture(name="update_learning_unit")
def update_learning_unit(add_data):
  test_learning_unit_2 = KnowledgeServiceLearningUnit.find_by_id(add_data[2].id)
  test_learning_unit_2.text = "sample text"
  test_learning_unit_2.parent_node = [add_data[6].id]
  test_learning_unit_2.update()


@pytest.mark.parametrize("idx", [0, 1, 2, 3])
def test_map_skill_to_nodes_by_ids(clean_firestore, mocker, add_data,
                                   get_skill_node_alignment_object, add_skill,
                                   idx):

  update_flag = False
  req_body, expected_response = [
    (
      {"source_name": ["snhu"], "learning_resource_ids": [add_data[0].id]},
      {"data" : {add_skill.id : {
        "mapped_lus": [
          {"id":add_data[1].id, "title": add_data[1].title, "score": 0.848},
          {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}
        ],
        "mapped_los": [
          {"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}
        ],
        "mapped_passages": [
          {"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848},
          {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}
        ],
        "mapped_subcompetencies": [
          {"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}
        ],
        "mapped_competencies": [
          {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665},
          {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}
        ],
        "mapped_learning_content": [add_data[0].id]}}}
    ),
    (
      {"ids": [add_skill.id], "learning_resource_ids": [add_data[0].id]},
      {"data" : {
        add_skill.id : {"mapped_passages": [
          {"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848},
          {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}
        ],
        "mapped_lus": [
          {"id":add_data[1].id, "title": add_data[1].title, "score": 0.848},
          {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}
        ],
        "mapped_los": [
          {"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}
        ],
        "mapped_subcompetencies": [
          {"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}
        ],
        "mapped_competencies": [
          {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665},
          {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}
        ],
        "mapped_learning_content": [add_data[0].id]}}}
    ),
    (
      {"ids": [add_skill.id]},
      {"data" : {
        add_skill.id : {
          "mapped_passages": [
            {"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848},
            {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}
          ],
          "mapped_lus": [
            {"id":add_data[1].id, "title": add_data[1].title, "score": 0.848},
            {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}
          ],
          "mapped_los": [
            {"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}
          ],
          "mapped_subcompetencies": [
            {"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}
          ],
          "mapped_competencies": [
            {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665},
            {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}
          ],
          "mapped_learning_content": [add_data[0].id]}}}
    ),
    (
      {"learning_resource_ids": [add_data[0].id]},
      Exception
    )
    ][idx]

  mocker.patch(
    "services.skill_to_knowledge.skill_to_node.SkillNodeAlignment.map_nodes",
    return_value = {"mapped_passages": [{"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848}, {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}], "mapped_lus": [{"id":add_data[1].id , "title": add_data[1].title, "score": 0.848}, {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}], "mapped_los": [{"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}], "mapped_subcompetencies": [{"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}], "mapped_competencies": [{"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}, {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}], "mapped_learning_content": [add_data[0].id]})

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_node_alignment_object.map_skill_to_nodes_by_ids(
          req_body, update_flag)
      assert "Both Skill IDs and Source name cannot be empty." == str(exc.value)
  else:
    response = get_skill_node_alignment_object.map_skill_to_nodes_by_ids(req_body, update_flag)
    assert response == expected_response, "Expected response not same"


@pytest.mark.parametrize("idx", [0,1])
def test_update_mapped_nodes(clean_firestore, add_data, add_skill, get_skill_node_alignment_object, idx):
  skill_list = [add_skill]
  aligned_nodes_list = [
    {add_data[0].id: {
      "mapped_passages": [
        {"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848},
        {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}
      ],
      "mapped_lus": [
        {"id":add_data[1].id , "title": add_data[1].title, "score": 0.848},
        {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}
      ],
      "mapped_los": [
        {"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}
      ],
      "mapped_subcompetencies": [
        {"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}
      ],
      "mapped_competencies": [
        {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665},
        {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}]}}]

  update_skills = [False, True][idx]

  expected_response = {
    "suggested": [
      {"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848, "type": "passage"},
      {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934, "type": "passage"},
      {"id": add_data[1].id, "title": add_data[1].title, "score": 0.848, "type": "learning_unit"},
      {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934, "type": "learning_unit"},
      {"id": add_data[6].id, "title": add_data[6].title, "score": 0.665, "type": "learning_objective"},
      {"id": add_data[5].id, "title": add_data[5].title, "score": 0.665, "type": "sub_competency"},
      {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665, "type": "competency"},
      {"id": add_data[0].id, "type": "learning_resource", "score": 1.0}
    ]}
  _ = get_skill_node_alignment_object.update_mapped_nodes(skill_list, aligned_nodes_list, update_skills)
  firestore_response = Skill.find_by_uuid(add_skill.id).to_dict()["alignments"]["knowledge_alignment"]
  assert sorted(expected_response) == sorted(firestore_response), "Expected response not same"


@pytest.mark.parametrize("idx", [0,1,2,3])
def test_map_skill_to_nodes_by_query(clean_firestore, mocker, add_data, get_skill_node_alignment_object, idx):

  req_body, expected_response = [
    (
      {"name": "Operating Systems", "description" : "Explain the purpose of operating systems"},
      {"data": {"mapped_passages": [{"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848}, {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}], "mapped_lus": [{"id":add_data[1].id , "title": add_data[1].title, "score": 0.848}, {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}], "mapped_los": [{"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}], "mapped_subcompetencies": [{"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}], "mapped_competencies": [{"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}, {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}], "mapped_learning_content": [add_data[0].id], "name": "Operating Systems", "description":"Explain the purpose of operating systems"}}
    ),
    (
      {"name": "", "description" : "Explain the purpose of operating systems"},
      {"data": {"mapped_passages": [{"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848}, {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}], "mapped_lus": [{"id":add_data[1].id , "title": add_data[1].title, "score": 0.848}, {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}], "mapped_los": [{"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}], "mapped_subcompetencies": [{"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}], "mapped_competencies": [{"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}, {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}], "mapped_learning_content": [add_data[0].id], "name": "", "description":"Explain the purpose of operating systems"}}
    ),
    (
      {"name": "", "description" : ""},
      Exception
    ),
    (
      {"name": "Operating Systems", "description" : ""},
      {"data": {"mapped_passages": [{"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848}, {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}], "mapped_lus": [{"id":add_data[1].id , "title": add_data[1].title, "score": 0.848}, {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}], "mapped_los": [{"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}], "mapped_subcompetencies": [{"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}], "mapped_competencies": [{"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}, {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}], "mapped_learning_content": [add_data[0].id], "name": "Operating Systems", "description":""}}
    )

  ][idx]

  mocker.patch(
    "services.skill_to_knowledge.skill_to_node.SkillNodeAlignment.map_nodes",
    return_value = {"mapped_passages": [{"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848}, {"id": str(add_data[2].id)+"##0", "title": str(add_data[2].title)+"_##Passage_0", "score": 0.934}], "mapped_lus": [{"id":add_data[1].id , "title": add_data[1].title, "score": 0.848}, {"id": add_data[2].id, "title": add_data[2].title, "score": 0.934}], "mapped_los": [{"id": add_data[6].id, "title": add_data[6].title, "score": 0.665}], "mapped_subcompetencies": [{"id": add_data[5].id, "title": add_data[5].title, "score": 0.665}], "mapped_competencies": [{"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}, {"id": add_data[4].id, "title": add_data[4].title, "score": 0.665}], "mapped_learning_content": [add_data[0].id]})

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_node_alignment_object.map_skill_to_nodes_by_query(
          req_body)
      assert "Both name and description cannot be empty." == str(exc.value)
  else:
    response = get_skill_node_alignment_object.map_skill_to_nodes_by_query(
        req_body)
    assert expected_response == response, "Expected response not same"


def test_map_nodes(clean_firestore, mocker, add_data,
                   get_skill_node_alignment_object, update_learning_unit):
  query = "Operating Systems. Explain the purpose of operating systems"
  learning_resource_ids = [add_data[0].id]

  expected_response = {add_data[0].id: {"mapped_passages": [{"id": str(add_data[1].id)+"##0", "title": str(add_data[1].title)+"_##Passage_0", "score": 0.848}], "mapped_lus": [{"id": add_data[1].id, "title": add_data[1].title, "score": 0.848}], "mapped_los": [{"id": add_data[6].id, "title": add_data[6].title, "score": 0.546}], "mapped_subconcepts": [{"id": add_data[5].id, "title": add_data[5].title, "score": 0.546}], "mapped_concepts": [{"id": add_data[4].id, "title": add_data[4].title, "score": 0.546}]}}
  response = get_skill_node_alignment_object.map_nodes(query, learning_resource_ids)
  print("#####################")
  print(response)
  print(expected_response)
  assert expected_response == response, "Expected response not same"


def test_filter_nodes(clean_firestore, mocker, add_data, add_skill, get_skill_node_alignment_object):
  passage_id = str(add_data[1].id) +"##0"
  passage_title = str(add_data[1].title) + "_##Passage_0"
  metadata = {"passage_text": "test passage", "skill_description": "test description" }
  list_nodes = [Skill_Passage(passage_id, passage_title, metadata)]

  expected_response = []
  response = get_skill_node_alignment_object.filter_nodes(list_nodes)
  assert expected_response == response, "Expected response not same"
