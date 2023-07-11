""" Import of the JSON file """
import json
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from json.decoder import JSONDecodeError
from common.utils.errors import ValidationError
from common.utils.config import STAFF_USERS
from common.models import User, UserGroup
from schemas.staff_schema import BasicStaffModel
from services.collection_handler import CollectionHandler
from services.staff import create_staff
from services.agent import create_agent
from services.learner import create_learner, create_learner_profile
# pylint: disable = broad-except


def add_user_to_db(headers, user_input_dict):
  '''Insert the data into the database'''
  user_type = user_input_dict.get("user_type")
  user_groups_uuids = user_input_dict.get("user_groups")
  user_groups = []
  user_group_names = []
  inspace_user_mapping = {
    "is_inspace_user": False,
    "inspace_user_id": ""
  }

  # both user_type and user_groups cannot be missing
  if user_type is None and not user_groups_uuids:
    raise ValidationError("Either user_type or user_groups is required")

  if user_groups_uuids:
    for uuid in user_groups_uuids:
      user_groups.append(UserGroup.find_by_uuid(uuid))

  # given user_groups must be immutable and of same type
  for user_group in user_groups:
    if not user_group.is_immutable:
      raise ValidationError(
        f"UserGroup with uuid {user_group.uuid} is not predefined")
    # user_type and user_group name must be same if both are present
    if user_type and user_type != user_group.name:
      raise ValidationError((f"User type {user_type} does not match with the "
      f"given User Group {user_group.name} with uuid {user_group.uuid}"))
    user_group_names.append(user_group.name)
  if len(set(user_group_names)) > 1:
    raise ValidationError("User can only belong to User Group of same type")

  if not user_type and user_groups:
    # assign user type based on user groups
    # added all the validations before using zeroth uuid in user_groups
    user_input_dict["user_type"] = user_groups[0].name

  if user_input_dict.get("user_type", "").lower() == "learner":
    # create learner and learner profile
    learner_data = {}
    learner_data["email_address"] = user_input_dict.get("email")
    learner_data["first_name"] = user_input_dict.get("first_name")
    learner_data["last_name"] = user_input_dict.get("last_name")
    learner_id = create_learner(headers, learner_data)
    create_learner_profile(headers, learner_id)
    user_input_dict["user_type_ref"] = learner_id

  elif user_input_dict.get("user_type", "").lower() in STAFF_USERS:
    staff_data = {}
    staff_data["email"] = user_input_dict.get("email")
    staff_data["first_name"] = user_input_dict.get("first_name")
    staff_data["last_name"] = user_input_dict.get("last_name")
    staff_fields = create_staff(BasicStaffModel(**staff_data))
    user_input_dict["user_type_ref"] = staff_fields["uuid"]

  else:
    user_input_dict["user_type_ref"] = ""

  # check if inspace user should be created and update mapping accordingly
  allowed_inspace_user_types = ["learner"]
  allowed_inspace_user_types.extend(STAFF_USERS)

  if user_input_dict.get("create_inspace_user") is True and \
    user_input_dict["user_type"] in allowed_inspace_user_types:
    inspace_user_mapping["is_inspace_user"] = True

  # create user
  user_dict = User.from_dict({**user_input_dict, "user_groups": []})
  user_dict.user_id = ""
  user_dict.inspace_user = inspace_user_mapping
  user_dict.save()
  user_dict.user_id = user_dict.id
  user_dict.update()
  user_id = user_dict.user_id
  user_groups = []
  input_group_list = user_input_dict.get("user_groups", [])
  if input_group_list and len(input_group_list) > 0:
    for group in input_group_list:
      if not group in user_groups:
        CollectionHandler.update_ref_of_document("user_groups", group,
                                                  "users", user_id, "add")
        user_groups.append(group)
        user_dict.user_groups = user_groups
        user_dict.update()
  # create agent for the user
  agent_dict = {
      "account_homepage": "",
      "object_type": "agent",
      "name": user_input_dict.get("first_name") + " " +
              user_input_dict.get("last_name"),
      "user_id": user_id
  }
  create_agent(headers, agent_dict)
  return user_id


def add_data_to_db(content, new_content_obj):
  '''Insert the data into the database'''
  new_content_obj = new_content_obj.from_dict(content)
  new_content_obj.uuid = ""
  new_content_obj.save()
  new_content_obj.uuid = new_content_obj.id
  new_content_obj.update()
  new_content_uuid = new_content_obj.uuid
  return new_content_uuid


def json_import_non_user(json_file, json_schema, model_obj, object_name):
  """Importing a json file and validating the schema before
     inserting the data into the database"""
  try:
    if not json_file.filename.endswith(".json"):
      raise ValidationError("Valid JSON file type is supported")
    else:
      contents = json.load(json_file.file)
      inserted_data = []

      # Validating the JSON schema of each obj in the input JSON file
      # before inserting the data into the database
      if isinstance(contents, list):
        for content in contents:
          json_schema(**content)
      else:
        json_schema(**contents)

      if isinstance(contents, list):
        for content in contents:
          new_content_obj = model_obj()
          new_content_uuid = add_data_to_db(content, new_content_obj)
          inserted_data.append(new_content_uuid)
      else:
        new_content_obj = model_obj()
        new_content_uuid = add_data_to_db(contents, new_content_obj)
        inserted_data.append(new_content_uuid)
      return {
          "success": True,
          "message": f"Successfully created the {object_name}",
          "data": inserted_data
      }

  except JSONDecodeError as e:
    raise ValidationError("Provided JSON is invalid") from e

  except PydanticValidationError as err:
    error_res = json.loads(err.json())
    req_fields = [i["loc"][-1] for i in error_res]
    req_fields_str = "Missing required fields - "+ \
        ",".join("'"+i+"'" for i in req_fields)
    raise ValidationError(req_fields_str, data=error_res) from err

  except Exception as err:
    raise err


def json_import(token, json_file, json_schema, object_name):
  """Importing a json file and validating the schema before
     inserting the data into the database"""
  try:
    if not json_file.filename.endswith(".json"):
      raise ValidationError("Valid JSON file type is supported")
    else:
      contents = json.load(json_file.file)
      inserted_data = []

      # Validating the JSON schema of each obj in the input JSON file
      # before inserting the data into the database
      if isinstance(contents, list):
        for content in contents:
          json_schema(**content)
      else:
        json_schema(**contents)

      if isinstance(contents, list):
        for content in contents:
          new_content_uuid = add_user_to_db(token, content)
          inserted_data.append(new_content_uuid)
      else:
        new_content_uuid = add_user_to_db(token, contents)
        inserted_data.append(new_content_uuid)
      return {
          "success": True,
          "message": f"Successfully created the {object_name}",
          "data": inserted_data
      }

  except JSONDecodeError as e:
    raise ValidationError("Provided JSON is invalid") from e

  except PydanticValidationError as err:
    error_res = json.loads(err.json())
    req_fields = [i["loc"][-1] for i in error_res]
    req_fields_str = "Missing required fields - "+ \
        ",".join("'"+i+"'" for i in req_fields)
    raise ValidationError(req_fields_str, data=error_res) from err

  except Exception as err:
    raise err
