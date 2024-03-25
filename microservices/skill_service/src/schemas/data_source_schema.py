"""
Pydantic Model for Data source API's
"""
from typing import Optional
from pydantic import BaseModel

# pylint: disable=line-too-long

class CreateDataSourceRequestModel(BaseModel):
  """Insert Data for new source Request Pydantic Model"""
  type: str
  source: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "type": "skill",
            "source": "emsi"
        }
    }

class UpdateDataSourceRequestModel(BaseModel):
  """Update Data Source Request Pydantic Model"""
  type: str
  source: str
  matching_engine_index_id: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "type": "skill",
            "source": "emsi",
            "matching_engine_index_id": "2564025931601543168"
        }
    }

class CreateDataSourceResponseModel(BaseModel):
  """Create Data Source Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created/updated the data source"
  data: Optional[dict]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created/updated the data source",
            "data": {
                    "type": "skill",
                    "source": ["emsi"],
                    "matching_engine_index_id": {
                                                "emsi": "2564025931601543168"
                                                }
                    }
            }
        }

class UpdateDataSourceResponseModel(BaseModel):
  """Update Data Source Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the data source"
  data: Optional[dict]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the data source",
            "data": {
                    "type": "skill",
                    "source": ["emsi"],
                    "matching_engine_index_id": {
                                                "emsi": "2564025931601543168"
                                                }
                    }
            }
        }

class DataSourceResponseModel(BaseModel):
  """Data Source Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the data sources"
  data: Optional[list]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the data sources",
            "data": [
                        {
                          "type": "skill",
                          "source": ["snhu", "emsi"],
                          "matching_engine_index_id": {
                                                "emsi": "8299360057057869824",
                                                "snhu": "7994663394768584704"
                                                }
                    },
                        {
                          "type": "role",
                          "source": ["o*net"],
                          "matching_engine_index_id": {}
                    }
                ]
            }
        }


class DeleteDataSource(BaseModel):
  """Delete Domain Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the data source"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the data source"
        }
    }
