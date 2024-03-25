"""Unit tests for Unified Alignment service"""

# pylint: disable=unused-argument,redefined-outer-name,unused-import,line-too-long,wrong-import-position
import os
from grpc import services
import pytest
import sys
sys.path.append("../../../common/src")
from testing.testing_objects import (TEST_SKILL_1, TEST_SKILL_2, TEST_SKILL_3,
                                    TEST_SKILL_4, TEST_LEARNING_RESOURCE_1)
from common.models import Skill, KnowledgeServiceLearningContent
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

from unittest import mock
with mock.patch("google.cloud.logging.Client",
  side_effect = mock.MagicMock()) as mok:
  from services.skill_unified_alignment.skill_unified_alignment import SkillUnifiedAlignment

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

@pytest.fixture(name="get_unified_alignment_object")
def get_unified_alignment_object():
  unified_alignment_object = SkillUnifiedAlignment()
  return unified_alignment_object

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

  test_skill_3 = Skill()
  test_skill_3 = test_skill_3.from_dict(TEST_SKILL_3)
  test_skill_3.save()
  test_skill_3.uuid = test_skill_3.id
  test_skill_3.update()

  test_skill_4 = Skill()
  test_skill_4 = test_skill_4.from_dict(TEST_SKILL_4)
  test_skill_4.save()
  test_skill_4.uuid = test_skill_4.id
  test_skill_4.update()

  return [test_skill_1.uuid, test_skill_2.uuid,test_skill_3.uuid,
    test_skill_4.uuid]

@pytest.fixture(name="add_learning_resource")
def add_learning_resource():
  test_learning_resource_1 = KnowledgeServiceLearningContent()
  test_learning_resource_1 = test_learning_resource_1.from_dict(
    TEST_LEARNING_RESOURCE_1)
  test_learning_resource_1.save()
  return [test_learning_resource_1.id]

def test_get_skill_alignments_by_id(clean_firestore, mocker,
  get_unified_alignment_object, add_skills):
  request_body = {
    "ids": [
      add_skills[2]
    ],
    "input_type": "skill",
    "top_k": 3,
    "output_alignment_sources": {
      "skill_sources": [
        "test-source1"
      ],
      "learning_resource_ids": [
        "W1HAobJsOGp36R5u9qRO"
      ]
    },
    "skill_alignment_sources": [
      "test-source1"
    ]
  }
  expected_response = {
    add_skills[2]: {
      "test-source1": [
        {
          "name": "Operating System Development",
          "id": add_skills[2],
          "score": 0.998
        },
        {
          "name": "Operating Systems",
          "id": add_skills[3],
          "score": 0.982
        }
      ]
    }
  }
  mocker.patch(
    "services.skill_alignment.skill_alignment.SkillAlignment.align_skills",
    return_value=[[{"name": "Operating System Development", "id": add_skills[2],
    "score": 0.998}, {"name": "Operating Systems",
    "id": add_skills[3], "score": 0.982}]])
  response = get_unified_alignment_object.get_skill_alignments_by_id(
    request_body)
  assert expected_response == response, "Expected response not the same"

def test_get_skill_alignments_by_query(clean_firestore, mocker,
  get_unified_alignment_object, add_skills):
  request_body = {
    "name": "Operating Systems",
    "description": "An operating system (OS) is system software that manages computer hardware, software resources, and provides common services for computer programs.",
    "input_type": "skill",
    "top_k": 3,
    "output_alignment_sources": {
      "skill_sources": [
        "test-source1"
      ],
      "learning_resource_ids": [
        "W1HAobJsOGp36R5u9qRO"
      ]
    },
    "skill_alignment_sources": [
      "test-source1"
    ]
  }
  expected_response = {
    "test-source1": [
      {
        "name": "Operating Systems",
        "id": add_skills[3],
        "score": 0.999
      },
      {
        "name": "Operating System Development",
        "id": add_skills[2],
        "score": 0.982
      }
    ]
  }
  mocker.patch(
    "services.skill_alignment.skill_alignment.SkillAlignment.align_skills",
    return_value=[[{"name": "Operating Systems", "id":
    add_skills[3], "score": 0.999}, {"name":
    "Operating System Development", "id": add_skills[2],
    "score": 0.982}]])
  response = get_unified_alignment_object.get_skill_alignments_by_query(
    request_body)
  assert expected_response == response, "Expected response not the same"

