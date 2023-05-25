"""
Service to map the learning content with the hiearchy
"""
from services.helper import get_all_nodes_for_alias
from common.utils.content_processing import FileUtils

from common.utils.collection_references import collection_references
from common.models import (LearningResource,
                            LearningObject,
                            LearningExperience)
from common.utils.errors import (ValidationError)
from common.utils.gcs_adapter import GcsCrudService
from config import (CONTENT_SERVING_BUCKET,
                    MADCAP_PATTERNS_TO_EXCLUDE)

ALLOWED_RESOURCE_TYPES = [
    "pdf", "image", "html", "video", "docx", "html_package", "scorm", ""
]


def link_content_to_le(le_uuid, prefix_path):
  """
        This function links a valid prefix path to the LE.
        Throws Validation Error if the provided prefix_path is
        not a valid madcap export.
        -------------------------------------------------------
        Input:
        1. le_uuid:
                uuid of the LE for which link is to be made
        2. prefix_path:
                a valid prefix path to be linked with LE
    """
  required_le = LearningExperience.find_by_uuid(le_uuid)

  _, _, files_list = get_file_and_folder_list(
      prefix_path, list_madcap_contents=True)
  if len(files_list) == 0:
    msg = f"Provided prefix_path {prefix_path} "
    msg += "does not point to a madcap export"
    raise ValidationError(msg)

  required_le.resource_path = prefix_path
  required_le.update()


def link_content_to_lr(le_uuid, lr_uuid, resource_path, resource_type, is_srl):
  """
        This function links a valid resource path to the LR.
        Throws Validation Error if the provided resource_path is
        not a part of the prefix given by LE.
        -------------------------------------------------------
        Input:
        1. le_uuid:
                uuid of the LE to reference the prefix path
        2. lr_uuid:
                uuid of the LR for which the link is to be made
        3. resource_path:
                a valid resource path to be linked with LR which
                has the prefix same as parent LE
        4. resource_type:
                a field representing the type of learning resource
    """
  required_le = LearningExperience.find_by_uuid(le_uuid)
  required_lr = LearningResource.find_by_uuid(lr_uuid)

  if is_srl is False:
    if required_le.resource_path in ["", None]:
      msg = f"The resource_path of Learning Experience {le_uuid} is empty."
      msg += " Hence, we cannot link content to "
      msg += f"Learning resource with uuid {lr_uuid}"
      raise ValidationError(msg)
  else:
    if required_le.srl_resource_path in ["", None]:
      msg = f"The srl_resource_path of Learning Experience {le_uuid} is empty."
      msg += " Hence, we cannot link content to "
      msg += f"Learning resource with uuid {lr_uuid}"
      raise ValidationError(msg)

  # Validate Resource Type
  if resource_type not in ALLOWED_RESOURCE_TYPES:
    raise ValidationError(f"resource_type {resource_type} not allowed")

  # TODO: Enable this validation if update of LR links is forbidden
  # if required_lr.resource_path != "":
  #   msg = f"Learning Resource {lr_uuid} already contains a resource_path"
  #   raise ValidationError(msg)

  lr_list = get_all_lr_for_le(le_uuid)

  if lr_uuid not in lr_list:
    msg = f"Given Learning Resource {lr_uuid} is not a "
    msg += f"child of Learning Experience {le_uuid}"
    raise ValidationError(msg)

  if is_srl is False:
    _, _, files_list = get_file_and_folder_list(
        required_le.resource_path, list_madcap_contents=True)
    if resource_path not in files_list:
      msg = "Cannot link Learning Resource with a file that does not "
      msg += "belong to the folder given by Learning Experience."
      msg += f"Required file path prefix: {required_le.resource_path}"
      raise ValidationError(msg)

    required_lr.resource_path = resource_path
    required_lr.type = resource_type
    required_lr.update()
  else:
    _, _, files_list = get_file_and_folder_list(
        required_le.srl_resource_path, list_madcap_contents=True)
    if resource_path not in files_list:
      msg = "Cannot link Learning Resource with a file that does not "
      msg += "belong to the folder given by Learning Experience."
      msg += f"Required file path prefix: {required_le.srl_resource_path}"
      raise ValidationError(msg)

    required_lr.resource_path = resource_path
    required_lr.type = resource_type
    required_lr.update()


