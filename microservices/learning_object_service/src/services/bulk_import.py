""" Import of the JSON file """
import copy
import json
import requests
from json.decoder import JSONDecodeError
from common.utils.logging_handler import Logger
from common.utils.collection_references import (LOS_COLLECTIONS,
                                                collection_references)
from common.utils.errors import ValidationError
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from config import ASSESSMENT_SERVICE_BASE_URL
from pydantic.error_wrappers import ValidationError as PydanticValidationError
from schemas.upload_pathway import UploadPathwayModel

# pylint: disable = global-variable-not-assigned
# creating global variable of SRL to insert its again directly
SRL_COLLECTIONS = {}
header = None

def get_all_nodes_for_project(uuid: str, level: str, nodes: list):
  """
  This method traverses the learning hierarchy from given level uuid till the
  final_alias and retrieves all the node where alias=final_alias.
  Args:
    uuid (str): uuid of the node from where to traverse.
    level (str): current level/type of the Node for given uuid.
    nodes (list): list to be used to return list of nodes
  Returns:
    nodes (list): List of nodes of alias=module and type=project
  """
  node = collection_references[level].find_by_uuid(uuid)
  if node.type == "project" and node.alias == "module":
    nodes.append(node)
    return
  child_nodes = node.child_nodes
  if child_nodes:
    for child_level in child_nodes:
      for child_uuid in child_nodes[child_level]:
        get_all_nodes_for_project(child_uuid, child_level, nodes)
  return nodes


def module_assessment_prerequisite_handler(uuid):
  """Module assessment prerequisite handler"""
  learning_object_project = get_all_nodes_for_project(uuid,
                                                      "curriculum_pathways", [])
  for learning_object in learning_object_project:
    if learning_object.child_nodes.get("assessments"):
      for assessment_id in learning_object.child_nodes.get("assessments"):
        assessment = collection_references["assessments"].find_by_uuid(
            assessment_id)
        assessment.prerequisites[
            "learning_objects"] = learning_object.prerequisites[
                "learning_objects"]
        assessment.update()


def skill_update_handler(content, new_content_obj):
  skills = new_content_obj.find_by_name(content["name"])
  skills = [skill.get_fields(reformat_datetime=True) for skill in skills]
  if len(skills) > 0:
    for i, skill in enumerate(skills):
      if skill["name"] == content["name"] and \
        skill["description"] == content["description"]:
        new_content_uuid, new_content_field = skills[i]["uuid"], skills[i]
        return new_content_uuid, new_content_field
  return None, None


def add_data_to_db_handler(content, new_content_obj, collection_name):
  """Add data to the database handler"""
  if collection_name == "assessments":
    global header
    url = ASSESSMENT_SERVICE_BASE_URL+"/assessment"
    # pylint: disable = missing-timeout, broad-exception-raised
    assessment = requests.post(url=url, json=content, headers=header)
    if assessment.status_code != 200:
      raise Exception("Post Request to Assessment service Fail with"\
                      f" status code {assessment.status_code}")
    content = assessment.json()["data"]
    new_content_obj = new_content_obj.find_by_uuid(content["uuid"])
  else:
    new_content_obj = new_content_obj.from_dict(content)
    new_content_obj.uuid = ""
    new_content_obj.save()
    new_content_obj.uuid = new_content_obj.id
    new_content_obj.is_locked = False
  if collection_name in LOS_COLLECTIONS:
    if not new_content_obj.prerequisites:
      new_content_obj.prerequisites = {}
    for prereq_level in new_content_obj.prerequisites:
      if new_content_obj.prerequisites[prereq_level]:
        new_content_obj.is_locked = True
        if new_content_obj.type == "project" and \
          new_content_obj.alias == "module":
          new_content_obj.is_locked = False
        break
    new_content_obj.root_version_uuid = new_content_obj.id
  new_content_obj.update()
  new_content_uuid = new_content_obj.uuid
  new_content_field = new_content_obj.get_fields(reformat_datetime=True)
  return new_content_uuid, new_content_field


