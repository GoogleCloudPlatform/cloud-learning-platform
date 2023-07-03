""" conftest.py: Consist of fixtures"""
import pytest
from common.models import (LearningObject, LearningExperience,
                           CurriculumPathway, LearningResource)


@pytest.fixture(name="create_learning_object")
def create_learning_object(request):
  learning_object = LearningObject.from_dict(request.param)
  learning_object.uuid = ""
  learning_object.version = 1
  learning_object.save()
  learning_object.uuid = learning_object.id
  learning_object.update()
  return learning_object


@pytest.fixture(name="create_learning_experience")
def create_learning_experience(request):
  learning_experience = LearningExperience.from_dict(request.param)
  learning_experience.uuid = ""
  learning_experience.version = 1
  learning_experience.save()
  learning_experience.uuid = learning_experience.id
  learning_experience.update()
  return learning_experience


@pytest.fixture(name="create_curriculum_pathway")
def create_curriculum_pathway(request):
  curriculum_pathway = CurriculumPathway.from_dict(request.param)
  curriculum_pathway.uuid = ""
  curriculum_pathway.version = 1
  curriculum_pathway.save()
  curriculum_pathway.uuid = curriculum_pathway.id
  curriculum_pathway.update()
  return curriculum_pathway


@pytest.fixture(name="create_learning_resource")
def create_learning_resource(request):
  learning_resource = LearningResource.from_dict(request.param)
  learning_resource.uuid = ""
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()
  return learning_resource
