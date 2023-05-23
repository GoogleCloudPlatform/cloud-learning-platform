# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Module to add cohort in Fireo
"""
from fireo.fields import TextField, ListField, IDField, ReferenceField
from common.models import BaseModel, User

# pylint: disable=unused-argument

class UserChat(BaseModel):
  """UserChat ORM class
  """
  id = IDField()
  user = ReferenceField(User, required=True)
  llm_type = TextField(required=True)
  history = ListField(default=[])
  
  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "user_chats"

  @classmethod
  def find_by_user(cls,
                   userid,
                   llm_type,
                   order_by="-created_time",
                   limit=1000):
    """_summary_

    Args:
        

    Returns:
        _type_: _description_
    """
    return None