def add_data_to_db(content, new_content_obj, collection_name):
  """
  Inserting the data into the database
  ### Args:
  content: `dict`
    The JSON object contains the data
  new_content_obj: `class object`
    fireo class object which is used to inject data in
    firestore
  ### Returns:
  new_content_uuid: `str`
    UUID of the ingested data
  new_content_field: `dict`
    JSON object contain the ingested data
  """
  new_content_field = None
  new_content_uuid = None

  if collection_name in ["skills", "competencies"]:
    new_content_uuid, new_content_field = skill_update_handler(
        content, new_content_obj)

  if not new_content_uuid and not new_content_field:

    if collection_name == "learning_objects":
      # converting dictionary into the class object
      new_content_srl_object = new_content_obj.from_dict(content)
      # if object_type == "srl" then we need to update
      # the prerequisites and parent_nodes
      # new srl object will only be create only once
      global SRL_COLLECTIONS

      if new_content_srl_object.type == "srl":
        if SRL_COLLECTIONS.get(content["name"]):
          trigger_srl = new_content_obj.find_by_uuid(
              SRL_COLLECTIONS.get(content["name"]))
          trigger_srl.parent_nodes["learning_experiences"].extend(
              new_content_srl_object.parent_nodes["learning_experiences"])
          trigger_srl.prerequisites["learning_objects"].extend(
              new_content_srl_object.prerequisites["learning_objects"])
          trigger_srl.update()
          new_content_uuid = trigger_srl.uuid
          new_content_field = trigger_srl.get_fields(reformat_datetime=True)
          return new_content_uuid, new_content_field
        else:
          new_content_uuid, new_content_field = add_data_to_db_handler(
              content, new_content_obj, collection_name)
          SRL_COLLECTIONS[content["name"]] = new_content_uuid
          return new_content_uuid, new_content_field

    new_content_uuid, new_content_field = add_data_to_db_handler(
        content, new_content_obj, collection_name)
  return new_content_uuid, new_content_field


def node_update_handler(content):
  """
  creating the key dynamically in the child_nodes
  of the content object
  ### Args:
  content: `dict`
    The JSON object contains the data
  ### Returns:
    None: we are modifying the same array
  """
  try:
    for obj, _ in content["child_nodes"].items():
      content["child_nodes"][obj] = []
  except KeyError:
    pass


def update_reference(node, obj):
  """
  Add data into the firestore and update the parent-child reference
  ### Args:
  node: `dict`
    JSON object containing the data
  obj: `str`
    object wrt to which this node added ingested in firestore
  """
  child_uuid, content_field = add_data_to_db(node, collection_references[obj],
                                             obj)
  # Updating the parent-child relationship
  ParentChildNodesHandler.update_child_references(
      content_field, collection_references[obj], operation="add")
  ParentChildNodesHandler.update_parent_references(
      content_field, collection_references[obj], operation="add")
  # Returning the uuid of the recently added node
  return child_uuid


def create_deep_copy_handler(content):
  """
  Separating the child_nodes data from the content object.
  we need to insert only the UUID of the child nodes.
  ### Args:
  content: `dict`
    JSON object contains the data
  ### Returns:
  deepcopy: list containing the child_nodes data
  """
  deepcopy = []
  try:
    # Coping the child_nodes content into the deepcopy array to
    # process it in later stage
    data = copy.deepcopy(content["child_nodes"])
    deepcopy.append(data)
  except KeyError:
    # If child_nodes key is not present means we need to stop recursion
    pass
  return deepcopy


def parent_node_key_generator(node, key, uuid):
  """
  The parent_node_key_generator function will create the parent_node key at
  a run time and add the UUID of its parent_node in the parent_node
  field of the current object
  ### Args:
  node: `dict`
    The JSON object contains the data
  key: `str`
    parent key
  UUID: `str`
    parent UUID
  ### Returns:
    None: we are modifying the same array
  """
  if node.get("parent_node", None) is not None:
    try:
      node["parent_nodes"][key].append(uuid)
    except KeyError:
      node["parent_nodes"][key] = [uuid]
  else:
    try:
      node["parent_nodes"] = {}
      node["parent_nodes"][key].append(uuid)
    except KeyError:
      node["parent_nodes"] = {}
      node["parent_nodes"][key] = [uuid]


def missing_order_insertion(vals):
  """Function to insert default order value in case
  the order value is not defined in the bulk import json"""
  for val in vals:
    if val.get("order", None) is None:
      val["order"] = 1


def ordered_content(content):
  """
  if object having two key
  this will make sure content
  that it will insert in the
  given order
  """
  content_list = []
  for key, values in content.items():
    missing_order_insertion(values)
    for val in values:
      content_list.append({key: val})
  content_list.sort(key=lambda x: next(iter(x.values()))["order"])
  return content_list


def handler(node, order_id, key):
  """
  Handler to decouple same logic from the
  support upload handler
  """
  upload_reference_handler(node)
  upload_achievements_handler(node)
  deepcopy = create_deep_copy_handler(node)
  node_update_handler(node)
  child_uuid = update_reference(node, key)
  if node["order"] == 0:
    pass
  elif node["order"] in order_id:
    order_id[node["order"]].append(child_uuid)
  else:
    order_id[node["order"]] = [child_uuid]
  support_upload_handler(key, deepcopy, child_uuid)


