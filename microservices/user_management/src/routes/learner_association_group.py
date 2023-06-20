""" Learner Association Group endpoints """
import traceback
from fastapi import APIRouter, Query
from typing import Optional
from traceback import print_exc
from common.models import AssociationGroup, User, CurriculumPathway
from common.utils.logging_handler import Logger
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 ConflictError)
from common.utils.http_exceptions import (Conflict, InternalServerError,
                                          BadRequest, ResourceNotFound)
from schemas.learner_association_group_schema import (
  GetLearnerAssociationGroupResponseModel, LearnerAssociationGroupModel,
  PostLearnerAssociationGroupResponseModel, DeleteLearnerAssociationGroup,
  UpdateLearnerAssociationGroupResponseModel, AddUsersModel, RemoveUserModel,
  AllAssociationGroupResponseModel, UpdateLearnerAssociationGroupModel,
  AddCoachesModel, RemoveCoachModel, UpdateLearnerAssociationStatusModel,
  AddUserToAssociationGroupResponseModel,
  RemoveUserFromAssociationGroupResponseModel,
  AddInstructorToLearnerAssociationGroup,
  AddInstructorToLearnerAssociationGroupResponseModel,
  RemoveInstructorFromLearnerAssociationGroup,
  RemoveInstructorFromLearnerAssociationGroupResponseModel,
  GetAllLearnerForCoachORInstructor)
from schemas.error_schema import (NotFoundErrorResponseModel,
                                ConflictResponseModel)
from services.association_group_handler import (load_learner_group_field_data,
                                        is_learner_association_group,
                                        check_instructor_discipline_association)
from services.helper import (get_all_discipline_for_given_program,
                             get_all_assign_user_for_given_instructor_or_coach)
from config import ERROR_RESPONSES, IMMUTABLE_ASSOCIATION_GROUPS

router = APIRouter(
  tags=["Learner Association Group"],
  prefix="/association-groups",
  responses=ERROR_RESPONSES)


@router.get("/learner-associations",
            response_model=AllAssociationGroupResponseModel,
            name="Get All Learner Association Groups")
def get_learner_association_groups(
                          skip: int = Query(0, ge=0, le=2000),
                          limit: int = Query(10, ge=1, le=100),
                          fetch_tree: Optional[bool] = False):
  """The get association groups endpoint will return an array of learner
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
                                                   "learner")

    learner_groups= collection_manager.fetch()
    for idx, _ in enumerate(learner_groups):
      count = idx + 1

    groups = collection_manager.order("-created_time").offset(skip).fetch(limit)

    if fetch_tree:
      association_groups = []
      for group in groups:
        association_group = group.get_fields(reformat_datetime=True)
        group_details = load_learner_group_field_data(association_group)
        association_groups.append(group_details)
    else:
      association_groups = [i.get_fields(reformat_datetime=True) for i \
                          in groups]

    response = {"records": association_groups, "total_count": count}

    return {
        "success": True,
        "message": "Successfully fetched the association groups",
        "data": response
    }
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.get(
    "/learner-association/{uuid}",
    response_model=GetLearnerAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def get_learner_association_group(uuid: str,
                                  fetch_tree: Optional[bool] = False):
  """The get learner association group endpoint will return the association
  group of learner type from firestore of which uuid is provided

  ### Args:
      uuid (str): Unique identifier for association group

  ### Raises:
      ResourceNotFoundException: If the association group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      GetLearnerAssociationGroupResponseModel: association group Object
  """
  try:
    association_group = AssociationGroup.find_by_uuid(uuid)
    association_group = association_group.get_fields(reformat_datetime=True)

    if not is_learner_association_group(association_group):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not learner type")

    if fetch_tree:
      association_group = load_learner_group_field_data(association_group)

    return {
        "success": True,
        "message": "Successfully fetched the association group",
        "data": association_group
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/learner-association",
    response_model=PostLearnerAssociationGroupResponseModel,
    responses={409: {
        "model": ConflictResponseModel
    }})
def create_learner_association_group(
    input_association_group: LearnerAssociationGroupModel):
  """The create learner association group endpoint will add a new association
  group of learner type to firestore as per details given in request body

  ### Args:
      input_association_group (LearnerAssociationGroupModel): input association
                                                    group to be inserted

  ### Raises:
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      PostLearnerAssociationGroupResponseModel: Association Group Object
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

    # FIXME: Need to remove this dependency
    curriculum_pathway = CurriculumPathway.find_active_pathway("program")

    learner_associations = {
        "coaches": [],
        "instructors": [],
        "curriculum_pathway_id": curriculum_pathway.uuid \
          if curriculum_pathway else ""
    }

    input_association_group_dict = {**input_association_group.dict()}
    input_association_group_dict["association_type"] = "learner"
    input_association_group_dict["associations"] = learner_associations

    new_group = AssociationGroup()
    new_group = new_group.from_dict(input_association_group_dict)
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
    raise Conflict(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/learner-association/{uuid}",
    response_model=UpdateLearnerAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }, 409: {
        "model": ConflictResponseModel
    }})
