"""
  Unit tests for skill to passage service
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import, line-too-long

import os
import pytest
import numpy as np
from collections import defaultdict
from unittest import mock
from common.models import (Skill, KnowledgeServiceLearningContent, Concept,
                          SubConcept, KnowledgeServiceLearningObjective,
                          KnowledgeServiceLearningUnit)
from common.testing.firestore_emulator import (firestore_emulator,
                                                clean_firestore)
from testing.testing_objects import  TEST_LEARNING_RESOURCE_1, \
                                    TEST_CONCEPT, TEST_SUBCONCEPT, TEST_LEARNING_OBJECTIVE, \
                                    TEST_LEARNING_UNIT_1, TEST_LEARNING_UNIT_2, TEST_LEARNING_UNIT_3,\
                                    TEST_SKILL_5

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


with mock.patch("google.cloud.logging.Client",
  side_effect = mock.MagicMock()) as mok:
  from services.skill_to_knowledge import skill_to_passage


@pytest.fixture(name="add_data")
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

  return [test_learning_resource, test_learning_unit_1, test_learning_unit_2,
      test_learning_unit_3, test_concept]

@pytest.fixture(name="get_skill_knowledge_alignment_object")
def get_skill_knowledge_alignment_object():
  skill_knowledge_alignment_object = skill_to_passage.SkillKnowledgeAlignment()
  return skill_knowledge_alignment_object

@pytest.fixture(name="add_skill")
def add_skill():
  test_skill = Skill()
  test_skill = test_skill.from_dict(TEST_SKILL_5)
  test_skill.save()
  test_skill.uuid = test_skill.id
  test_skill.update()
  return test_skill


def test_get_learning_units(clean_firestore, mocker, add_data, get_skill_knowledge_alignment_object):
  lr_id = add_data[0].uuid
  response = get_skill_knowledge_alignment_object.get_learning_units(lr_id)
  print("resp: ", response)
  expected_result = [add_data[1], add_data[2], add_data[3]]
  assert [lu.uuid for lu in response] == [lu.uuid for lu in expected_result]


@pytest.mark.parametrize("idx", [0,1,2,3,4])
def test_get_similar_passages(clean_firestore, mocker, add_data, get_skill_knowledge_alignment_object, add_skill, idx):
  req_body = {
    "ids" : [],
    "name" : "Operating Systems",
    "description" : "Explain the purpose of operating systems",
  }

  req_body, mocked_response, expected_response = [
    (
      {"name" : "Operating Systems", "description" : "Explain the purpose of operating systems"},
      {"name": "Operating Systems", "description": "Explain the purpose of operating systems", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.8482568860054016], "lu_score": 1.0, "learning_resource_id": add_data[0].id},
        {"lu_id": add_data[2].id, "passages": [add_data[2].text], "passage_scores": [0.937], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]},
      {"data": {"name": "Operating Systems", "description": "Explain the purpose of operating systems", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.8482568860054016], "lu_score": 1.0, "learning_resource_id": add_data[0].id},
        {"lu_id": add_data[2].id, "passages": [add_data[2].text], "passage_scores": [0.937], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]}}
    ),
    (
      {"ids" : [add_skill.id]},
      {"name": "Operating Systems", "description": "Explain the purpose of operating systems", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.8482568860054016], "lu_score": 1.0, "learning_resource_id": add_data[0].id},
        {"lu_id": add_data[2].id, "passages": [add_data[2].text], "passage_scores": [0.937], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]},
      {"data": [{"name": "Operating Systems", "description": "Explain the purpose of operating systems", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.8482568860054016], "lu_score": 1.0, "learning_resource_id": add_data[0].id},
        {"lu_id": add_data[2].id, "passages": [add_data[2].text], "passage_scores": [0.937], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]}]}
    ),
    (
      {"description" : "Explain the purpose of operating systems"},
      {"name": "", "description": "Explain the purpose of operating systems", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.8482568860054016], "lu_score": 1.0, "learning_resource_id": add_data[0].id},
        {"lu_id": add_data[2].id, "passages": [add_data[2].text], "passage_scores": [0.937], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]},
      {"data": {"name": "", "description": "Explain the purpose of operating systems", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.8482568860054016], "lu_score": 1.0, "learning_resource_id": add_data[0].id},
        {"lu_id": add_data[2].id, "passages": [add_data[2].text], "passage_scores": [0.937], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]}}
    ),
    (
      {"name" : "Operating Systems"},
      {"name": "Operating Systems", "description": "", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.8482568860054016], "lu_score": 1.0, "learning_resource_id": add_data[0].id},
        {"lu_id": add_data[2].id, "passages": [add_data[2].text], "passage_scores": [0.937], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]},
      {"data": {"name": "Operating Systems", "description": "", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.8482568860054016], "lu_score": 1.0, "learning_resource_id": add_data[0].id},
        {"lu_id": add_data[2].id, "passages": [add_data[2].text], "passage_scores": [0.937], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]}}
    ),
    (
      {},
      None,
      Exception
    )
  ][idx]

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.search_docs",
    return_value = [{"0": {"id": str(add_data[1].id)+"##0", "distance": 0.932}, "1": {"id": str(add_data[2].id)+"##0", "distance": 0.931}, "2": {"id": str(add_data[3].id)+"##0", "distance": 0.930}}])

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.create_reranker_input",
    return_value = ([["Operating Systems. Explain the purpose of operating systems", add_data[1].text], ["Operating Systems. Explain the purpose of operating systems", add_data[2].text]], [add_data[1].id, add_data[2].id]))

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.rerank_docs",
    return_value = np.asarray([np.float32(0.848), np.float32(0.937)]))

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.filter_passages",
    return_value = ([add_data[1].text, add_data[2].text], [0.848, 0.937], [add_data[1].id, add_data[2].id]))

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.create_response",
    return_value = mocked_response)

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_knowledge_alignment_object.get_similar_passages(req_body)
      assert "Either of IDs or Name or Description are required" == str(exc.value)
  else:
    response = get_skill_knowledge_alignment_object.get_similar_passages(req_body)
    assert expected_response == response, "Expected response not same"


@pytest.mark.parametrize("idx", [0,1])
def test_create_response(clean_firestore, mocker, add_data, get_skill_knowledge_alignment_object, add_skill, idx):
  get_skill_knowledge_alignment_object.LEARNING_RESOURCE_CONCEPT_MAPPING = {add_data[0].id : add_data[4].id}
  lu_ids = [add_data[1].id]
  skill = "Operating Systems"
  skill_description =  "Explain the purpose of operating systems"
  skill_id = []
  scores =  [0.848]
  passages = [add_data[1].text]

  lu_ids, skill, skill_description, skill_id, scores, passages, expected_response = [
    (
      [add_data[1].id], "Operating Systems", "Explain the purpose of operating systems", [], [0.848], [add_data[1].text],
      {"name": "Operating Systems", "description": "Explain the purpose of operating systems", "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.848], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]}
    ),
    (
      [add_data[1].id], "", "", [add_skill.id], [0.848], [add_data[1].text],
      {"id":[add_skill.id], "learning_units": [{"lu_id": add_data[1].id, "passages": [add_data[1].text], "passage_scores": [0.848], "lu_score": 1.0, "learning_resource_id": add_data[0].id}]}
    )
  ][idx]

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.get_mapped_learning_resource",
    return_value= add_data[0].id)

  response = get_skill_knowledge_alignment_object.create_response(lu_ids, skill, skill_description, skill_id, scores, passages)
  assert expected_response == response, "Expected response not same"


def test_get_mapped_learning_resource(clean_firestore, add_data, get_skill_knowledge_alignment_object):
  get_skill_knowledge_alignment_object.LEARNING_RESOURCE_CONCEPT_MAPPING = {add_data[0].id : add_data[4].id}
  lu_object = add_data[1]

  expected_response = add_data[0].id
  response = get_skill_knowledge_alignment_object.get_mapped_learning_resource(lu_object)
  assert expected_response == response, "Expected response not same"


def test_filter_passages(clean_firestore, get_skill_knowledge_alignment_object):
  norm_score_passages = [0.848, 0.937, 0.275]
  reranker_input = [["Operating Systems. Explain the purpose of operating systems", "Before closing this introduction, let us present a brief history of how operating systems developed. Like any system built by humans, good ideas accumulated in operating systems over time, as engineers learned what was important in their design. Here, we discuss a few major devel- opments. For a richer treatment, see Brinch Hansen's excellent history of operating systems [BH00]."], ["Operating Systems. Explain the purpose of operating systems", "In the beginning, the operating system didn\'t do too much. Basically, it was just a "
                    "set of libraries of commonly-used functions; for example, instead of having each programmer of the system write low-level I/O handling code, the 'OS' would provide such APIs, and thus make life easier for the developer."], ["Operating Systems. Explain the purpose of operating systems", "The primary way the OS does this is through a general technique that we call virtualization . That is, the OS takes a physical resource (such as the processor, or memory, or a disk) and transforms it into a more gen- eral, powerful, and easy-to-use virtual form of itself. Thus, we sometimes refer to the operating system as a virtual machine ."]]
  similar_lu_ids = ["jDz7evRd6WtnoZHVApqW", "xefHtOUvPwXYphhRChpk", "2wqkWA3tKwslu0CL0Cal"]

  expected_response =  (["Before closing this introduction, let us present a brief history of how operating systems developed. Like any system built by humans, good ideas accumulated in operating systems over time, as engineers learned what was important in their design. Here, we discuss a few major devel- opments. For a richer treatment, see Brinch Hansen's excellent history of operating systems [BH00].", "In the beginning, the operating system didn't do too much. Basically, it was just a set of libraries of commonly-used functions; for example, instead of having each programmer of the system write low-level I/O handling code, the 'OS' would provide such APIs, and thus make life easier for the developer."], [0.848, 0.937], ["jDz7evRd6WtnoZHVApqW", "xefHtOUvPwXYphhRChpk"])
  response = get_skill_knowledge_alignment_object.filter_passages(norm_score_passages, reranker_input, similar_lu_ids)
  assert expected_response == response, "Expected response not same"


def test_create_reranker_input(clean_firestore, add_data, get_skill_knowledge_alignment_object ):
  query = "Operating Systems. Explain the purpose of operating systems"
  para_ids_dict = {"0": {"id": str(add_data[1].id)+"##0", "distance": 0.932}, "1": {"id": str(add_data[2].id)+"##0", "distance": 0.931}, "2": {"id": str(add_data[3].id)+"##0", "distance": 0.930}}

  expected_response =  ([["Operating Systems. Explain the purpose of operating systems", add_data[1].text], ["Operating Systems. Explain the purpose of operating systems", add_data[2].text], ["Operating Systems. Explain the purpose of operating systems", add_data[3].text]],
                       [add_data[1].id, add_data[2].id, add_data[3].id])
  response = get_skill_knowledge_alignment_object.create_reranker_input(query, para_ids_dict)
  assert expected_response == response, "Expected response not same"


@pytest.mark.parametrize("idx", [0,1])
def test_store_embeddings_knowledge(clean_firestore, mocker, add_data, get_skill_knowledge_alignment_object, idx):
  req_body, expected_response = [
    ({"learning_resource_ids" : add_data[0].id},
    {"status": "Successfully generated and saved embeddings."}),
    ({}, Exception)
  ][idx]

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.get_learning_units",
    return_value = [add_data[1], add_data[2], add_data[3]])

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.export_embedding_csv",
    return_value = "gcs:/sample path")

  mocker.patch(
    "services.skill_to_knowledge.skill_to_passage.SkillKnowledgeAlignment.populate_embedding_db",
    return_value = None)

  if expected_response == Exception:
    with pytest.raises(Exception) as exc:
      response = get_skill_knowledge_alignment_object.store_embeddings_knowledge(req_body)
      assert "Provide atleast one Learning Content ID" == str(exc.value)
  else:
    response = get_skill_knowledge_alignment_object.store_embeddings_knowledge(req_body)
    assert expected_response == response, "Expected response not same"

