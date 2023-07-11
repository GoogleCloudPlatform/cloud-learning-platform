"""Credential and Pathway Data Models"""
from fireo.fields import TextField, MapField, ListField, BooleanField, DateTime
from common.models import BaseModel
from common.utils.errors import (ResourceNotFoundException, ValidationError)
from common.utils.http_exceptions import (InternalServerError, BadRequest)
from datetime import datetime


class BadgeClass(BaseModel):
  """Badge Model Class"""
  # schema for object
  uuid = TextField(required=True)
  entity_type = TextField(required=True)
  entity_id = TextField(required=True)
  open_badge_id = TextField(required=True)
  issuer = TextField()
  issuer_open_badge_id = TextField()
  name = TextField()
  image = TextField()
  description = TextField()
  achievement_type = TextField()
  criteria_url = TextField()
  criteria_narrative = TextField()
  alignments = MapField()
  tags = ListField()
  expires = MapField()
  extensions = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "badge_classes"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    badge_object = BadgeClass.collection.filter("uuid", "==", uuid).get()
    if badge_object is None:
      raise ResourceNotFoundException(f"BadgeClass with uuid {uuid} not found")
    return badge_object

  @classmethod
  def find_by_name(cls, name):
    badge_object = BadgeClass.collection.filter("name", "==", name).get()
    return badge_object


class Issuer(BaseModel):
  """Issuer Model Class"""
  # schema for object
  uuid = TextField(required=True)
  entity_type = TextField()
  entity_id = TextField()
  open_badge_id = TextField()
  name = TextField(required=True)
  image = TextField()
  email = TextField(required=True)
  description = TextField()
  url = TextField(required=True)
  staff = ListField()
  extensions = TextField()
  badgr_domain = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "issuers"

  ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    issuer_object = Issuer.collection.filter("uuid", "==", uuid).get()
    if issuer_object is None:
      raise ResourceNotFoundException(f"Issuer with uuid {uuid} not found")
    return issuer_object

  @classmethod
  def find_by_name(cls, name):
    issuer_object = Issuer.collection.filter("name", "==", name).get()
    return issuer_object


class Assertion(BaseModel):
  """Assertion Model Class"""
  # schema for object
  uuid = TextField(required=True)
  entity_type = TextField()
  entity_id = TextField()
  open_badge_id = TextField()
  badgeclass = TextField()
  badgeclass_open_badge_id = TextField()
  issuer = TextField()
  issuer_open_badge_id = TextField()
  image = TextField()
  recipient = MapField()
  issued_on = TextField()
  narrative = TextField()
  evidence = ListField()
  revoked = BooleanField()
  revocation_reason = TextField()
  acceptance = TextField()
  expires = DateTime()
  extensions = TextField()
  badgeclass_name = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "assertions"

  ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    assertion_object = Assertion.collection.filter("uuid", "==", uuid).get()
    if assertion_object is None:
      raise ResourceNotFoundException(f"Assertion with uuid {uuid} not found")
    return assertion_object

  @classmethod
  def from_dict(cls, model_dict):
    """Instantiate model from dict"""
    try:
      if model_dict is not None and model_dict.get(
          "expires", None) is not None and isinstance(
              model_dict.get("expires"), str):
        model_dict["expires"] = datetime.strptime(model_dict["expires"],
                                                  "%Y-%m-%d %H:%M:%S")
      return super().from_dict(model_dict)

    except ValidationError as e:
      raise BadRequest(str(e), data=e.data) from e

    except Exception as e:
      raise InternalServerError(str(e)) from e
