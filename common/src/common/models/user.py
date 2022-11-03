"""
User object in the ORM
"""

import os

from common.models import BaseModel
from common.utils.errors import ResourceNotFoundException
from fireo.fields import TextField,DateTime

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.environ.get("PROJECT_ID", "")


class User(BaseModel):
  """
  User ORM class
  """
  uuid=TextField()
  auth_id=TextField(required=True)
  email=TextField(required=True)
  role=TextField()
  created_timestamp = DateTime()
  last_updated_timestamp = DateTime()

  class Meta:
    ignore_none_field = False
    collection_name = DATABASE_PREFIX + "user"

  @classmethod
  def find_by_email(cls, email):
    """Find a user using email (string)
    Args:
        email (string): User Email
    Returns:
        User: User Object
    """
    user= User.collection.filter("email", "==", email).get()
    if user is None:
      raise ResourceNotFoundException(f"User with email {email} is not found")
    return user

  @classmethod
  def find_by_uuid(cls, uuid):
    """Find a user using uuid (UUID)
    Args:
        uuid (string): User ID
    Returns:
        User: User Object
    """
    user=User.collection.filter("uuid", "==", uuid).get()
    if user is None:
      raise ResourceNotFoundException(f"User with uuid {uuid} is not found")
    return user