@pytest.mark.parametrize(
"request_body, create_for, aligned_skills, aligned_knowledge, expected_response",
[
  (
    {"ids": ["pzAvrAzdT9JAW4pG742D"], "input_type": "skill", "top_k": 3, "output_alignment_sources": {"skill_sources": ["emsi"], "learning_resource_ids": ["W1HAobJsOGp36R5u9qRO"]}, "skill_alignment_sources": ["emsi"], "learning_resource_ids": ["W1HAobJsOGp36R5u9qRO"]},
    "id",
    {"pzAvrAzdT9JAW4pG742D": {"emsi": [{"name": "Operating System Development", "id": "pzAvrAzdT9JAW4pG742D", "score": 0.998}, {"name": "Operating Systems", "id": "15aor2vzGW9aVOvM2opG", "score": 0.995}, {"name": "Linux On Embedded Systems", "id": "ybgzcGYWAAHf3Yo6wdYe", "score": 0.995}]}},
    {"data": {"pzAvrAzdT9JAW4pG742D": {"W1HAobJsOGp36R5u9qRO": {"mapped_passages": [{"id": "NctXsNCc6YCqmX9Tw5Xc##2", "score": 0.955}, {"id": "TCmNZRm2pLyYLPUO6Gi3##1", "score": 0.628}, {"id": "TCmNZRm2pLyYLPUO6Gi3##4", "score": 0.881}, {"id": "aIJGT5uxdemGzNugwDSf##2", "score": 0.522}, {"id": "jDz7evRd6WtnoZHVApqW##0", "score": 0.996}, {"id": "jDz7evRd6WtnoZHVApqW##1", "score": 0.748}, {"id": "xefHtOUvPwXYphhRChpk##1", "score": 0.928}, {"id": "xefHtOUvPwXYphhRChpk##2", "score": 0.962}], "mapped_lus": [{"id": "jDz7evRd6WtnoZHVApqW", "score": 0.245}, {"id": "xefHtOUvPwXYphhRChpk", "score": 0.405}], "mapped_los": [], "mapped_subconcepts": [], "mapped_concepts": []}}}},
    {"data": {"pzAvrAzdT9JAW4pG742D": {"aligned_skills": {"emsi": [{"name": "Operating System Development", "id": "pzAvrAzdT9JAW4pG742D", "score": 0.998}, {"name": "Operating Systems", "id": "15aor2vzGW9aVOvM2opG", "score": 0.995}, {"name": "Linux On Embedded Systems", "id": "ybgzcGYWAAHf3Yo6wdYe", "score": 0.995}]}, "aligned_knowledge": {"W1HAobJsOGp36R5u9qRO": {"mapped_passages": [{"id": "NctXsNCc6YCqmX9Tw5Xc##2", "score": 0.955}, {"id": "TCmNZRm2pLyYLPUO6Gi3##1", "score": 0.628}, {"id": "TCmNZRm2pLyYLPUO6Gi3##4", "score": 0.881}, {"id": "aIJGT5uxdemGzNugwDSf##2", "score": 0.522}, {"id": "jDz7evRd6WtnoZHVApqW##0", "score": 0.996}, {"id": "jDz7evRd6WtnoZHVApqW##1", "score": 0.748}, {"id": "xefHtOUvPwXYphhRChpk##1", "score": 0.928}, {"id": "xefHtOUvPwXYphhRChpk##2", "score": 0.962}], "mapped_lus": [{"id": "jDz7evRd6WtnoZHVApqW", "score": 0.245}, {"id": "xefHtOUvPwXYphhRChpk", "score": 0.405}], "mapped_los": [], "mapped_subconcepts": [], "mapped_concepts": []}}}}}
  ),
  (
    {"name": "Expert", "description": "Diagnose, adjust, repair, or overhaul small engines used to power lawn mowers, chain saws, recreational sporting equipment, and related equipment.", "input_type": "skill", "top_k": 3, "output_alignment_sources": {"skill_sources": ["emsi"], "learning_resource_ids": ["W1HAobJsOGp36R5u9qRO"]}, "skill_alignment_sources": ["emsi"], "learning_resource_ids": ["W1HAobJsOGp36R5u9qRO"]},
    "query",
    {"emsi": [{"name": "Small Engine Repair", "id": "569IXAcnlOvfv2mwb1E8", "score": 0.984}, {"name": "Automobile Advanced Engine Performance Specialist", "id": "7buvwcDuvvKRGac12rWR", "score": 0.003}, {"name": "Certified Industrial Maintenance Mechanic", "id": "miiWPBs3B0h4g3TypSkn", "score": 0.001}]},
    {"data": {"W1HAobJsOGp36R5u9qRO": {"mapped_passages": [], "mapped_lus": [], "mapped_los": [], "mapped_subconcepts": [], "mapped_concepts": []}, "name": "Expert", "description": "Diagnose, adjust, repair, or overhaul small engines used to power lawn mowers, chain saws, recreational sporting equipment, and related equipment."}},
    {"data": {"name": "Expert", "description": "Diagnose, adjust, repair, or overhaul small engines used to power lawn mowers, chain saws, recreational sporting equipment, and related equipment.", "aligned_skills": {"emsi": [{"name": "Small Engine Repair", "id": "569IXAcnlOvfv2mwb1E8", "score": 0.984}, {"name": "Automobile Advanced Engine Performance Specialist", "id": "7buvwcDuvvKRGac12rWR", "score": 0.003}, {"name": "Certified Industrial Maintenance Mechanic", "id": "miiWPBs3B0h4g3TypSkn", "score": 0.001}]}, "aligned_knowledge": {"W1HAobJsOGp36R5u9qRO": {"mapped_passages": [], "mapped_lus": [], "mapped_los": [], "mapped_subconcepts": [], "mapped_concepts": []}}}}
  )
])
def test_create_response(get_unified_alignment_object, request_body, create_for,
  aligned_skills, aligned_knowledge, expected_response):
  response = get_unified_alignment_object.create_response(request_body,
  create_for, aligned_skills=aligned_skills,
  aligned_knowledge=aligned_knowledge)
  assert expected_response == response, "Expected response not the same"

