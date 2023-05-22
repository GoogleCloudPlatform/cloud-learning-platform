"""
Pydantic Model for UserGroup API's
"""
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, Extra
from schemas.schema_examples import (FULL_GROUP_MODEL_EXAMPLE,
                                     BASIC_GROUP_USERS_EDIT_EXAMPLE,
                                     UPDATE_GROUP_MODEL_EXAMPLE,
                                     POST_USERGROUP_MODEL_EXAMPLE,
                                     FULL_USER_MODEL_EXAMPLE)
from schemas.user_schema import FullUserDataModel
from config import IMMUTABLE_USER_GROUPS

# pylint: disable=invalid-name
ALLOWED_IMMUTABLE_GROUPS = Literal[tuple(IMMUTABLE_USER_GROUPS)]

class BasicUserGroupModel(BaseModel):
  """UserGroup Skeleton Pydantic Model"""
  name: str
  description: str


class FullUserGroupDataModel(BasicUserGroupModel):
  """UserGroup Model with uuid, created and updated time"""
  uuid: str
  created_time: str
  last_modified_time: str
  permissions: Optional[list]
  applications: Optional[list]
  users: Optional[list]
  is_immutable: Optional[bool]


class PostUserGroupModel(BasicUserGroupModel):
  """UserGroup Input Pydantic Model"""

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": POST_USERGROUP_MODEL_EXAMPLE}


class ImmutableUserGroupModel(BasicUserGroupModel):
  """Immutable UserGroup Input Pydantic Model"""
  name: ALLOWED_IMMUTABLE_GROUPS

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": POST_USERGROUP_MODEL_EXAMPLE}


class UpdateUserGroupModel(BaseModel):
  """Update UserGroup Pydantic Request Model"""
  name: Optional[str]
  description: Optional[str]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": UPDATE_GROUP_MODEL_EXAMPLE}


class AddUserFromUserGroupModel(BaseModel):
  """Update UserGroup Pydantic Request Model"""
  user_ids: List[str]

  class Config():
    orm_mode = True
    schema_extra = {"example": BASIC_GROUP_USERS_EDIT_EXAMPLE}


class RemoveUserFromUserGroupModel(BaseModel):
  """Update UserGroup Pydantic Request Model"""
  user_id: str

  class Config():
    orm_mode = True
    schema_extra = {"example": {"user_id": "44qxEpc35pVMb6AkZGbi"}}


class GetUserGroupResponseModel(BaseModel):
  """UserGroup Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the UserGroup"
  data: Optional[FullUserGroupDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the UserGroup",
            "data": FULL_GROUP_MODEL_EXAMPLE
        }
    }


class PostUserGroupResponseModel(BaseModel):
  """UserGroup Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the UserGroup"
  data: FullUserGroupDataModel

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the UserGroup",
            "data": FULL_GROUP_MODEL_EXAMPLE
        }
    }


class UpdateUserGroupResponseModel(BaseModel):
  """UserGroup Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated the UserGroup"
  data: Optional[FullUserGroupDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated the UserGroup",
            "data": FULL_GROUP_MODEL_EXAMPLE
        }
    }


class AddUserToUserGroupResponseModel(BaseModel):
  """Add users to UserGroup Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully added users to user user group"
  data: Optional[FullUserGroupDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully added users to user user group",
            "data": FULL_GROUP_MODEL_EXAMPLE
        }
    }


class RemoveUserFromUserGroupResponseModel(BaseModel):
  """Remove users from UserGroup Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully removed users from user user group"
  data: Optional[FullUserGroupDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully removed users from user user group",
            "data": FULL_GROUP_MODEL_EXAMPLE
        }
    }


class DeleteUserGroup(BaseModel):
  """Delete UserGroup Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully deleted the user group"

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully deleted the UserGroup"
        }
    }

class TotalCountResponseModel(BaseModel):
  records: Optional[List[FullUserGroupDataModel]]
  total_count: int

class AllUserGroupResponseModel(BaseModel):
  """UserGroup Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched the UserGroup"
  data: Optional[TotalCountResponseModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the UserGroup",
            "data": {
                      "records":[FULL_GROUP_MODEL_EXAMPLE],
                      "total_count": 50
                    }
        }
    }


class UserGroupImportJsonResponse(BaseModel):
  """UserGroup Import Json Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully created the UserGroups"
  data: Optional[List[str]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully created the UserGroups",
            "data": [
                "44qxEpc35pVMb6AkZGbi", "00MPqUhCbyPe1BcevQDr",
                "lQRzcrRuDpJ9IoW8bCHu"
            ]
        }
    }


class UserGroupSearchResponseModel(BaseModel):
  """UserGroup Search Response Pydantic Model"""
  success: bool = True
  message: str = "Successfully fetched the user group"
  data: List[FullUserGroupDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched the user group",
            "data": [FULL_GROUP_MODEL_EXAMPLE]
        }
    }


class UpdateGroupApplications(BaseModel):
  """Update applications of Group Request Pydantic Model"""
  applications: List[str]
  action_id: str

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {
        "example": {
            "applications": ["4GATUsfrj4vvdfghjkui"],
            "action_id": "fht67frfghjhnb678"
        }
    }


class CreateGroupRequestModel(BaseModel):
  """Create Group Request Pydantic Model"""
  name: str
  description: str
  users: Optional[list]
  permissions: Optional[list]
  roles: Optional[list]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": {**UPDATE_GROUP_MODEL_EXAMPLE, "users": []}}


class UpdateApplicationsOfGroupResponseModel(BaseModel):
  """Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated applications of a user group"
  data: Optional[FullUserGroupDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated applications of a user group",
            "data": FULL_GROUP_MODEL_EXAMPLE
        }
    }


class UpdatePermissionsOfGroupResponseModel(BaseModel):
  """Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully updated permissions \
              for the applcation of a user group"

  data: Optional[FullUserGroupDataModel]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully updated permissions \
              for the applcation of a user group",
            "data": FULL_GROUP_MODEL_EXAMPLE
        }
    }


class UpdateUserGroupPermissions(BaseModel):
  """Update permissions of UserGroup Request Pydantic Model"""
  permission_ids: List[str]

  class Config():
    orm_mode = True
    extra = Extra.forbid
    schema_extra = {"example": {"permission_ids": ["fht67frfghjhnb678"]}}


class GetUsersBasedOnGroupIdResponseModel(BaseModel):
  """Group Response Pydantic Model"""
  success: Optional[bool] = True
  message: Optional[str] = "Successfully fetched users "\
              "that can be added to user group"
  data: Optional[List[FullUserDataModel]]

  class Config():
    orm_mode = True
    schema_extra = {
        "example": {
            "success": True,
            "message": "Successfully fetched users "\
              "that can be added to user group",
            "data": FULL_USER_MODEL_EXAMPLE
        }
    }
