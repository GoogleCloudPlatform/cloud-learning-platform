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
Module to add course enrollment in Fireo
"""
from fireo.fields import TextField, ReferenceField, IDField
from common.models import BaseModel,Section

def check_status(field_val):
  """validator method for status field"""
  status = ["active", "inactive"]
  if field_val.lower() in ["active", "inactive"]:
    return True
  return (False,
          "Status must be one of " + ",".join("'" + i + "'" for i in status))

def check_role(field_val):
  """validator method for status field"""
  role = ["learner", "faculty","other"]
  if field_val.lower() in ["learner", "faculty","other"]:
    return True
  return (False,
          "role must be one of " + ",".join("'" + i + "'" for i in role))

class CourseEnrollmentMapping(BaseModel):
  """Course Enrollment Mapping ORM class
  """
  id = IDField()
  section = ReferenceField(Section,required=True)
  user = TextField(required=True)
  status = TextField(validator=check_status)
  role = TextField(validator=check_role)

  class Meta:
    ignore_none_field = False
    collection_name = BaseModel.DATABASE_PREFIX + "course_enrollment_mapping"
  @classmethod
  def find_by_user(cls, user_id):
    """Find user using using user_id
    Args:
        user_id (string): node item name
    Returns:
        user_object
    """
    result = CourseEnrollmentMapping.collection.filter("user","==",user_id).\
      filter(
        "status", "==","active").fetch()
    return list(result)

  @classmethod
  def fetch_all_by_section(cls,
                          section_key,
                          role,
                          ):
    """_summary_

    Args:
        cohort_key (str): cohort unique key to filter data
        skip (int, optional): number of sections to be skip.
        order_by(str, optional): order list according to order_by field.
        limit (int, optional): limit till sections to be fetched.

    Returns:
        list: list of sections
    """
    objects = CourseEnrollmentMapping.collection.\
      filter("section", "==", section_key).filter(
        "status", "==","active").filter("role", "==",role).fetch()
    return list(objects)
