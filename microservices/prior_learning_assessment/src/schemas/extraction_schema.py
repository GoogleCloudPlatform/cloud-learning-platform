"""
Pydantic Model for Extraction API's
"""
from typing import List, Optional
from pydantic import BaseModel


class BasicExtractionInputModel(BaseModel):
  """Extraction Input Skeleton Pydantic Model"""
  doc_class: Optional[str]
  context: Optional[str]
  gcs_urls: List[str]


class ExtractedEntityModel(BaseModel):
  """Individual Extracted Entity Pydantic Model"""
  text: Optional[str]
  score: Optional[float]


class ExtractedExperitenceModel(BaseModel):
  """Experience Skeleton Pydantic Model"""
  name: ExtractedEntityModel
  skills: ExtractedEntityModel
  competencies: ExtractedEntityModel
  organization: ExtractedEntityModel
  experience_title: ExtractedEntityModel
  date_completed: ExtractedEntityModel
  credits_earned: ExtractedEntityModel
  description: ExtractedEntityModel
  url: ExtractedEntityModel

class PostExtractionResponseModel(BaseModel):
  """Eaxtraction output response skeleton Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully parsed the transcript"
  data: Optional[List[ExtractedExperitenceModel]]