def test_get_knowledge_alignments(clean_firestore, mocker, add_skills,
  add_learning_resource, get_unified_alignment_object):
  request_body = {
    "ids": [
      add_skills[2]
    ],
    "input_type": "skill",
    "top_k": 3,
    "output_alignment_sources": {
      "skill_sources": [
        "emsi"
      ],
      "learning_resource_ids": [
        add_learning_resource[0]
      ]
    },
    "learning_resource_ids": [
      add_learning_resource[0]
    ]
  }
  expected_response = {
    "data": {
      add_skills[2]: {add_learning_resource[0]: {"mapped_passages": [{"id": "NctXsNCc6YCqmX9Tw5Xc##2", "score": 0.955}, {"id": "TCmNZRm2pLyYLPUO6Gi3##1", "score": 0.628}, {"id": "TCmNZRm2pLyYLPUO6Gi3##4", "score": 0.881}, {"id": "aIJGT5uxdemGzNugwDSf##2", "score": 0.522}, {"id": "jDz7evRd6WtnoZHVApqW##0", "score": 0.996}, {"id": "jDz7evRd6WtnoZHVApqW##1", "score": 0.747}, {"id": "xefHtOUvPwXYphhRChpk##1", "score": 0.928}, {"id": "xefHtOUvPwXYphhRChpk##2", "score": 0.961}], "mapped_lus": [{"id": "jDz7evRd6WtnoZHVApqW", "score": 0.245}, {"id": "xefHtOUvPwXYphhRChpk", "score": 0.404}], "mapped_los": [], "mapped_subconcepts": [], "mapped_concepts": []}}
    }
  }
  mocker.patch(
    "services.skill_to_knowledge.skill_to_node.SkillNodeAlignment.map_nodes",
    return_value={add_learning_resource[0]: {"mapped_passages": [{"id": "NctXsNCc6YCqmX9Tw5Xc##2", "score": 0.955}, {"id": "TCmNZRm2pLyYLPUO6Gi3##1", "score": 0.628}, {"id": "TCmNZRm2pLyYLPUO6Gi3##4", "score": 0.881}, {"id": "aIJGT5uxdemGzNugwDSf##2", "score": 0.522}, {"id": "jDz7evRd6WtnoZHVApqW##0", "score": 0.996}, {"id": "jDz7evRd6WtnoZHVApqW##1", "score": 0.747}, {"id": "xefHtOUvPwXYphhRChpk##1", "score": 0.928}, {"id": "xefHtOUvPwXYphhRChpk##2", "score": 0.961}], "mapped_lus": [{"id": "jDz7evRd6WtnoZHVApqW", "score": 0.245}, {"id": "xefHtOUvPwXYphhRChpk", "score": 0.404}], "mapped_los": [], "mapped_subconcepts": [], "mapped_concepts": []}})
  response = get_unified_alignment_object.get_knowledge_alignments(
    request_body, "id")
  assert expected_response == response, "Expected response not the same"

