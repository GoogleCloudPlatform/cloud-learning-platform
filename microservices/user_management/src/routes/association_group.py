"""Association Group endpoints """
from traceback import print_exc
from fastapi import APIRouter, Query
from typing import Optional
from common.models import AssociationGroup, CurriculumPathway, User
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError)
from common.utils.http_exceptions import (InternalServerError, Conflict,
                                          BadRequest, ResourceNotFound)
from schemas.association_group_schema import (
                  GetAllAssociationGroupResponseModel,
                  GetAssociationGroupResponseModel,
                  ImmutableAssociationGroupModel,
                  PostImmutableAssociationGroupResponseModel,
                  AutoUpdateAllAssociationGroupDisciplines,
                  AutoUpdateAllAssociationGroupsResponseModel,
                  UserTypeResponseModel)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                  ConflictResponseModel)
from config import ERROR_RESPONSES


router = APIRouter(
  tags=["Association Group"],
  prefix="/association-groups",
  responses=ERROR_RESPONSES)

@router.get("",
            response_model=GetAllAssociationGroupResponseModel,
            name="Get All Association Groups")
def get_association_groups(
                          skip: int = Query(0, ge=0, le=2000),
                          limit: int = Query(10, ge=1, le=100),
                          association_type: Optional[str] = None):
  """The get association groups endpoint will return an array of
  association groups from firestore

  ### Args:
      skip (int): Number of objects to be skipped
      limit (int): Size of group array to be returned
      association_type (str): To get the association type

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AllGroupResponseModel: Array of association group Object
  """
  try:
    collection_manager = AssociationGroup.collection
    if association_type:
      collection_manager = collection_manager.filter(
                              "association_type", "==", association_type)

    groups = collection_manager.order("-created_time").offset(skip).fetch(limit)

    association_groups = [i.get_fields(reformat_datetime=True) for i \
                          in groups]
    return {
        "success": True,
        "message": "Successfully fetched the association groups",
        "data": association_groups
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/search",
    response_model=GetAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def search_association_group(search_query: str,
                            skip: int = Query(0, ge=0, le=2000),
                            limit: int = Query(10, ge=1, le=100)):
  """Search association group endpoint will return the association
  group for the given search query from firestore regardless of the
  type of group

  ### Args:
      search_query(str): key to search against name and description

  ### Raises:
      ResourceNotFoundException: If the association group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetAssociationGroupResponseModel: association group Object
  """
  try:
    if len(search_query) < 1:
      raise ValidationError("search_query cannot be empty")
    filtered_association_list = []
    fetch_length = skip+limit

    association_groups = AssociationGroup.collection.order(
                          "-created_time").fetch()

    for association_group in association_groups:
      association_dict = association_group.get_fields(reformat_datetime=True)

      if search_query.lower() in association_dict["name"].lower():
        filtered_association_list.append(association_dict)

      elif search_query.lower() in association_dict["description"].lower():
        filtered_association_list.append(association_dict)

      if len(filtered_association_list) == fetch_length:
        break

    result = filtered_association_list[skip:fetch_length]

    return {
        "success": True,
        "message": "Successfully fetched the association group",
        "data": result
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/immutable",
             include_in_schema=False,
             response_model=PostImmutableAssociationGroupResponseModel,
             responses={409: {"model": ConflictResponseModel}})
def create_immutable_association_group(input_group:
                                       ImmutableAssociationGroupModel):
  """
  The create immutable association group endpoint will add the immutable
  association group in request body to the firestore

  Args:
    input_group (ImmutableAssociationGroupModel): input association group to be
                                                  inserted

  Raises:
    Exception: 500 Internal Server Error if something went wrong

  Returns:
    PostImmutableAssociationGroupResponseModel: Association Group Object
  """
  try:
    existing_group = AssociationGroup.find_by_name(input_group.name)
    if existing_group is not None:
      raise ConflictError((f"AssociationGroup with the given name: "
                           f"{input_group.name} already exists"))
    input_group_dict = {**input_group.dict(), "is_immutable": True}
    if "discipline" in input_group_dict["name"].lower():
      input_group_dict["association_type"] = "discipline"
    elif "learner" in input_group_dict["name"].lower():
      input_group_dict["association_type"] = "learner"
    new_group = AssociationGroup()
    new_group = new_group.from_dict({**input_group_dict})
    new_group.uuid = ""
    new_group.save()
    new_group.uuid = new_group.id
    new_group.update()
    group_fields = new_group.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the association group",
        "data": group_fields
    }
  except ConflictError as e:
    Logger.error(e)
    Logger.error(print_exc())
    raise Conflict(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(print_exc())
    raise InternalServerError(str(e)) from e


@router.put(
    "/active-curriculum-pathway/update-all",
    response_model=AutoUpdateAllAssociationGroupsResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_disciplines_with_active_pathway(
                nodes: AutoUpdateAllAssociationGroupDisciplines):
  """Update curriculum_pathway_id across all association groups

  ### Args:
      nodes: List of nodes of alias type

  ### Raises:
      ResourceNotFoundException: If the pathway does not exists
      ValidationError: If the pathway does not have alias as program
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      updated_groups: List of Association Groups that have been updated
        Object
  """
  try:
    nodes = {**nodes.dict()}
    program_id = nodes["program_id"]
    nodes = nodes.get("disciplines", [])
    program = CurriculumPathway.find_by_uuid(program_id)

    if not program.is_active:
      raise ValidationError("Input program_id is not active")
    if program.alias != "program":
      raise ValidationError(f"Input pathway has alias as {program.alias} "
                            "instead of program")

    # Update All Learner Association Groups
    association_groups = AssociationGroup.collection.filter(
      "association_type", "==", "learner").fetch()
    update_groups = []
    for group in association_groups:
      associations = group.associations
      associations["curriculum_pathway_id"] = program_id
      # Update Instructor and Discipline Associations in Learner Group
      for i, instructor_data in enumerate(associations["instructors"]):
        old_discipline = CurriculumPathway.find_by_uuid(
          instructor_data["curriculum_pathway_id"])
        for node in nodes:
          if old_discipline.name == node["name"]:
            associations["instructors"][i][
              "curriculum_pathway_id"] = node["uuid"]
      group.associations = associations
      group.update()
      update_groups.append(group.id)

    # Update all discipline Association Groups
    association_groups = AssociationGroup.collection.filter(
      "association_type", "==", "discipline").fetch()

    new_associations = [{"curriculum_pathway_id": node["uuid"],
                         "status": "active"} for node in nodes]
    new_associations = {"curriculum_pathways": new_associations}
    for group in association_groups:
      group.associations = new_associations
      group.update()
      update_groups.append(group.id)

    return {
          "success": True,
          "message": "Successfully updated the following association groups",
          "data": update_groups
    }

  except ResourceNotFoundException as e:
    Logger.error(print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/{uuid}/addable-users", response_model=UserTypeResponseModel,
    name="Get users by user_type")
def get_users_by_usertype(user_type: str, uuid: str):
  """The endpoint returns a list of users for the given user_type which
  are not part of given association group.

  ### Args:
    user_type(str) : user type of user
    association_group_id(str) : association group id

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      Array of users
  """
  try:
    user_collections = User.collection.filter(
      "user_type", "==", user_type).filter(
      "is_deleted", "==", False).fetch()
    users = [i.get_fields(reformat_datetime=True) for i \
                          in user_collections]

    existing_association_group = AssociationGroup.find_by_uuid(
                                  uuid)
    group_fields = existing_association_group.get_fields()

    existing_users = []

    if group_fields["association_type"] == "learner":
      if user_type == "learner":
        existing_users = [i["user"] for i in group_fields["users"]]
      if user_type == "coach":
        existing_users = [i["coach"] for i in \
                          group_fields["associations"]["coaches"]]
      if user_type == "instructor":
        existing_users = [i["instructor"] for i in \
                          group_fields["associations"]["instructors"]]
    elif group_fields["association_type"] == "discipline":
      if user_type in ["assessor","instructor"]:
        existing_users = [i["user"] for i in group_fields["users"] if \
                          i["user_type"] == user_type]
    users = [user for user in users if user["user_id"] not in existing_users]

    if user_type == "learner":
      learner_association_groups = AssociationGroup.collection.filter(
                                    "association_type", "==","learner").fetch()
      learner_associations = [i.get_fields(reformat_datetime=True) for i \
                          in learner_association_groups]
      existing_learners = []
      for learners in learner_associations:
        if learners["users"] is not None:
          for i in learners["users"]:
            existing_learners.append(i["user"])

      users = [user for user in users if \
               user["user_id"] not in existing_learners]

    return {
        "success": True,
        "message": "Successfully fetched users",
        "data": users
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e
