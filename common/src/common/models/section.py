"""
Module to add section in Fireo
"""
import os

from common.models import BaseModel,CourseTemplate,Cohort
from fireo.fields import TextField,DateTime,ReferenceField,ListField

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class Section(BaseModel):
  """Section ORM class
  """
  section_name = TextField(required=True)
  section_sec = TextField(required=True)
  section_description=TextField()
  section_classroom_id = TextField(required=True)
  section_classroom_code = TextField(required=True)
  course_reference=ReferenceField(CourseTemplate,required=True)
  cohort_reference=ReferenceField(Cohort,required=True)
  section_teachers=ListField(required=True)
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "section"