def support_upload_handler(key, contents, uuid):
  """
  Helper function to achieve ingestion of data
  into the firestore using recursion
  ### Args:
  key: `str`
    parent key string of which the particular content belongs
  content: `dict`
    JSON object contain the data
  UUID: `str`
    UUID of the parent_nodes which was ingested in the firestore
  ### Return:
  None: we are terminating the recursion using the for-loop
  """
  for content in contents:

    if len(content.keys()) > 1:

      # let content = {
      #   "learning_experience": [
      #       {"order":1},
      #       {"order":3}
      #       ],
      #   "assessments" : [
      #     {"order":2},
      #     {"order":3}
      #   ]
      # }

      # According to the problem we need to
      # maintain the prerequisites such that order 2
      # the object will contain the UUID of order 1 in their
      # prerequisites["learning_experience"] field and soon...

      # we have created one function
      # def ordered_content(content)-> LIST
      # which will return the list in the below format

      # ordered_list = [
      #   {"learning_experience":{"order":1}},
      #   {"assessments":{"order":2}},
      #   {"learning_experience":{"order":1}},
      #   {"assessments":{"order":3}}
      # ]

      # Let UUID of the order:1 object is UUID1
      # then insert this in the object of order:2

      # we need to find the exact key inside the
      # prerequisites where we need to add this UUID1

      # key = list(ordered_list[count -1].keys())[0]]

      # After getting the key insert it into the

      # Object["prerequisites"] = UUID1

      # And rest of the logic is simple recursion to
      # do the same above process again and again
      # util we reach at the end of the
      # hierarchy

      previous_order_id = {}
      ordered_list = ordered_content(content)
      count = 0
      for val in ordered_list:
        for obj, value in val.items():
          parent_node_key_generator(value, key, uuid)
          if value["order"] > 1:
            value["prerequisites"] = {}
            value["prerequisites"][list(
                ordered_list[count -
                             1].keys())[0]] = previous_order_id[value["order"] -
                                                                1]
          count += 1
          handler(value, previous_order_id, obj)
    else:
      for obj, vals in content.items():
        previous_order_id = {}
        missing_order_insertion(vals)
        vals = sorted(vals, key=lambda x: x["order"])
        for parent_node in vals:
          parent_node_key_generator(parent_node, key, uuid)
          if parent_node["order"] > 1:
            parent_node["prerequisites"] = {}
            parent_node["prerequisites"][obj] = previous_order_id[
                parent_node["order"] - 1]
          handler(parent_node, previous_order_id, obj)


def upload_reference_handler(contents):
  """
  Add the reference key data recursively into the database
  before the insertion of child_nodes because reference requires only
  uni-directional link
  ### Args:
  content: `dict`
    The JSON object contains the data
  ### Returns:
  None: we are terminating the recursion using the for-loop
  """
  references = contents.get("references", None)
  if references is not None:
    for key, values in references.items():
      id_list = []
      for value in values:
        deepcopy = create_deep_copy_handler(value)
        node_update_handler(value)
        uuid, _ = add_data_to_db(value, collection_references[key], key)
        support_upload_handler(key, deepcopy, uuid)
        id_list.append(uuid)
      references[key] = id_list


def upload_achievements_handler(contents):
  """
  Helper function to update achievements key
  in the firestore
  ### Args:
  content: `dict`
    The JSON object contains the data
  ### Returns:
  None: we are terminating the recursion using the for-loop
  """
  key = "achievements"
  achievements = contents.get(key, None)

  if achievements is not None:
    id_list = []
    for achievement in achievements:
      if achievement is not None:
        deepcopy = create_deep_copy_handler(achievement)
        node_update_handler(achievement)
        uuid, _ = add_data_to_db(achievement, collection_references[key], key)
        support_upload_handler(key, deepcopy, uuid)
        id_list.append(uuid)
    contents[key] = id_list


def upload_handler(key, content, uuid):
  """
  Helper function to upload the learning hierarchy into the
  firestore database
  ### Args:
  key: `str`
    parent key string of which the particular content belongs
  content: `dict`
    JSON object contain the data
  UUID: `str`
    UUID of the parent_nodes which was ingested in the firestore
  ### Return:
  UUID: `str`
    UUID of the topmost parent node
  """
  upload_reference_handler(content)
  upload_achievements_handler(content)
  deepcopy = create_deep_copy_handler(content)
  node_update_handler(content)
  uuid, _ = add_data_to_db(content, collection_references[key], key)
  support_upload_handler(key, deepcopy, uuid)
  return uuid


