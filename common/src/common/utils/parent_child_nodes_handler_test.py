"""Unit test cases for get child and parent nodes functions"""
import pytest
import copy
from common.models import LearningObject, CurriculumPathway
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.example_objects import (PARENT_LEARNING_OBJECT,
                                            CHILD_LEARNING_OBJECTS,
                                            PARENT_CURRICULUM_PATHWAY_OBJECT,
                                            CHILD_CURRICULUM_PATHWAY_OBJECTS)
from common.testing.firestore_emulator import (clean_firestore,
                                               firestore_emulator)
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.collection_references import collection_references
from common.utils.errors import ResourceNotFoundException


@pytest.fixture(name="insert_data_to_db")
def test_insert_data_to_db():
  child_ids = []
  ids = []

  parent_lo = LearningObject.from_dict(PARENT_LEARNING_OBJECT)
  parent_lo.version = 1
  parent_lo.is_deleted = False
  parent_lo.save()
  parent_id = parent_lo.id
  parent_lo.uuid = parent_id
  parent_lo.update()

  child_lo = LearningObject()
  for each_object in CHILD_LEARNING_OBJECTS:
    lo = LearningObject.from_dict(each_object)
    lo.parent_nodes["learning_objects"] = [parent_id]
    lo.version = 1
    lo.is_deleted = False
    lo.save()
    lo.uuid = lo.id
    lo.update()
    child_lo = lo
    child_ids.append(lo.id)
    ids.append(lo.id)

  parent_lo = LearningObject.find_by_uuid(parent_id)
  parent_lo.child_nodes["learning_objects"].extend(child_ids)
  parent_lo.update()

  new_independent_lo = LearningObject.from_dict(PARENT_LEARNING_OBJECT)
  new_independent_lo.version = 1
  new_independent_lo.is_deleted = False
  new_independent_lo.save()
  new_independent_lo.uuid = new_independent_lo.id
  new_independent_lo.update()

  yield parent_lo, child_ids, child_lo, new_independent_lo
  #teardown part
  for each_id in ids:
    LearningObject.delete_by_id(each_id)

@pytest.fixture(name="insert_cirriculum_data_to_db")
def test_insert_cirriculum_data_to_db():
  child_ids = []
  ids = []

  parent_cp = CurriculumPathway.from_dict(PARENT_CURRICULUM_PATHWAY_OBJECT)
  parent_cp.version = 1
  parent_cp.is_deleted = False
  parent_cp.save()
  parent_cp_id = parent_cp.id
  parent_cp.uuid = parent_cp_id
  parent_cp.update()

  child_cp = CurriculumPathway()
  for each_object in CHILD_CURRICULUM_PATHWAY_OBJECTS:
    lo = CurriculumPathway.from_dict(each_object)
    lo.parent_nodes["learning_objects"] = [parent_cp_id]
    lo.version = 1
    lo.is_deleted = False
    lo.save()
    lo.uuid = lo.id
    lo.update()
    child_cp = lo
    child_ids.append(lo.id)
    ids.append(lo.id)

  parent_cp = CurriculumPathway.find_by_uuid(parent_cp_id)
  parent_cp.child_nodes["curriculum_pathways"].extend(child_ids)
  parent_cp.update()

  yield parent_cp, child_ids, child_cp
  #teardown part
  for each_id in ids:
    CurriculumPathway.delete_by_id(each_id)


