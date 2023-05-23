"""module to add competency,sub_competency,
learning objective and learning unit to firestore collections"""
from common.models import NodeItem, BaseModel
from fireo.fields import ReferenceField, TextField, NumberField, BooleanField

class Competency(NodeItem):
  """Competency Class"""
  # schema for object
  title = TextField(required=True)
  description = TextField()
  label = TextField(required=True)
  type = TextField(required=False, default="competency")
  is_valid = BooleanField(required=True, default=True)
  child_type = "SubCompetency"

  @property
  def sub_competencies(self):
    return self.children_nodes

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX+"competencies"
    ignore_none_field = False

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.add_sub_competency = self.add_child
    self.add_sub_competency_from_dict = self.add_child_from_dict
    self.module = "common.models.competency"


# TODO: all own files
class SubCompetency(NodeItem):
  """SubCompetency Class"""
  title = TextField(required=True)
  description = TextField()
  all_learning_resource = TextField(required=True)
  parent_node = ReferenceField(Competency, auto_load=False)
  label = TextField(required=True)
  total_lus = NumberField(required=True, default=0)
  is_valid = BooleanField(required=True, default=True)
  child_type = "LearningObjective"
  type = TextField(required=False, default="sub_competency")

  @property
  def learning_objectives(self):
    return self.children_nodes

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX+"sub_competencies"
    ignore_none_field = False

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.add_learning_objective = self.add_child
    self.add_learning_objective_from_dict = self.add_child_from_dict
    self.module = "common.models.competency"


# TODO: sub-learning objectives, can we nest these arbitrarily?
class LearningObjective(NodeItem):
  """Learning Objective Class"""
  # schema for object
  title = TextField(required=True)
  description = TextField()
  parent_node = ReferenceField(SubCompetency, auto_load=False)
  is_valid = BooleanField(required=True, default=True)
  text = TextField()
  child_type = "LearningUnit"
  type = TextField(required=False, default="learning_objective")

  @property
  def learning_units(self):
    return self.children_nodes

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX+"learning_objectives"
    ignore_none_field = False

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.add_learning_unit = self.add_child
    self.add_learning_unit_from_dict = self.add_child_from_dict
    self.module = "common.models.competency"


class LearningUnit(NodeItem):
  """Learning Unit Class"""
  # schema for object
  title = TextField(required=True)
  text = TextField(required=True)
  pdf_title = TextField()
  parent_node = ReferenceField(LearningObjective, auto_load=False)
  topics = TextField()
  is_valid = BooleanField(required=True, default=True)
  child_type = "Triple"
  type = TextField(required=False, default="learning_unit")
  coref_text = TextField(required=False, default="")
  @property
  def triples(self):
    return self.children_nodes

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX+"learning_units"
    ignore_none_field = False

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.add_triple = self.add_child
    self.add_triple_from_dict = self.add_child_from_dict
    self.module = "common.models.competency"


class Triple(NodeItem):
  """Triple model class"""

  sentence = TextField(required=True)
  subject = TextField(required=True)
  predicate = TextField(required=True)
  object = TextField(required=True)
  confidence = NumberField(required=True)
  parent_node = ReferenceField(LearningUnit, auto_load=False)
  # leaf node
  child_type = None
  type = TextField(required=False, default="triple")

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX+"triples"
    ignore_none_field = False

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # leaf node
    self.children_nodes = None
