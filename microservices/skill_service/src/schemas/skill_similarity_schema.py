"""
Pydantic Model for Skill Alignment APIs
"""
from typing import Dict, Optional
from pydantic import BaseModel

class SimilarityScoreRequestModel(BaseModel):
  id_1: str
  id_2: str
  data_source: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "id_1": "WqkAqVrY2MPV8iPs3ukH",
            "id_2": "V6GIQyXVgPbfrunDOQuW",
            "data_source": "osn"
        }
    }


class SimilarityScoreResponseModel(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully calculated the similarity score."
  data: Optional[Dict[str, float]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully calculated the similarity score.",
            "data": {
                "similarity_score": 2.412006324448157e-05
            }
        }
    }