def get_parent_node_list(node_id, collection):
  """Get the list of parent nodes"""
  parent_list = []
  node_doc = collection.find_by_uuid(node_id)
  parent_nodes = node_doc.parent_nodes
  for key, value in parent_nodes.items():
    node_item = {
        "node_type": key,
        "node_uuid": value,
    }
    parent_list.append(node_item)

  return parent_list


def is_hierarchy_root(node_uuid, node_type):
  current_node = collection_references[node_type].find_by_uuid(node_uuid)

  if current_node.alias == "program" and \
      current_node.parent_nodes.get("learning_opportunities") == [] and \
      current_node.parent_nodes.get("curriculum_pathways") == []:

    return True
  return False


def get_hierarchy_root(node_uuid, node_type):
  """
    This function returns the uuid of the root of the hierarchy,
    which is by definition a Curriculum Pathway with alias Program
    and has no parent LOS nodes.
    -------------------------------------------------------
    Input
      1. node_uuid: `str`
          uuid of any kind of LOS node
      2. node_type: `str`
          type of the node for which the node_uuid is passed
    -------------------------------------------------------
    Output
      1. root_uuid: `str`
          uuid of the root LOS node of the hierarchy.
  """
  root_uuid = ""

  required_parent = ""

  queue = []

  queue.append({"node_uuid": node_uuid, "node_type": node_type})

  is_visited = {}

  while len(queue) != 0:
    node_obj = queue.pop(0)

    if is_hierarchy_root(node_obj["node_uuid"], node_obj["node_type"]) is True:
      # We have reached the root of the hierarchy AKA Program
      required_parent = node_obj["node_uuid"]
      break

    # Get required LOS document
    node_doc = collection_references[node_obj["node_type"]].find_by_uuid(
        node_obj["node_uuid"])

    # Explore Parent Nodes if they are not visited Previously
    for key, value in node_doc.parent_nodes.items():
      for elem in value:
        if is_visited.get(elem) is None:
          # Once visited, mark it True
          is_visited[elem] = True

          # Extend queue
          queue.append({"node_uuid": elem, "node_type": key})

  root_uuid = required_parent

  return root_uuid


def get_all_sibling_le(le_uuid):
  """
    This function returns a list of all sibling LEs for a
    given LE. The function traverses the learning hierarchy
    via parent_nodes and reaches upto the root. It then collects
    all the LEs under the Programs. Finally returns the list of
    siblings.
    -------------------------------------------------------
    Input
      1. le_uuid:
          uuid of the LE for which the sibling LEs should be fetched
    -------------------------------------------------------
    Output
      1. le_list:
          list of LE uuids which are siblings for the input LE id.
  """
  sibling_le_list = []

  _ = LearningExperience.find_by_uuid(le_uuid)

  program_uuid = get_hierarchy_root(le_uuid, "learning_experiences")

  le_list = get_all_nodes_for_alias(
      uuid=program_uuid,
      level="curriculum_pathways",
      final_alias="learning_experience",
      nodes=sibling_le_list)

  return le_list


def link_srl_to_all_le(le_uuid, srl_resource_path):
  """
    This function accepts any valid LE uuid, finds its siblings
    from the hierarchy, and update the srl_resource_path of each of
    the sibling LEs
    -------------------------------------------------------
    Input
      1. le_uuid:
          uuid of the LE for which the sibling LEs should be updated
      2. srl_resource_path:
          string representing the path of the SRL
  """
  le_sibling_list = get_all_sibling_le(le_uuid)

  for le in le_sibling_list:
    if le["uuid"] != le_uuid:
      le_doc = LearningExperience.find_by_uuid(le["uuid"])
      le_doc.srl_resource_path = srl_resource_path
      le_doc.update()

  # Note: This list has stale data.
  # Do not rely on this output except for the UUIDs
  return le_sibling_list


