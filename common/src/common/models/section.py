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
Module to add section in Fireo
"""
from fireo.fields import TextField, ReferenceField, IDField, NumberField
from common.models import BaseModel, CourseTemplate, Cohort


def check_section_status(field_val):
  """validator method for status field"""
  status = ["PROVISIONING", "FAILED_TO_PROVISION", "ACTIVE", "ARCHIVED"]
  if field_val.upper() in status:
    return True
  return (False, "Status must be one of " + ",".join("'" + i + "'"
                                                     for i in status))


def check_enrollment_status(field_val):
  """validator method for status field"""
  status = ["OPEN", "CLOSED"]
  if field_val.upper() in status:
    return True
  return (False, "Status must be one of " + ",".join("'" + i + "'"
                                                     for i in status))


class Section(BaseModel):
  """Section ORM class
  """
  id = IDField()
  name = TextField(required=True)
  section = TextField(required=True)
  description = TextField()
  classroom_id = TextField(required=True)
  classroom_code = TextField(required=True)
  classroom_url = TextField(required=True)
  course_template = ReferenceField(CourseTemplate, required=True)
  cohort = ReferenceField(Cohort, required=True)
  status = TextField(required=True,
                     default="PROVISIONING",
                     validator=check_section_status)
  enrollment_status = TextField(default="CLOSED",
                                validator=check_enrollment_status)
  enrolled_students_count = NumberField(default=0)
  max_students = NumberField()
  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "sections"

  @classmethod
  def fetch_all_by_cohort(cls,
                          cohort_key,
                          skip=0,
                          order_by="-created_time",
                          limit=1000):
    """_summary_

    Args:
        cohort_key (str): cohort unique key to filter data
        skip (int, optional): number of sections to be skip.
        order_by(str, optional): order list according to order_by field.
        limit (int, optional): limit till sections to be fetched.

    Returns:
        list: list of sections
    """
    objects = cls.collection.filter("cohort", "==", cohort_key).filter(
        "deleted_at_timestamp", "==",
        None).order(order_by).offset(skip).fetch(limit)
    return list(objects)

  @classmethod
  def get_section_by_status(cls,
                          status,
                          skip=0,
                          order_by="-created_time",
                          limit=1000):
    """_summary_

    Args:
        cohort_key (str): cohort unique key to filter data
        skip (int, optional): number of sections to be skip.
        order_by(str, optional): order list according to order_by field.
        limit (int, optional): limit till sections to be fetched.

    Returns:
        list: list of sections
    """
    objects = cls.collection.filter("status", "==", status).order(
      order_by).offset(skip).fetch(limit)
    return list(objects)
