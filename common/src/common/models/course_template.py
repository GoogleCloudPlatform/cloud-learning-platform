"""
Module to add course in Fireo
"""

import os

from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException
from fireo.fields import TextField,DateTime

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class CourseTemplate(BaseModel):
  """Course ORM class
  """
  uuid=TextField()
  name = TextField(required=True)
  description = TextField(required=True)
  topic = TextField(required=True)
  admin = TextField(required=True)
  instructional_designer=TextField(required=True)
  classroom_id=TextField()
  classroom_code=TextField()
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "course"

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find a CourseTemplate using uuid (UUID)
    Args:
        uuid (string): CourseTemplate ID
    Returns:
        CourseTemplate: CourseTemplate Object
    """
    course_template=CourseTemplate.collection.filter("uuid", "==", uuid).get()
    if course_template is None:
      raise ResourceNotFoundException(
        f"Course Template with uuid {uuid} is not found"
        )
    return course_template
