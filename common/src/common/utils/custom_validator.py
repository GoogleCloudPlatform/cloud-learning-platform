"class for checking empty string and spaces"
from pydantic import BaseModel

class BaseConfigModel(BaseModel):
  """Base class for pydantic schema models where str validation required"""

  class Config:
    anystr_strip_whitespace = True
    min_anystr_length =1
    error_msg_templates = {
            "value_error.any_str.min_length":
              "String length must be at least {limit_value}",
            "validation_failed": "String is empty or has only spaces"
        }
