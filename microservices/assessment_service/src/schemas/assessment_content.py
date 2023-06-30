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

class FileDescriptionResponseModel(BaseModel):
  """Pydantic Model for File Description"""
  file_size_bytes: Optional[int]
  file_path: str

class InputFileListModel(BaseModel):
  """ Pydantic Model for file list input """
  file_list: List[str]

class FileDeleteSuccessResponseModel(BaseModel):
  """ Pydantic Model for file delete success response"""
  success: Optional[bool]
  message: Optional[str]
  data: List[str]

class GetSignedURLListResponseModel(BaseModel):
  """Assessment Linking Response Pydantic Model"""
  success: Optional[bool]
  message: Optional[str]
  data: Optional[List[SignedURLResponseModel]]

class GetFileListResponseModel(BaseModel):
  """ Pydantic model for fetching file list """
  success: Optional[bool]
  message: Optional[str]
  data: Optional[List[FileDescriptionResponseModel]]
