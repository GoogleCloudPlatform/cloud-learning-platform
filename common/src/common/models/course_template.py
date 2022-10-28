import os

from common.models import BaseModel
from fireo.fields import (TextField,DateTime)

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class CourseTemplate(BaseModel):
  """Course ORM class
  """
  course_name = TextField(required=True)
  course_description = TextField(required=True)
  course_topic = TextField()
  course_admin = TextField(required=True)
  course_instructional_designer=TextField(required=True)
  course_classroom_id=TextField()
  course_classroom_code=TextField()
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "course"
