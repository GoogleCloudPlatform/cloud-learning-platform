"""Credential and Pathway Service Data Models"""

from fireo.fields import TextField
from common.models import NodeItem, BaseModel
from common.utils.errors import ResourceNotFoundException


class Credential(NodeItem):
  """Credential Class"""
  # schema for object
  uuid = TextField(required=True)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "credentials"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    credential = Credential.collection.filter("uuid", "==", uuid).get()
    if credential is None:
      raise ResourceNotFoundException(f"Credential with uuid {uuid} not found")
    return credential


class LearningPathway(NodeItem):
  """Learning Pathway Class"""
  # schema for object
  uuid = TextField(required=True)
  title = TextField(required=True)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "learning_pathways"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    learning_pathways = LearningPathway.collection.filter("uuid", "==",
                                                          uuid).get()
    if learning_pathways is None:
      raise ResourceNotFoundException(
          f"Learning Pathway with uuid {uuid} not found")
    return learning_pathways


class Program(NodeItem):
  """Program Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "programs"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    program = Program.collection.filter("uuid", "==", uuid).get()
    if program is None:
      raise ResourceNotFoundException(f"Program with uuid {uuid} not found")
    return program

  @classmethod
  def find_by_name(cls, name):
    """Find the program item using name
    Args:
        name (string): node item name
    Returns:
        Program: Program Object
    """
    return Program.collection.filter("name", "==", name).fetch()