def get_all_lr_for_le(le_uuid):
  """
        This function returns a list of LR uuids which can be
        present anywhere in the hierarchy under current LE node
        -------------------------------------------------------
        Input
        1. le_uuid:
            uuid of the LE for which the child LRs should be fetched
        -------------------------------------------------------
        Output
        1. lr_list:
            list of LR uuids which are nested under the given LE
    """
  lr_list = []

  start_le = LearningExperience.find_by_uuid(le_uuid)

  queue = []

  child_lo_list = start_le.child_nodes["learning_objects"]

  for child in child_lo_list:
    queue.append({"node_type": "learning_objects", "node_uuid": child})

  while len(queue) > 0:
    node_obj = queue.pop(0)

    if node_obj["node_type"] == "learning_objects":
      lo_obj = LearningObject.find_by_uuid(node_obj["node_uuid"])

      if lo_obj.child_nodes.get("learning_objects") is not None:
        if len(lo_obj.child_nodes.get("learning_objects")) > 0:
          for child in lo_obj.child_nodes["learning_objects"]:
            queue.append({"node_type": "learning_objects", "node_uuid": child})

      if lo_obj.child_nodes.get("learning_resources") is not None:
        if len(lo_obj.child_nodes.get("learning_resources")) > 0:
          for child in lo_obj.child_nodes.get("learning_resources"):
            lr_list.append(child)

  return lr_list


def get_file_and_folder_list(prefix, list_madcap_contents=False):
  """Get the file and folder list for a given prefix"""
  if prefix is None:
    prefix = ""
  else:
    if prefix[-1] != "/":
      prefix += "/"

  gcs_service = GcsCrudService(CONTENT_SERVING_BUCKET)

  folders_list = []
  files_list = []

  if list_madcap_contents is True:
    folders_list = gcs_service.get_bucket_folders(prefix, delimiter=None)
    files_list = gcs_service.get_files_from_folder(prefix, delimiter=None)
    files_list_formatted = []

    temp_list = []
    for file in files_list:
      if "/Content/" in file and \
        file.split(".")[-1] == "htm":
        temp_list.append(file)

    allowed_files = temp_list
    for pattern in MADCAP_PATTERNS_TO_EXCLUDE:
      temp_list_1 = []
      for file in allowed_files:
        if pattern not in file and \
          file not in temp_list_1:
          temp_list_1.append(file)
      allowed_files = temp_list_1

    files_list_formatted = allowed_files

  else:
    folders_list = gcs_service.get_bucket_folders(prefix)
    files_list = gcs_service.get_files_from_folder(prefix)
    files_list_formatted = []

    for file in files_list:
      if file[-1] != "/":
        files_list_formatted.append(file)

  if prefix is None:
    prefix = ""

  return prefix, folders_list, files_list_formatted


# TODO: This validation if only Alpha scope.
def is_missing_linked_files(folder_path, gcs_prefix):
  """
      This function compares the htm files in the content folder of the uploaded
      zip with the htm files in the content folder on the gcs bucket. The prefix
      is given by learning experience.

      1. If any file names are missing, a list of such files is
          returned with error msg
      2. If any new files are present, no error
      ----------------------------------------------------------
      Input:

      folder_path `str`:
        The path at which the uploaded zip is extracted.
      gcs_prefix `str`:
        The prefix path provided by the learning resource to compare
        the contents.
      -----------------------------------------------------------
      Output:

      flag `bool`:
        The flag describing if the zip is valid or not.
        if False, it implies some (or all) file names are not present
        in the new zip file
      error_msg `str`:
        A string describing the error.
          1. list of missing files, if any
          2. None, otherwise
      -----------------------------------------------------------
      Note:
        The files will only be compared if
          1. they belong to the Content folder (reminiscent of a madcap export)
          2. they have extension .htm (HTML)
    """
  futils = FileUtils()

  existing_files_list = []
  new_files_list = []
  missing_files_list = []

  _, _, existing_files_list = get_file_and_folder_list(gcs_prefix, True)
  if len(existing_files_list) == 0:
    raise ValidationError(
        "Given prefix path does not contain any .htm files in Content folder")
  existing_file_name_list = [
      file.split("/")[-1] for file in existing_files_list
  ]

  new_files_list = futils.getContentFolderFiles(f"{folder_path}")
  if len(new_files_list) == 0:
    raise ValidationError(
        "Given zip does not contain any .htm files in Content folder")
  new_file_name_list = [file.split("/")[-1] for file in new_files_list]

  for i in range(len(existing_file_name_list)):
    if existing_file_name_list[i] not in new_file_name_list:
      missing_files_list.append(existing_files_list[i])

  if len(missing_files_list) > 0:
    msg = "Content override is forbidden because of missing files.\n"
    msg += "Following files were not found:\n["
    missing_files = ", ".join(missing_files_list)
    msg += missing_files + "]"
    return False, msg

  return True, None
