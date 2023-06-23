"""Schema for training IRT"""

from typing import Optional
from pydantic import BaseModel


class TrainIRTRequest(BaseModel):
  level: str
  update_collections: Optional[bool] = False
  id : str


