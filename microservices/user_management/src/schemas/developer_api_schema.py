"""
Pydantic Model for Developer API
"""
from typing import List, Optional
from pydantic import BaseModel, Extra
from common.utils.schema_validator import BaseConfigModel

class FieldsModel(BaseModel):
  key: str
  existing_value: Optional[str]
  new_value: Optional[str]
  delete_key: Optional[bool]


class BasicUpdateModel(BaseConfigModel):
  collection_name: str
  fields: List[FieldsModel]

  class Config():
    orm_mode = True
    extra = Extra.forbid
