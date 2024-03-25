"""
Pydantic Model for Query API's
"""
from typing import List,Optional
from pydantic import BaseModel

# pylint: disable=line-too-long


class QueryModel(BaseModel):
  """Query Pydantic Model"""
  deployed_index_id: str
  index_endpoint_id: str
  queries: List[List[float]]
  nearest_neighbors: Optional[int] = 1
  filters: Optional[List] = []


  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "deployed_index_id":
                "Sample Deployed Index id",
            "index_endpoint_id":
                "sample index endpoint id",
            "queries":
                [
                  [1.0, 2.0, 3.0],
                  [1.3, 2.2, 3.1]
                ]
        }
    }
