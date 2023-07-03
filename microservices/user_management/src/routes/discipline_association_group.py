""" Discipline Association Group endpoints """
import traceback
from fastapi import APIRouter, Query
from typing import Optional
from typing_extensions import Literal
from common.models import AssociationGroup, User, CurriculumPathway
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                ConflictError)
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import (Conflict, InternalServerError,
                                          BadRequest, ResourceNotFound)
from schemas.discipline_association_group_schema import (
  GetDisciplineAssociationGroupResponseModel, DisciplineAssociationGroupModel,
  PostDisciplineAssociationGroupResponseModel, DeleteDisciplineAssociationGroup,
  UpdateDisciplineAssociationGroupResponseModel, AddUsersModel, RemoveUserModel,
  UpdateDisciplineAssociationGroupModel, UpdateDisciplineAssociationStatusModel,
  AllAssociationGroupResponseModel, AddUserToAssociationGroupResponseModel,
  RemoveUserFromAssociationGroupResponseModel, AddCurriculumPathwayRequestModel,
  RemoveDisciplineFromAssociationGroupModel,
  UsersAssociatedToDisciplineResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  ConflictResponseModel)
from services.collection_handler import CollectionHandler
from services.association_group_handler import (
              load_discipline_group_field_data, is_discipline_association_group,
              get_all_learner_association_groups,
              remove_discipline_from_learner_association_group)
from config import ERROR_RESPONSES, IMMUTABLE_ASSOCIATION_GROUPS

# pylint: disable=invalid-name

router = APIRouter(
    tags=["Discipline Association Group"],
    prefix="/association-groups",
    responses=ERROR_RESPONSES)

ALLOWED_FILTER_BY_TYPE_VALUES = Literal["instructor", "assessor"]

@router.get(
    "/discipline-associations",
    response_model=AllAssociationGroupResponseModel,
    name="Get All Discipline Association Groups")
def get_discipline_association_groups(skip: int = Query(0, ge=0, le=2000),
                                      limit: int = Query(10, ge=1, le=100),
                                      fetch_tree: Optional[bool] = False):
  """The get association groups endpoint will return an array of Discipline
  association groups from firestore

  ### Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of group array to be returned
      fetch_tree (bool): To fetch the entire object
                        instead of the UUID of the object

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AllGroupResponseModel: Array of association group Object
  """
  try:
    collection_manager = AssociationGroup.collection

    collection_manager = collection_manager.filter("association_type", "==",
                                                   "discipline")

    groups = collection_manager.order("-created_time").offset(skip).fetch(limit)

    if fetch_tree:
      association_groups = []
      for group in groups:
        association_group = group.get_fields(reformat_datetime=True)
        group_details = load_discipline_group_field_data(association_group)
        association_groups.append(group_details)
    else:
      association_groups = [i.get_fields(reformat_datetime=True) for i \
                          in groups]
    return {
        "success": True,
        "message": "Successfully fetched the association groups",
        "data": association_groups
    }
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
  "/discipline-association/discipline/{curriculum_pathway_id}/users",
  response_model=UsersAssociatedToDisciplineResponseModel,
    responses={ 404: {
      "model": NotFoundErrorResponseModel
    }}
  )
