"""
Module to add section in Fireo
"""
import os

from common.models import BaseModel,CourseTemplate,Cohort
from common.utils.errors import ResourceNotFoundException
from fireo.fields import TextField,DateTime,ReferenceField,ListField

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class Section(BaseModel):
  """Section ORM class
  """
  uuid=TextField()
  name = TextField(required=True)
  section = TextField(required=True)
  description=TextField()
  classroom_id = TextField(required=True)
  classroom_code = TextField(required=True)
  course_template=ReferenceField(CourseTemplate,required=True)
  cohort=ReferenceField(Cohort,required=True)
  teachers_list=ListField(required=True)
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "section"

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find a Section using uuid (UUID)
    Args:
        uuid (string): Section ID
    Returns:
        Section: Section Object
    """
    section= Section.collection.filter("uuid", "==", uuid).get()
    if section is None:
      raise ResourceNotFoundException(f"Section with uuid {uuid} is not found")
    return section
