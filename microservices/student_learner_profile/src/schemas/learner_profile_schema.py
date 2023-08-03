"""
Pydantic Model for Learner Profile API's
"""
from typing import Dict, List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field, validator
from schemas.schema_examples import (
  POST_LEARNER_PROFILE_EXAMPLE,
  FULL_LEARNER_PROFILE_EXAMPLE,
  UPDATE_LEARNER_PROFILE_EXAMPLE,
  EDUCATION_TAB_DROPDOWN_VALUES
)
# pylint: disable=no-self-argument
# pylint: disable = invalid-name
STATUS = Literal["in_progress", "not_attempted", "completed",
                "evaluation_pending", "evaluated", "non_evaluated", "skipped"]
EMPLOYMENT_STATUS = Literal["Full-time","Part-time","Seeking work",
    "Unemployed", ""]

class Progress(BaseModel):
  """
  Progress Nodes Pydantic Model
  """
  name: str
  status: Optional[STATUS] = "not_attempted"
  #is_hidden and is_optional is applicable only for the parent_node
  is_optional: Optional[bool] = False
  is_hidden: Optional[bool] = True
  parent_node: Optional[str]
  is_locked: Optional[bool] = True
  progress: Optional[float] = 0
  last_attempted: Optional[str]
  num_attempts: Optional[int]
  child_count: Optional[int]
  completed_child_count: Optional[int]
  ungate: Optional[bool] = False
  instruction_completed: Optional[bool]

class LearningConstraints(BaseModel):
  """
  Learning Contraints Pydandic Model
  """
  weekly_study_time: int = Field(0, ge=0, le=30)


class ContactPreferences(BaseModel):
  """
  Contact Preferences Pydandic Model
  """
  email: Optional[bool] = False
  phone: Optional[bool] = False


class LOSNodes(BaseModel):
  """
  LOS Nodes Pydantic Model
  """
  curriculum_pathways: Optional[Dict[str, Progress]] = {}
  learning_experiences: Optional[Dict[str, Progress]] = {}
  learning_objects: Optional[Dict[str, Progress]] = {}
  learning_resources: Optional[Dict[str, Progress]] = {}
  assessments: Optional[Dict[str, Progress]] = {}


class BasicLearnerProfileModel(BaseModel):
  """
  LearnerProfile Skeleton Pydantic Model
  """
  learner_id: str
  learning_goals: Optional[list] = []
  learning_constraints: Optional[LearningConstraints]
  learning_preferences: Optional[dict] = {}
  patterns_of_participation: Optional[dict] = {}
  employment_status: Optional[EMPLOYMENT_STATUS] = ""
  employment_history: Optional[dict] = {}
  education_history: Optional[dict] = {}
  potential_career_fields: Optional[List] = Field([], max_items=3)
  personal_goals: Optional[str] = Field("", max_length=500)
  account_settings: Optional[dict] = {}
  contact_preferences: Optional[ContactPreferences] = {}
  enrollment_information: Optional[dict] = {}
  attestation_object: Optional[dict] = {}
  progress: Optional[LOSNodes] = {}
  achievements: Optional[list] = []
  tagged_skills: Optional[list] = []
  tagged_competencies: Optional[list] = []
  mastered_skills: Optional[list] = []
  mastered_competencies: Optional[list] = []
  # TODO override this if schema of any of these fields changes
  @validator("account_settings","employment_history","education_history")
  def validate_nested_dict(cls, value):
    """
    Validate that nested dict is not empty.
    Args:
        value (dict): empty dictionary

    Raises:
        ValueError: is dictionary is not empty

    Returns:
        dict: dictionary is empty
    """
    if value != {}:
      raise ValueError("Only an empty dictionary is allowed.")
    return value


class FullLearnerProfileDataModel(BasicLearnerProfileModel):
  """
  LearnerProfile Skeleton Model with uuid, created and updated time
  """
  uuid: str
  is_archived: bool
  created_time: str
  last_modified_time: str


