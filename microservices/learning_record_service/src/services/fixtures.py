"""Pytest fixtures for unit testing"""
import pytest
from common.models import (
  Learner, LearnerProfile, User, Agent, Verb,
  Skill, CurriculumPathway, LearningExperience,
  LearningObject, LearningResource, AssessmentItem,
  Achievement
)
from testing.testing_objects import (
  TEST_LEARNER, TEST_LEARNER_PROFILE, TEST_USER,
  TEST_AGENT, TEST_VERB, TEST_CURRICULUM_PATHWAY,
  TEST_LEARNING_EXPERIENCE, TEST_LEARNING_OBJECT,
  TEST_LEARNING_RESOURCE, TEST_ASSESSMENT_ITEM, TEST_SKILL,
  TEST_ACHIEVEMENT
)

@pytest.fixture(name="add_data")
def add_data():
  """Fixture to add data for Unit Tests"""
  # Add test learner
  test_learner = Learner()
  test_learner = test_learner.from_dict(TEST_LEARNER)
  test_learner.uuid = ""
  test_learner.save()
  test_learner.uuid = test_learner.id
  test_learner.update()

  # Add test learner profile
  test_learner_profile = LearnerProfile()
  test_learner_profile = test_learner_profile.from_dict(TEST_LEARNER_PROFILE)
  test_learner_profile.learner_id = test_learner.uuid
  test_learner_profile.uuid = ""
  test_learner_profile.save()
  test_learner_profile.uuid = test_learner_profile.id
  test_learner_profile.update()

  # Add test User
  test_user = User()
  test_user = test_user.from_dict(TEST_USER)
  test_user.user_id = ""
  test_user.save()
  test_user.user_id = test_user.id
  test_user.user_type_ref = test_learner.uuid
  test_user.update()

  # Add Agent
  test_agent = Agent()
  test_agent = test_agent.from_dict(TEST_AGENT)
  test_agent.user_id = test_user.user_id
  test_agent.uuid = ""
  test_agent.save()
  test_agent.uuid = test_agent.id
  test_agent.update()

  # Add Verb
  test_verb = Verb()
  test_verb = test_verb.from_dict(TEST_VERB)
  test_verb.uuid = ""
  test_verb.save()
  test_verb.uuid = test_verb.id
  test_verb.update()

  # Add skill
  test_skill = Skill()
  test_skill = test_skill.from_dict(TEST_SKILL)
  test_skill.save()
  test_skill.uuid = test_skill.id
  test_skill.update()

  # Add Curriculum Pathway
  test_pathway = CurriculumPathway()
  test_pathway = test_pathway.from_dict(TEST_CURRICULUM_PATHWAY)
  test_pathway.uuid = ""
  test_pathway.save()
  test_pathway.uuid = test_pathway.id
  test_pathway.update()

  # Add Learning Experience
  test_le = LearningExperience()
  test_le = test_le.from_dict(TEST_LEARNING_EXPERIENCE)
  test_le.uuid = ""
  test_le.save()
  test_le.uuid = test_le.id
  test_le.update()

  # Add Learning Object
  test_lo = LearningObject()
  test_lo = test_lo.from_dict(TEST_LEARNING_OBJECT)
  test_lo.uuid = ""
  test_lo.save()
  test_lo.uuid = test_lo.id
  test_lo.update()

  # Add Learning Resource
  test_lr = LearningResource()
  test_lr = test_lr.from_dict(TEST_LEARNING_RESOURCE)
  test_lr.uuid = ""
  test_lr.save()
  test_lr.uuid = test_lr.id
  test_lr.update()

  # Add Assessment Item
  test_assessment_item = AssessmentItem()
  test_assessment_item = test_assessment_item.from_dict(
    TEST_ASSESSMENT_ITEM)
  test_assessment_item.uuid = ""
  test_assessment_item.save()
  test_assessment_item.uuid = test_assessment_item.id
  test_assessment_item.update()

  # Add Achievement
  test_achievement = Achievement()
  test_achievement = test_achievement.from_dict(
    TEST_ACHIEVEMENT)
  test_achievement.uuid = ""
  test_achievement.save()
  test_achievement.uuid = test_achievement.id
  test_achievement.update()

  # Adding the relation for Assessment
  test_assessment_item.parent_nodes = {
    "learning_objects": [test_lo.uuid]
  }

  # Adding the relation for Learning Resource
  test_lr.parent_nodes = {
    "learning_objects": [test_lo.uuid]
  }

  # Adding the relation for Learning Object
  test_lo.parent_nodes = {
    "learning_experiences": [test_le.uuid]
  }
  test_lo.child_nodes = {
    "learning_resources": [test_lr.uuid],
    "assessment_items": [test_assessment_item.uuid]
  }

  # Adding the relation for Learning Experience
  test_le.parent_nodes = {
    "curriculum_pathways": [test_pathway.uuid]
  }
  test_le.child_nodes = {
    "learning_objects": [test_lo.uuid]
  }

  # Adding the relation for Curriculum Pathway
  test_pathway.child_nodes = {
    "learning_experiences": [test_le.uuid]
  }

  # Adding Achievements to Learning Experience
  test_le.achievements = [test_achievement.uuid]

  # Adding Skill to Learning Resource
  test_lr.references = {
    "skills": [test_skill.uuid]
  }

  test_assessment_item.update()
  test_lr.update()
  test_lo.update()
  test_le.update()
  test_pathway.update()

  return {
    "learner": test_learner,
    "learner_profile": test_learner_profile,
    "user": test_user,
    "agent": test_agent,
    "verb": test_verb,
    "skill": test_skill,
    "pathway": test_pathway,
    "learning_experience": test_le,
    "learning_resource": test_lr,
    "assessment": test_assessment_item,
    "achievement": test_achievement,
    "learning_object": test_lo

  }
