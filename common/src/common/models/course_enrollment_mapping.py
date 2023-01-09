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
Module to add cohort in Fireo
"""
from fireo.fields import TextField, ReferenceField, IDField
from common.models import BaseModel,Section


class CourseEnrollmentMapping(BaseModel):
  """Course Enrollment Mapping ORM class
  """
  id = IDField()
  section = ReferenceField(Section,required=True)
  user = TextField(required=True)
  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "course_enrollment_mapping"

  @classmethod
  def find_by_user(cls, user_id):
    """Find the rubric item using name
    Args:
        name (string): node item name
    Returns:
        Rubric: Rubric Object
    """
    return CourseEnrollmentMapping.collection.filter("user", "==", user_id).fetch()