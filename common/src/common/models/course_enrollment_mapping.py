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
  section = ReferenceField(Section)
  user = TextField()
  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "courseenrollmentmapping"

  @classmethod
  def fetch_all_by_courseenrollmentmapping(cls,
                                   course_template_key,
                                   skip=0,
                                   order_by="-created_time",
                                   limit=1000):
    """_summary_

    Args:
        course_template_key (str): course_template unique key to filter data.
        skip (int, optional): number of cohorts to be skip.
        order_by (str, optional): order list according to order_by field.
        limit (int, optional): limit till cohorts to be fetched.

    Returns:
        _type_: _description_
    """
    objects = cls.collection.filter(
        "course_template", "==", course_template_key).filter(
            "deleted_at_timestamp", "==",
            None).order(order_by).offset(skip).fetch(limit)
    return list(objects)