def test_align_by_query(clean_firestore, mocker, add_skills,
  add_learning_resource, get_unified_alignment_object):
  request_body = {
    "name": "Expert",
    "description": "sample description",
    "input_type": "skill",
    "top_k": 3,
    "output_alignment_sources": {
      "skill_sources": [
        "test-source1"
      ],
      "learning_resource_ids": [
        add_learning_resource[0]
      ]
    },
    "learning_resource_ids": [
      add_learning_resource[0]
    ],
    "skill_alignment_sources": [
      "test-source1"
    ]
  }
  expected_response = {
    "data": {
      "name": "Expert",
      "description": "sample description",
      "aligned_skills": {
        "test-source1": [
          {
            "name": "Operating System Development",
            "id": add_skills[2],
            "score": 0.984
          }
        ]
      },
      "aligned_knowledge": {
        add_learning_resource[0]: {
          "mapped_passages": [],
          "mapped_lus": [],
          "mapped_los": [],
          "mapped_subconcepts": [],
          "mapped_concepts": []
        }
      }
    }
  }
  mocker.patch(
    "services.skill_to_knowledge.skill_to_node.SkillNodeAlignment.map_nodes",
    return_value={add_learning_resource[0]: {"mapped_passages": [], "mapped_lus": [], "mapped_los": [], "mapped_subconcepts": [], "mapped_concepts": []}})
  mocker.patch(
    "services.skill_alignment.skill_alignment.SkillAlignment.align_skills",
    return_value=[[{"name": "Operating System Development", "id": add_skills[2],
    "score": 0.984}]])
  response = get_unified_alignment_object.align_by_query(request_body)
  assert expected_response == response, "Expected response not the same"

def test_align_by_id(clean_firestore, mocker, add_skills,
  add_learning_resource, get_unified_alignment_object):
  request_body = {
    "ids": [
      add_skills[2]
    ],
    "input_type": "skill",
    "top_k": 1,
    "output_alignment_sources": {
      "skill_sources": [
        "test-source1"
      ],
      "learning_resource_ids": [
        add_learning_resource[0]
      ]
    },
    "learning_resource_ids": [
      add_learning_resource[0]
    ],
    "skill_alignment_sources": [
      "test-source1"
    ]
  }
  expected_response = {
    "data": {
      add_skills[2]: {
        "aligned_skills": {
          "test-source1": [
            {
              "name": "Operating System Development",
              "id": add_skills[2],
              "score": 0.984
            }
          ]
        },
        "aligned_knowledge": {
          add_learning_resource[0]: {
            "mapped_passages": [],
            "mapped_lus": [
              {"id": "jDz7evRd6WtnoZHVApqW", "score": 0.245}
            ],
            "mapped_los": [],
            "mapped_subconcepts": [],
            "mapped_concepts": []
          }
        }
      }
    }
  }
  mocker.patch(
    "services.skill_to_knowledge.skill_to_node.SkillNodeAlignment.map_nodes",
    return_value={add_learning_resource[0]: {"mapped_passages": [], "mapped_lus": [{"id": "jDz7evRd6WtnoZHVApqW", "score": 0.245}], "mapped_los": [], "mapped_subconcepts": [], "mapped_concepts": []}})
  mocker.patch(
    "services.skill_alignment.skill_alignment.SkillAlignment.align_skills",
    return_value=[[{"name": "Operating System Development", "id": add_skills[2],
    "score": 0.984}]])
  response = get_unified_alignment_object.align_by_id(request_body)
  assert expected_response == response, "Expected response not the same"
