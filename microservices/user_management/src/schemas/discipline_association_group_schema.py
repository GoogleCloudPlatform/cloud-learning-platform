"""
Pydantic Model for Discipline Group Association API's
"""
from typing import List, Optional, Union
from typing_extensions import Literal
from pydantic import BaseModel, constr, Extra
from schemas.user_schema import FullUserDataModel
from schemas.schema_examples import (BASIC_ASSOCIATION_GROUP_EXAMPLE,
                                  FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE,
                                  UPDATE_DISCIPLINE_ASSOCIATION_STATUS_EXAMPLE,
                                  ADD_USER_EXAMPLE, REMOVE_USER_EXAMPLE)

#pylint: disable=no-self-argument
STATUS = Literal["active", "inactive"]


class UserModel(BaseModel):
  """User Type Pydantic Model"""
  user: Optional[Union[str, dict]] = ""
  user_type: Optional[str] = ""
  status: STATUS

class CurriculumPathwayModel(BaseModel):
  """Coach Type Pydantic Model"""
  curriculum_pathway_id: Optional[Union[dict, str]] = ""
  status: STATUS

class DisciplineGroupAssociations(BaseModel):
  """Discipline Association Group Type Pydantic Model"""
  curriculum_pathways: Optional[List[CurriculumPathwayModel]] = []

class BasicDisciplineAssociationGroupModel(BaseModel):
  """Association Group Skeleton Pydantic Model"""
  name: constr(max_length=100, regex=r"[a-zA-Z0-9`!#&*%_[\]{}\\;:'\,.\?\s-]+$")
  description: str


class FullDisciplineAssociationGroupModel(BasicDisciplineAssociationGroupModel):
  """Association Group Model with uuid, created and updated time"""
  uuid: str
  association_type: str = "discipline"
  users: Optional[List[UserModel]] = []
  associations: Optional[DisciplineGroupAssociations] = {}
  created_time: str
  last_modified_time: str
  is_immutable: Optional[bool] = False


class DisciplineAssociationGroupModel(BasicDisciplineAssociationGroupModel):
  """Association Group Input Pydantic Model"""

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": BASIC_ASSOCIATION_GROUP_EXAMPLE}


class UpdateDisciplineAssociationGroupModel(BaseModel):
  """Update Association Group Pydantic Request Model"""
  name: Optional[constr(
    max_length=100, regex=r"[a-zA-Z0-9`!#&*%_[\]{}\\;:'\,.\?\s-]+$")] = None
  description: Optional[str]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": BASIC_ASSOCIATION_GROUP_EXAMPLE}


class GetDisciplineAssociationGroupResponseModel(BaseModel):
  """Fetch Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the association group"
  data: Optional[FullDisciplineAssociationGroupModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the association group",
            "data": FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class PostDisciplineAssociationGroupResponseModel(BaseModel):
  """Create Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the association group"
  data: FullDisciplineAssociationGroupModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the association group",
            "data": FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class AddCurriculumPathwayRequestModel(BaseModel):
  """Add curriculum pathwat id to Discipline Group Type Pydantic Model"""
  curriculum_pathway_id: str
  status: STATUS


class UpdateDisciplineAssociationGroupResponseModel(BaseModel):
  """Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the association group"
  data: Optional[FullDisciplineAssociationGroupModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the association group",
            "data": FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class DeleteDisciplineAssociationGroup(BaseModel):
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

class RemoveDisciplineFromAssociationGroupModel(BaseModel):
  """RemoveDiscipline from Association Group Data Model"""
  curriculum_pathway_id: str

class AddDisciplineToAssociationGroupModel(
  RemoveDisciplineFromAssociationGroupModel):
  """AddDiscipline to Association Group Data Model"""
  status: Literal[STATUS]

class AllAssociationGroupResponseModel(BaseModel):
  """Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the association groups"
  data: Optional[List[FullDisciplineAssociationGroupModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the association groups",
            "data": [FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE]
        }
    }


class UsersAssociatedToDisciplineResponseModel(BaseModel):
  """Users Associated To Discipline Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the users"
  data: Optional[List[Union[FullUserDataModel, str]]]


class AddUsersModel(BaseModel):
  """Add User To Discipline Association Group Response Pydantic Model"""
  users: List[str]
  status: STATUS

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": ADD_USER_EXAMPLE}


class RemoveUserModel(BaseModel):
  """Remove User from Discipline Association Group Response Pydantic Model"""
  user: str

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": REMOVE_USER_EXAMPLE}


class AddUserToAssociationGroupResponseModel(BaseModel):
  """Add User Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully added the user "\
    "to the association group"
  data: Optional[FullDisciplineAssociationGroupModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully added the user to the association group",
            "data": FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE
        }
    }

class RemoveUserFromAssociationGroupResponseModel(BaseModel):
  """Remove User Association Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully Remove the user from association group"
  data: Optional[FullDisciplineAssociationGroupModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully remove the user from association group",
            "data": FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE
        }
    }


class UserAssociationStatus(BaseModel):
  """Association Status for User Pydantic Model"""
  user_id: str
  status: STATUS

class DisciplineAssociationStatus(BaseModel):
  """Association Status for User Pydantic Model"""
  curriculum_pathway_id: str
  status: STATUS


class UpdateDisciplineAssociationStatusModel(BaseModel):
  """Update status of fields in Discipline Association Group Request Pydantic
      Model"""
  user: Optional[UserAssociationStatus]
  curriculum_pathway: Optional[DisciplineAssociationStatus]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {
      "example": UPDATE_DISCIPLINE_ASSOCIATION_STATUS_EXAMPLE
      }
