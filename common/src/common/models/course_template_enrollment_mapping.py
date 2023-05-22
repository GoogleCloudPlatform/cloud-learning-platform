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
from common.models import BaseModel, CourseTemplate, User


def check_status(field_val):
  """validator method for status field"""
  status = ["active", "inactive", "invited"]
  if field_val.lower() in ["active", "inactive", "invited"]:
    return True
  return (False, "Status must be one of " + ",".join("'" + i + "'"
                                                     for i in status))


def check_role(field_val):
  """validator method for status field"""
  role = ["faculty", "admin"]
  if field_val.lower() in role:
    return True
  return (False, "role must be one of " + ",".join("'" + i + "'"
                                                   for i in role))


class CourseTemplateEnrollmentMapping(BaseModel):
  """Course Template Enrollment Mapping ORM class
  """
  id = IDField()
  course_template = ReferenceField(CourseTemplate, required=True)
  user = ReferenceField(User, required=True)
  status = TextField(validator=check_status)
  role = TextField(validator=check_role)
  invitation_id = TextField()

  class Meta:
    ignore_none_field = False
    collection_name = (BaseModel.DATABASE_PREFIX +
                       "course_template_enrollment_mapping")

  @classmethod
  def find_by_user(cls, user_id):
    """Find user using using user_id
    Args:
        user_id (string): node item name
    Returns:
        user_object
    """
    user_key = f"{User.collection_name}/{user_id}"
    result = CourseTemplateEnrollmentMapping.collection.filter(
        "user", "==", user_key).filter("status", "==", "active").fetch()
    return list(result)

  @classmethod
  def fetch_all_by_course_template(cls, course_template):
    """find all records by course template.

    Args:
        course_template (str): Course template key.

    Returns:
        List of CourseTemplateEnrollmentMapping: list of object
    """
    objects = CourseTemplateEnrollmentMapping.collection.\
      filter("course_template", "==", course_template).filter(
        "status", "in",["active","invited"]).fetch()
    return list(objects)

  @classmethod
  def find_course_enrollment_record(cls, course_template_key, user_id):
    """
    find course template enrollment record by user id and course template key.

    Args:
        course_template_key (str): unique key of course template key
        user_id (str): unique id.

    Returns:
        CourseTemplateEnrollmentMapping: Object of \
          CourseTemplateEnrollmentMapping Model.
    """
    user_key = f"{User.collection_name}/{user_id}"
    return CourseTemplateEnrollmentMapping.collection.filter(
        "user", "==",
        user_key).filter("status", "in", ["active", "invited"]).filter(
            "course_template", "==", course_template_key).get()

  @classmethod
  def find_enrolled_active_record(cls, course_template_key, user_id):
    """Find enrolled active records by course template and user id.

    Args:
        course_template (str): course template unique key to filter data
        user_id(str): user_id from user collection

    Returns:
        course_enrollment object
    """
    user_key = f"{User.collection_name}/{user_id}"
    return CourseTemplateEnrollmentMapping.collection.filter(
        "user", "==",
        user_key).filter("status", "==",
                         "active").filter("course_template", "==",
                                          course_template_key).get()
