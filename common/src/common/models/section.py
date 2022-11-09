"""
Module to add section in Fireo
"""
import datetime
import os

from common.models import BaseModel,CourseTemplate,Cohort
from fireo.fields import TextField,DateTime,ReferenceField,ListField,BooleanField

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
  is_deleted = BooleanField(default=False)
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()
  deleted_at_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "sections"

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find a Section using uuid (UUID)
    Args:
        uuid (string): Section ID
    Returns:
        Section: Section Object
    """
    section = Section.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", False).get()
    return section

  @classmethod
  def archive_by_uuid(cls, uuid):
    '''Soft Delete a Section by using uuid
      Args:
          uuid (String): Section ID
      '''
    section = Section.collection.filter("uuid", "==", uuid).filter(
        "is_deleted", "==", False).get()
    if section is None:
      return False
    else:
      section.is_deleted = True
      section.deleted_at_timestamp = datetime.datetime.utcnow()
      section.update()
      return True
