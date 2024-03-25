"""
Pydantic Model for Knowledge embedding APIs
"""
from typing import List
from pydantic import BaseModel, Extra


class SkillGraphEmbd(BaseModel):
  level: List[str]
  source: List[str]

  def __getitem__(self, item):
    return getattr(self, item)

  class Config:
    extra = Extra.forbid


class KnowledgeGraphEmbd(BaseModel):
  level: List[str]

  def __getitem__(self, item):
    return getattr(self, item)

  class Config:
    extra = Extra.forbid


class LearningContentEmbd(BaseModel):
  ids: List[str]

  def __getitem__(self, item):
    return getattr(self, item)

  class Config:
    extra = Extra.forbid


class PopulateEmbdRequestModel(BaseModel):
  """Request model"""
  skill_graph: SkillGraphEmbd
  knowledge_graph: KnowledgeGraphEmbd
  learning_resource: LearningContentEmbd

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
          "skill_graph": {
            "level": ["domain"],
            "source": ["emsi"]
          },
          "knowledge_graph": {
            "level": ["concepts", "sub_concepts"]
          },
          "learning_resource": {
            "ids": ["kAf6WVUL3hg8V5wHfwq4"]
          }
        }
    }
