"""Skill Service Data Models"""

from fireo.fields import TextField, ListField, MapField
from common.models import NodeItem, BaseModel
from common.utils.errors import ResourceNotFoundException


class Skill(NodeItem):
  """Skill Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  keywords = ListField(default=[])
  author = TextField()
  creator = TextField()
  alignments = MapField()
  organizations = ListField()
  certifications = ListField()
  occupations = MapField()
  onet_job = TextField(default="")
  type = MapField()
  parent_nodes = MapField(default={})
  reference_id = TextField()
  source_uri = TextField()
  source_name = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "skills"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    skill = Skill.collection.filter("uuid", "==", uuid).get()
    if skill is None:
      raise ResourceNotFoundException(f"Skill with uuid {uuid} not found")
    return skill

  @classmethod
  def find_by_source_name(cls, source_name):
    """Find the skill using source name
    Args:
        source_name (string): name of source
    Returns:
        skills: List of Skill Objects
    """
    skills = Skill.collection.filter("source_name", "==", source_name).fetch()
    return list(skills)

  @classmethod
  def find_by_name(cls, name):
    """Find the skill using name
    Args:
        name (string): node item name
    Returns:
        Skill: Skill Object
    """
    return Skill.collection.filter("name", "==", name).fetch()

  @classmethod
  def find_by_keywords(cls, keyword):
    """Find the skill using keyword
    Args:
        keyword (string): node item keyword
    Returns:
        Skill: Skill Object
    """
    return Skill.collection.filter("keywords", "array_contains",
                                   keyword).fetch()

  @classmethod
  def find_by_reference_id(cls, reference_id):
    skill = Skill.collection.filter("reference_id", "==", reference_id).get()
    if skill is None:
      raise ResourceNotFoundException \
      (f"Skill with reference_id {reference_id} not found")
    return skill


class SkillServiceCompetency(NodeItem):
  """Competency Data Model Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField()
  description = TextField(required=True)
  keywords = ListField(default=[])
  level = TextField()
  subject_code = TextField()
  course_code = TextField()
  course_title = TextField()
  alignments = MapField()
  occupations = MapField()
  parent_nodes = MapField(default={})
  child_nodes = MapField(default={})
  reference_id = TextField()
  source_uri = TextField()
  source_name = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "v3_competencies"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    skill_service_competency = SkillServiceCompetency.collection.filter(
        "uuid", "==", uuid).get()
    if skill_service_competency is None:
      raise ResourceNotFoundException(f"Competency with uuid {uuid} not found")
    return skill_service_competency

  @classmethod
  def find_by_name(cls, name):
    return SkillServiceCompetency.collection.filter("name", "==", name).fetch()

  @classmethod
  def find_by_reference_id(cls, reference_id):
    competency = SkillServiceCompetency.collection.filter(
        "reference_id", "==", reference_id).get()
    if competency is None:
      raise ResourceNotFoundException\
        (f"Competency with reference_id {reference_id} not found")
    return competency

  @classmethod
  def find_by_keywords(cls, keyword):
    return SkillServiceCompetency.collection.filter("keywords",
                                                    "array_contains",
                                                    keyword).fetch()


class Category(NodeItem):
  """Category Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  keywords = ListField(default=[])
  parent_nodes = MapField(default={})
  child_nodes = MapField(default={})
  reference_id = TextField()
  source_uri = TextField()
  source_name = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "categories"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    category = Category.collection.filter("uuid", "==", uuid).get()
    if category is None:
      raise ResourceNotFoundException(f"Category with uuid {uuid} not found")
    return category

  @classmethod
  def find_by_name(cls, name):
    return Category.collection.filter("name", "==", name).fetch()

  @classmethod
  def find_by_reference_id(cls, reference_id):
    category = Category.collection\
      .filter("reference_id", "==", reference_id).get()
    if category is None:
      raise ResourceNotFoundException\
        (f"Category with reference_id {reference_id} not found")
    return category

  @classmethod
  def find_by_keywords(cls, keyword):
    return Category.collection.filter("keywords", "array_contains",
                                      keyword).fetch()


class SubDomain(NodeItem):
  """SubDomain Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  keywords = ListField(default=[])
  parent_nodes = MapField(default={})
  child_nodes = MapField(default={})
  reference_id = TextField()
  source_uri = TextField()
  source_name = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "sub_domains"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    sub_domain = SubDomain.collection.filter("uuid", "==", uuid).get()
    if sub_domain is None:
      raise ResourceNotFoundException(f"Sub Domain with uuid {uuid} not found")
    return sub_domain

  @classmethod
  def find_by_name(cls, name):
    return SubDomain.collection.filter("name", "==", name).fetch()

  @classmethod
  def find_by_reference_id(cls, reference_id):
    subdomain = SubDomain.collection\
      .filter("reference_id", "==", reference_id).get()
    if subdomain is None:
      raise ResourceNotFoundException\
        (f"Subdomain with reference_id {reference_id} not found")
    return subdomain

  @classmethod
  def find_by_keywords(cls, keyword):
    return SubDomain.collection.filter("keywords", "array_contains",
                                       keyword).fetch()


class Domain(NodeItem):
  """Domain Class"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField(required=True)
  keywords = ListField(default=[])
  child_nodes = MapField(default={})
  reference_id = TextField()
  source_uri = TextField()
  source_name = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "domains"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    domain = Domain.collection.filter("uuid", "==", uuid).get()
    if domain is None:
      raise ResourceNotFoundException(f"Domain with uuid {uuid} not found")
    return domain

  @classmethod
  def find_by_name(cls, name):
    return Domain.collection.filter("name", "==", name).fetch()

  @classmethod
  def find_by_reference_id(cls, reference_id):
    domain = Domain.collection.filter("reference_id", "==", reference_id).get()
    if domain is None:
      raise ResourceNotFoundException\
        (f"Domain with reference_id {reference_id} not found")
    return domain

  @classmethod
  def find_by_keywords(cls, keyword):
    return Domain.collection.filter("keywords", "array_contains",
                                    keyword).fetch()


class DataSource(NodeItem):
  """Data Source Class"""
  # schema for object
  type = TextField(required=True)
  source = ListField(required=True)
  matching_engine_index_id = MapField(default={})

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "data_sources"
    ignore_none_field = False

  @classmethod
  def find_by_type(cls, input_type):
    """Find the skill using name
    Args:
        input_type (string): type of object
    Returns:
        DataSource: DataSource Object
    """
    data_source = DataSource.collection.filter("type", "==", input_type).get()
    if data_source is None:
      raise ResourceNotFoundException(f"No Sources for type {input_type} found")
    return data_source