def update_learner_association_group(
                  uuid: str,
                  input_association_group: UpdateLearnerAssociationGroupModel):
  """Update an association group of learner type with the uuid passed in the
    request body

  ### Args:
      input_group (GroupModel): Required body of the association group

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateGroupResponseModel: association group Object
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

    if is_learner_association_group(group_fields):
      for key, value in input_group_dict.items():
        group_fields[key] = value
      for key, value in group_fields.items():
        setattr(existing_association_group, key, value)

      existing_association_group.update()
      group_fields = existing_association_group.get_fields(
          reformat_datetime=True)

    else:
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not learner type")

    return {
        "success": True,
        "message": "Successfully updated the association group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ConflictError as e:
    raise Conflict(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.delete(
    "/learner-association/{uuid}",
    response_model=DeleteLearnerAssociationGroup,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def delete_learner_association_group(uuid: str):
  """Delete an association group of learner type with the given uuid
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
    group_fields = association_group.get_fields()

    if is_learner_association_group(group_fields):
      AssociationGroup.collection.delete(association_group.key)

    else:
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not learner type")

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
    "/learner-association/{uuid}/users/add",
    response_model=AddUserToAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def add_user_to_learner_association_group(uuid: str,
                                          input_users: AddUsersModel):
  """Add user to the learner association group with
  the uuid passed in the request body

  ### Args:
      input_users: Required body to the add users in
      the learner association group with the status field
      NOTE: A user can be part of only
      # one learner association group at a time

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AddUserToAssociationGroupResponseModel: learner
      association group Object
  """
  try:
    existing_association_group = AssociationGroup.find_by_uuid(uuid)

    input_users_dict = {**input_users.dict()}
    group_fields = existing_association_group.get_fields()

    # Checking the given UUID if of learner type or not
    if not is_learner_association_group(group_fields):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not learner type")

    if not isinstance(group_fields.get("users"), list):
      group_fields["users"] = []

    learner_association_groups = AssociationGroup.collection.filter(
        "association_type", "==", "learner").fetch()

    learner_association_groups = [i.get_fields(reformat_datetime=True) for i \
                          in learner_association_groups]

    for input_user in input_users_dict.get("users"):

      # Checking wheather given user is of type learner or not
      learner = User.find_by_user_id(input_user)

      learner_fields = learner.get_fields(reformat_datetime=True)
      if learner_fields["user_type"] != "learner":
        raise ValidationError(
          f"User for given user_id {input_user} is not of learner type")

      # TODO: A user can be part of only
      # one learner association group at a time
      if any(input_user == user_dict.get("user","")
             for learner_association_group in learner_association_groups
             for user_dict in learner_association_group["users"]):
        raise ValidationError("A user can be part of only one learner "\
          "association group at a time")

      # FIXME: To add validation wheather that user belongs
      # to leaner user-group or not

      # Only insert the User if its not exist in the learner association group
      if not any(
          users["user"] == input_user for users in group_fields["users"]):
        group_fields["users"].append({
            "user": input_user,
            "status": input_users_dict.get("status")
        })

    for key, value in group_fields.items():
      setattr(existing_association_group, key, value)

    # Update the data once all the incoming users validate
    existing_association_group.update()
    group_fields = existing_association_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully added the users "\
          "to the learner association group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise BadRequest(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e


@router.post(
    "/learner-association/{uuid}/user/remove",
    response_model=RemoveUserFromAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def remove_user_from_learner_association_group(uuid: str,
                                               input_user: RemoveUserModel):
  """Remove user from the learner association
  group with the uuid passed in the request body

  ### Args:
      input_user: UUID of the user that need to
      remove from the learner association group

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      RemoveUserFromAssociationGroupResponseModel: learner
      association group Object
  """
  try:
    existing_association_group = AssociationGroup.find_by_uuid(uuid)

    input_users_dict = {**input_user.dict()}
    group_fields = existing_association_group.get_fields()

    # Checking the given UUID if of learner type or not
    if not is_learner_association_group(group_fields):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not learner type")

    # Check if given user_id exists in given learner association group or not
    user_exists =  False
    for user_dict in group_fields.get("users"):
      if user_dict["user"] == input_users_dict["user"]:
        user_exists = True
        break

    if user_exists:
      # The filter returns an iterator containing all the users
      group_fields["users"][:] = filter(
          lambda x: x["user"] != input_users_dict["user"],
          group_fields.get("users"))
    else:
      input_user_id = input_users_dict["user"]
      raise ValidationError(f"The given user_id {input_user_id} does not " + \
              f"exist in the Learner Association Group for given uuid {uuid}")

    for key, value in group_fields.items():
      setattr(existing_association_group, key, value)

    # Update the data once all the incoming users validate
    existing_association_group.update()
    group_fields = existing_association_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully removed the user "\
          "from the learner association group",
        "data": group_fields
    }

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/learner-association/{uuid}/coaches/add",
    response_model=AddUserToAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def add_coach_to_learner_association_group(uuid: str,
                                           input_coaches: AddCoachesModel):
  """Add the coach to the learner association group
  with the uuid passed in the request body

  ### Args:
      input_coaches: Required body to the add coaches in the learner
      association group with the status field
      NOTE: Currently we are accepting only single user_id in the coaches array


  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      AddUserToAssociationGroupResponseModel: learner
      association group Object
  """
  try:

    input_coaches_dict = {**input_coaches.dict()}

    # TODO: Currently single coach can be associated
    # to the Learner Association Group

    if len(input_coaches_dict.get("coaches")) > 1:
      raise ValidationError(
        "Only one coach can be associated with the "\
          "Learner Association Group"
      )

    existing_association_group = AssociationGroup.find_by_uuid(uuid)

    group_fields = existing_association_group.get_fields()

    if group_fields.get("association_type") != "learner":
      raise ValidationError(
          f"AssociationGroup for given uuid: {uuid} is not learner type")

    if not isinstance(group_fields["associations"]["coaches"], list):
      group_fields["associations"]["coaches"] = []

    # FIXME: currently we are allowing to add one
    # coach to the learner association group

    if len(group_fields["associations"]["coaches"])>=1 and \
    len(input_coaches_dict.get("coaches"))>0 and \
    input_coaches_dict.get("coaches")[0] == \
    group_fields["associations"]["coaches"][0]["coach"]:
      raise ValidationError(
        f"Leaner association group with uuid {uuid} "\
          "already contains the given coach")

    if len(group_fields["associations"]["coaches"]) == 1:
      raise ValidationError(
        f"Leaner association group with uuid {uuid} "\
          "already contains coach"
      )

    for input_coach in input_coaches_dict.get("coaches"):

      # checking if given coach id is valid and has user_type as coach
      user = User.find_by_user_id(input_coach)

      coach_fields = user.get_fields(reformat_datetime=True)

      if coach_fields["user_type"] != "coach":
        raise ValidationError(
          f"User for given user_id {input_coach} is not of coach type")

      # FIXME: To add validation wheather that user belongs
      # to coach user-group or not

      # any function return True if condition satisfy
      if not any(coaches["coach"] == input_coach
                 for coaches in group_fields["associations"]["coaches"]):
        group_fields["associations"]["coaches"].append({
            "coach": input_coach,
            "status": input_coaches_dict.get("status")
        })

    for key, value in group_fields.items():
      setattr(existing_association_group, key, value)

    # Update the data once all the incoming users validate
    existing_association_group.update()
    group_fields = existing_association_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully added the coaches "\
          "to the learner association group",
        "data": group_fields
    }

  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post(
    "/learner-association/{uuid}/coach/remove",
    response_model=RemoveUserFromAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def remove_coach_from_learner_association_group(uuid: str,
                                                input_coach: RemoveCoachModel):
  """Remove the coach from the learner association group with the uuid
  passed in the request body

  ### Args:
      input_coach: UUID of the coach that need to remove from the learner
      association group

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      RemoveUserFromAssociationGroupResponseModel: learner
      association group Object
  """
  try:
    existing_association_group = AssociationGroup.find_by_uuid(uuid)

    input_coach_dict = {**input_coach.dict()}
    group_fields = existing_association_group.get_fields()

    if not is_learner_association_group(group_fields):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not learner type")

    # Check if given coach exists in given learner association group or not
    coach_exists =  False
    for coach_dict in group_fields.get("associations").get("coaches"):
      if coach_dict["coach"] == input_coach_dict["coach"]:
        coach_exists = True
        break

    if coach_exists:
      # The filter returns an iterator containing all the users
      group_fields["associations"]["coaches"][:] = filter(
          lambda x: x["coach"] != input_coach_dict["coach"],
          group_fields["associations"]["coaches"])
    else:
      input_coach_id = input_coach_dict["coach"]
      raise ValidationError(f"The given coach_id {input_coach_id} does not " + \
              f"exist in the Learner Association Group for given uuid {uuid}")

    for key, value in group_fields.items():
      setattr(existing_association_group, key, value)

    # Update the data once all the incoming users validate
    existing_association_group.update()
    group_fields = existing_association_group.get_fields(reformat_datetime=True)

    return {
        "success": True,
        "message": "Successfully removed the coach "\
        "from the learner association group",
        "data": group_fields
    }

  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.put(
    "/learner-association/{uuid}/user-association/status",
    response_model=UpdateLearnerAssociationGroupResponseModel,
    responses={404: {
        "model": NotFoundErrorResponseModel
    }})
def update_learner_association_status(
                  uuid: str,
                  input_association_status:UpdateLearnerAssociationStatusModel):
  """Update status of users or associations provided in request body
  in learner association group for uuid given as path param.

  ### Args:
      uuid (str): Unique id of the association group
      request_body: Required body having user/association uuid and status
        that needs to be updated

      NOTE: User field will contain user_id for learner type of users only.

  ### Raises:
      ResourceNotFoundException: If the group does not exist
      Exception: 500 Internal Server Error if something went wrong

  ### Returns:
      UpdateLearnerAssociationGroupResponseModel: learner association group
        Object
  """
  try:
    existing_association_group = AssociationGroup.find_by_uuid(uuid)
    group_fields = existing_association_group.get_fields()

    if not is_learner_association_group(group_fields):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
        "is not learner type")

    input_dict = {**input_association_status.dict()}
    for key, val in input_dict.items():
      if key == "user" and val:
        is_user_present = False
        for user in group_fields.get("users"):
          if val.get("user_id") == user.get("user"):
            is_user_present = True
            if val.get("status") != user.get("status"):
              user["status"] = val["status"]
        if not is_user_present:
          raise ValidationError("User for given user_id is not present "
                                "in the learner association group")

      if key == "coach" and val:
        is_coach_present = False
        for coach in group_fields.get("associations").get("coaches"):
          if val.get("coach_id") == coach.get("coach"):
            is_coach_present = True
            if val.get("status") != coach.get("status"):
              coach["status"] = val["status"]

        if not is_coach_present:
          raise ValidationError("Coach for given coach_id is not present "
                                "in the learner association group")

      if key == "instructor" and val:
        is_instructor_present = False
        for instructor in group_fields.get("associations").get("instructors"):
          if val.get("instructor_id") == instructor.get("instructor"):
            is_instructor_present = True
            if val.get("status") == "active":
              # Fetch all discipline association groups
              discipline_groups = AssociationGroup.collection.filter(
                            "association_type", "==", "discipline").fetch()
              discipline_group_fields = [i.get_fields() for i in \
                                         discipline_groups]
              if check_instructor_discipline_association(val["instructor_id"],
                                                val["curriculum_pathway_id"],
                                                discipline_group_fields):
                instructor["status"] = val["status"]
              else:
                instructor_id = val["instructor_id"]
                curriculum_pathway_id = val["curriculum_pathway_id"]
                raise ValidationError("Instructor for given instructor_id " +
                  f"{instructor_id} is not actively associated with the " +
                  f"given curriculum_pathway_id {curriculum_pathway_id} in " +
                  "discipline association group")
            else:
              if val.get("status") != instructor.get("status"):
                instructor["status"] = val["status"]

        if not is_instructor_present:
          raise ValidationError("Instructor for given instructor_id is not "
                                "present in the learner association group")

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
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except Exception as e:
    raise InternalServerError(str(e)) from e


