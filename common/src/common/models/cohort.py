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
from fireo.fields import TextField, DateTime, NumberField, ReferenceField, IDField
from common.models import BaseModel, CourseTemplate


def check_non_zero_number(field_val):
  """validator method for max_student field"""
  if field_val == 0:
    return (False,"Max student value in cohort cannot be zero")
  else:
    return True


class Cohort(BaseModel):
  """Cohort ORM class
  """
  id = IDField()
  name = TextField(required=True)
  description = TextField(required=True)
  start_date = DateTime(required=True)
  end_date = DateTime(required=True)
  registration_start_date = DateTime(required=True)
  registration_end_date = DateTime(required=True)
  max_students = NumberField(required=True,validator=check_non_zero_number)
  enrolled_students_count = NumberField(default=0)
  course_template = ReferenceField(CourseTemplate, required=True)

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "cohorts"
  @classmethod
  def fetch_all_by_course_template(cls,
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