class PostLearnerProfileModel(BaseModel):
  """
  Learner Profile Pydantic Model
  """
  learning_goals: Optional[list] = []
  learning_constraints: Optional[LearningConstraints]
  learning_preferences: Optional[dict] = {}
  patterns_of_participation: Optional[dict] = {}
  employment_status: Optional[EMPLOYMENT_STATUS] = ""
  employment_history: Optional[dict] = {}
  education_history: Optional[dict] = {}
  potential_career_fields: Optional[List] = Field([], max_items=3)
  personal_goals: Optional[str] = ""
  account_settings: Optional[dict] = {}
  contact_preferences: Optional[ContactPreferences] = {}
  enrollment_information: Optional[dict] = {}
  attestation_object: Optional[dict] = {}
  progress: Optional[LOSNodes] = {}
  achievements: Optional[list] = []
  tagged_skills: Optional[list] = []
  tagged_competencies: Optional[list] = []
  mastered_skills: Optional[list] = []
  mastered_competencies: Optional[list] = []

  # TODO override this if schema of any of these fields changes
  @validator("account_settings","employment_history","education_history")
  def validate_nested_dict(cls, value):
    """
    Validate that nested dict is not empty.
    Args:
        value (dict): empty dictionary

    Raises:
        ValueError: is dictionary is not empty

    Returns:
        dict: dictionary is empty
    """
    if value != {}:
      raise ValueError("Only an empty dictionary is allowed.")
    return value

  class Config():
    orm_mode = True
    schema_extra = {"example": POST_LEARNER_PROFILE_EXAMPLE}

class UpdateLearnerProfileModel(BaseModel):
  """
  Update Learner Profile Pydantic Model
  """
  learning_goals: Optional[list]
  learning_constraints: Optional[LearningConstraints]
  learning_preferences: Optional[dict]
  patterns_of_participation: Optional[dict]
  employment_status: Optional[EMPLOYMENT_STATUS]
  employment_history: Optional[dict]
  education_history: Optional[dict]
  potential_career_fields: Optional[List]
  personal_goals: Optional[str]
  account_settings: Optional[dict]
  contact_preferences: Optional[ContactPreferences]
  attestation_object: Optional[dict]
  progress: Optional[LOSNodes]
  achievements: Optional[list]
  is_archived: Optional[bool]
  tagged_skills: Optional[list]
  tagged_competencies: Optional[list]
  mastered_skills: Optional[list]
  mastered_competencies: Optional[list]

  # TODO override this if schema of any of these fields changes
  @validator("account_settings","employment_history","education_history")
  def validate_nested_dict(cls, value):
    """
    Validate that nested dict is not empty.
    Args:
        value (dict): empty dictionary

    Raises:
        ValueError: is dictionary is not empty

    Returns:
        dict: dictionary is empty
    """
    if value != {}:
      raise ValueError("Only an empty dictionary is allowed.")
    return value

  class Config():
    orm_mode = True
    extra = "forbid"
    schema_extra = {"example": UPDATE_LEARNER_PROFILE_EXAMPLE}


class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullLearnerProfileDataModel]]
  total_count: int


class GetAllLearnerProfilesResponseModel(BaseModel):
  """
  Get All Learner Profiles Response Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learner profile"
  data: Optional[TotalCountResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the learner profile",
        "data": {
                  "records":[FULL_LEARNER_PROFILE_EXAMPLE],
                  "total_count": 50
                }
      }
    }


class GetLearnerProfileResponseModel(BaseModel):
  """
  Get Learner Profile Response Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learner profile"
  data: Optional[FullLearnerProfileDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the learner profile",
        "data": FULL_LEARNER_PROFILE_EXAMPLE
      }
    }


class PostLearnerProfileResponseModel(BaseModel):
  """
  Post Learner Profile Response Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learner profile"
  data: Optional[FullLearnerProfileDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully created the learner profile",
        "data": FULL_LEARNER_PROFILE_EXAMPLE
      }
    }


class UpdateLearnerProfileResponseModel(BaseModel):
  """
  Update Learner Profile Response Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the learner profile"
  data: Optional[FullLearnerProfileDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully updated the learner profile",
        "data": FULL_LEARNER_PROFILE_EXAMPLE
      }
    }


class DeleteLearnerProfile(BaseModel):
  """
  Delete Learner Profile Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the learner profile"

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully deleted the learner profile"
      }
    }


class LearnerProfileSearchResponseModel(BaseModel):
  """
  Learner Profile Search Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the learner profiles"
  data: Optional[List[FullLearnerProfileDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the learner profiles",
        "data": [FULL_LEARNER_PROFILE_EXAMPLE]
      }
    }


class LearnerProfileImportJsonResponse(BaseModel):
  """
  Learner Profile Import Json Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the learner profiles"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully created the learner profiles",
        "data": [
          "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
          "lQRzcrRuDpJ9IoW8bCHu"
        ]
      }
    }

class EducationDropdownModel(BaseModel):
  """
  Education Dropdown Pydantic Model
  """
  education_goals: Optional[list]
  employment_status: Optional[list]
  potential_career_fields: Optional[list]

class EducationDropdownResponseModel(BaseModel):
  """
  Education Dropdown Response Pydantic Model
  """
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the possible options for"
  " education goals, employment status, potential career fields"
  data: Optional[EducationDropdownModel]

  class Config():
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetched the possible options for"
  " education goals, employment status, potential career fields",
        "data": EDUCATION_TAB_DROPDOWN_VALUES
      }
    }
