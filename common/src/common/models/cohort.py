"""
Module to add cohort in Fireo
"""
import os


from common.models import BaseModel,CourseTemplate
from fireo.fields import TextField,DateTime,NumberField,ReferenceField

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class Cohort(BaseModel):
  """Cohort ORM class
  """
  cohort_name = TextField(required=True)
  cohort_description = TextField(required=True)
  cohort_start_date = DateTime(required=True)
  cohort_end_date = DateTime(required=True)
  cohort_max_student = NumberField()
  course_reference=ReferenceField(CourseTemplate,required=True)
  created_timestamp = TextField()
  last_updated_timestamp = TextField()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "cohort"
