"""Functions to get and update child and parent nodes data"""
from typing_extensions import Literal
from common.utils.collection_references import collection_references, LOS_COLLECTIONS
import copy
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
#pylint: disable=dangerous-default-value
class ParentChildNodesHandler():
  """ Class to handle parent child node relationship operations """

  @classmethod
  def load_child_nodes_data(cls, document_fields):
    """To fetch the data of the child nodes for a given document
        and their subsequent ones"""
    child_nodes_dict = cls.get_child_nodes(document_fields)

    for collection_name, document_id_list in child_nodes_dict.items():
      for list_index, child_node_document_id in enumerate(document_id_list):
        collection = collection_references[collection_name]
        document = collection.find_by_uuid(child_node_document_id)
        child_document_fields = document.get_fields(reformat_datetime=True)
        document_id_list[list_index] = cls.load_child_nodes_data(
            child_document_fields)

    return document_fields

  @classmethod
  def load_nodes_data(cls,
                      document_fields,
                      coll_name,
                      learner_profile,
                      keys_to_expand,
                      list_to_expand):
    """To fetch the data of the child nodes for a given document
        and their subsequent ones"""
    all_child_nodes = {}
    for key in keys_to_expand:
      all_child_nodes[key] = cls.get_nodes_by_key(document_fields, key)
    for key in list_to_expand:
      all_child_nodes[key] = cls.get_nodes_by_key(document_fields, key)
    document_fields = cls.update_hierarchy_with_profile_data(
        learner_profile, document_fields, coll_name, document_fields["uuid"])
    for field_name, child_nodes_dict in all_child_nodes.items():
      if field_name in list_to_expand:
        child_nodes_list = child_nodes_dict
        for list_index, child_node_document_id in enumerate(child_nodes_list):
          collection = collection_references[field_name]
          document = collection.find_by_uuid(child_node_document_id)
          child_document_fields = document.get_fields(reformat_datetime=True)
          child_nodes_list[list_index] = cls.load_nodes_data(
              child_document_fields,
              field_name,
              learner_profile,
              keys_to_expand,
              list_to_expand)
      else:
        for collection_name, document_id_list in child_nodes_dict.items():
          for list_index, child_node_document_id in enumerate(document_id_list):
            collection = collection_references[collection_name]
            document = collection.find_by_uuid(child_node_document_id)
            child_document_fields = document.get_fields(reformat_datetime=True)
            child_document_fields = cls.update_hierarchy_with_profile_data(
                learner_profile, child_document_fields, collection_name,
                child_node_document_id)
            document_id_list[list_index] = cls.load_nodes_data(
                child_document_fields,
                collection_name,
                learner_profile,
                keys_to_expand,
                list_to_expand)
    return document_fields

  @classmethod
  def load_hierarchy_progress(cls, document_fields, coll_name, learner_profile,
    is_progress_updated = False):
    """To fetch learner progress for a given learning node
    Args:
      document_fields: dict - dictionary of fields of given learning node
      coll_name: str - collection name / hierarchy level of the learning node
      learner_profile: dict - learner profile dictionary
      is_progress_updated - whether progress is already updated
    Returns:
      dict - nested dictionary containing learner progress
    """
    all_child_nodes = document_fields.get("child_nodes",{})
    if not is_progress_updated:
      document_fields = cls.update_hierarchy_with_profile_data(
        learner_profile, document_fields, coll_name, document_fields["uuid"])
    for collection_name, document_id_list in all_child_nodes.items():
      if not document_id_list:
        continue
      learning_objects_counts = 0
      if collection_name == "learning_objects":
        learning_objects_counts = len(document_id_list)
      collection_class = collection_references[collection_name]
      keys = [f"{collection_class.collection_name}/{id}"
      for id in document_id_list]
      all_child_docs = [node.get_fields(reformat_datetime=True)
      for node in collection_class.collection.get_all(keys)]
      child_count = len(document_id_list)
      # map the arguments to the function using threads in the thread pool
      with ThreadPoolExecutor(max_workers=child_count) as executor:
        all_child_docs = list(
          executor.map(cls.update_hierarchy_with_profile_data,
        repeat(learner_profile),all_child_docs,repeat(collection_name),
        document_id_list,repeat(document_fields["uuid"])))

      for list_index, child_document_fields in enumerate(all_child_docs):
        if collection_name == "curriculum_pathways":
          document_id_list[list_index] = cls.load_hierarchy_progress(
            child_document_fields, collection_name, learner_profile,
            is_progress_updated = True)
        elif collection_name in ["learning_experiences", "learning_objects"]:
          if not (collection_name == "learning_experiences" and \
              child_document_fields.get("status") == "not_attempted"):
            child_document_fields = cls.load_hierarchy_progress(
            child_document_fields, collection_name, learner_profile,
            is_progress_updated = True)
          else:
            child_document_fields["recent_child_node"] = {}
          del child_document_fields["child_nodes"]
          document_id_list[list_index] = child_document_fields
        else:
          document_id_list[list_index] = child_document_fields
      all_child_nodes[collection_name] = cls.sort_nodes_by_recent_activity(
        document_id_list, coll_name, learning_objects_counts)
    # Condition to ensure we do not fill in recent child node data for
    # curriculum pathways
    if coll_name != "curriculum_pathways":
      all_child_collection_nodes = []
      for _, document_list in all_child_nodes.items():
        all_child_collection_nodes.extend(document_list)
      document_fields["recent_child_node"] = cls.recent_child_node(
        all_child_collection_nodes, document_fields.get("uuid"))
    return document_fields

  @classmethod
  def reinitialize_ordering(cls, nodes):
    """ function to reinitialize the order according to prerequisites
    """
    for given_order in range(len(nodes)):
      for current_order in range(len(nodes)):
        if nodes[given_order]["uuid"] in nodes[
          current_order]["prerequisites"].get(
          "learning_objects",[]) and nodes[given_order][
          "uuid"] != nodes[current_order]["uuid"]:
          nodes[current_order]["order"] = nodes[given_order][
            "order"]+1
    sorted_nodes = sorted(nodes, key=lambda x: x["order"])
    return sorted_nodes

  @classmethod
  def recent_child_node(cls, nodes, parent_node):
    """Function to fetch recent child node"""
    attempted_nodes = []
    unattempted_nodes = []
    for node in nodes:
      if node.get("parent_node") == parent_node and \
        node.get("status") not in ["completed", "skipped"] and \
          node.get("is_hidden") is False:
        if node.get("last_attempted") != "" and \
          node.get("status") != "not_attempted":
          attempted_nodes.append(node)
        else:
          unattempted_nodes.append(node)
    # Sort nodes first based on is_optional in ASC order
    # Then sort by last_attempted time in DESC order
    attempted_nodes = sorted(attempted_nodes, key=lambda x:
        (-x["is_optional"], x["last_attempted"]), reverse=True)
    if not attempted_nodes:
      # Sort nodes first based on is_optional in ASC order
      # Then sort by order key in ASC order
      unattempted_nodes = sorted(unattempted_nodes, key=lambda x: (
         x["is_optional"], x["order"]))
    sorted_nodes = attempted_nodes + unattempted_nodes
    if sorted_nodes:
      return sorted_nodes[0]
    else:
      return {}

  @classmethod
  #pylint: disable = unused-argument
  def sort_nodes_by_recent_activity(cls, nodes, coll_name,
                                    learning_objects_counts):
    """Sorts the passed nodes based on the recent activity with
    sorting preferences as following
    1. latest attempted active nodes
    2. unlocked nodes
    3. locked nodes
    4. completed nodes
    Args:
    nodes : List of nodes of a given hierarchy level
    Returns : List of sorted nodes
    """
    # NOTE: Use coll_name to add specific conditions
    # per node type
    if coll_name == "curriculum_pathways":
      node_dict = {"active": [],
      "completed": [], "locked": [], "not_attempted": []}
      for node in nodes:
        if node.get("is_locked"):
          node_dict["locked"].append(node)
        else:
          if node.get("status") == "completed":
            node_dict["completed"].append(node)
          elif node.get("status") == "not_attempted":
            node_dict["not_attempted"].append(node)
          elif node.get("status") == "in_progress":
            node_dict["active"].append(node)
      sorted_nodes = (
        sorted(
          node_dict["active"],
          key=lambda node: node["last_attempted"],reverse=True) +
        sorted(
          node_dict["not_attempted"],
          key=lambda node: node["order"], reverse=True) +
        sorted(node_dict["locked"], key=lambda node: node["order"]) +
        sorted(
          node_dict["completed"],
          key=lambda node: node["last_attempted"],  reverse=True))
    else:
      sorted_nodes = sorted(nodes, key=lambda x: x["order"])
      if len(sorted_nodes) == learning_objects_counts:
        sorted_nodes = cls.reinitialize_ordering(sorted_nodes)
    return sorted_nodes

  @classmethod
  def return_child_nodes_data(cls, document_dict):
    """To fetch the data of the child nodes for a given document
        and their subsequent ones"""
    #child_nodes_dict = cls.get_child_nodes(document_fields)

    document_fields = copy.deepcopy(document_dict)

    if "child_nodes" in document_fields:
      child_nodes_dict = document_fields.get("child_nodes")

    for collection_name, document_id_list in child_nodes_dict.items():
      for list_index, child_node_document_id in enumerate(document_id_list):
        collection = collection_references[collection_name]
        document = collection.find_by_uuid(child_node_document_id)
        child_document_fields = document.get_fields(reformat_datetime=True)
        document_id_list[list_index] = cls.load_child_nodes_data(
            child_document_fields)

    return document_fields

  @classmethod
  def load_immediate_parent_nodes_data(cls,
                                       document_fields,
                                       learner_profile=None):
    """To fetch the data of the immediate parent nodes of a given document"""
    parent_nodes_dict = cls.get_parent_nodes(document_fields)

    for collection_type, document_id_list in parent_nodes_dict.items():
      for list_index, each_document_id in enumerate(document_id_list):
        collection = collection_references[collection_type]
        parent_document = collection.find_by_uuid(each_document_id)
        parent_document_fields = parent_document.get_fields(
            reformat_datetime=True)
        parent_document_fields = cls.update_hierarchy_with_profile_data(
            learner_profile, parent_document_fields, collection_type,
            each_document_id)
        document_id_list[list_index] = parent_document_fields

    return document_fields

  @classmethod
  def validate_parent_child_nodes_references(cls, input_dict):
    """To validate that the document uuid present in the child nodes and parent
    nodes for a given document exists"""
    child_nodes_dict = cls.get_child_nodes(input_dict)
    if child_nodes_dict is not None:
      for collection_type, document_id_list in child_nodes_dict.items():
        for each_document_id in document_id_list:
          collection = collection_references[collection_type]
          collection.find_by_uuid(each_document_id)

    parent_nodes_dict = cls.get_parent_nodes(input_dict)
    if parent_nodes_dict is not None:
      for collection_type, document_id_list in parent_nodes_dict.items():
        for each_document_id in document_id_list:
          collection = collection_references[collection_type]
          collection.find_by_uuid(each_document_id)

  @classmethod
  def update_child_references(cls, document_fields, collection,
                              operation: Literal["add", "remove"]):
    """To add/remove the references of given document in the parent nodes of a
    child document"""
    collection_name = cls.get_collection_name(collection)
    child_nodes_dict = cls.get_child_nodes(document_fields)

    for collection_type, document_id_list in child_nodes_dict.items():
      for each_document_id in document_id_list:
        collection = collection_references[collection_type]
        child_document = collection.find_by_uuid(each_document_id)

        if operation == "add":
          if document_fields.get(
              "uuid") not in child_document.parent_nodes[collection_name]:
            child_document.parent_nodes[collection_name].append(
                document_fields.get("uuid"))

        if operation == "remove":
          if document_fields.get(
              "uuid") in child_document.parent_nodes[collection_name]:
            child_document.parent_nodes[collection_name].remove(
                document_fields.get("uuid"))
        child_document.update()

  @classmethod
  def update_parent_references(cls, document_fields, collection,
                               operation: Literal["add", "remove"]):
    """To add/remove the references of given document in the child nodes of a
    parent document"""
    collection_name = cls.get_collection_name(collection)
    parent_nodes_dict = cls.get_parent_nodes(document_fields)

    for collection_type, document_id_list in parent_nodes_dict.items():
      for each_document_id in document_id_list:
        collection = collection_references[collection_type]
        parent_document = collection.find_by_uuid(each_document_id)
        if operation == "add":
          if document_fields.get(
              "uuid") not in parent_document.child_nodes[collection_name]:
            parent_document.child_nodes[collection_name].append(
                document_fields.get("uuid"))
        if operation == "remove":
          if document_fields.get(
              "uuid") in parent_document.child_nodes[collection_name]:
            parent_document.child_nodes[collection_name].remove(
                document_fields.get("uuid"))
        parent_document.update()

  @classmethod
  def compare_and_update_child_nodes_references(cls, base_doc_dict, doc_dict,
                                                collection, operation):
    """
    This function is used to add/remove the references of given document in the
    parent nodes of a child document
    Args:
      base_doc_dict: Base document object that is used as reference
      doc_dict: Document object that is being compared with base one
      collection: The collection of the document
      operation: add or remove the node"""
    base_child_nodes_dict = cls.get_child_nodes(base_doc_dict)
    child_nodes_dict = cls.get_child_nodes(doc_dict)

    collection_name = cls.get_collection_name(collection)

    for collection_type, document_id_list in base_child_nodes_dict.items():
      for each_document_id in document_id_list:
        if child_nodes_dict and each_document_id not in child_nodes_dict.get(
          collection_type):
          collection = collection_references[collection_type]
          child_document = collection.find_by_uuid(each_document_id)

          if operation == "add":
            if doc_dict.get(
                "uuid") not in child_document.parent_nodes[collection_name]:
              child_document.parent_nodes[collection_name].append(
                  doc_dict.get("uuid"))
          if operation == "remove":
            if base_doc_dict.get(
                "uuid") in child_document.parent_nodes[collection_name]:
              child_document.parent_nodes[collection_name].remove(
                  base_doc_dict.get("uuid"))
          child_document.update()

  @classmethod
  def compare_and_update_parent_nodes_references(cls, base_doc_dict, doc_dict,
                                                 collection, operation):
    """
    This function is used to add/remove the references of given document in the
    child nodes of a parent document
    Args:
      base_doc_dict: Base document object that is used as reference
      doc_dict: Document object that is being compared with base one
      collection: The collection of the document
      operation: add or remove the node"""
    base_parent_nodes_dict = cls.get_parent_nodes(base_doc_dict)
    parent_nodes_dict = cls.get_parent_nodes(doc_dict)

    collection_name = cls.get_collection_name(collection)
    for collection_type, document_id_list in base_parent_nodes_dict.items():
      for each_document_id in document_id_list:
        if parent_nodes_dict and each_document_id not in parent_nodes_dict.get(
          collection_type):
          collection = collection_references[collection_type]
          parent_document = collection.find_by_uuid(each_document_id)

          if operation == "add":
            if doc_dict.get(
                "uuid") not in parent_document.child_nodes[collection_name]:
              parent_document.child_nodes[collection_name].append(
                  doc_dict.get("uuid"))
          if operation == "remove":
            if base_doc_dict.get(
                "uuid") in parent_document.child_nodes[collection_name]:
              parent_document.child_nodes[collection_name].remove(
                  base_doc_dict.get("uuid"))
          parent_document.update()

  @classmethod
  def compare_and_update_nodes_references(cls, input_document_dict,
                                          existing_document_dict, collection):
    """
    This function is used to add/remove the references of given document in the
    child/parent nodes of a parent/child document
    Args:
      input_document_dict: Input document object that is provided by the user
      existing_document_dict: Existing document object that is present in the DB
      collection: The collection of the document"""
    cls.compare_and_update_child_nodes_references(existing_document_dict,
                                                  input_document_dict,
                                                  collection, "remove")
    cls.compare_and_update_child_nodes_references(input_document_dict,
                                                  existing_document_dict,
                                                  collection, "add")
    cls.compare_and_update_parent_nodes_references(existing_document_dict,
                                                   input_document_dict,
                                                   collection, "remove")
    cls.compare_and_update_parent_nodes_references(input_document_dict,
                                                   existing_document_dict,
                                                   collection, "add")

  @classmethod
  def delete_tree(cls, document_dict, collection):
    for collection_name, document_list in document_dict["child_nodes"].items():
      child_collection = collection_references[collection_name]
      for child_document_fields in document_list:
        cls.delete_tree(child_document_fields, child_collection)
    collection.delete_by_uuid(document_dict["uuid"])

  @classmethod
  def delete_child_tree(cls, document_dict):
    document_dict = cls.load_child_nodes_data(document_dict)
    for collection_name, document_list in document_dict["child_nodes"].items():
      collection = collection_references[collection_name]
      for child_document_fields in document_list:
        cls.delete_tree(child_document_fields, collection)

  @classmethod
  def get_collection_name(cls, collection):
    """ Get the collection name key from the collection"""
    for key, value in collection_references.items():
      if value == collection:
        return key

  @classmethod
  def get_parent_nodes(cls, document_dict):
    """ Extract the parent nodes from the document"""
    parent_nodes = document_dict.get("parent_nodes", {})
    if parent_nodes is None:
      parent_nodes = {}
    return parent_nodes

  @classmethod
  def get_child_nodes(cls, document_dict):
    """ Extract the child nodes from the document"""
    child_nodes = document_dict.get("child_nodes", {})
    if child_nodes is None:
      child_nodes = {}
    return child_nodes

  @classmethod
  def get_nodes_by_key(cls, document_dict, key="child_nodes"):
    """ Extract the child nodes from the document"""
    list_type_keys = ["achievements"]
    if key in list_type_keys:
      child_nodes = document_dict.get(key, [])
    else:
      child_nodes = document_dict.get(key, {})
    if child_nodes is None:
      child_nodes = {}
    return child_nodes

  @classmethod
  def get_child_node_count(cls, node):
    """Returns the number of child nodes for the given node"""
    child_nodes = node.child_nodes
    total_child_nodes = 0
    if child_nodes:
      for child_level in child_nodes:
        total_child_nodes += len(child_nodes[child_level])
    return total_child_nodes

  @classmethod
  def update_hierarchy_with_profile_data(cls, learner_profile, node_dict,
                                         collection_type, doc_id,
                                         parent_id=None):
    """This function will find the correct data for a Node Item in LOS in
    LearnerProfile and update it in the hierarchy"""
    # Logic to check if the item is locked/unlocked
    # Update the is_locked flag and progress flag from LearnerProfile
    if learner_profile is not None and learner_profile.progress is not None\
        and collection_type in LOS_COLLECTIONS:

      is_hidden = learner_profile.progress.get(
            collection_type, {}).get(doc_id,
                                    {}).get("is_hidden",
                                            node_dict.get("is_hidden"))
      is_locked = learner_profile.progress.get(
          collection_type, {}).get(doc_id,
                                   {}).get("is_locked",
                                           node_dict.get("is_locked"))
      is_optional = learner_profile.progress.get(
          collection_type, {}).get(doc_id,
                                   {}).get("is_optional",
                                           node_dict.get("is_optional"))

      progress_parent = learner_profile.progress.get(
        collection_type, {}).get(doc_id, {}).get("parent_node", "")
      if not progress_parent:
        progress_parent = ""

      # FIXME: this is done to add ungate flag for first LR in project
      # this flags specifies whether cognitive wrapper is unlocked
      # Ticket 4928
      if collection_type == "learning_resources" and node_dict["order"] == 1:
        node = collection_references["learning_resources"].find_by_uuid(doc_id)
        module = collection_references["learning_objects"]\
          .find_by_uuid(node.parent_nodes["learning_objects"][0])
        if module.type == "project":
          cw_is_locked = True
          unit = collection_references["learning_experiences"].find_by_uuid(
            module.parent_nodes["learning_experiences"][0])
          modules = unit.child_nodes
          for level in modules:
            for module_id in modules[level][::-1]:
              neighbor = collection_references["learning_objects"].find_by_uuid(
                module_id)
              if neighbor.type == "cognitive_wrapper":
                cw_is_locked = learner_profile.progress.get("learning_objects",
                        {}).get(neighbor.id, {}).get("is_locked", True)
                break
          node_dict["ungate"] = not cw_is_locked

      if not (progress_parent != parent_id and node_dict["type"] == "srl"
              and node_dict["alias"] == "module" and parent_id):
        node_dict["is_hidden"] = is_hidden
        node_dict["is_locked"] = is_locked
        node_dict["is_optional"] = is_optional
        if collection_type == "assessments":
          node_dict["num_attempts"] = learner_profile.progress.get(
        collection_type, {}).get(doc_id, {}).get("num_attempts", 0)
      node_dict["progress"] = learner_profile.progress.get(
          collection_type, {}).get(doc_id, {}).get("progress", 0)
      node_dict["status"] = learner_profile.progress.get(
          collection_type, {}).get(doc_id, {}).get("status", "not_attempted")
      node_dict["last_attempted"] = learner_profile.progress.get(
        collection_type, {}).get(doc_id, {}).get("last_attempted", "")
      node_dict["parent_node"] = learner_profile.progress.get(
        collection_type, {}).get(doc_id, {}).get("parent_node", "")
      child_count =learner_profile.progress.get(
        collection_type, {}).get(doc_id, {}).get("child_count", 0)
      if child_count == 0 and node_dict.get("child_nodes"):
        child_count = sum(len(node_dict.get(
          "child_nodes",{}).get(child_type,[]))
         for child_type in node_dict.get("child_nodes",{}))
      node_dict["child_count"] = child_count
      node_dict["completed_child_count"] = learner_profile.progress.get(
        collection_type, {}).get(doc_id, {}).get("completed_child_count", 0)

    if learner_profile is not None and learner_profile.achievements is not None\
         and collection_type == "curriculum_pathways":
      achievement_intersection = list(
          set(learner_profile.achievements)
          & set(node_dict.get("achievements", [])))
      node_dict["earned_achievements"] = []
      for achievement in achievement_intersection:
        node_dict["earned_achievements"].append(
            cls.get_document_from_collection("achievements", achievement))
    return node_dict

  @classmethod
  def get_document_from_collection(cls, collection_type, doc_id):
    collection = collection_references[collection_type]
    document = collection.find_by_uuid(doc_id)
    child_document_fields = document.get_fields(reformat_datetime=True)
    return child_document_fields
