"""Learning Record Service Data Models"""

from fireo.fields import TextField, ListField, MapField, BooleanField
from common.models import NodeItem, BaseModel
from common.utils.errors import ResourceNotFoundException


class LearningRecord(NodeItem):
  """Learning Record Class"""
  # schema for learning record
  uuid = TextField(required=True)
  actor = TextField(required=True)
  verb = TextField(required=True)
  object = TextField(required=True)
  result = TextField()
  context = TextField()
  timestamp = TextField()
  stored = TextField()
  authority = TextField()
  version = TextField()
  attachments = ListField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "learning_records"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    learning_record = LearningRecord.collection.filter("uuid", "==", uuid).get()
    if learning_record is None:
      raise ResourceNotFoundException(
          f"Learning Record with uuid {uuid} not found")
    return learning_record


class ActivityState(NodeItem):
  """Activity State Class"""
  uuid = TextField(required=True)
  agent_id = TextField(required=True)
  activity_id = TextField(required=True)
  canonical_data = MapField(default={})

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "activity_states"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    activity_state = ActivityState.collection.filter("uuid", "==", uuid).get()
    if activity_state is None:
      raise ResourceNotFoundException(
        f"Activity State with uuid {uuid} not found")
    return activity_state

class Agent(NodeItem):
  """Agent Class"""
  # schema for agent
  uuid = TextField(required=True)
  object_type = TextField(required=True)
  name = TextField(required=True)
  mbox = TextField()
  mbox_sha1sum = TextField()
  open_id = TextField()
  account_homepage = TextField()
  account_name = TextField(required=True)
  members = ListField()
  user_id = TextField(required=True)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "agents"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    agent = Agent.collection.filter(
      "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if agent is None:
      raise ResourceNotFoundException(
          f"Agent with uuid {uuid} not found")
    return agent

  @classmethod
  def find_by_name(cls, name, is_deleted=False):
    agents = Agent.collection.filter(
      "name", "==", name).filter("is_deleted", "==", is_deleted).fetch()
    if agents is None:
      raise ResourceNotFoundException(
          f"{cls.__name__} with name {name} not found")
    return agents

  @classmethod
  def find_by_user_id(cls, user_id):
    agent = Agent.collection.filter(
      "user_id", "==", user_id).filter("is_deleted", "==", False).get()
    return agent


class Verb(NodeItem):
  """Verb Class"""
  # schema for verb
  uuid = TextField(required=True)
  name = TextField(required=True)
  url = TextField(default="")
  canonical_data = MapField(default={})

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "verbs"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    verb = Verb.collection.filter("uuid", "==", uuid).get()
    if verb is None:
      raise ResourceNotFoundException(
          f"Verb with uuid {uuid} not found")
    return verb

  @classmethod
  def find_by_name(cls, name):
    verb = Verb.collection.filter("name", "==", name).get()
    return verb

class Activity(NodeItem):
  """Activity Class"""
  # schema for activity
  uuid = TextField(required=True)
  name = TextField(required=True)
  canonical_data = MapField(default={})
  authority = TextField(default="")

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "activities"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    activity = Activity.collection.filter("uuid", "==", uuid).get()
    if activity is None:
      raise ResourceNotFoundException(f"Activity with uuid {uuid} not found")
    return activity
