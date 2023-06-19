"""Staff Data Model"""

import regex
import re
from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException
from fireo.fields import (TextField, ListField, BooleanField)


def validate_name(name):
  """Validator method to validate name"""
  if regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", name):
    return True
  else:
    return (False, "Invalid name format")


def validate_name_for_non_required(name):
  """Validator method to validate name"""
  if name == "" or regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", name):
    return True
  else:
    return (False, "Invalid name format")


def validate_email(email):
  """Validator method to validate email"""
  if re.match(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
    return True
  else:
    return (False, "Invalid email")


def validate_email_for_non_required(email):
  """Validator method to validate email"""
  if email == "" or re.match(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email):
    return True
  else:
    return (False, "Invalid email")


class Availability(BaseModel):
  """Availability Model"""
  day_of_week = ListField()
  start_time = TextField()
  end_time = TextField()


class Staff(BaseModel):
  """Staff Model"""
  uuid = TextField(required=True)
  first_name = TextField(required=True, max_length=60, validator=validate_name)
  last_name = TextField(required=True, max_length=60, validator=validate_name)
  preferred_name = TextField(validator=validate_name_for_non_required)
  bio = TextField(max_length = 500)
  pronoun = TextField()
  email = TextField(required=True, validator=validate_email, to_lowercase=True)
  phone_number = TextField()
  shared_inboxes = TextField(validator=validate_email_for_non_required)
  timezone = TextField()
  office_hours = ListField(Availability(), default=[])
  is_deleted = BooleanField(default=False)
  photo_url = TextField()
  calendly_url = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "staffs"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    """Find the staff using uuid
    Args:
        uuid (string): uuid of staff member
    Returns:
        staff Object
    """
    staff = cls.collection.filter(
      "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if staff is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with uuid {uuid} not found")
    return staff

  @classmethod
  def find_by_email(cls, email):
    """Find the staff using email
    Args:
        email (string): staff member's email address
    Returns:
        Staff: Staff Object
    """
    if email:
      email = email.lower()
    return cls.collection.filter("email", "==", email).filter(
      "is_deleted", "==", False).get()

  @classmethod
  def delete_by_uuid(cls, uuid):
    """
    Soft delete the staff using uuid
    Args:
      uuid (str): uuid of staff
    """
    staff = cls.collection.filter(
      "uuid", "==", uuid).filter("is_deleted", "==", False).get()
    if staff is not None:
      staff.is_deleted = True
      staff.update()
    else:
      raise ResourceNotFoundException(
        f"{cls.__name__} with uuid {uuid} not found")