def get_users_assigned_to_discipline(
                  curriculum_pathway_id: str,
                  user_type: Optional[ALLOWED_FILTER_BY_TYPE_VALUES] = None,
                  fetch_tree: Optional[bool] = False):
  """The get users endpoint will fetch users from disicpline association group
     from firestore where provided discipline is associated

  ### Args:
      user_uuid (str): Unique id of the discipline for which users
                             are to be fetched
      user_type (str): Filter by user type(instructor/assessor)
      fetch_tree (bool): To fetch the entire object
                        instead of the UUID of the object

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UsersAssociatedToDisciplineResponseModel: Array of User Object
  """
  try:
    curriculum_pathway = CurriculumPathway.find_by_uuid(curriculum_pathway_id)
    if curriculum_pathway.alias != "discipline":
      raise ValidationError(
        f"Given curriculum pathway id {curriculum_pathway_id} "
        "is not of discipline type")

    collection_manager = AssociationGroup.collection.filter(
                              "association_type", "==", "discipline")

    groups = collection_manager.order("-created_time").fetch()

    association_groups = [i.get_fields(reformat_datetime=True) for i in groups]

    discipline_group = None
    for group in association_groups:
      for curriculum_pathway_dict in group.get("associations", {}).get(
        "curriculum_pathways", []):
        if isinstance(curriculum_pathway_dict, dict) and \
          curriculum_pathway_id == curriculum_pathway_dict.get(
            "curriculum_pathway_id") and curriculum_pathway_dict.get(
            "status") == "active":
          discipline_group = group
          break

    if discipline_group:
      if user_type is not None:
        users = [user["user"] for user in discipline_group["users"]
                if user["user_type"] == user_type and
                user["status"] == "active"]
      else:
        users = [user["user"] for user in discipline_group["users"]
                 if user["status"] == "active"]

    else:
      raise ValidationError(
        f"Given curriculum pathway id {curriculum_pathway_id} "
        "is not actively associated in any discipline association group")

    if fetch_tree:
      users = [CollectionHandler.get_document_from_collection("users", user) \
                for user in users]

    return {
        "success": True,
        "message": "Successfully fetched the users",
        "data": users
    }
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/discipline-association/{uuid}",
    response_model=GetDisciplineAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_discipline_association_group(uuid: str,
                                     fetch_tree: Optional[bool] = False):
  """The get discipline association group endpoint will return the association
  group of discipline type from firestore of which uuid is provided

  ### Args:
      uuid (str): Unique identifier for association group

  ### Raises:
      ResourceNotFoundException: If the association group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetDisciplineAssociationGroupResponseModel: association group Object
  """
  try:
    association_group = AssociationGroup.find_by_uuid(uuid)
    association_group = association_group.get_fields(reformat_datetime=True)
    if fetch_tree:
      association_group = load_discipline_group_field_data(association_group)
    if not is_discipline_association_group(association_group):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not discipline type")

    return {
        "success": True,
        "message": "Successfully fetched the association group",
        "data": association_group
    }

  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/discipline-association",
    response_model=PostDisciplineAssociationGroupResponseModel,
    responses={409: {"model": ConflictResponseModel}})
def create_discipline_association_group(
    input_association_group: DisciplineAssociationGroupModel):
  """The create discipline association group endpoint will add a new association
  group of discipline type to firestore as per details given in request body

  ### Args:
      input_association_group (DisciplineAssociationGroupModel): input
                                            association group to be inserted

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostDisciplineAssociationGroupResponseModel: Association Group Object
  """
  try:
    if input_association_group.name in IMMUTABLE_ASSOCIATION_GROUPS:
      raise ValidationError((f"Cannot create an association group with name "
        f"{input_association_group.name} as it is for immutable association "
        "group"))
    existing_group = AssociationGroup.find_by_name(input_association_group.name)
    if existing_group is not None:
      raise ConflictError(
          "AssociationGroup with the given name: "\
            f"{input_association_group.name} already exists")

    discipline_associations = {"curriculum_pathways": []}

    input_association_group_dict = {**input_association_group.dict()}
    input_association_group_dict["association_type"] = "discipline"
    input_association_group_dict["associations"] = discipline_associations

    new_group = AssociationGroup()
    new_group = new_group.from_dict(input_association_group_dict)
    new_group.uuid = ""
    new_group.save()
    new_group.uuid = new_group.id
    new_group.update()
    association_group_fields = new_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully created the association group",
        "data": association_group_fields
    }
  except ConflictError as e:
    Logger.info(traceback.print_exc())
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/discipline-association/{uuid}",
    response_model=UpdateDisciplineAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }, 409: {
        "model": ConflictResponseModel
    }})