@router.post("/learner-association/{uuid}/instructors/add",
             response_model=AddInstructorToLearnerAssociationGroupResponseModel,
             responses={404: {"model": NotFoundErrorResponseModel}})
def add_instructors(uuid: str,
                    input_data: AddInstructorToLearnerAssociationGroup) -> dict:
  """
  Endpoint to add instructor to learner association group

  Parameters
  ----------
  uuid: str
  input_data: PydanticModel

  Returns
  -------
  AddInstructorToLearnerAssociationGroupResponseModel: dict

  Raise:
  -----
  404: raise Resource Not Found Error
  400: raise Bad Request Error
  500: raise Internal Server Error
  """
  try:
    data = {**input_data.dict()}
    association_group = AssociationGroup.find_by_uuid(uuid=uuid)
    group_fields = association_group.get_fields(reformat_datetime=True)


    # validating given UUID is learner type
    if not is_learner_association_group(
      association_group_fields=group_fields):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not learner type")

    if len(data["instructors"]) > 1:
      raise ValidationError("Only one instructor can be assigned to a "
                            "discipline/curriculum pathway in a learner "
                            "association group")

    # adding the validation for the instructor discipline
    disciplines = []
    disciplines = get_all_discipline_for_given_program(
      association_group.associations["curriculum_pathway_id"],disciplines)

    if data["curriculum_pathway_id"] not in disciplines:
      discipline_id = data["curriculum_pathway_id"]
      program_id = association_group.associations["curriculum_pathway_id"]
      raise ValidationError(f"The given curriculum_pathway_id {discipline_id} "\
                            f"doesn't belong to the program {program_id} "\
                              "tagged to the learner association group")

    users = [i for i in data["instructors"] if User.find_by_user_id(
      i).user_type != "instructor"]

    # validating User Type as instructor
    if len(users) > 0:
      raise ValidationError(f"The following list of users are not instructors "
                            f"{users}")

    # validating the curriculum pathway id
    CurriculumPathway.find_by_uuid(uuid=data["curriculum_pathway_id"])

    instructor_list = [{"instructor": i, "curriculum_pathway_id": data[
      "curriculum_pathway_id"], "status": data["status"]} for i in data[
      "instructors"]]
    # The condition is true when the instructor list is not empty
    if "instructors" in association_group.associations.keys():

      # Finding index of the existing curriculum pathway instructor
      instructors = [i for i, _ in enumerate(association_group.associations[
                    "instructors"]) if _["curriculum_pathway_id"] ==
                     data["curriculum_pathway_id"]]

      # condition true when the index is found
      if instructors:
        raise ValidationError("Only one instructor can be associated with "
                              "the Learner Association Group")
      else:
        association_group.associations["instructors"].extend(instructor_list)
    else:
      association_group.associations["instructors"] = instructor_list

    # Logic to check if given instructors are actively associated to the
    # curriculum_pathway in Discipline Association Groups

    # Fetch all discipline association groups
    discipline_groups = AssociationGroup.collection.filter(
                  "association_type", "==", "discipline").fetch()
    discipline_group_fields = [i.get_fields() for i in \
                               discipline_groups]

    # Identify instructors given in request body that are not associated to
    # given curriculum_pathway_id in Discipline Association Groups
    non_associated_instructors = []
    for instructor_dict in instructor_list:
      if not check_instructor_discipline_association(
                                              instructor_dict["instructor"],
                                              data["curriculum_pathway_id"],
                                              discipline_group_fields):
        non_associated_instructors.append(instructor_dict["instructor"])

    if non_associated_instructors:
      curriculum_pathway_id = data["curriculum_pathway_id"]
      raise ValidationError("Instructors for given instructor_ids " +
        f"{non_associated_instructors} are not actively associated with the " +
        f"given curriculum_pathway_id {curriculum_pathway_id} in " +
        "discipline association group")

    association_group.update()
    group_fields = association_group.get_fields(reformat_datetime=True)

    Logger.info(f"Successfully the list of instructors {data['instructors']} "
                f"are added in the Learning Association Group")
    return {
      "success": True,
      "message": "Successfully added the instructors to the learner "
                 "association group",
      "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(f"Add Instructor Resource Not Found Error Occurred: {e}")
    Logger.error(print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(f"Add Instructor Validation Error Occurred: {e}")
    Logger.error(print_exc())
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    Logger.error(f"Add Instructor Internal Server Error Occurred: {e}")
    Logger.error(print_exc())
    raise InternalServerError(str(e)) from e


@router.post("/learner-association/{uuid}/instructor/remove",
        response_model=RemoveInstructorFromLearnerAssociationGroupResponseModel,
        responses={404: {"model": NotFoundErrorResponseModel}})
def remove_instructor(uuid: str,
                      input_data: RemoveInstructorFromLearnerAssociationGroup):
  """
  Endpoint to remove instructor from learner association group

  Parameters
  ----------
  uuid: str
  input_data: PydanticModel

  Returns
  -------
  RemoveInstructorFromLearnerAssociationGroupResponseModel: dict

  Raise:
  -----
  404: raise Resource Not Found Error
  400: raise Bad Request Error
  500: raise Internal Server Error
  """
  try:
    data = {**input_data.dict()}
    association_group = AssociationGroup.find_by_uuid(uuid=uuid)
    group_fields = association_group.get_fields(reformat_datetime=True)

    # validating given UUID is learner type
    if not is_learner_association_group(
      association_group_fields=group_fields):
      raise ValidationError(f"AssociationGroup for given uuid: {uuid} "
                            "is not learner type")

    instructors = [i for i, _ in enumerate(association_group.associations[
                  "instructors"]) if _["curriculum_pathway_id"] ==
                   data["curriculum_pathway_id"]]

    if instructors:
      idx = instructors[0]
      instructor_data = association_group.associations["instructors"]
      if data["instructor"] == instructor_data[idx]["instructor"]:
        del instructor_data[idx]
        association_group.associations["instructors"] = instructor_data
        association_group.update()
        group_fields = association_group.get_fields(reformat_datetime=True)
      else:
        raise ValidationError(f"This instructor {data['instructor']} is "
                              f"not associated with this curriculum pathway "
                              f"{data['curriculum_pathway_id']}")
    else:
      raise ValidationError(f"This curriculum pathway id"
                            f" {data['curriculum_pathway_id']} is not "
                            f"associated with any instructors")

    Logger.info(f"Successfully removed a instructor {data['instructor']} "
                f"from the Learning Association Group")
    return {
      "success": True,
      "message": "Successfully removed the instructors from the learner "
                 "association group",
      "data": group_fields
    }

  except ResourceNotFoundException as e:
    Logger.error(f"Remove Instructor Resource Not Found Error Occurred: {e}")
    Logger.error(print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(f"Remove Instructor Validation Error Occurred: {e}")
    Logger.error(print_exc())
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    Logger.error(f"Remove Instructor Internal Server Error Occurred: {e}")
    Logger.error(print_exc())
    raise InternalServerError(str(e)) from e

@router.get(
    "/learner-association/instructor/{user_id}/learners",
    response_model=GetAllLearnerForCoachORInstructor,
    responses={404: {"model": NotFoundErrorResponseModel}},
)
def get_all_the_learners_of_instructor(
    user_id: str, fetch_tree: Optional[bool] = False
):
  """
  Endpoint to get all the learners that belong to given
  instructor from all the learner association group
  Parameters
  ----------
  user_id: is the unique ID of the user having user_type instructor

  Returns: list of learner belong to given coach or
  instructor
  -------

  Raise:
  -----
  422: raise validation error
  404: raise Resource Not Found Error
  400: raise Bad Request Error
  500: raise Internal Server Error
  """
  try:
    user = User.find_by_user_id(user_id)
    if not user.user_type == "instructor":
      raise ValidationError(
        f"User for given uuid: {user_id} is not a instructor"
      )

    user_list = get_all_assign_user_for_given_instructor_or_coach(
      user_id, user.user_type
    )

    if fetch_tree:
      user_list = [User.find_by_user_id(user_id).get_fields(
        reformat_datetime=True) for user_id in user_list]

    return {
      "success": True,
      "message": "Successfully fetched the learners "\
        "for the given instructor",
      "data": user_list,
  }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(print_exc())
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    Logger.error(e)
    Logger.error(print_exc())
    raise InternalServerError(str(e)) from e


@router.get(
    "/learner-association/coach/{user_id}/learners",
    response_model=GetAllLearnerForCoachORInstructor,
    responses={404: {"model": NotFoundErrorResponseModel}},
)
def get_all_the_learners_of_coach(
    user_id: str, fetch_tree: Optional[bool] = False
):
  """
  Endpoint to get all the learner that belong to given coach
  from all the learner association group
  Parameters
  ----------
  user_id: is the unique ID of the user having user_type coach

  Returns: list of learner belong to given coach or
  instructor
  -------

  Raise:
  -----
  422: raise validation error
  404: raise Resource Not Found Error
  400: raise Bad Request Error
  500: raise Internal Server Error
  """
  try:
    user = User.find_by_user_id(user_id)
    if not user.user_type == "coach":
      raise ValidationError(
        f"User for given uuid: {user_id} is not a coach"
      )

    user_list = get_all_assign_user_for_given_instructor_or_coach(
      user_id, user.user_type
    )

    if fetch_tree:
      user_list = [User.find_by_user_id(user_id).get_fields(
        reformat_datetime=True) for user_id in user_list]

    return {
      "success": True,
      "message": "Successfully fetched the learners "\
        "for the given coach",
      "data": user_list,
  }

  except ResourceNotFoundException as e:
    Logger.error(e)
    Logger.error(print_exc())
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    Logger.error(e)
    Logger.error(print_exc())
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    Logger.error(e)
    Logger.error(print_exc())
    raise InternalServerError(str(e)) from e
