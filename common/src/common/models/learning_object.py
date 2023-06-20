"""Learning Object Service Data Models"""

from fireo.fields import (TextField, MapField, NumberField, BooleanField,
                          ListField, DateTime)
from common.models import NodeItem, BaseModel
from common.utils.errors import ResourceNotFoundException

# pylint: disable = arguments-renamed
LOS_LITERALS = {
  "CP_TYPES" : ["pathway"],
  "LE_TYPES" : ["learning_experience"],
  "LO_TYPES" : ["srl", "static_srl", "cognitive_wrapper", "pretest",
                "learning_module", "unit_overview", "project"],
  "LR_TYPES" : ["pdf", "image", "html_package", "html",
                "video", "scorm", "docx",""],

  "CP_ALIASES" : ["program", "level", "discipline", "unit"],
  "LE_ALIASES" : ["learning_experience"],
  "LO_ALIASES" : ["module"],
  "LR_ALIASES" : ["lesson"]
}


def check_type(level):
  """Function to check type"""
  allowed_types = LOS_LITERALS[level + "_TYPES"]

  def _check_type(field_val):
    """validator method for type field"""
    if field_val.lower() in allowed_types:
      return True
    return (False, level + " Type must be one of " +
            ",".join("'" + i + "'" for i in allowed_types))

  return _check_type


def check_alias(level):
  """Function to check alias"""
  allowed_aliases = LOS_LITERALS[level + "_ALIASES"]

  def _check_alias(field_val):
    """validator method for alias field"""
    if field_val.lower() in allowed_aliases:
      return True
    return (False, level + " Alias must be one of " +
            ",".join("'" + i + "'" for i in allowed_aliases))

  return _check_alias


def check_resource_status(field_val):
  """validator method for resource status field"""
  resource_status = ["initial", "draft", "published", "unpublished"]
  if field_val.lower() in resource_status:
    return True
  return (False, "Resource Type must be one of " +
          ",".join("'" + i + "'" for i in resource_status))


class CurriculumPathway(NodeItem):
  """Learning Pathway Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  display_name = TextField()
  description = TextField()
  author = TextField()
  version = NumberField(default=1)
  parent_version_uuid = TextField(default="")
  root_version_uuid = TextField(default="")
  metadata = MapField(default={})
  completion_criteria = MapField(default={})
  equivalent_credits = NumberField(default=0)
  duration = NumberField(default=15)
  # skills, competencies and achievements
  achievements = ListField(default=[])
  alignments = MapField()
  references = MapField(default={})
  # hierarchy
  prerequisites = MapField(default={})
  child_nodes = MapField(default={})
  parent_nodes = MapField(default={})
  # meta fields
  order = NumberField()
  alias = TextField(default="unit", validator=check_alias("CP"))
  type = TextField(default="pathway", validator=check_type("CP"))
  is_locked = BooleanField()
  is_optional = BooleanField(default=False)
  is_hidden = BooleanField(default=False)
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)
  is_active = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "curriculum_pathways"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    curriculum_pathway = CurriculumPathway.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if curriculum_pathway is None:
      raise ResourceNotFoundException(
          f"Curriculum Pathway with uuid {uuid} not found")
    return curriculum_pathway

  @classmethod
  def find_by_name(cls, name, is_deleted=False):
    curriculum_pathways = CurriculumPathway.collection.filter(
        "name", "==", name).filter("is_deleted", "==", is_deleted).fetch()
    return curriculum_pathways

  @classmethod
  def find_by_alias(cls, alias, is_deleted=False):
    curriculum_pathways = CurriculumPathway.collection.filter(
        "alias", "==", alias).filter("is_deleted", "==",
                                     is_deleted).order("-created_time").fetch()
    return curriculum_pathways

  @classmethod
  def find_active_pathway(cls, alias="program", is_deleted=False):
    curriculum_pathway = CurriculumPathway.collection.filter(
      "alias", "==", alias).filter(
      "is_deleted", "==", is_deleted).filter(
      "is_active", "==", True).get()
    return curriculum_pathway

class LearningExperience(NodeItem):
  """Learning Experience Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  display_name = TextField()
  description = TextField()
  author = TextField()
  version = NumberField(default=1)
  parent_version_uuid = TextField(default="")
  root_version_uuid = TextField(default="")
  metadata = MapField(default={})
  completion_criteria = MapField(default={})
  equivalent_credits = NumberField(default=0)
  duration = NumberField(default=15)
  resource_path = TextField(default="")
  srl_resource_path = TextField(default="")
  # skills, competencies and achievements
  achievements = ListField(default=[])
  alignments = MapField(default={})
  references = MapField(default={})
  # hierarchy
  prerequisites = MapField(default={})
  child_nodes = MapField(default={})
  parent_nodes = MapField(default={})
  # meta fields
  order = NumberField()
  alias = TextField(default="learning_experience", validator=check_alias("LE"))
  type = TextField(default="learning_experience", validator=check_type("LE"))
  is_locked = BooleanField()
  is_optional = BooleanField(default=False)
  is_hidden = BooleanField(default=False)
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "learning_experiences"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    learning_experience = LearningExperience.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if learning_experience is None:
      raise ResourceNotFoundException(
          f"Learning Experience with uuid {uuid} not found")
    return learning_experience

  @classmethod
  def find_by_name(cls, name, is_deleted=False):
    learning_experiences = LearningExperience.collection.filter(
        "name", "==", name).filter("is_deleted", "==", is_deleted).fetch()
    return learning_experiences


