"""
Pydantic Model for Assessment Item API's
"""
from typing import List, Optional
from pydantic import BaseModel

class FileUploadResourcePathModel(BaseModel):
  """Pydantic Model for resource path of uploaded file"""
  resource_path: str

class FileUploadResponseModel(BaseModel):
  """Assessment Content Upload Response Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: FileUploadResourcePathModel

class SignedURLResponseModel(BaseModel):
  """ Pydantic Model for signed URL of each file"""
  file_size_bytes: Optional[int]
  file_path: str
  signed_url: Optional[str]
  status: Optional[str]

class GetSignedURLListResponseModel(BaseModel):
  """Assessment Linking Response Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[List[SignedURLResponseModel]]
