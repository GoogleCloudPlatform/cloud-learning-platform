"""
Module to add cohort in Fireo
"""
import os


from common.models import BaseModel,CourseTemplate
from common.utils.errors import ResourceNotFoundException
from fireo.fields import TextField,DateTime,NumberField,ReferenceField

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class Cohort(BaseModel):
  """Cohort ORM class
  """
  uuid=TextField()
  name = TextField(required=True)
  description = TextField(required=True)
  start_date = DateTime(required=True)
  end_date = DateTime(required=True)
  registration_start_date = DateTime(required=True)
  registration_end_date = DateTime(required=True)
  max_student = NumberField()
  enrolled_student_count=NumberField()
  course_template=ReferenceField(CourseTemplate,required=True)
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "cohort"

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find a Cohort using uuid (UUID)
    Args:
        uuid (string): Cohort ID
    Returns:
        Cohort: Cohort Object
    """
    cohort= Cohort.collection.filter("uuid", "==", uuid).get()
    if cohort is None:
      raise ResourceNotFoundException(f"Cohort with uuid {uuid} is not found")
    return cohort
