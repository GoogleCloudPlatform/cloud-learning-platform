# Copyright 2022 Google LLC
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
Module to add course in Fireo
"""

from fireo.fields import TextField, IDField
from common.models import BaseModel


class CourseTemplate(BaseModel):
  """Course ORM class
  """
  id = IDField()
  name = TextField(required=True)
  description = TextField(required=True)
  admin = TextField(required=True, format="lower")
  classroom_id = TextField()
  classroom_code = TextField()
  classroom_url = TextField()

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "course_templates"
