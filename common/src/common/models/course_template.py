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

import datetime
import os

from common.models import BaseModel
from fireo.fields import TextField,DateTime,BooleanField

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class CourseTemplate(BaseModel):
  """Course ORM class
  """
  uuid=TextField()
  name = TextField(required=True)
  description = TextField(required=True)
  admin = TextField(required=True)
  instructional_designer=TextField(required=True)
  classroom_id=TextField()
  classroom_code=TextField()
  is_deleted = BooleanField(default=False)
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()
  deleted_at_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "course_templates"

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find a CourseTemplate using uuid (UUID)
    Args:
        uuid (string): CourseTemplate ID
    Returns:
        CourseTemplate: CourseTemplate Object
    """
    course_template = CourseTemplate.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", False).get()
    return course_template


  @classmethod
  def archive_by_uuid(cls, uuid):
    
    '''Soft Delete a Course Template by using uuid
      Args:
          uuid (String): Course Template ID
      '''
    course_template = CourseTemplate.collection.filter("uuid", "==", uuid).filter(
          "is_deleted", "==", False).get()
    if course_template is None:
      return False
    else:
      course_template.is_deleted = True
      course_template.deleted_at_timestamp = datetime.datetime.utcnow()
      course_template.update()
      return True