def test_load_child_nodes_data(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  child_node_ids = insert_data_to_db[1]
  func_output = ParentChildNodesHandler.load_child_nodes_data(document_dict)
  assert func_output["uuid"] == document.uuid

  uuid_list = []
  for child_node_type in func_output["child_nodes"]:
    child_node_docs = func_output["child_nodes"][child_node_type]
    for index in range(0, len(child_node_docs)):
      uuid_list.append(
          func_output["child_nodes"][child_node_type][index]["uuid"])
  assert set(uuid_list).intersection(set(child_node_ids)) == set(child_node_ids)


def test_load_immediate_parent_nodes_data(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[2]
  document_dict = document.to_dict()
  parent_doc_id = insert_data_to_db[0].uuid
  func_output = ParentChildNodesHandler.load_immediate_parent_nodes_data(
      document_dict)
  assert func_output["uuid"] == document.uuid
  uuid_list = []
  for parent_node_type in func_output["parent_nodes"]:
    parent_node_docs = func_output["parent_nodes"][parent_node_type]
    for index in range(0, len(parent_node_docs)):
      uuid_list.append(
          func_output["parent_nodes"][parent_node_type][index]["uuid"])

  assert parent_doc_id in uuid_list


def test_get_document_from_collection(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  collection = "learning_objects"
  func_output = ParentChildNodesHandler.get_document_from_collection(
    collection, document_dict["uuid"])
  del document_dict["id"]
  del document_dict["key"]
  del document_dict["created_time"]
  del document_dict["last_modified_time"]
  del func_output["created_time"]
  del func_output["last_modified_time"]
  assert func_output == document_dict

def test_get_child_node_count(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  child_nodes = insert_data_to_db[1]
  func_output = ParentChildNodesHandler.get_child_node_count(document)
  assert func_output == len(child_nodes)

def test_get_nodes_by_key(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  func_output = ParentChildNodesHandler.get_nodes_by_key(document_dict)
  assert func_output == document_dict["child_nodes"]

def test_get_child_nodes(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  func_output = ParentChildNodesHandler.get_child_nodes(document_dict)
  assert func_output == document_dict["child_nodes"]

def test_get_parent_nodes(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  func_output = ParentChildNodesHandler.get_parent_nodes(document_dict)
  assert func_output == document_dict["parent_nodes"]

def test_get_collection_name(clean_firestore):
  func_output = ParentChildNodesHandler.get_collection_name(LearningObject)
  assert func_output == "learning_objects"

def test_delete_child_tree(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  child_nodes = insert_data_to_db[1]
  ParentChildNodesHandler.delete_child_tree(document_dict)
  for uuid in child_nodes:
    with pytest.raises(ResourceNotFoundException):
      LearningObject.find_by_uuid(uuid)

def test_delete_tree(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document = insert_data_to_db[2]
  document_dict = document.to_dict()
  ParentChildNodesHandler.delete_tree(
                                document_dict, LearningObject)
  with pytest.raises(ResourceNotFoundException):
    LearningObject.find_by_uuid(document_dict["uuid"])

def test_update_child_references_remove_add(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  child_nodes = document = insert_data_to_db[1]

  ParentChildNodesHandler.update_child_references(
                          document_dict, LearningObject, operation="remove")
  for child_node in child_nodes:
    child_document = LearningObject.find_by_uuid(child_node)
    child_document_fields = child_document.get_fields(reformat_datetime=True)
    assert child_document_fields["parent_nodes"]["learning_objects"] == []

  ParentChildNodesHandler.update_child_references(
                            document_dict, LearningObject, operation="add")
  for child_node in child_nodes:
    child_document = LearningObject.find_by_uuid(child_node)
    child_document_fields = child_document.get_fields(reformat_datetime=True)
    assert child_document_fields["parent_nodes"]["learning_objects"] != []


def test_update_parent_references_remove_add(clean_firestore, insert_data_to_db): # pylint: disable=line-too-long
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  parent_id = document_dict["uuid"]
  document = insert_data_to_db[2]
  document_dict = document.to_dict()
  child_document_id = document_dict["uuid"]

  ParentChildNodesHandler.update_parent_references(
    document_dict, LearningObject, operation="remove")
  parent_document = LearningObject.find_by_uuid(parent_id)
  parent_document_fields = parent_document.get_fields(reformat_datetime=True)
  assert child_document_id not in parent_document_fields[
                        "child_nodes"]["learning_objects"]

  ParentChildNodesHandler.update_parent_references(
    document_dict, LearningObject, operation="add")
  parent_document = LearningObject.find_by_uuid(parent_id)
  parent_document_fields = parent_document.get_fields(reformat_datetime=True)
  assert child_document_id in parent_document_fields[
                        "child_nodes"]["learning_objects"]

def test_return_child_nodes_data(clean_firestore, insert_data_to_db):
  document = insert_data_to_db[0]
  document_dict = document.to_dict()
  func_output = ParentChildNodesHandler.return_child_nodes_data(document_dict)
  assert func_output != []

def test_compare_and_update_child_nodes_references(clean_firestore, insert_data_to_db): # pylint: disable=line-too-long
  document = insert_data_to_db[0]
  base_doc_dict = document.to_dict()
  child_nodes = insert_data_to_db[1]
  doc_dict = copy.deepcopy(base_doc_dict)
  doc_dict["child_nodes"]["learning_objects"] = [child_nodes[0]]

  ParentChildNodesHandler.compare_and_update_child_nodes_references(  # pylint: disable=line-too-long
    base_doc_dict, doc_dict, LearningObject, operation="remove")
  child_document = LearningObject.find_by_uuid(child_nodes[1])
  child_document_fields = child_document.get_fields(reformat_datetime=True)
  assert child_document_fields["parent_nodes"]["learning_objects"] == []


def test_compare_and_update_parent_nodes_references(clean_firestore, insert_data_to_db):   # pylint: disable=line-too-long
  document = insert_data_to_db[0]
  base_doc_dict = document.to_dict()
  child_document = insert_data_to_db[2]
  child_document_dict = child_document.to_dict()
  doc_dict = copy.deepcopy(child_document_dict)
  doc_dict["parent_nodes"]["learning_objects"] = []

  ParentChildNodesHandler.compare_and_update_parent_nodes_references( # pylint: disable=line-too-long
    child_document_dict, doc_dict, LearningObject, operation="remove")
  parent_document = LearningObject.find_by_uuid(base_doc_dict["uuid"])
  parent_document_fields = parent_document.get_fields(
                                  reformat_datetime=True)
  assert child_document_dict["uuid"] not in parent_document_fields[
    "child_nodes"]["learning_objects"]

def test_load_nodes_data(clean_firestore, insert_cirriculum_data_to_db):
  document = insert_cirriculum_data_to_db[0]
  base_doc_dict = document.to_dict()
  learner_profile = None
  expansion_map = ["child_nodes"]
  expansion_list = []
  func_output = ParentChildNodesHandler.load_nodes_data(base_doc_dict,
                "curriculum_pathways", learner_profile, expansion_map,
                expansion_list)
  assert func_output != {}

