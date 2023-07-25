"""Prior Learning Assessment Data Models"""
from fireo.fields import (TextField, ListField, MapField, DateTime,
                          BooleanField, NumberField)
from common.models import BaseModel, User
from common.utils.errors import ResourceNotFoundException


class PriorExperience(BaseModel):
  """Prior Experience Class"""
  # schema for object
  uuid = TextField(required=True)
  organization = TextField()
  experience_title = TextField()
  date_completed = DateTime()
  credits_earned = NumberField()
  description = TextField()
  url = TextField()
  competencies = ListField()
  skills = ListField()
  documents = ListField()
  cpl = NumberField()
  is_flagged = BooleanField(default=False)
  metadata = MapField(default={})
  alignments = MapField(default={})
  type_of_experience = TextField()
  validation_type = MapField(default={})
  terms = ListField(default=[])

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "prior_experiences"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    prior_experience = PriorExperience.collection.filter(
      "uuid", "==", uuid).get()
    if prior_experience is None:
      raise ResourceNotFoundException(
          f"Prior Experience with uuid {uuid} not found")
    return prior_experience


class PLARecord(BaseModel):
  """Prior Experience Class"""
  # schema for object
  uuid = TextField(required=True)
  title = TextField()
  description = TextField()
  user_id = TextField(required=True)
  type = TextField(required=True)
  assessor_name = TextField(required=True)
  status = TextField(required=True, default="In progress")
  prior_experiences = ListField(default=[])
  approved_experiences = ListField(default=[])
  id_number = NumberField(int_only=True, default=10000)
  progress = NumberField(default=0)
  is_archived = BooleanField(default=False)
  is_flagged = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "pla_records"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    pla_record = PLARecord.collection.filter(
      "uuid", "==", uuid).get()
    if pla_record is None:
      raise ResourceNotFoundException(
          f"PLA Record with uuid {uuid} not found")
    return pla_record

  @classmethod
  def find_by_name(cls, name):
    pla_records = PLARecord.collection.filter("title", "==", name).fetch()
    return pla_records

  @classmethod
  def find_by_user_id(cls, user_id):
    """Find the pla record using user id
    Args:
        user_id (string): node item user id
    Returns:
        PLARecord: PLA Record Object
    """
    User.find_by_uuid(user_id)
    pla_record = PLARecord.collection.filter("user_id", "==",\
       user_id).filter("type", "==", "draft").get()
    if  pla_record is None:
      raise ResourceNotFoundException(
          f"PLA record with user id {user_id} not found")
    return pla_record


class ApprovedExperience(BaseModel):
  """Approved Experience Class"""
  # schema for object
  uuid = TextField(required=True)
  title = TextField()
  organization = TextField()
  description = TextField()
  type = TextField()
  student_type = TextField()
  class_level = TextField()
  credits_range = MapField()
  status = TextField()
  metadata = MapField(default={})

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "approved_experiences"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    approved_experience = ApprovedExperience.collection.filter(
      "uuid", "==", uuid).get()
    if approved_experience is None:
      raise ResourceNotFoundException(
          f"Approved Experience with uuid {uuid} not found")
    return approved_experience

  @classmethod
  def find_by_title(cls, title):
    approved_expereiences = ApprovedExperience.collection.filter("title", "==",
                                                                  title).fetch()
    return approved_expereiences
