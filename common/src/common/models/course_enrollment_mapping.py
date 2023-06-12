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
from common.models import BaseModel, Section, User


def check_status(field_val):
  """validator method for status field"""
  status = ["active", "inactive", "invited"]
  if field_val.lower() in ["active", "inactive", "invited"]:
    return True
  return (False, "Status must be one of " + ",".join("'" + i + "'"
                                                     for i in status))


def check_role(field_val):
  """validator method for status field"""
  role = ["learner", "faculty", "admin"]
  if field_val.lower() in ["learner", "faculty", "other", "admin"]:
    return True
  return (False, "role must be one of " + ",".join("'" + i + "'"
                                                   for i in role))


class CourseEnrollmentMapping(BaseModel):
  """Course Enrollment Mapping ORM class
  """
  id = IDField()
  section = ReferenceField(Section, required=True)
  user = ReferenceField(User, required=True)
  status = TextField(validator=check_status)
  role = TextField(validator=check_role)
  invitation_id = TextField()

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
    user_key = f"{User.collection_name}/{user_id}"
    result = CourseEnrollmentMapping.collection.filter("user","==",user_key).\
      filter(
        "status", "==","active").fetch()
    return list(result)

  @classmethod
  def fetch_all_by_section(
      cls,
      section_key,
      role,
  ):
    """_summary_

    Args:
        section_key (str): section unique key to filter data
        skip (int, optional): number of sections to be skip.
        order_by(str, optional): order list according to order_by field.
        limit (int, optional): limit till sections to be fetched.

    Returns:
        list: list of sections
    """
    objects = CourseEnrollmentMapping.collection.\
      filter("section", "==", section_key).filter(
        "status", "in",["active","invited"]).filter("role", "==",role).fetch()
    return list(objects)

  @classmethod
  def fetch_users_by_section(
      cls,
      section_key):
    """_summary_

    Args:
      section_key (str): cohort unique key to filter data
    Returns:
      list: list of sections
    """
    objects = CourseEnrollmentMapping.collection.\
      filter("section", "==", section_key).fetch()
    return list(objects)

  @classmethod
  def find_course_enrollment_record(
      cls,
      section_key,
      user_id,
      role
  ):
    """_summary_

    Args:
        section_key (str): section unique key to filter data
        user_id(str, optional): user_id from user collection

    Returns:
        course_enrollment object
    """
    user_key = f"{User.collection_name}/{user_id}"
    return CourseEnrollmentMapping.collection.filter("user","==",user_key).\
    filter("status", "in",["active","invited"]).\
    filter("section","==",section_key).filter("role","==",role).get()

  @classmethod
  def find_active_enrolled_student_record(
      cls,
      section_key,
      user_id
  ):
    """_summary_

    Args:
        section_key (str): section unique key to filter data
        user_id(str, optional): user_id from user collection

    Returns:
        course_enrollment object
    """
    user_key = f"{User.collection_name}/{user_id}"
    return CourseEnrollmentMapping.collection.filter("user","==",user_key).\
    filter("status", "==","active").filter("role","==","learner").\
      filter("section","==",section_key).get()

  @classmethod
  def find_active_enrolled_teacher_record(
      cls,
      section_key,
      user_id
  ):
    """_summary_

    Args:
        section_key (str): section unique key to filter data
        user_id(str, optional): user_id from user collection

    Returns:
        course_enrollment object
    """
    user_key = f"{User.collection_name}/{user_id}"
    return CourseEnrollmentMapping.collection.filter("user","==",user_key).\
    filter("status", "==","active").filter("role","==","faculty").\
      filter("section","==",section_key).get()

  @classmethod
  def check_enrollment_exists_section(cls,
      section_key,
      user_id):
    """check if any enrollment exists for a section by user id

    Args:
        section_key (str): unique section key
        user_id (str): unique user id

    Returns:
        CourseEnrollmentMapping: returns a object.
    """
    user_key = f"{User.collection_name}/{user_id}"
    return CourseEnrollmentMapping.collection.filter("user","==",user_key).\
    filter("status", "in",["active","invited"]).\
      filter("section","==",section_key).get()
