"""
Pydantic Model for Search in Skill Graph
"""
from typing import List, Optional, Dict
from pydantic import BaseModel
from config import ALLOWED_SKILLGRAPH_LEVELS, SKILL_GRAPH_LEVELS

# pylint: disable = line-too-long
class SemanticSearchRequestModel(BaseModel):
  query: str
  levels: Optional[List[ALLOWED_SKILLGRAPH_LEVELS]] = SKILL_GRAPH_LEVELS
  top_k: Optional[int] = 10

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "query": "cyber security",
            "levels": ["domain", "skill"],
            "top_k": 5
        }
    }


class MappingObject(BaseModel):
  id: str
  name: str
  score: float

class QueryData(BaseModel):
  query: str
  domain: Optional[List[MappingObject]] = []
  sub_domain: Optional[List[MappingObject]] = []
  category: Optional[List[MappingObject]] = []
  competency: Optional[List[MappingObject]] = []
  skill: Optional[List[MappingObject]] = []


class SemanticSearchResponseModel(BaseModel):
  success: bool = True
  message: str = "Successfully searched results for given query"
  data: Optional[QueryData]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
          "success": True,
          "message": "Successfully searched results for given query",
          "data": {
              "query": "cyber security",
              "domain": [
                  {
                      "id": "0026jXQm8gMnYbHMgcMC",
                      "name": "Healthcare",
                      "score": 1.617691850697156e-05
                  },
                  {
                      "id": "0DfFGkXB7PwLiRqiRQAo",
                      "name": "Healthcare",
                      "score": 1.617691850697156e-05
                  },
                  {
                      "id": "0MkP0AguFxzHYdOMSCJo",
                      "name": "Healthcare",
                      "score": 1.617691850697156e-05
                  },
                  {
                      "id": "14afMP1DsFsOaO7estMW",
                      "name": "Healthcare",
                      "score": 1.617691850697156e-05
                  },
                  {
                      "id": "1Gxuqngkw2wNc80fy3YM",
                      "name": "Healthcare",
                      "score": 1.617691850697156e-05
                  }
              ],
              "sub_domain": [],
              "category": [],
              "competency": [],
              "skill": [
                  {
                      "id": "BZvHuBO2y4qVE82bPR65",
                      "name": "Situational Security Assessment",
                      "score": 0.8299806714057922
                  },
                  {
                      "id": "VArMJ4g797du7dlkysue",
                      "name": "Network Security IT Professionals",
                      "score": 0.10509206354618073
                  },
                  {
                      "id": "9rT6EsB38MHv7cyiX2DQ",
                      "name": "System & Network Protection",
                      "score": 0.06888928264379501
                  },
                  {
                      "id": "xeiwmWvwKHTOoWMwE6L1",
                      "name": "System & Network Protection",
                      "score": 0.017801878973841667
                  },
                  {
                      "id": "munEHhQNrj2d3T3ZdmqU",
                      "name": "Breach Protection & Prevention",
                      "score": 0.01055500004440546
                  }
              ]
          }
  }
}


class KeywordSearchRequestModel(BaseModel):
  name: Optional[str]
  keyword: Optional[str]
  levels: Optional[List[ALLOWED_SKILLGRAPH_LEVELS]] = SKILL_GRAPH_LEVELS

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "name": "Digital Evidence Law Awareness",
            "keyword": "Presentations",
            "levels": [
                "domain",
                "sub_domain",
                "category",
                "competency",
                "skill"
            ]
        }
    }


class KeywordSearchResponseModel(BaseModel):
  """Skill Search Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the skills"
  data: Optional[Dict[str, List]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the skills",
            "data": {
                "domain": [],
                "sub_domain": [],
                "category": [
                    {
                        "uuid": "pRM5G3APsOSuC7aEN0Ed",
                        "name": "Teaching",
                        "description": "",
                        "keywords": [],
                        "parent_nodes": [],
                        "reference_id": "",
                        "source_uri": "",
                        "source_name": "osn",
                        "created_time": "2022-04-12 09:53:40.028719+00:00",
                        "last_modified_time": "2022-04-12 09:53:40.139412+00:00",
                        "created_by": "",
                        "last_modified_by": ""
                    }
                ],
                "competency": [],
                "skill": [
                    {
                        "uuid": "KS120PQ6XD1JWMFQVJNW",
                        "name": "Teaching",
                        "description": "A teacher is a person who helps students to acquire knowledge, competence or virtue.",
                        "keywords": [],
                        "author": "",
                        "creator": "",
                        "alignments": {
                            "organizational_alignment": "",
                            "external_skill_alignment": {},
                            "credential_alignment": "",
                            "standard_alignment": ""
                        },
                        "organizations": [],
                        "certifications": [],
                        "occupations": {
                            "broad_occupation": "",
                            "occupations_major_group": "",
                            "detailed_occupation": "",
                            "occupations_minor_group": ""
                        },
                        "onet_job": "",
                        "type": {
                            "id": "ST2",
                            "name": "Common Skill"
                        },
                        "parent_nodes": [],
                        "reference_id": "KS120PQ6XD1JWMFQVJNW",
                        "source_uri": "https://skills.emsidata.com/skills/KS120PQ6XD1JWMFQVJNW",
                        "source_name": "emsi",
                        "created_time": "2022-03-03 09:24:37.789116+00:00",
                        "last_modified_time": "2022-03-03 09:24:37.789116+00:00",
                        "created_by": "",
                        "last_modified_by": ""
                    }
                ]
            }
        }
    }
