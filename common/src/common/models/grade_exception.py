"""Temporary collection for storing list of users for whom grade passback needs to be skipped"""
from fireo.fields import TextField, BooleanField, IDField
from common.utils.errors import ResourceNotFoundException
from common.models import BaseModel


class UserGradeException(BaseModel):
  """LTI Tool Data Model"""
  id = IDField()
  email_id = TextField(required=True)
  user_id = TextField(required=True)
  tool_id = TextField(required=True)
  allow_exception = BooleanField(default=True)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "lti_grade_exception_users"
    ignore_none_field = False

  @classmethod
  def find_by_user_and_tool_id(cls, user_id, tool_id):
    user = cls.collection.filter("user_id", "==", user_id).filter("tool_id", "==", tool_id).get()
    return user

  @classmethod
  def find_by_email_and_tool_id(cls, email_id, tool_id):
    email = cls.collection.filter("email_id", "==", email_id).filter("tool_id", "==", tool_id).get()
    if email is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with email_id {email_id} & tool_id {tool_id} not found")
    return email