def update_discipline_association_group(
              uuid: str,
              input_association_group: UpdateDisciplineAssociationGroupModel):
  """Update an association group of discipline type with the uuid passed in the
    request body

  ### Args:
      input_group (UpdateDisciplineAssociationGroupModel): Required body of the
            association group

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateDisciplineAssociationGroupResponseModel: association group Object
  """
  try:
    input_group_dict = {**input_association_group.dict(exclude_unset=True)}
    input_group_name = input_group_dict.get("name")
    if input_group_name in IMMUTABLE_ASSOCIATION_GROUPS:
      raise ValidationError(f"Cannot update name to {input_group_name} as "
                            "it is for immutable groups only")
    existing_association_group = AssociationGroup.find_by_uuid(uuid)

    if input_group_name:
      existing_group = AssociationGroup.find_by_name(input_group_dict["name"])
      if existing_group is not None:
        raise ConflictError(
            "AssociationGroup with the given name: "\
              f"{input_association_group.name} already exists")
      if existing_association_group.is_immutable or\
        existing_association_group.name in IMMUTABLE_ASSOCIATION_GROUPS:
        raise ValidationError(f"Cannot update name of an "
                              f"immutable association group with uuid: {uuid}")

    group_fields = existing_association_group.get_fields()

    if is_discipline_association_group(group_fields):
      for key, value in input_group_dict.items():
        group_fields[key] = value
      for key, value in group_fields.items():
        setattr(existing_association_group, key, value)

      existing_association_group.update()
      group_fields = existing_association_group.get_fields(
          reformat_datetime=True)

    else:
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not discipline type")

    return {
        "success": True,
        "message": "Successfully updated the association group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    Logger.info(traceback.print_exc())
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.delete(
    "/discipline-association/{uuid}",
    response_model=DeleteDisciplineAssociationGroup,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_discipline_association_group(uuid: str):
  """Delete an association group of discipline type with the given uuid
    from firestore

  ### Args:
      uuid (str): Unique id of the association group

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    association_group = AssociationGroup.find_by_uuid(uuid)
    if association_group.is_immutable or\
      association_group.name in IMMUTABLE_ASSOCIATION_GROUPS:
      raise ValidationError(
        f"Cannot delete an immutable association group with uuid: {uuid}")
    association_group_fields = association_group.get_fields(
      reformat_datetime=True)
    if is_discipline_association_group(association_group_fields):
      for discipline in association_group_fields["associations"].get(
      "curriculum_pathways"):
        if discipline.get("status")=="active":
          remove_discipline_from_learner_association_group(discipline[
            "curriculum_pathway_id"])
      AssociationGroup.collection.delete(association_group.key)

    else:
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not discipline type")

    return {
        "success": True,
        "message": "Successfully deleted the association group"
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/discipline-association/{uuid}/users/add",
    response_model=AddUserToAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def add_user_to_discipline_association_group(uuid: str,
                                             input_users: AddUsersModel):
  """Add instructors or assessors to the discipline association group
  with the uuid passed in the request body
  Note: Only user belong to instructor or assessor user group
  can be added in the discipline association group

  ### Args:
      input_users: Required body to the add users in the
      discipline association group with the status field

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AddUserToAssociationGroupResponseModel: discipline
      association group Object
  """
  try:
    existing_association_group = AssociationGroup.find_by_uuid(uuid)

    input_users_dict = {**input_users.dict()}
    group_fields = existing_association_group.get_fields()

    # Checking the given UUID if of discipline type or not
    if not is_discipline_association_group(group_fields):
      raise ValidationError(
          f"AssociationGroup for given uuid: {uuid} "\
                            "is not discipline type")

    if not isinstance(group_fields.get("users"), list):
      group_fields["users"] = []

    discipline_users = [i["user"] for i in group_fields["users"]]

    for user in input_users_dict.get("users"):

      if user in discipline_users:
        raise ValidationError(f"User {user} is already present "\
                            "in the discipline association group")

      # Checking wheather given user should belong
      # to the user_group type instructor/assessor
      add_user = User.find_by_user_id(user)

      add_user_fields = add_user.get_fields(reformat_datetime=True)

      if add_user_fields.get("user_type") not in ["instructor", "assessor"]:
        raise ValidationError(
          f"User for given user_id {user} is not instructor or assessor")

      # FIXME: To add validation wheather that user belongs
      # to instructor or assessor user-group or not

      # Only insert the User if its not exist in the discipline
      # association group
      if not any(users["user"] == user for users in group_fields["users"]):
        group_fields["users"].append({
            "user": user,
            "user_type": add_user_fields.get("user_type"),
            "status": input_users_dict.get("status")
        })

    for key, value in group_fields.items():
      setattr(existing_association_group, key, value)

    existing_association_group.update()
    group_fields = existing_association_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully added the users "\
          "to the discipline association group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e



@router.post(
    "/discipline-association/{uuid}/discipline/add",
    response_model=UpdateDisciplineAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def add_discipline_to_discipline_association_group(uuid: str,
    input_discipline: AddCurriculumPathwayRequestModel):
  """Add a discipline to a discipline association group with the
  given status

  ### Args:
      uuid (str): Unique id of the association group
      input_discipline (dict):
                            pathway: str
                            status: str : Literal[`active`, `inactive`]
  ### Returns:
      Updated Discipline Association Group Data
  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong
  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    association_group = AssociationGroup.find_by_uuid(uuid)
    association_group_fields = association_group.get_fields(
      reformat_datetime=True)
    input_discipline = {**input_discipline.dict()}
    cp = CurriculumPathway.find_by_uuid(
      input_discipline["curriculum_pathway_id"])
    if cp.alias != "discipline":
      raise ValidationError("Input ID is not a valid Discipline ID")
    if association_group_fields["association_type"] == "discipline":
      if "curriculum_pathways" in association_group_fields["associations"]:
        # Validate if the Discipline ID is already added or not
        for discipline in association_group_fields["associations"][
          "curriculum_pathways"]:
          if discipline["curriculum_pathway_id"] == \
            input_discipline["curriculum_pathway_id"]:
            raise ValidationError(
            f"Discipline ID={input_discipline['curriculum_pathway_id']} "+\
            f"already added to the DisciplineAssociationGroup={uuid}")
      else:
        association_group_fields["associations"]["curriculum_pathways"] = []

      # Validate that the discipline is not added to
      # any other discipline association group

      group = AssociationGroup.collection.filter(
        "association_type", "==", "discipline").filter(
        "associations.curriculum_pathways", "array_contains",
        input_discipline).get()
      if group:
        raise ValidationError(
          f"{input_discipline['curriculum_pathway_id']} found"+ \
          " in Another Discipline Association Group")
      inactive_discipline = {
        "curriculum_pathway_id": input_discipline["curriculum_pathway_id"],
        "status": "inactive"
      }
      group = AssociationGroup.collection.filter(
        "association_type", "==", "discipline").filter(
        "associations.curriculum_pathways", "array_contains",
        inactive_discipline).get()
      if group:
        raise ValidationError(
          f"{input_discipline['curriculum_pathway_id']} found"+ \
            " in Another Discipline Association Group")
      # Add the Discipline ID to the associations in curriculum_pathways
      association_group_fields["associations"][
        "curriculum_pathways"].append(input_discipline)
      association_group.associations = association_group_fields["associations"]
      association_group.update()
    else:
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
        "is not discipline type")
    return {
      "success": True,
      "message": "Successfully added the discipline to the association group",
      "data": association_group_fields
    }

  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/discipline-association/{uuid}/discipline/remove",
    response_model=UpdateDisciplineAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def remove_discipline_from_discipline_association_group(uuid: str,
    input_discipline: RemoveDisciplineFromAssociationGroupModel):
  """Remove a discipline to a discipline association group with the
  given status

  ### Args:
      uuid (str): Unique id of the association group
  ### Returns:
      Updated Discipline Association Group Data
  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong
  ### Returns:
      JSON: Success/Fail Message
  """
  try:
    association_group = AssociationGroup.find_by_uuid(uuid)
    association_group_fields = association_group.get_fields(
      reformat_datetime=True)
    input_discipline = {**input_discipline.dict()}

    if not association_group_fields["association_type"] == "discipline":
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
        "is not discipline type")

    if "curriculum_pathways" in association_group_fields["associations"]:
      # Validate if the Discipline ID is already added or not
      del_idx = None
      for i, discipline in enumerate(association_group_fields["associations"][
        "curriculum_pathways"]):
        if discipline["curriculum_pathway_id"] == \
        input_discipline["curriculum_pathway_id"]:
          del_idx = i
          break
      if del_idx is not None:
        del association_group_fields["associations"][
          "curriculum_pathways"][del_idx]
        remove_discipline_from_learner_association_group(
          input_discipline["curriculum_pathway_id"])
        association_group.associations = association_group_fields[
          "associations"]
        association_group.update()
      else:
        raise ValidationError(
          f"""Discipline ID = {input_discipline[
        "curriculum_pathway_id"]} not found in Association Group = {uuid}""")

    return {
    "success": True,
    "message": "Successfully removed the discipline from the association group",
    "data": association_group_fields
    }

  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/discipline-association/{uuid}/user/remove",
    response_model=RemoveUserFromAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def remove_user_from_discipline_association_group(uuid: str,
                                                  input_user: RemoveUserModel):
  """Remove instructor or assessor from the discipline
  association group with the uuid passed in the
  request body

  ### Args:
      input_user: UUID of the user that need to
      remove from the discipline association group

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      RemoveUserFromAssociationGroupResponseModel: discipline
      association group Object
  """
  try:
    existing_association_group = AssociationGroup.find_by_uuid(uuid)

    input_users_dict = {**input_user.dict()}
    group_fields = existing_association_group.get_fields()

    # Checking the given UUID if of discipline type or not
    if not is_discipline_association_group(group_fields):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not discipline type")

    group_users = map(lambda x: x["user"], group_fields["users"])

    # Check if user exists in association group
    if input_users_dict["user"] not in group_users:
      raise ValidationError(f"User with uuid {input_users_dict['user']} "\
        f"is not a part of Association Group with uuid {uuid}")

    if isinstance(group_fields.get("users"), list):
      # Identify if user being deleted is instructor type
      is_instructor = False
      for user_dict in group_fields.get("users"):
        if input_users_dict["user"] == user_dict["user"] and \
          user_dict["user_type"] == "instructor":
          is_instructor = True
          break

      # The filter returns an iterator containing all the users
      group_fields["users"][:] = filter(
          lambda x: x["user"] != input_users_dict["user"],
          group_fields.get("users"))

      # Logic to remove instructor associated from learner association group
      if is_instructor and group_fields.get("associations"):
        # Get active curriculum_pathway_id for discipline from Discipline Group
        for pathway_dict in group_fields.get("associations").get(
          "curriculum_pathways"):
          if pathway_dict["status"] == "active":
            discipline_id = pathway_dict["curriculum_pathway_id"]
            break

        # Fetch all learner association groups
        learner_association_groups = AssociationGroup.collection.filter(
                      "association_type", "==", "learner").fetch()
        learner_group_fields = [i.get_fields() for i in \
                                  learner_association_groups]

        # Find Learner Association Group in which given instructor exists
        learner_group = None
        for group in learner_group_fields:
          for instructor_dict in group.get("associations").get("instructors"):
            if input_users_dict["user"] == instructor_dict["instructor"] and \
              instructor_dict["curriculum_pathway_id"] == discipline_id:
              learner_group = group
              break
        # Remove instructor from Learner Association Group
        if learner_group:
          learner_group.get("associations").get("instructors")[:] = [
            instructor for instructor in learner_group.get("associations").get(
            "instructors") if instructor.get("instructor") != input_users_dict[
            "user"] and instructor.get("curriculum_pathway_id") != discipline_id
          ]
          learner_association_group_object = AssociationGroup.find_by_uuid(
            learner_group["uuid"])
          for key, value in learner_group.items():
            setattr(learner_association_group_object, key, value)
          learner_association_group_object.update()

    else:
      # No users exist
      raise ValidationError(
          f"Discipline association group with uuid {uuid} "\
          "doesn't contain any Instructor or Assessors"
      )

    for key, value in group_fields.items():
      setattr(existing_association_group, key, value)

    existing_association_group.update()
    group_fields = existing_association_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully removed the user "\
          "from the discipline association group",
        "data": group_fields
    }

  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/discipline-association/{uuid}/user-association/status",
    response_model=UpdateDisciplineAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_discipline_association_status(
              uuid: str,
              input_association_status:UpdateDisciplineAssociationStatusModel):
  """Update status of users or associations provided in request body
  in discipline association group for uuid given in path param

  ### Args:
      uuid (str): Unique id of the association group
      request_body: Required body having user/association uuid and status
        that needs to be updated

      NOTE: Curriculum_pathway field will correspond to discipline
      and pathway will contain uuid for curriculum pathway
      having alias as discipline.

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateDisciplineAssociationGroupResponseModel: discipline association
        group Object
  """
  try:
    existing_association_group = AssociationGroup.find_by_uuid(uuid)
    group_fields = existing_association_group.get_fields()

    if not is_discipline_association_group(group_fields):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
        "is not discipline type")

    input_dict = {**input_association_status.dict()}
    for key, val in input_dict.items():
      if key == "user" and val:
        is_user_present = False
        is_user_instructor = False
        for user in group_fields["users"]:
          if val.get("user_id") == user["user"]:
            is_user_present = True
            if val.get("status") != user["status"]:
              user["status"] = val["status"]
              if user["user_type"] == "instructor":
                is_user_instructor = True
        if not is_user_present:
          raise ValidationError("User for given user_id is not present "
                                "in the discipline association group")

        # Logic to de-activate instructor in learner association group as well
        if is_user_instructor and group_fields.get("associations") and \
          val.get("status") == "inactive":
          # Get active curriculum_pathway_id from Discipline Group
          for pathway_dict in group_fields.get("associations").get(
            "curriculum_pathways"):
            if pathway_dict["status"] == "active":
              discipline_id = pathway_dict["curriculum_pathway_id"]
              break
          # Fetch all learner association groups
          learner_group_fields = get_all_learner_association_groups()

          # Find Learner Association Group in which given instructor exists
          learner_group = None
          for group in learner_group_fields:
            for instructor_dict in group.get("associations").get("instructors"):
              if val["user_id"] == instructor_dict["instructor"] and \
                instructor_dict["curriculum_pathway_id"] == discipline_id:
                learner_group = group
                break

          # De-activate instructor in Learner Association Group
          if learner_group:
            for instructor_dict in learner_group.get(
              "associations").get("instructors"):
              if instructor_dict.get("instructor") == val["user_id"] and \
                instructor_dict.get("status") != val["status"]:
                instructor_dict["status"] = val["status"]
            learner_association_group_object = AssociationGroup.find_by_uuid(
              learner_group["uuid"])
            for k, value in learner_group.items():
              setattr(learner_association_group_object, k, value)
            learner_association_group_object.update()

      if key == "curriculum_pathway" and val:
        is_pathway_present = False
        for pathway in group_fields["associations"]["curriculum_pathways"]:
          if val.get("curriculum_pathway_id") == \
              pathway["curriculum_pathway_id"]:
            is_pathway_present = True
            if val.get("status") != pathway["status"]:
              pathway["status"] = val["status"]

            # Logic to de-activate instructor in learner association group
            if val.get("status") == "inactive":
              # Fetch all learner association groups
              learner_group_fields = get_all_learner_association_groups()
              # Find Learner Association Group in which discipline to
              # de-activate exists & de-activate instructor linked to given
              # discipline
              for group in learner_group_fields:
                for instructor_dict in group.get("associations").get(
                  "instructors"):
                  if val.get("curriculum_pathway_id") == \
                    instructor_dict["curriculum_pathway_id"]:
                    instructor_dict["status"] = val["status"]
                    learner_group_object = AssociationGroup.find_by_uuid(
                      group["uuid"])
                    for k, value in group.items():
                      setattr(learner_group_object, k, value)
                    learner_group_object.update()

        if not is_pathway_present:
          raise ValidationError(
            "CurriculumPathway for given curriculum_pathway_id is not "
            "present in the discipline association group")

    for key, value in group_fields.items():
      setattr(existing_association_group, key, value)

    # Update the data
    existing_association_group.update()
    group_fields = existing_association_group.get_fields(
      reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully updated the association group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.info(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.info(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.info(traceback.print_exc())
    raise InternalServerError(str(e)) from e