def find_redundent_id(content):
  """Find the redundent ID"""

  result = {"learning_resources": [], "assessments": []}
  input_dict = {"learning_resources": [], "assessments": []}

  for key, vals in content.items():
    for val in vals:
      redundent_object = collection_references[key].find_by_uuid(val)
      input_dict[key].append(
          redundent_object.get_fields(reformat_datetime=True))

  for key, val in input_dict.items():
    lr_dict = {}
    for lr in val:
      if lr["name"] in lr_dict:
        lr_dict[lr["name"]].append(lr["uuid"])
      else:
        lr_dict[lr["name"]] = [lr["uuid"]]

    for _, uuids in lr_dict.items():
      if len(uuids) > 1:
        result[key].append(uuids[0])
  return result


def srl_redundency_cleaner():
  """SRL Redundency Cleaner"""
  learning_objects = collection_references["learning_objects"].find_by_type(
      "srl")
  for learning_object in learning_objects:
    id_dict = find_redundent_id(learning_object.child_nodes)

    for key, val in id_dict.items():
      if len(val) > 0:
        for ids in val:
          learning_object.child_nodes[key].remove(ids)
          delete_object = collection_references[key].find_by_uuid(ids)
          collection_references[key].collection.delete(delete_object.key)

    learning_object.update()


def bulk_import(headers, json_file):
  """
  Importing a JSON file and validating the schema
  before inserting the data into the database and
  initiating the helper function to do the ingestion
  of the content into the firestore
  ### Args:
  json_file: file
    learning hierarchy file
  ### Raises:
  JSONDecodeError:
    If the learning hierarchy is not in JSON format.
  PydanticValidationError:
    If data in the learning hierarchy is containing the
    invalid field
  ### Returns:
  Return the success message with UUID of the topmost parent node
  """
  try:
    if not json_file.filename.endswith(".json"):
      raise ValidationError("Valid JSON file type is supported")
    else:
      contents = json.load(json_file.file)
      if isinstance(contents, dict):
        for _, content in contents.items():
          UploadPathwayModel(**content)

        data = []

        for key, content in contents.items():
          global header
          header = headers
          data.append(upload_handler(key=key, content=content, uuid=""))

        # to remove the redundent data from the object
        srl_redundency_cleaner()
        module_assessment_prerequisite_handler(data[0])
        return {
            "success": True,
            "message": "Successfully inserted the pathway",
            "data": data
        }
      else:
        raise ValidationError("Provided JSON is invalid")
  except JSONDecodeError as e:
    raise ValidationError("Provided JSON is invalid") from e

  except PydanticValidationError as err:
    error_res = json.loads(err.json())
    req_fields = [i["loc"][-1] for i in error_res]
    req_fields_str = "Missing required fields - " + \
        ",".join("'"+i+"'" for i in req_fields)
    raise ValidationError(req_fields_str, data=error_res) from err

  except Exception as err:
    raise err

  finally:
    # resetting the global variable SRL_COLLECTIONS
    global SRL_COLLECTIONS
    SRL_COLLECTIONS = {}


def delete_hierarchy_handler(node_id: str,
                             node_type: str,
                             delete_achievements: bool = True,
                             delete_skills: bool = True,
                             delete_competencies: bool = True):
  """
  Function to delete the entire hierarchy and all of its components
  Args:
      cp_id: str
      delete_achievements: bool, Set to true to delete achievements
      delete_skills: bool, Set to true to delete skills
      delete_competencies: bool, Set to true to delete competencies
  Returns:
      None
  """
  node = collection_references[node_type].find_by_uuid(node_id)
  node_data = node.get_fields()
  node_name = node_data["name"]
  collection_references[node_type].delete_by_uuid(node_id)

  Logger.info(f"DELETED NODE_ID={node_id} NODE_TYPE={node_type} \
              NODE_NAME={node_name}")
  if node_data["child_nodes"]:
    for coll_name in node_data["child_nodes"].keys():
      if node_data["child_nodes"][coll_name]:
        for id_ in node_data["child_nodes"][coll_name]:
          delete_hierarchy_handler(id_, coll_name)

  # NOTE: Achievements, Skills and Competencies will be deleted by ID and hence,
  # will be deleted from firestore
  if delete_achievements:
    if node_data.get("achievements", []):
      for ac_id in node_data["achievements"]:
        collection_references["achievements"].delete_by_id(ac_id)
        Logger.info(f"DELETED NODE_ID = {ac_id} NODE_TYPE=Achievement")

  if delete_skills:
    if node_data.get("references", []):
      if node_data["references"].get("skills", []):
        for ac_id in node_data["references"]["skills"]:
          collection_references["skills"].delete_by_id(ac_id)
          Logger.info(f"DELETED NODE_ID = {ac_id} NODE_TYPE=Skill")

  if delete_competencies:
    if node_data.get("references", []):
      if node_data["references"].get("competencies", []):
        for ac_id in node_data["references"]["competencies"]:
          collection_references["competencies"].delete_by_id(ac_id)
          Logger.info(f"DELETED NODE_ID = {ac_id} NODE_TYPE=Competency")
