"""
Pydantic Model for deploy API's
"""
from typing import Optional
from pydantic import BaseModel

# pylint: disable=line-too-long

class DeployIndexModel(BaseModel):
  """Deploy Index Pydantic Model"""
  deployed_index_display_name: str
  index_id: str
  index_endpoint_id: str
  machine_type: Optional[str] = "e2-standard-2"
  min_replica_count: Optional[int] = 1
  max_replica_count: Optional[int] = 1

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "deployed_index_display_name":
                "Sample Deployed Index",
            "index_id": 8723824321937539027,
            "index_endpoint_id": 4437945589052735848,
            "machine_type": "e2-standard-2",
            "min_replica_count": 1,
            "max_replica_count": 1
        }
    }

class UndeployIndexModel(BaseModel):
  """Undeploy Index Pydantic Model"""
  deployed_index_id: str
  index_endpoint_id: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "deployed_index_id": 8723824321937539027,
            "index_endpoint_id": 4437945589052735848
        }
    }
