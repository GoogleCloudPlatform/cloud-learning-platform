"""
Pydantic Model for Learner Group Association API's
"""
from typing import List, Optional, Union
from typing_extensions import Literal
from pydantic import BaseModel, constr, Extra
from schemas.schema_examples import (BASIC_ASSOCIATION_GROUP_EXAMPLE,
  FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
  UPDATE_LEARNER_ASSOCIATION_STATUS_EXAMPLE,
  ADD_USER_EXAMPLE, REMOVE_USER_EXAMPLE, ADD_COACH_EXAMPLE,
  REMOVE_COACH_EXAMPLE, ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE,
  REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE)


#pylint: disable=no-self-argument
STATUS = Literal["active", "inactive"]

class UserModel(BaseModel):
  """User Type Pydantic Model"""
  user: Optional[Union[str, dict]] = ""
  status: STATUS


class CoachModel(BaseModel):
  """Coach Type Pydantic Model"""
  coach: Optional[Union[str, dict]] = ""
  status: STATUS


class InstructorModel(BaseModel):
  """Instructor Type Pydantic Model"""
  instructor: Optional[Union[str, dict]] = ""
  curriculum_pathway_id: Optional[Union[str, dict]] = ""
  status: STATUS


class LearnerGroupAssociations(BaseModel):
  """Learner Association Group Type Pydantic Model"""
  coaches: Optional[List[CoachModel]] = []
  instructors: Optional[List[InstructorModel]] = []
  curriculum_pathway_id: Optional[Union[str, dict]] = ""


class BasicLearnerAssociationGroupModel(BaseModel):
  """Association Group Skeleton Pydantic Model"""
  name: constr(max_length=100, regex=r"[a-zA-Z0-9`!#&*%_[\]{}\\;:'\,.\?\s-]+$")
  description: str


class FullLearnerAssociationGroupModel(BasicLearnerAssociationGroupModel):
  """Association Group Model with uuid, created and updated time"""
  uuid: str
  association_type: str = "learner"
  users: Optional[List[UserModel]] = []
  associations: Optional[LearnerGroupAssociations] = {}
  created_time: str
  last_modified_time: str
  is_immutable: Optional[bool] = False


class LearnerAssociationGroupModel(BasicLearnerAssociationGroupModel):
  """Association Group Input Pydantic Model"""

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": BASIC_ASSOCIATION_GROUP_EXAMPLE}


class UpdateLearnerAssociationGroupModel(BaseModel):
  """Update Association Group Pydantic Request Model"""
  name: Optional[constr(
    max_length=100, regex=r"[a-zA-Z0-9`!#&*%_[\]{}\\;:'\,.\?\s-]+$")] = None
  description: Optional[str]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": BASIC_ASSOCIATION_GROUP_EXAMPLE}


class GetLearnerAssociationGroupResponseModel(BaseModel):
  """Fetch Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the association group"
  data: Optional[FullLearnerAssociationGroupModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the association group",
            "data": FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class PostLearnerAssociationGroupResponseModel(BaseModel):
  """Create Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the association group"
  data: FullLearnerAssociationGroupModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the association group",
            "data": FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class UpdateLearnerAssociationGroupResponseModel(BaseModel):
  """Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the association group"
  data: Optional[FullLearnerAssociationGroupModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the association group",
            "data": FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class DeleteLearnerAssociationGroup(BaseModel):
  """Delete Association Group Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the association group"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the association group"
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullLearnerAssociationGroupModel]]
  total_count: int

class AllAssociationGroupResponseModel(BaseModel):
  """Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the association groups"
  data: Optional[TotalCountResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the association groups",
            "data": {
                      "records":[FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class UserAssociationStatus(BaseModel):
  """Association Status Pydantic Model"""
  user_id: str
  status: STATUS

class CoachAssociationStatus(BaseModel):
  """Association Status Pydantic Model"""
  coach_id: str
  status: STATUS

class InstructorAssociationStatus(BaseModel):
  """Association Status Pydantic Model"""
  instructor_id: str
  curriculum_pathway_id: str
  status: STATUS

class UpdateLearnerAssociationStatusModel(BaseModel):
  """Update status of fields in Learner Association Group Request Pydantic
      Model"""
  user: Optional[UserAssociationStatus]
  coach: Optional[CoachAssociationStatus]
  instructor: Optional[InstructorAssociationStatus]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {
      "example": UPDATE_LEARNER_ASSOCIATION_STATUS_EXAMPLE
      }


class AddUsersModel(BaseModel):
  """Add User to Learner Association Group Response Pydantic Model"""
  users: List[str] = []
  status: STATUS = "active"

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": ADD_USER_EXAMPLE}


class RemoveUserModel(BaseModel):
  """Remove User from Learner Association Group Response Pydantic Model"""
  user: str

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": REMOVE_USER_EXAMPLE}


class AddCoachesModel(BaseModel):
  """Add coaches to Association Group Response Pydantic Model"""
  coaches: List[str] = []
  status: STATUS = "active"

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": ADD_COACH_EXAMPLE}


class RemoveCoachModel(BaseModel):
  """Remove coaches to Association Group Response Pydantic Model"""
  coach: str

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": REMOVE_COACH_EXAMPLE}


class AddUserToAssociationGroupResponseModel(BaseModel):
  """Add User Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully added the "\
    "user to the association group"
  data: Optional[FullLearnerAssociationGroupModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully added the user to the association group",
            "data": FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class RemoveUserFromAssociationGroupResponseModel(BaseModel):
  """Remove User Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Remove the user from association group"
  data: Optional[FullLearnerAssociationGroupModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully remove the user from association group",
            "data": FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class AddInstructorToLearnerAssociationGroup(BaseModel):
  """
  Add Instructor To Learner Association Group
  """
  instructors: list
  curriculum_pathway_id: str
  status: STATUS

  class Config:
    """
    Meta Class For Baseclass
    """
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE}


class AddInstructorToLearnerAssociationGroupResponseModel(BaseModel):
  """
  Response Model For Add Instructor To Learner Association Group Example
  """

  success: bool = True
  message: str = "Successfully added the instructors to the learner " \
                 "association group"
  data: FullLearnerAssociationGroupModel

  class Config:
    """
    Meta Class For Baseclass
    """
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully added the instructors to the "
                   "learner association group",
        "data": FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE
      }
    }


class RemoveInstructorFromLearnerAssociationGroup(BaseModel):
  """
  Remove Instructor From Learner Association Group
  """

  instructor: str
  curriculum_pathway_id: str

  class Config:
    """
    Meta Class for Base Class
    """
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {
      "example": REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE
    }


class RemoveInstructorFromLearnerAssociationGroupResponseModel(BaseModel):
  """
  Response Model For Remove Instructor To Learner Association Group Example
  """
  success: bool = True
  message: str = "Successfully removed the instructors from the learner " \
                 "association group"
  data: FullLearnerAssociationGroupModel

  class Config:
    """
    Meta Class For Baseclass
    """
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully removed the instructors from the "
                   "learner association group",
        "data": FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE
      }
    }

class GetAllLearnerForCoachORInstructor(BaseModel):
  """
  Response Model For Get All Learner For Coach or Instructor
  """
  success: bool = True
  message: str = "Successfully fetch the learners for"\
    " the given instructor or coach"
  data: list = []

  class Config:
    orm_mode = True
    schema_extra = {
      "example": {
        "success": True,
        "message": "Successfully fetch the learners for the given instructor",
        "data": ["GDAuFBlir7AyWJjvDipD"]
      }
    }
