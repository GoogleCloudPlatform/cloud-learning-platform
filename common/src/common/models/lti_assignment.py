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
Module to add lti assignment in FireO
"""
from fireo.fields import TextField, DateTime, IDField
from common.models import BaseModel


class LTIAssignment(BaseModel):
  """LTI Assignment Data Model"""
  id = IDField()
  section_id = TextField()
  lti_content_item_id = TextField()
  tool_id = TextField()
  course_work_id = TextField()
  start_date = DateTime()
  end_date = DateTime()
  due_date = DateTime()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "lti_assignments"
    ignore_none_field = False
