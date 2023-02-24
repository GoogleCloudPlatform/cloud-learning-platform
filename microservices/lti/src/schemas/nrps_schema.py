"""
Pydantic Model for NRPS API's
"""
from pydantic import BaseModel
from typing import Optional
from schemas.schema_examples import NRPS_EXAMPLE


# pylint: disable = invalid-name
class GetNRPSModel(BaseModel):
  """Basic NRPS Pydantic Model"""
  id: str
  context: Optional[dict] = {}
  members: Optional[list] = []

  class Config():
    orm_mode = True
    schema_extra = {"example": NRPS_EXAMPLE}
