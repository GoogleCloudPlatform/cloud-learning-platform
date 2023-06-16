"""Knowledge Service Data Models"""
from fireo.fields import TextField, NumberField, BooleanField, ListField, MapField
from common.models import NodeItem, BaseModel
from common.utils.errors import ResourceNotFoundException


class KnowledgeServiceLearningContent(NodeItem):
  """Learning Resource Class"""
  uuid = TextField(required=True)
  title = TextField(required=True)
  description = TextField(required=True)
  document_type = TextField(required=True)
  child_type = "Concept"
  concept_ids = ListField(default=[])
  child_nodes = MapField()
  resource_path = TextField(required=True, default="")
  type = TextField(required=False, default="learning_resource")
  course_category = TextField(default="")
  alignments = MapField(default={})
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  @property
  def concepts(self):
    return self.children_nodes

  def __init__(self, *args, **kwargs):
    #pylint: disable=useless-super-delegation
    super().__init__(*args, **kwargs)
    self.children_nodes = []

  def load_tree(self):
    """ loads entire tree """
    self.load_children()
    if self.children_nodes:
      for child in self.children_nodes:
        child.load_tree()

  def load_children(self):
    """loads child nodes"""
    for concept_id in self.concept_ids:  #pylint: disable=not-an-iterable
      concept = Concept.find_by_id(concept_id)
      self.children_nodes.append(concept)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "v3_learning_contents"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted = False):
    learning_resource = KnowledgeServiceLearningContent.collection.filter(
      "uuid", "==", uuid).filter("is_deleted","==", is_deleted).get()
    if learning_resource is None:
      raise ResourceNotFoundException(
          f"Learning Resource with uuid {uuid} not found")
    return learning_resource

  @classmethod
  def find_by_title(cls, title):
    return KnowledgeServiceLearningContent.collection.filter(
        "title", "==", title).fetch()


class Concept(NodeItem):
  """Concept Class"""
  uuid = TextField(required=True)
  title = TextField(required=True)
  description = TextField()
  label = TextField(required=True)
  type = TextField(required=False, default="concept")
  is_valid = BooleanField(required=True, default=True)
  child_type = "SubConcept"
  child_nodes = MapField()
  parent_nodes = MapField()
  alignments = MapField(default={})
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)


  @property
  def sub_concepts(self):
    return self.children_nodes

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "concepts"
    ignore_none_field = False

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.module = "common.models.knowledge"

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted = False):
    concept = Concept.collection.filter(
      "uuid", "==", uuid).filter("is_deleted","==", is_deleted).get()
    if concept is None:
      raise ResourceNotFoundException(f"Concept with uuid {uuid} not found")
    return concept

  @classmethod
  def find_by_title(cls, title):
    return Concept.collection.filter("title", "==", title).fetch()


class SubConcept(NodeItem):
  """SubConcept Class"""
  uuid = TextField(required=True)
  title = TextField(required=True)
  description = TextField()
  all_learning_resource = TextField(required=True)
  child_nodes = MapField()
  parent_nodes = MapField()
  label = TextField(required=True)
  total_lus = NumberField(required=True, default=0)
  is_valid = BooleanField(required=True, default=True)
  child_type = "KnowledgeServiceLearningObjective"
  type = TextField(required=False, default="subconcept")
  alignments = MapField(default={})
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  @property
  def learning_objectives(self):
    return self.children_nodes

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "sub_concepts"
    ignore_none_field = False

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.module = "common.models.knowledge"

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted = False):
    subconcept = SubConcept.collection.filter(
      "uuid", "==", uuid).filter("is_deleted","==", is_deleted).get()
    if subconcept is None:
      raise ResourceNotFoundException(f"SubConcept with uuid {uuid} not found")
    return subconcept

  @classmethod
  def find_by_title(cls, title):
    return SubConcept.collection.filter("title", "==", title).fetch()


class KnowledgeServiceLearningObjective(NodeItem):
  """Learning Objective Class"""
  uuid = TextField(required=True)
  title = TextField(required=True)
  description = TextField()
  child_nodes = MapField()
  parent_nodes = MapField()
  is_valid = BooleanField(required=True, default=True)
  text = TextField()
  child_type = "KnowledgeServiceLearningUnit"
  type = TextField(required=False, default="learning_objective")
  alignments = MapField(default={})
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  @property
  def learning_units(self):
    return self.children_nodes

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "v3_learning_objectives"
    ignore_none_field = False

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.add_learning_unit = self.add_child
    self.add_learning_unit_from_dict = self.add_child_from_dict
    self.module = "common.models.knowledge"

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted = False):
    learning_objective = KnowledgeServiceLearningObjective.collection.filter(
      "uuid", "==", uuid).filter("is_deleted","==", is_deleted).get()
    if learning_objective is None:
      raise ResourceNotFoundException(
          f"Learning Objective with uuid {uuid} not found")
    return learning_objective

  @classmethod
  def find_by_title(cls, title):
    return KnowledgeServiceLearningObjective.collection.filter(
        "title", "==", title).fetch()


class KnowledgeServiceLearningUnit(NodeItem):
  """Learning Unit Class"""
  uuid = TextField(required=True)
  title = TextField(required=True)
  text = TextField(required=True)
  pdf_title = TextField()
  child_nodes = MapField()
  parent_nodes = MapField()
  topics = TextField()
  is_valid = BooleanField(required=True, default=True)
  type = TextField(required=False, default="learning_unit")
  child_type = "KnowledgeServiceTriple"
  coref_text = TextField(required=False, default="")
  alignments = MapField(default={})
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "v3_learning_units"
    ignore_none_field = False

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.module = "common.models.knowledge"

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted = False):
    learning_unit = KnowledgeServiceLearningUnit.collection.filter(
      "uuid", "==", uuid).filter("is_deleted","==", is_deleted).get()
    if learning_unit is None:
      raise ResourceNotFoundException(
          f"Learning Unit with uuid {uuid} not found")
    return learning_unit

  @classmethod
  def find_by_title(cls, title):
    return KnowledgeServiceLearningUnit.collection.filter("title", "==",
                                                          title).fetch()


class KnowledgeServiceTriple(NodeItem):
  """Triple model class"""
  uuid = TextField(required=True)
  sentence = TextField(required=True)
  subject = TextField(required=True)
  predicate = TextField(required=True)
  object = TextField(required=True)
  confidence = NumberField(required=True)
  parent_nodes = MapField()
  # leaf node
  child_type = None
  type = TextField(required=False, default="triple")

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "v3_triples"
    ignore_none_field = False

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # leaf node
    self.children_nodes = None
