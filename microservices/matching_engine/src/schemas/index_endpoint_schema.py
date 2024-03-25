"""
Pydantic Model for Index API's
"""
from pydantic import BaseModel

# pylint: disable=line-too-long

class CreateIndexEndpointModel(BaseModel):
  """Create Index Pydantic Model"""
  display_name: str

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "display_name":
                "Sample Index Endpoint",
        }
    }
