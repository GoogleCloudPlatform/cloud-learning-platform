"""
Pydantic Model for Content Serving API's
"""
from typing import Optional, List
from pydantic import BaseModel
from config import LR_TYPES


class Data(BaseModel):
  job_name: Optional[str]
  status: Optional[str]
  meta_data: Optional[dict]


class BatchJobModel(BaseModel):
  """Batch Job Response Pydantic Model"""
  success: bool
  message: str
  data: Optional[Data]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully initiated the job with type \
              'validate_and_upload_zip'. Please use the job name \
                to track the job status",
            "data": {
                "job_name": "abcd-ajdf-sdfk-sdff",
                "status": "active"
            }
        }
    }

class SignedUrlDataModel(BaseModel):
  signed_url: str
  resource_type: Optional[str]
  resource_uuid: str


class GetSignedUrlModelResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the signed url"
  data: Optional[SignedUrlDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the signed url",
            "data": {
                "signed_url": "http://some/signed_url",
                "resource_type": "html",
                "resource_uuid": "lr_uuid"
            }
        }
    }

class ContentUploadResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully uploaded the learning content"
  data: Optional[SignedUrlDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully uploaded the learning content",
            "data": {
                "signed_url": "http://some/signed_url",
                "resource_type": "html",
                "resource_uuid": "lr_uuid"
            }
        }
    }

class ContentPublishResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully published content"
  data: Optional[SignedUrlDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully published content",
            "data": {
                "signed_url": "http://some/signed_url",
                "resource_type": "html",
                "resource_uuid": "lr_uuid"
            }
        }
    }

class ContentLinkInputModel(BaseModel):
  resource_path: str
  type: LR_TYPES

class ContentLinkResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully linked learning resource with content"
  data: Optional[SignedUrlDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully linked learning resource with content",
            "data": {
                "signed_url": "http://some/signed_url",
                "resource_type": "html",
                "resource_uuid": "lr_uuid"
            }
        }
    }

class BlobListModel(BaseModel):
  prefix: str
  files: List[str]
  folders: List[str]
class ListFilesAndFolderResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully listed all files and folder \
                            at given prefix"
  data: Optional[BlobListModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully listed all files and folder at given \
                        prefix",
            "data": {
                "prefix": "abc/",
                "files": ["abc/index.html"],
                "folders": ["scripts","styles","assets"]
            }
        }
    }

class ContentVersionModel(BaseModel):
  """Pydantic model for Content Versions"""
  resource_path: Optional[str]
  type: Optional[str]
  content_version_uuid: Optional[str]
  created_time: Optional[str]
  last_published_on: Optional[str]
  status: Optional[str]

  def __init__(self, **kwargs):
    if kwargs["status"] == "initial":
      kwargs["status"] = "draft"
    super().__init__(**kwargs)

class GetContentVersionsResponse(BaseModel):
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched all content versions"
  data: Optional[List[ContentVersionModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched all content versions",
            "data": [{
                "resource_path": "/some/resource/path",
                "type":"pdf",
                "content_version_uuid": "efb382hf32b8nlweife",
                "last_published_on": "2022-03-03 09:22:49.843674+00:00",
                "status": "draft"
            }]
        }
    }
