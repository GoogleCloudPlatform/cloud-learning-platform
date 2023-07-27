"""Helper functions to facilitate CRUD Operations"""
from common.utils.collection_references import collection_references
from common.models import CurriculumPathway
from config import LOS_NODES, SKILL_NODES


def custom_hierarchy_sort(children):
  """Function to sort the learning hierarchy in custom manner
  such that learning objects will be come first
  then learning resources
  then assessment items
  """
  low = 0
  high = len(children) - 1
  middle = 0
  while middle <= high:
    # If the element is learning_objects
    if children[middle]["type"] == "learning_objects":
      children[low], children[middle] = children[middle], children[low]
      low = low + 1
      middle = middle + 1
    # If the element is learning_resources
    elif children[middle]["type"] == "learning_resources":
      middle = middle + 1
    # If the element is assessment_items
    else:
      children[middle], children[high] = children[high], children[middle]
      high = high - 1
  return children


def transform_dict(data, level="curriculum_pathways"):
  """Function to transform nested dictionary response of GET route
  (with fetch_tree=True) to a list of dictionary response
  updated_response = {
    label: str,
    type: str,
    data: dict,
    children: list[dict]
  }
  """
  # Used to convert the data into original dictionary format as
  # stored in Firestore
  new_dict = {}
  # Used to place in the updated format
  resp_dict = {}
  for key in data:
    if key not in ["child_nodes"]:
      new_dict[key] = data[key]
    if key == "name":
      resp_dict["label"] = data[key]
      resp_dict["type"] = level

  resp_dict["children"] = []
  if data.get("child_nodes") is None:
    data["child_nodes"] = {}
  children = []

  # Looping over each collection name in child nodes
  for coll in data.get("child_nodes", {}):
    if "child_nodes" not in new_dict:
      new_dict["child_nodes"] = {}
    new_dict["child_nodes"][coll] = []
    # Looping over each item in the collection list
    for item in data["child_nodes"][coll]:
      if isinstance(new_dict["child_nodes"][coll],dict):
        new_dict["child_nodes"][coll].append(item["uuid"])
      else:
        new_dict["child_nodes"][coll].append(item)
      # Recursively transforming the item in the desired
      # format and storing it in children(list)
      if isinstance(item,dict):
        children.append(transform_dict(item, coll))
      if resp_dict["type"] == "learning_objects":
        children = custom_hierarchy_sort(children)
  resp_dict["children"] = children
  resp_dict["data"] = new_dict
  # dict-comprehension to send the response in a more readable format
  #pylint: disable=unnecessary-comprehension
  return {k: v for k, v in sorted(resp_dict.items(), key=lambda x: len(x[0]))}


def get_all_nodes(uuid: str,
                  level: str,
                  node_type: str,
                  nodes: list):
  """
  This method traverses the learning hierarchy from given level uuid and fetches
  the list of nodes of type node_type
  Args:
    uuid (str): uuid of the node from where to traverse.
    level (str): current level/type of the Node for given uuid.
    node_type (str): Type of node to fetch.
    [curriculum_pathways, learning_experiences, learning_objects,
    learning_resources, assessments]
    nodes (list): List to be used to return list of nodes
  Returns:
    nodes (list): list of nodes of type node_type
  """
  node = collection_references[level].find_by_uuid(uuid)
  node = node.get_fields(reformat_datetime=True)
  if node_type == level:
    if node_type == "curriculum_pathways":
      if not node.get("child_nodes", {}).get("curriculum_pathways", []):
        return nodes.append(node)
    elif node_type == "learning_objects":
      if not node.get("child_nodes", {}).get("learning_objects", []):
        return nodes.append(node)
    else:
      return nodes.append(node)
  child_nodes = node.get("child_nodes", {})

  # Fetch nodes of type node_type
  if node_type in LOS_NODES:
    if node_type == level:
      nodes.append(node)
  if node_type in SKILL_NODES:
    if node.get("references", {}) and node["references"].get(node_type, []):
      for id_ in node["references"][node_type]:
        nodes.append(collection_references[node_type].find_by_uuid(
          id_).get_fields(reformat_datetime=True))
  # Use Recursion to fetch all nodes of node_type from child_nodes
  if child_nodes:
    for child_level in child_nodes:
      for child_uuid in child_nodes[child_level]:
        get_all_nodes(child_uuid, child_level, node_type, nodes)
  return nodes


def prerequisite_handler(uuid):
  """Function to handle prerequisites of a node item
  when ingesting the learning hierarchy"""
  curriculum_pathway = CurriculumPathway.find_by_uuid(uuid)
  level_pathways = []

  if curriculum_pathway.child_nodes.get("curriculum_pathways") and len(
      curriculum_pathway.child_nodes.get("curriculum_pathways",[])) > 1:

    for level in curriculum_pathway.child_nodes.get("curriculum_pathways", []):
      level_pathways.append(CurriculumPathway.find_by_uuid(level))

    #Missing order insertion
    for level in level_pathways:
      if level.order is None:
        level.order = 1

    level_pathways = sorted(level_pathways, key=lambda level: level.order)
    for node in level_pathways:
      if node.order > 1:
        prerequisites = []
        for level_pathway in level_pathways:
          if (node.uuid != level_pathway.uuid) and (level_pathway.order
                                                    == (node.order - 1)):
            prerequisites.append(level_pathway.uuid)
        node.prerequisites["curriculum_pathways"] = prerequisites
        node.update()
  elif curriculum_pathway.child_nodes.get("curriculum_pathways") and len(
      curriculum_pathway.child_nodes.get("curriculum_pathways", [])) == 1:
    pathway = curriculum_pathway.child_nodes.get("curriculum_pathways")
    level_pathway = CurriculumPathway.find_by_uuid(pathway[0])
    level_pathway.prerequisites["curriculum_pathways"] = []
    level_pathway.update()
