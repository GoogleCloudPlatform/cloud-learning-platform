"""Helper functions to facilitate CRUD Operations"""
from common.utils.collection_references import collection_references


def custom_hierarchy_sort(children):
  """Function to sort the learning hierarchy in custom manner
  such that learning objects will be come first
  then learning resources
  then assessement items
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


def get_all_nodes_for_alias(uuid: str,
                            level: str,
                            final_alias: str,
                            nodes: list):
  """
  This method traverses the learning hierarchy from given level uuid till the
  final_alias and retrieves all the node where alias=final_alias.
  Args:
    uuid (str): uuid of the node from where to traverse.
    level (str): current level/type of the Node for given uuid.
    final_alias (str): alias till which the traverse should be done.
    nodes (list): list to be used to return list of nodes
  Returns:
    nodes (list): List of nodes of alias=final_alias
  """
  node = collection_references[level].find_by_uuid(uuid)
  node = node.get_fields(reformat_datetime=True)
  if node.get("alias", "") == final_alias:
    nodes.append(node)
    return
  child_nodes = node.get("child_nodes", [])
  if child_nodes:
    for child_level in child_nodes:
      for child_uuid in child_nodes[child_level]:
        get_all_nodes_for_alias(child_uuid, child_level, final_alias, nodes)
  return nodes
