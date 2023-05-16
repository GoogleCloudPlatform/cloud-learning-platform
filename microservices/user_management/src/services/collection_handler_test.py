"""Unit Test for Rules Engine"""
import os
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from services.collection_handler import CollectionHandler
from schemas.schema_examples import BASIC_USER_MODEL_EXAMPLE, BASIC_GROUP_MODEL_EXAMPLE
from common.models import UserGroup, User
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_collection_handler(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}
  del group_dict["users"]
  del group_dict["permissions"]
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()
  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": [group.id]}
  document = CollectionHandler.loads_field_data_from_collection(user_dict)
  assert isinstance(document["user_groups"][0], dict) is True


def test_collection_handler_negative(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE}
  del group_dict["users"]
  del group_dict["permissions"]
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": [group.id]}
  assert isinstance(user_dict["user_groups"][0], dict) is False


def test_update_refs_between_models(clean_firestore):
  group_list = [{
      **BASIC_GROUP_MODEL_EXAMPLE, "users": []
  }, {
      **BASIC_GROUP_MODEL_EXAMPLE, "users": []
  }]
  group_uuids = []
  for group_dict in group_list:
    group = UserGroup.from_dict(group_dict)
    group.uuid = ""
    group.save()
    group.uuid = group.id
    group.update()
    group_uuids.append(group.uuid)

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": [group_uuids[0]]}
  user_dict["user_type_ref"] = ""
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id
  # add new user to group
  CollectionHandler.update_ref_of_document("user_groups", group_uuids[0],
                                           "users", user.id, "add")

  #update groups of a user
  validated_group_ids = CollectionHandler.update_existing_references(
      user.id, "user_groups", "users", [group_uuids[1], "random_group_id"],
      user_dict["user_groups"])
  assert validated_group_ids == [group_uuids[1]]

  #check if user is added to group
  get_assigned_group = UserGroup.find_by_uuid(group_uuids[1])
  get_assigned_group_dict = get_assigned_group.get_fields()
  assert user.id in get_assigned_group_dict.get("users", [])

  #check if user is removed from group
  get_unassigned_group = UserGroup.find_by_uuid(group_uuids[0])
  get_unassigned_group_dict = get_unassigned_group.get_fields()
  assert not user.id in get_unassigned_group_dict.get("users", [])


def test_add_in_many_to_many_relationship(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": []}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": []}
  user_dict["user_type_ref"] = ""
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id

  CollectionHandler.update_many_to_many_relations("user_groups", group.uuid,
                                                  "users", "users", [user.id],
                                                  "user_groups", True, False,
                                                  "add")

  #check if user is added to group
  get_group = UserGroup.find_by_uuid(group.uuid)
  get_group_dict = get_group.get_fields()
  assert user.id in get_group_dict.get("users", [])

  #check if group is assigned to user
  get_user = User.find_by_uuid(user.id)
  get_user_dict = get_user.get_fields()
  assert group.uuid in get_user_dict.get("user_groups", [])


def test_remove_in_many_to_many_relationship(clean_firestore):
  group_dict = {**BASIC_GROUP_MODEL_EXAMPLE, "users": []}
  group = UserGroup.from_dict(group_dict)
  group.uuid = ""
  group.save()
  group.uuid = group.id
  group.update()

  user_dict = {**BASIC_USER_MODEL_EXAMPLE, "user_groups": [group.uuid]}
  user_dict["user_type_ref"] = ""
  user = User.from_dict(user_dict)
  user.user_id = ""
  user.save()
  user.user_id = user.id
  user.update()
  user_dict["user_id"] = user.id

  # add new user to group
  CollectionHandler.update_ref_of_document("user_groups", group.uuid, "users",
                                           user.id, "add")

  CollectionHandler.update_many_to_many_relations("user_groups", group.uuid,
                                                  "users", "users", [user.id],
                                                  "user_groups", True, False,
                                                  "remove")

  #check if user is removed from the group
  get_group = UserGroup.find_by_uuid(group.uuid)
  get_group_dict = get_group.get_fields()
  assert not user.id in get_group_dict.get("users", [])

  #check if group is unassigned from user
  get_user = User.find_by_uuid(user.id)
  get_user_dict = get_user.get_fields()
  assert not group.uuid in get_user_dict.get("user_groups", [])
