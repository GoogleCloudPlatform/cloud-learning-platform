"""Assessment Service Data Models"""

from common.models import NodeItem, BaseModel
from common.utils.errors import ResourceNotFoundException
from fireo.fields import TextField, ListField, MapField, NumberField, BooleanField, DateTime


ASSESSMENT_LITERALS = {
  "assessments":{
    "type" : ["practice", "project", "pretest", "srl", "static_srl",
                "cognitive_wrapper"],
    "alias" : ["assessment"]
  }
}

def check_type(level):
  allowed_types = ASSESSMENT_LITERALS[level]["type"]
  def _check_type(field_val):
    """validator method for type field"""
    if field_val.lower() in allowed_types:
      return True
    return (False, level + " Type must be one of " +
            ",".join("'" + i + "'" for i in allowed_types))
  return _check_type

def check_alias(level):
  allowed_aliases = ASSESSMENT_LITERALS[level]["alias"]
  def _check_alias(field_val):
    """validator method for alias field"""
    if field_val.lower() in allowed_aliases:
      return True
    return (False, level + " Alias must be one of " +
            ",".join("'" + i + "'" for i in allowed_aliases))
  return _check_alias


class Rubric(NodeItem):
  """Rubric Class"""
  uuid = TextField()
  name = TextField()
  description = TextField()
  author = TextField()
  evaluation_criteria = MapField()
  parent_nodes = MapField()
  child_nodes = MapField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "rubrics"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    rubric = Rubric.collection.filter("uuid", "==", uuid).get()
    if rubric is None:
      raise ResourceNotFoundException(f"Rubric with uuid {uuid} not found")
    return rubric

  @classmethod
  def find_by_name(cls, name):
    """Find the rubric item using name
    Args:
        name (string): node item name
    Returns:
        Rubric: Rubric Object
    """
    return Rubric.collection.filter("name", "==", name).fetch()


class RubricCriterion(NodeItem):
  """RubricCriterion Class"""
  uuid = TextField()
  name = TextField()
  description = TextField()
  author = TextField()
  parent_nodes = MapField()
  performance_indicators = ListField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "rubric_criterions"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid):
    rubric_criterion = RubricCriterion.collection.filter("uuid", "==",
                                                         uuid).get()
    if rubric_criterion is None:
      raise ResourceNotFoundException(
          f"Rubric criterion with uuid {uuid} not found")
    return rubric_criterion

  @classmethod
  def find_by_name(cls, name):
    """Find the rubric criterion item using name
    Args:
        name (string): node item name
    Returns:
        RubricCriterion: Rubric Criterion Object
    """
    return RubricCriterion.collection.filter("name", "==", name).fetch()


class AssessmentItem(NodeItem):
  """AssessmentItem Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  question = TextField()
  answer = TextField()
  context = TextField()
  options = ListField()
  question_type = TextField()
  activity_type = TextField()
  use_type = TextField()
  metadata = MapField(default={})
  author = TextField()
  difficulty = NumberField()
  alignments = MapField(default={})
  parent_nodes = MapField(default={})
  child_nodes = MapField(default={})
  references = MapField(default={})
  assessment_reference = MapField(default={})
  achievements = ListField(default=[])
  pass_threshold = NumberField()
  is_deleted = BooleanField(default=False)
  is_locked = BooleanField()
  is_optional = BooleanField(default=False)
  prerequisites = MapField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "assessment_items"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    assessment_item = AssessmentItem.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if assessment_item is None:
      raise ResourceNotFoundException(
          f"Assessment Item with uuid {uuid} not found")
    return assessment_item

  @classmethod
  def find_by_name(cls, name, is_deleted=False):
    """Find the assessment item using name
    Args:
        name (string): node item name
    Returns:
        AssessmentItem: Assessment Item Object
    """
    return AssessmentItem.collection.filter("name", "==", name).filter(
        "is_deleted", "==", is_deleted).fetch()


class Assessment(NodeItem):
  """Assessment Class"""
  uuid = TextField(required=True)
  name = TextField(required=True)
  display_name = TextField()
  author_id = TextField()
  assessment_reference = MapField()
  instructor_id = TextField()
  assessor_id = TextField()
  pass_threshold = NumberField(default=0)
  max_attempts = NumberField()
  metadata = MapField()
  is_autogradable = BooleanField(default=False)
  resource_paths = ListField()
  instructions = MapField()
  # skills, competencies and achievements
  achievements = ListField(default=[])
  alignments = MapField()
  references = MapField()
  # hierarchy
  prerequisites = MapField()
  parent_nodes = MapField()
  child_nodes = MapField()
  # meta fields
  order = NumberField()
  alias = TextField(default="assessment", validator=check_alias("assessments"))
  type = TextField(required=True, validator=check_type("assessments"))
  is_locked = BooleanField()
  is_optional = BooleanField(default=False)
  is_hidden = BooleanField(default=False)
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "assessments"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    assessment = Assessment.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if assessment is None:
      raise ResourceNotFoundException(
          f"Assessment with uuid {uuid} not found")
    return assessment

  @classmethod
  def find_by_name(cls, name, is_deleted=False):
    """Find the assessment item using name
    Args:
        name (string): node item name
    Returns:
        Assessment: Assessment Object
    """
    assessment = Assessment.collection.filter("name", "==", name).filter(
        "is_deleted", "==", is_deleted).fetch()
    if assessment is None:
      raise ResourceNotFoundException(
          f"Assessment with name {name} not found")
    return assessment


class SubmittedAssessment(NodeItem):
  """SubmittedAssessment Class"""
  uuid = TextField(required=True)
  assessment_id = TextField(required=True)
  learner_id = TextField(required=True)
  assessor_id = TextField()
  type = TextField(required=True)
  plagiarism_score = NumberField()
  plagiarism_report_path = TextField()
  result = TextField(default=None)
  pass_status = BooleanField(default=None)
  status = TextField(default="non_evaluated")
  is_flagged = BooleanField(default=False)
  is_autogradable = BooleanField()
  comments = ListField()
  timer_start_time = DateTime(auto=True)
  is_deleted = BooleanField(default=False)
  attempt_no = NumberField(int_only=True)
  learner_session_id = TextField()
  learner_session_data = MapField()
  assessor_session_id = TextField()
  submission_gcs_paths = ListField()
  metadata = MapField(default={})
  submitted_rubrics = ListField()
  overall_feedback = TextField()

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "submitted_assessments"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    submitted_assessment = SubmittedAssessment.collection.filter(
        "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if submitted_assessment is None:
      raise ResourceNotFoundException(
          f"Submitted Assessment with uuid {uuid} not found")
    return submitted_assessment

  @classmethod
  def find_by_name(cls, name, is_deleted=False):
    """Find the submitted assessment using name
    Args:
        name (string): node item name
    Returns:
        SubmittedAssessment: Submitted Assessment Object
    """
    return SubmittedAssessment.collection.filter("name", "==", name).filter(
        "is_deleted", "==", is_deleted).fetch()
