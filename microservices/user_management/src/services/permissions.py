""" create and get permissions """
from typing import Optional
from typing_extensions import Literal
from common.models import Permission
from common.utils.errors import ValidationError
from services.collection_handler import CollectionHandler

# pylint: disable=invalid-name
def check_and_create_permission(data, module_name, application_name):
  """Creates if permission with same name exist and
    creates permission if there is no conflict"""
  permission_exists = None
  if data.get("name"):
    permission_exists = Permission.find_by_name(data["name"])
    permission_uuid = permission_exists.get_fields().get("uuid")
  if not permission_exists:
    permission_name = f"{module_name}.\
        {CollectionHandler.get_document(data['action_id'],'actions','name')}"

    if data["application_id"]:
      permission_name = application_name + "." + permission_name
    permission_exists = Permission.find_by_name(permission_name)
    if permission_exists:
      permission_uuid = permission_exists.get_fields().get("uuid")
    else:
      data["name"] = permission_name
      new_permission = Permission()
      new_permission = new_permission.from_dict(data)
      new_permission.uuid = ""
      new_permission.save()
      new_permission.uuid = new_permission.id
      new_permission.update()
      permission_uuid = new_permission.id
  return permission_uuid


def filter_and_update_permissions_of_applications(
    application_id,
    user_group,
    operation: Literal["add", "remove"] = "add",
    default_action: Optional[str] = None):
  """filters permissions based on application and usergroups.
     Updates usergroups field of permissions.
     Add/remove usergroup in permissions.
     Returns list of filtered permission ids."""
  collection_manager = Permission.collection
  if default_action:
    collection_manager = collection_manager.filter("application_id", "==",
                                                   application_id).filter(
                                                       "action_id", "==",
                                                       default_action).fetch()
  else:
    collection_manager = collection_manager.filter("application_id", "==",
                                                   application_id).filter(
                                                       "user_groups",
                                                       "array_contains",
                                                       user_group).fetch()
  permission_ids = []
  for permission in collection_manager:
    update_permissions_with_user_group(permission,user_group,operation)
    permission_ids.append(permission.uuid)
  return permission_ids


def create_permissions_for_application(modules, application_id,
                                       application_name):
  """Creates permissions for the application"""
  permissions = []
  default_permissions = []
  for module in modules:
    module_fields = CollectionHandler.get_document(module, "modules")
    for action in module_fields["actions"]:
      permission_data = {
          "application_id": application_id,
          "module_id": module,
          "action_id": action,
          "user_groups": []
      }
      permission_id = check_and_create_permission(permission_data,
                                                  module_fields.get("name", ""),
                                                  application_name)
      permissions.append(permission_id)
      if action in module_fields.get("default_actions", []):
        default_permissions.append(permission_id)
  return permissions, default_permissions

def get_permissions_based_on_application(application_id):
  """Function to get permissions based on application"""
  collection_manager = Permission.collection
  collection_manager = collection_manager.filter("application_id", "==",
                                                   application_id).fetch()
  user_groups =[]
  permission_ids =[]
  for permission in collection_manager:
    permission_dict = permission.get_fields()
    permission_ids.append(permission_dict.get("uuid"))
    user_groups +=permission_dict.get("user_groups")
    Permission.collection.delete(permission.key)

  user_groups = list(set(user_groups))
  permission_ids = list(set(permission_ids))
  return user_groups,permission_ids

def validate_permission_with_application(permission_id,
                                         application_id,
                                         raise_exception: bool = True):
  """Check if the permission is related to the application"""
  collection_manager = Permission.collection
  permission = collection_manager.filter("uuid", "==", \
            permission_id).filter("application_id", "==", application_id).get()
  if raise_exception and not permission:
    raise ValidationError(
        f"The permission with uuid {permission_id} " +
        f"doesn't belong to the application with uuid {application_id}")

  return permission


def update_permissions_with_user_group(permission_doc,
                                       user_group_id,
                                       operation: Literal["add",
                                                          "remove"] = "add"):
  """Add/Remove user group ref from permission"""
  permission = permission_doc.get_fields()
  user_groups = permission.get("user_groups")
  if not user_groups or not isinstance(user_groups, list):
    user_groups = []
  if operation == "add":
    if user_group_id not in user_groups:
      user_groups.append(user_group_id)
  else:
    if user_group_id in user_groups:
      user_groups.remove(user_group_id)
  setattr(permission_doc, "user_groups", user_groups)
  permission_doc.update()

def get_unique_records(list_of_dicts, keys):
  """Gives unique records with specified keys"""
  list_of_dicts = [i.get_fields(reformat_datetime=True) for i in list_of_dicts]
  distinct_records = []
  for subVal in list_of_dicts:
    key_set = set(subVal.keys()) and set(keys)
    if subVal not in distinct_records:
      distinct_records.append({key: subVal[key] for key in key_set})
  return distinct_records