class LearningObject(NodeItem):
  """Learning Object Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  display_name = TextField()
  description = TextField()
  author = TextField()
  version = NumberField(default=1)
  parent_version_uuid = TextField(default="")
  root_version_uuid = TextField(default="")
  metadata = MapField(default={})
  completion_criteria = MapField(default={})
  equivalent_credits = NumberField(default=0)
  duration = NumberField(default=15)
  # skills, competencies and achievements
  achievements = ListField(default=[])
  alignments = MapField(default={})
  references = MapField(default={})
  # hierarchy
  prerequisites = MapField(default={})
  child_nodes = MapField(default={})
  parent_nodes = MapField(default={})
  # meta fields
  order = NumberField()
  alias = TextField(default="module", validator=check_alias("LO"))
  type = TextField(default="learning_module", validator=check_type("LO"))
  is_locked = BooleanField()
  is_optional = BooleanField(default=False)
  is_hidden = BooleanField(default=False)
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "learning_objects"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    learning_object = LearningObject.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if learning_object is None:
      raise ResourceNotFoundException(
          f"Learning Object with uuid {uuid} not found")
    return learning_object

  @classmethod
  def find_by_name(cls, name, is_deleted=False):
    learning_objects = LearningObject.collection.filter(
        "name", "==", name).filter("is_deleted", "==", is_deleted).fetch()
    return learning_objects

  @classmethod
  def find_by_type(cls, object_type, is_deleted=False):
    learning_objects = LearningObject.collection.filter("type", "==",
                                                        object_type).filter(
                                                            "is_deleted", "==",
                                                            is_deleted).fetch()
    return learning_objects


class LearningResource(NodeItem):
  """Learning Resource Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  display_name = TextField()
  description = TextField()
  author = TextField()
  resource_path = TextField(default="")
  lti_content_item_id = TextField()
  course_category = ListField(default=[])
  version = NumberField(default=1)
  parent_version_uuid = TextField(default="")
  root_version_uuid = TextField(default="")
  metadata = MapField(default={})
  completion_criteria = MapField(default={})
  status = TextField(default="initial", validator=check_resource_status)
  current_content_version = TextField()
  last_published_on = DateTime()
  last_published_by = TextField(default="")
  is_implicit = BooleanField(default=False)
  duration = NumberField(default=15)
  # skills, competencies and achievements
  achievements = ListField(default=[])
  alignments = MapField(default={})
  references = MapField(default={})
  # hierarchy
  parent_nodes = MapField(default={})
  child_nodes = MapField(default={})
  prerequisites = MapField(default={})
  # meta fields
  order = NumberField()
  alias = TextField(default="lesson", validator=check_alias("LR"))
  type = TextField(default="", validator=check_type("LR"))
  is_locked = BooleanField()
  is_hidden = BooleanField(default=False)
  is_optional = BooleanField(default=False)
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "learning_resources"
    ignore_none_field = False

  def get_fields(self, reformat_datetime=False):
    """overrides default method to fix data type for datetime fields"""
    fields = super()._get_fields()
    if reformat_datetime:
      fields["created_time"] = str(fields["created_time"])
      fields["last_modified_time"] = str(fields["last_modified_time"])
      fields["last_published_on"] = str(fields["last_published_on"])
    return fields

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    learning_resource = LearningResource.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if learning_resource is None:
      raise ResourceNotFoundException(
          f"Learning Resource with uuid {uuid} not found")
    return learning_resource

  @classmethod
  def find_by_name(cls, name, is_deleted=False):
    learning_resources = LearningResource.collection.filter(
        "name", "==", name).filter("is_deleted", "==", is_deleted).fetch()
    return learning_resources
