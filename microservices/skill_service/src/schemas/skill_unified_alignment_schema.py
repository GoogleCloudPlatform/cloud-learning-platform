"""
Pydantic Model for Unified Skill Alignment APIs
"""
from typing import Dict, List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, conlist

# pylint: disable= line-too-long,invalid-name

ALLOWED_OBJECT_TYPES = Literal["skill"]

class AlignByIdsRequestModel(BaseModel):
  """Request Model for Unified Skill Alignment"""
  ids: conlist(str, min_items=1)
  input_type: ALLOWED_OBJECT_TYPES
  top_k: Optional[int] = 10
  output_alignment_sources: Dict[str, List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "ids": [
          "ZJYw5XczcLAEtdM081oG",
          "0QLxMB93ERzrSSJSyxQk",
          "yLBCSJBKYekcMicNy4eD"
        ],
        "input_type": "skill",
        "top_k": 5,
        "output_alignment_sources": {
          "skill_sources": [
            "emsi"
          ],
          "learning_resource_ids": [
            "kAf6WVUL3hg8V5wHfwq4"
          ]
        }
      }
    }


class BaseResponse(BaseModel):
  name: str
  id: str
  score: float

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "id": "0pgLV4eAsbzdMLVzFul5",
            "name": "Communication Access",
            "score": 0.9822302460670471
        }
    }


class NodeItem(BaseModel):
  """Model for Knowledge node item"""
  id: str
  title: str
  score: float


class MappedNodeResponse(BaseModel):
  mapped_passages: List[NodeItem]
  mapped_lus: List[NodeItem]
  mapped_los: List[NodeItem]
  mapped_subconcepts: List[NodeItem]
  mapped_concepts: List[NodeItem]


class UnifiedResponseModel(BaseModel):
  aligned_skills: Optional[Dict[str, List[BaseResponse]]]
  aligned_knowledge: Optional[Dict[str, MappedNodeResponse]]


class AlignByIdsResponseModel(BaseModel):
  """Response Model Unified Skill Alignment"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully found the alignments for "\
    "the given id(s)"
  data: Optional[Dict[str, UnifiedResponseModel]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully found the alignments for the given id(s)",
        "data": {
            "3kx3zp90VE6Xxckn1zCI": {
                "aligned_skills": {
                    "emsi": [
                        {
                            "name": "Operating Systems",
                            "id": "15aor2vzGW9aVOvM2opG",
                            "score": 0.9989437460899353
                        },
                        {
                            "name": "Embedded Operating Systems",
                            "id": "yjTLzgWDPka0VSdEXB9X",
                            "score": 0.9295615553855896
                        },
                        {
                            "name": "Disk Operating Systems",
                            "id": "fpvUai1iQsLS4i3JTu2S",
                            "score": 0.7733532190322876
                        },
                        {
                            "name": "Computer Systems",
                            "id": "ExHY2UFUD6RYL422vPb8",
                            "score": 0.4581495225429535
                        },
                        {
                            "name": "Operating System Development",
                            "id": "pzAvrAzdT9JAW4pG742D",
                            "score": 0.4352039396762848
                        }
                    ]
                },
                "aligned_knowledge": {
                  "W1HAobJsOGp36R5u9qRO": {
                    "mapped_passages": [
                        {
                            "id": "2wqkWA3tKwslu0CL0Cal##0",
                            "score": 0.711
                        },
                        {
                            "id": "Ht3G2zabdsFTc5v53pgG##0",
                            "score": 0.978
                        }
                    ],
                    "mapped_lus": [
                        {
                            "id": "Ht3G2zabdsFTc5v53pgG",
                            "score": 0.863
                        },
                        {
                            "id": "NctXsNCc6YCqmX9Tw5Xc",
                            "score": 0.856
                        }
                    ],
                    "mapped_los": [
                        {
                            "id": "yLnGsubidAEH2OZuf32M",
                            "score": 0.564
                        }
                    ],
                    "mapped_subcompetencies": [],
                    "mapped_competencies": []
                  }
                }
            }
          }
        }
    }


class AlignByQueryRequestModel(BaseModel):
  """Request Model for Unified Skill Alignment"""
  name: Optional[str]
  description: Optional[str]
  input_type: ALLOWED_OBJECT_TYPES
  top_k: Optional[int] = 10
  output_alignment_sources: Dict[str, List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "name": "Power Plant Operators",
        "description": "Control, operate, or maintain machinery to "
        "generate electric power. Includes auxiliary equipment operators.",
        "input_type": "skill",
        "top_k": 5,
        "output_alignment_sources": {
          "skill_sources": [
              "osn"
          ],
          "learning_resource_ids": [
            "0254iM8tMzR7XaKdWoxQ"
          ]
        }
      }
    }


class QueryResponseModel(BaseModel):
  name: Optional[str]
  description: Optional[str]
  aligned_skills: Optional[Dict[str, List[BaseResponse]]]
  aligned_knowledge: Optional[Dict[str, MappedNodeResponse]]


class AlignByQueryResponseModel(BaseModel):
  """Response Model Unified Skill Alignment"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully found the alignments "\
    "for the given query"
  data: Optional[QueryResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
          "success": True,
          "message": "Successfully found the alignments for the given query",
          "data": {
            "name": "Power Plant Operators",
            "description": "Control, operate, or maintain machinery to generate electric power. Includes auxiliary equipment operators.",
            "aligned_skills": {
              "emsi": [
                {
                  "name": "Transmission System Operator",
                  "id": "N0L5Hg0oFjh2onMmPN6C",
                  "score": 0.4599936008453369
                },
                {
                  "name": "Electric Utility",
                  "id": "VGrzrFIAFppO8EgUjaN6",
                  "score": 0.2736193537712097
                },
                {
                  "name": "Steam Power Plant",
                  "id": "i2wFJCCJCzkvarxxFX39",
                  "score": 0.2654588222503662
                },
                {
                  "name": "Certified Plant Maintenance Manager",
                  "id": "toyYfHQdAKE1Q7FFcHr3",
                  "score": 0.2308318316936493
                },
                {
                  "name": "Electrical Equipment",
                  "id": "Ia0v6vDYsAaxz0GjRuRy",
                  "score": 0.19369706511497498
                }
              ]
            },
            "aligned_knowledge": {
              "W1HAobJsOGp36R5u9qRO": {
                "mapped_passages": [
                  {
                      "id": "DRnIsyGOgToPTtTK4tSy##0",
                      "score": 0.743
                  }
                ],
                "mapped_lus": [
                  {
                      "id": "DRnIsyGOgToPTtTK4tSy",
                      "score": 0.743
                  }
                ],
                "mapped_los": [],
                "mapped_subcompetencies": [],
                "mapped_competencies": []
              }
            }
          }
        }
    }


class UnifiedBatchRequestModel(BaseModel):
  """Request Model for Unified Skill Alignment using Batch Jobs"""
  ids: Optional[List[str]]
  source_name: Optional[List[str]]
  input_type: ALLOWED_OBJECT_TYPES
  top_k: Optional[int] = 10
  output_alignment_sources: Dict[str, List[str]]
  update_alignments: Optional[bool] = True

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "ids": [
          "ZJYw5XczcLAEtdM081oG",
          "5nySGat8HgnfwvZL08ys"
        ],
        "source_name": [
        ],
        "input_type": "skill",
        "top_k": 5,
        "output_alignment_sources": {
          "skill_sources": [
            "osn"
          ],
          "learning_resource_ids": [
            "kAf6WVUL3hg8V5wHfwq4"
          ]
        },
        "update_alignments": True
      }
    }
