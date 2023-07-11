"""Learner Profile Service Data Models"""

import regex
import re
from fireo.fields import (TextField, BooleanField, MapField, ListField,
                          NumberField)
from common.models import NodeItem, BaseModel
from common.utils.errors import ResourceNotFoundException

def validate_name(name):
  """Validator method to validate name"""
  if regex.fullmatch(r"[\D\p{L}\p{N}\s]+$", name):
    return True
  else:
    return (False, "Invalid name format")

def check_gender(field_val):
  """validator method for gender field"""
  if field_val.lower() in ["male", "female", "notselected"]:
    return True
  return (False, "Gender must be one of 'Male','Female','NotSelected'")


def check_email_address(field_val):
  """validator method for email_address field"""
  if "@" in field_val and len(field_val) >= 7:
    return True
  return (False, "Invalid Email Address")


def check_backup_email_address(field_val):
  """validator method for email_address field"""
  if (len(field_val) == 0) or ((re.match(
      r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", field_val) and
                                len(field_val) >= 7)):
    return True
  return (False, "Invalid Email Address")


def check_email_address_type(field_val):
  """validator method for email_address_type field"""
  if field_val.lower() in ["home", "work", "organizational", "other"]:
    return True
  return (False, "Email Address Type must be one of " +
          "'Home','Work','Organizational','Other'")


def check_do_not_publish_indicator(field_val):
  """validator method for do not publish field"""
  if field_val.lower() in ["yes", "no", "unknown"]:
    return True
  return (False,
          "Do not publish indicator must be one of " + "'Yes','No','Unknown'")


class Learner(NodeItem):
  """Data model class for Learner"""
  uuid = TextField(required=True)
  #name
  first_name = TextField(required=True, max_length=60, validator=validate_name)
  middle_name = TextField(max_length=60)
  last_name = TextField(required=True, max_length=60, validator=validate_name)
  suffix = TextField(max_length=10)
  prefix = TextField(max_length=30)

  #preferred_name
  preferred_name = TextField()
  preferred_first_name = TextField()
  preferred_middle_name = TextField()
  preferred_last_name = TextField()
  preferred_name_type = TextField()
  preferred_pronoun = TextField()
  #identification
  student_identifier = TextField(max_length=40)
  student_identification_system = TextField(max_length=15)
  personal_information_verification = TextField()
  personal_information_type = TextField()

  #address
  address_type = TextField(max_length=30)
  street_number_and_name = TextField(max_length=100)
  apartment_room_or_suite_number = TextField(max_length=100)
  city = TextField(max_length=100)
  state_abbreviation = TextField(max_length=2)
  postal_code = TextField(max_length=17)
  country_name = TextField(max_length=30)
  country_code = TextField(max_length=2)
  latitude = TextField(max_length=20)
  longitude = TextField(max_length=20)
  country_ansi_code = NumberField(int_only=True, range=(10000, 99999))
  address_do_not_publish_indicator = TextField(
      validator=check_do_not_publish_indicator)

  #telephone
  phone_number = MapField()

  #email
  email_address_type = TextField(validator=check_email_address_type)
  email_address = TextField(required=True, max_length=128,
      validator=check_email_address, to_lowercase=True)
  email_do_not_publish_indicator = TextField(
      validator=check_do_not_publish_indicator)
  backup_email_address = TextField(max_length=128,
      validator=check_backup_email_address, to_lowercase=True)

  #demographics
  birth_date = TextField()
  gender = TextField(validator=check_gender)
  country_of_birth_code = TextField()
  ethnicity = TextField(max_length=100)

  organisation_email_id = TextField(validator=check_email_address,
                                    to_lowercase=True)
  employer_id = TextField()
  employer = TextField(default="")
  employer_email = TextField(validator=check_email_address, to_lowercase=True)
  affiliation = TextField()
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "learners"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    learner = Learner.collection.filter(
      "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if learner is None:
      raise ResourceNotFoundException(f"Learner with uuid {uuid} not found")
    return learner

  @classmethod
  def find_by_first_name(cls, first_name):
    """Find the learner using first name
    Args:
        first_name (string): node item first name
    Returns:
        Learner: Learner Object
    """
    return Learner.collection.filter(
      "first_name", "==", first_name).filter("is_deleted", "==", False).fetch()

  @classmethod
  def find_by_email_address(cls, email_address):
    """Find the learner using email address
    Args:
        email_address (string): node item email address
    Returns:
        Learner: Learner Object
    """
    if email_address:
      email_address = email_address.lower()
    return Learner.collection.filter(
      "email_address", "==", email_address).filter(
      "is_deleted", "==", False).fetch()

  @classmethod
  def delete_by_uuid(cls, uuid, delete_children = True):
    learner = cls.collection.filter(
      "uuid", "==", uuid).filter("is_deleted", "==", False).get()
    if learner is not None:
      learner.is_deleted = True
      learner.update()
      if delete_children:
        LearnerProfile.delete_by_learner_id(learner.uuid)
    else:
      raise ResourceNotFoundException(f"Learner with uuid {uuid} not found")

  @classmethod
  def archive_by_uuid(cls, uuid, archive=True, archive_children=True):
    learner = Learner.collection.filter("uuid", "==",
                                        uuid).filter("is_deleted", "==",
                                                     False).get()
    if learner is not None:
      learner.is_archived = archive
      learner.update()
      if archive_children:
        LearnerProfile.archive_by_learner_id(learner.uuid, archive)
    else:
      raise ResourceNotFoundException(
          f"Learner Profile with uuid {uuid} not found")


class LearnerProfile(NodeItem):
  """Data model class for Learner Profile"""
  # schema for object
  uuid = TextField(required=True)
  learner_id = TextField(required=True)
  learning_goals = ListField()
  learning_constraints = MapField()
  learning_preferences = MapField()
  patterns_of_participation = MapField()
  employment_status = TextField(default="")
  employment_history = MapField()
  education_history = MapField()
  potential_career_fields = ListField(default=[])
  personal_goals = TextField(default="")
  account_settings = MapField()
  contact_preferences = MapField()
  enrollment_information = MapField()
  attestation_object = MapField()
  progress = MapField(default={})
  achievements = ListField(default=[])
  tagged_skills = ListField(default=[])
  tagged_competencies = ListField(default=[])
  mastered_skills = ListField(default=[])
  mastered_competencies = ListField(default=[])
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "learner_profiles"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    learner_profile = LearnerProfile.collection.filter(
      "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if learner_profile is None:
      raise ResourceNotFoundException(
          f"Learner profile with uuid {uuid} not found")
    return learner_profile

  @classmethod
  def find_by_learner_id(cls, learner_id):
    """Find the learner profile item using learner id
    Args:
        learner_id (string): node item learner id
    Returns:
        LearnerProfile: Learner Profile Object
    """
    Learner.find_by_uuid(learner_id)
    learner_profile = LearnerProfile.collection.filter("learner_id", "==",\
       learner_id).filter("is_deleted", "==", False).get()
    if learner_profile is None:
      raise ResourceNotFoundException(
          f"LearnerProfile with learner id {learner_id} not found")
    return learner_profile

  @classmethod
  def create_object(cls, input_learner_profile_dict):
    """Function to create learner object"""
    new_learner_profile = cls()
    learner = Learner.collection.filter(
        "uuid", "==", input_learner_profile_dict["learner_id"]).get()

    # Raises an error for not creating a learner profile if a
    # learner is not found for the given id
    if learner is None:
      raise ResourceNotFoundException(
          f"Cannot create learner profile as learner with uuid "
          f"'{input_learner_profile_dict['learner_id']}' not found"
      )
    existing_learner_profile = cls.collection.filter(
        "learner_id", "==", input_learner_profile_dict["learner_id"]).get()

    # If Learning profile already exists for the learner then
    # the existing learner profile is returned
    if existing_learner_profile is None:
      new_learner_profile = new_learner_profile.from_dict(
          input_learner_profile_dict)
      new_learner_profile.uuid = ""

      new_learner_profile.save()
      new_learner_profile.uuid = new_learner_profile.id
      new_learner_profile.update()
    else:
      new_learner_profile = existing_learner_profile
    return new_learner_profile

  @classmethod
  def delete_by_learner_id(cls, learner_id):
    learner_profiles = LearnerProfile.collection.filter(
      "learner_id", "==", learner_id).filter("is_deleted", "==", False).fetch()
    for learner_profile in learner_profiles:
      learner_profile.is_deleted = True
      learner_profile.update()

  @classmethod
  def archive_by_learner_id(cls, learner_id, archive=True):
    learner_profiles = LearnerProfile.collection.filter("learner_id", "==",
                                                        learner_id).filter(
                                                            "is_deleted", "==",
                                                            False).fetch()
    for learner_profile in learner_profiles:
      learner_profile.is_archived = archive
      learner_profile.update()


class Achievement(NodeItem):
  """Data model class for Achievement"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  type = TextField(required=True)
  alignments = MapField()
  associations = MapField()
  credits_available = NumberField()
  field_of_study = TextField()
  image = TextField()
  result_descriptions = ListField()
  tags = ListField()
  description = TextField()
  metadata = MapField()
  timestamp = TextField()
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "achievements"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted=False):
    achievement = Achievement.collection.filter(
      "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if achievement is None:
      raise ResourceNotFoundException(f"Achievement with uuid {uuid} not found")
    return achievement

  @classmethod
  def find_by_type(cls, type):  # pylint: disable=redefined-builtin
    """Find the achievement using type of achievement
    Args:
        type (string): node item type
    Returns:
        Achievement: Achievement Object
    """
    return Achievement.collection.filter(
      "type", "==", type).filter("is_deleted", "==", False).fetch()

  @classmethod
  def find_by_learner_id(cls, learner_id):  # pylint: disable=redefined-builtin
    """Find the list of achievements using learner_id
    Args:
        learner_id (string): node item learner id
    Returns:
        Achievement: Achievement Object
    """
    Learner.find_by_uuid(learner_id)
    return Achievement.collection.filter(
      "learner_id", "==", learner_id).filter("is_deleted", "==", False).fetch()

  @classmethod
  def create_object(cls, input_achievement_dict):
    """Function to create new achievement object"""
    new_achievement = cls()
    new_achievement = new_achievement.from_dict(input_achievement_dict)
    new_achievement.uuid = ""

    new_achievement.save()
    new_achievement.uuid = new_achievement.id
    new_achievement.update()
    print("Added new achievement - ", new_achievement.uuid)
    return new_achievement

  @classmethod
  def delete_by_learner_id(cls, learner_id):
    achievements = Achievement.collection.filter(
      "learner_id", "==", learner_id).filter("is_deleted", "==", False).fetch()
    for achievement in achievements:
      achievement.is_deleted = True
      achievement.update()

  @classmethod
  def archive_by_learner_id(cls, learner_id, archive=True):
    achievements = Achievement.collection.filter("learner_id", "==",
                                                 learner_id).filter(
                                                     "is_deleted", "==",
                                                     False).fetch()
    for achievement in achievements:
      achievement.is_archived = archive
      achievement.update()


class Goal(NodeItem):
  """Data model class for Goal"""
  # schema for object
  uuid = TextField(required=True)
  name = TextField(required=True)
  description = TextField()
  type = TextField(required=True)
  aligned_skills = ListField()
  aligned_workforces = ListField()
  aligned_credentials = ListField()
  aligned_learning_experiences = ListField()
  is_archived = BooleanField(default=False)
  is_deleted = BooleanField(default=False)

  class Meta:
    collection_name = BaseModel.DATABASE_PREFIX + "goals"
    ignore_none_field = False

  @classmethod
  def find_by_uuid(cls, uuid, is_deleted = False):
    goal = Goal.collection.filter(
      "uuid", "==", uuid).filter("is_deleted", "==", is_deleted).get()
    if goal is None:
      raise ResourceNotFoundException(f"Goal with uuid {uuid} not found")
    return goal

  @classmethod
  def find_by_name(cls, name):
    """Find the goal using name
    Args:
        name (string): Goal name
    Returns:
        Goal: Goal Object
    """
    return Goal.collection.filter(
      "name", "==", name).filter("is_deleted", "==", False).fetch()
