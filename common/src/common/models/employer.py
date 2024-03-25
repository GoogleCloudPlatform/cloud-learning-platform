"""Employer Data Models"""

from fireo.fields import TextField, ListField, MapField
from common.models import NodeItem, BaseModel
from common.utils.errors import ResourceNotFoundException


class Employer(NodeItem):
  """Employer Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "employers"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    employer = Employer.collection.filter("uuid", "==", uuid).get()
    if employer is None:
      raise ResourceNotFoundException(f"Employer with uuid {uuid} not found")
    return employer

  @classmethod
  def find_by_name(cls, name):
    """Find the employer item using name
    Args:
        name (string): node item name
    Returns:
        Employer: Employer Object
    """
    return Employer.collection.filter("name", "==", name).fetch()


class EmploymentRole(NodeItem):
  """EmploymentRole Class"""
  # schema for object
  uuid = TextField(required=True)
  code = TextField(required=True)
  title = TextField(required=True)
  also_called = ListField(required=True)
  description = TextField(required=True)
  task = ListField(required=True)
  source_uri = TextField(required=True)
  type = TextField(required=True)
  source_name = TextField(required=True)
  alignments = MapField(default={})

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "employment_roles"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    role = EmploymentRole.collection.filter("uuid", "==", uuid).get()
    if role is None:
      raise ResourceNotFoundException(
          f"EmploymentRole with uuid {uuid} not found")
    return role

  @classmethod
  def find_by_title(cls, title):
    """Find the employment role item using title
    Args:
        title (string): node item title
    Returns:
        EmploymentRole: EmploymentRole Object
    """
    return EmploymentRole.collection.filter("title", "==", title).fetch()

  @classmethod
  def find_by_code(cls, code):
    """Find the employment role item using code
    Args:
        code (string): node item code
    Returns:
        EmploymentRole: EmploymentRole Object
    """
    return EmploymentRole.collection.filter("code", "==", code).get()

  @classmethod
  def find_by_source_name(cls, source_name):
    """Find the employment role items using source name
    Args:
        source_name (string): name of source
    Returns:
        roles: List of EmploymentRole Objects
    """
    roles = EmploymentRole.collection.filter(
        "source_name", "==", source_name).fetch()
    return list(roles)
