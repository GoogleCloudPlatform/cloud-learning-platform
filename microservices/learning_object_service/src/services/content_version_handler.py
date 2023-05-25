""" Service to handle Learning Resource Content Versioning """
from datetime import datetime
from common.models import LearningResource, LearningObject
from common.utils.errors import (ResourceNotFoundException, ValidationError,
                                 InternalServerError)
from common.utils.http_exceptions import (BadRequest, ResourceNotFound,
                                          InternalServerError as
                                          InternalServerException)
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.gcs_adapter import is_valid_path
from schemas.learning_resource_schema import (UpdateLearningResourceModel)
from config import (RESOURCE_BASE_PATH, CONTENT_SERVING_BUCKET,
                    LR_TYPES_LIST)
from services.hierarchy_content_mapping import (get_all_lr_for_le)

PRESERVED_FIELDS = [
    "resource_path", "type", "uuid", "parent_version_uuid",
    "root_version_uuid", "version", "status", "last_published_on"
]


def link_content_and_create_version(parent_uuid, resource_path, resource_type):
  """
        This function creates an empty learning resource
        with its root and parent version ID as the uuid of
        the learning resource that is connected to the
        learning hierarchy. The resource_type and type fields
        of this LR will be populated after validating the
        GCS contents. This function will link the GCS contents
        to the LR documents.
        -------------------------------------------------------------
        Input:
            parent_uuid: `str`
                This is the uuid of the learning resource
                which will be the parent version of the newly
                created learning resource.
            resource_path: `str`
                This is the relative path of the contents present
                on GCS bucket. Ideally it should be the entrypoint
                in case the content is of type html_package otherwise
                it can point to an independent file like docx or pdf.
            resource_type:  `str`
                This field describes the type of the content that is
                being represented by the learning resource.
        -------------------------------------------------------------
        Output:
            new_content_dict: `str`
                This will be the dict of the newly created LR document.
                By default, the status field of this document will be
                draft, unless explicitly published by a user.
    """
  try:

    # Validate LR uuid
    _ = LearningResource.find_by_id(parent_uuid)

    # Validate Resource Type
    if resource_type not in LR_TYPES_LIST:
      raise ValidationError(f"resource_type {resource_type} not allowed")

    # Validate if the path exists on GCS
    path_exists = is_valid_path(
        f"gs://{CONTENT_SERVING_BUCKET}/{RESOURCE_BASE_PATH}/{resource_path}")
    if path_exists is False:
      raise ResourceNotFoundException(
          "Provided resource path does not exist on GCS bucket")

    # Create a versioned document
    new_lr = UpdateLearningResourceModel(
        resource_path=resource_path, type=resource_type)
    new_lr_dict = new_lr.dict()
    new_document = CommonAPIHandler.create_versioned_document(
        LearningResource, parent_uuid, new_lr_dict)
    new_document_obj = LearningResource.find_by_id(new_document["uuid"])
    new_document_obj.status = "draft"
    new_document_obj.is_implicit = True
    new_document_obj.update()
    return new_document_obj.get_fields(reformat_datetime=True)

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


def lazy_sync(content_version_uuid, linked_version_uuid):
  """Lazy-sync of content version with linked version"""
  current_content_data = LearningResource.find_by_id(content_version_uuid)
  linked_content_data = LearningResource.find_by_id(linked_version_uuid)
  linked_content_dict = linked_content_data.get_fields()

  for key, value in linked_content_dict.items():
    if value is not None:
      if key not in PRESERVED_FIELDS:
        setattr(current_content_data, key, value)

  current_content_data.update()


def update_hierarchy_references(existing_document_dict, input_document_dict,
                                collection):
  """Update the hierarchy references for the given document"""
  ParentChildNodesHandler.update_child_references(existing_document_dict,
                                                  collection, "remove")
  ParentChildNodesHandler.update_child_references(input_document_dict,
                                                  collection, "add")
  ParentChildNodesHandler.update_parent_references(existing_document_dict,
                                                   collection, "remove")
  ParentChildNodesHandler.update_parent_references(input_document_dict,
                                                   collection, "add")

  updated_doc = collection.find_by_id(input_document_dict["uuid"])
  return updated_doc.get_fields(reformat_datetime=True)


def unpublish_other_versions(content_version_uuid):
  """Unpublish other versions"""
  content_dict = LearningResource.find_by_id(content_version_uuid)
  root_version_uuid = content_dict.root_version_uuid

  # Fetch all content version documents
  version_list_manager = LearningResource.collection.filter(
      "is_deleted", "==", False)
  version_list_manager = version_list_manager.filter("root_version_uuid", "==",
                                                     root_version_uuid)
  version_list_manager = version_list_manager.order("-created_time").fetch()

  # Mark all other LR versions as unpublished
  for doc in version_list_manager:
    if doc.uuid != content_version_uuid:

      # Only unpublish a document if it was published
      if doc.status == "published":
        doc.status = "unpublished"
        doc.update()


def handle_publish_event(linked_lr_uuid, content_version_uuid):
  """
        This function publishes a particular learning resource.
        When a document is published, it is connected to the
        hierarchy and replaces old document. The status of all
        previous documents is set as unpublished and the new one
        is marked as published.
        -------------------------------------------------------------
        Input:
            linked_lr_uuid: `str`
                This is the uuid of the learning resource
                which is currently connected to the hierarchy.
            content_version_uuid: `str`
                This is the uuid of the learning resource
                which should be marked as published.
                If the content_version_uuid is not passed, then
                the document will be published against itself if its
                a draft. Otherwise an error will be thrown that we
                cannot publish an document that is currently published.
        -------------------------------------------------------------
        Output:
            published_content_dict: `dict`
                This will be the dict of the published LR document.
                All the other versions of the LR Contents will be marked
                as unpublished.
    """
  try:

    connected_lr = LearningResource.find_by_id(linked_lr_uuid)
    connected_lr_dict = connected_lr.get_fields(reformat_datetime=True)

    # verify connected_lr
    parent_nodes = connected_lr_dict.get("parent_nodes")\
                    .get("learning_objects")
    if parent_nodes is not None:
      for node_id in parent_nodes:
        parent_node = LearningObject.find_by_id(node_id).get_fields(
            reformat_datetime=True)
        child_nodes = parent_node.get("child_nodes").get("learning_resources")
        if child_nodes is not None:
          if connected_lr.uuid not in child_nodes:
            raise ValidationError(
                "Given resource uuid is not connected to a valid parent")

    # Publish timestamp
    publish_timestamp = datetime.now()

    if content_version_uuid is None or \
      content_version_uuid == linked_lr_uuid:

      unpublish_other_versions(connected_lr.uuid)

      # Validate if user is trying to publish the same document
      if connected_lr.status == "published":
        raise ValidationError(
            "Cannot publish content that is currently published.")

      # pylint: disable = line-too-long
      if connected_lr.resource_path == "":
        raise ValidationError(
          f"resource_path is empty for Learning Resource with uuid {linked_lr_uuid}"
        )

      # publish the connected LR
      connected_lr.status = "published"
      connected_lr.last_published_on = publish_timestamp
      connected_lr.update()

      return connected_lr.get_fields(reformat_datetime=True)
    else:
      lr_doc = LearningResource.find_by_id(content_version_uuid)

      if lr_doc.status == "initial" and \
        lr_doc.resource_path == "":
        raise ValidationError(
          "Resource path cannot be empty for a resource to be published"
        )

      unpublish_other_versions(content_version_uuid)

      # Validate if user is trying to publish the same document
      if lr_doc.status == "published":
        raise ValidationError(
            "Cannot publish content that is currently published.")

      connected_published_document = None

      if lr_doc.status == "unpublished":
        # Handle republish scenario
        # ---------------------------------------

        resource_path = lr_doc.resource_path
        resource_type = lr_doc.type
        parent_uuid = content_version_uuid

        # Create a versioned document
        new_lr = UpdateLearningResourceModel(
            resource_path=resource_path, type=resource_type)
        new_lr_dict = new_lr.dict()
        new_document = CommonAPIHandler.create_versioned_document(
            LearningResource, parent_uuid, new_lr_dict)
        new_document_obj = LearningResource.find_by_id(new_document["uuid"])
        new_document_obj.status = "published"
        new_document_obj.is_implicit = True
        new_document_obj.last_published_on = publish_timestamp
        new_document_obj.update()

        # pylint: disable = line-too-long
        # connected_published_document = new_document_obj.get_fields(reformat_datetime=True)

        published_document = new_document_obj.get_fields(reformat_datetime=True)
        connected_document = connected_lr.get_fields(reformat_datetime=True)

        connected_published_document = update_hierarchy_references(
            connected_document, published_document, LearningResource)

        lazy_sync(new_document_obj.uuid, connected_lr.uuid)
      else:
        # Handle simple publish scenario
        # ---------------------------------------

        if lr_doc.resource_path == "":
          raise ValidationError(
            f"Resource Path is empty for Learning resource with uuid {lr_doc.uuid}"
          )

        # Publish required document
        lr_doc.status = "published"
        lr_doc.last_published_on = publish_timestamp
        lr_doc.update()

        published_document = lr_doc.get_fields(reformat_datetime=True)
        connected_document = connected_lr.get_fields(reformat_datetime=True)

        connected_published_document = update_hierarchy_references(
            connected_document, published_document, LearningResource)

        lazy_sync(lr_doc.uuid, connected_lr.uuid)

      return connected_published_document

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e


def get_content_versions(lr_uuid, status, skip, limit):
  """
        This function returns a list of the content version documents
        that have same root_version_uuid which the uuid of the LR
        which is connected to the Learning Hierarchy.

        Note: This function does not take into consideration that the
        content versions are based on unique resource paths. It will return
        all the available versions of documents even if it was a
        small change like title change.
        -------------------------------------------------------------
        Input:
            lr_uuid: `str`
                This is the uuid of the learning resource
                which is connected to the learning hierarchy
        -------------------------------------------------------------
        Output:
            content_version_list: `list`
                This will be the list of dicts of all the available
                contents versions that were linked against the hierarchy
                connected learning resource.
    """
  try:

    if skip < 0:
      raise ValidationError("Invalid value passed to \"skip\" query parameter")

    if limit < 1:
      raise ValidationError("Invalid value passed to \"limit\" query parameter")

    lr_doc = LearningResource.find_by_id(lr_uuid)

    root_version_uuid = lr_doc.root_version_uuid

    version_list_manager = LearningResource.collection.filter(
        "root_version_uuid", "==", root_version_uuid)
    version_list_manager = version_list_manager.filter("is_deleted", "==",
                                                       False)

    if status is not None:
      if status == "draft":
        version_list_manager = version_list_manager.filter("status", "in",
                                                          ["draft","initial"])
      else:
        version_list_manager = version_list_manager.filter("status", "==",
                                                          status)

    version_list_manager = version_list_manager.order("-created_time").offset(
        skip).fetch(limit)

    content_version_list = []
    for doc in version_list_manager:
      doc_dict = doc.get_fields(reformat_datetime=True)
      content_version = {
            "resource_path": doc_dict["resource_path"],
            "type": doc_dict["type"],
            "content_version_uuid": doc_dict["uuid"],
            "created_time": doc_dict["created_time"],
            "last_published_on": doc_dict["last_published_on"],
            "status": doc_dict["status"]
        }
      content_version_list.append(content_version)

    return content_version_list

  except ResourceNotFoundException as e:
    raise ResourceNotFound(str(e)) from e
  except ValidationError as e:
    raise BadRequest(str(e)) from e
  except InternalServerError as e:
    raise InternalServerException(str(e)) from e

def update_lr_resource_path(le_uuid,new_file_paths):
  """Update the learning resource path"""
  new_file_name_list = [ path.split("/")[-1] for path in new_file_paths]
  lr_list = get_all_lr_for_le(le_uuid)

  lr_doc_list = []
  for lr in lr_list:
    lr_doc_list.append(LearningResource.find_by_id(lr))

  for i in range(len(lr_doc_list)):
    file_name = lr_doc_list[i].resource_path
    if file_name is not None and file_name != "":
      file_name = file_name.split("/")[-1]
      if file_name in new_file_name_list:
        index = new_file_name_list.index(file_name)
        lr_doc_list[i].resource_path = new_file_paths[index]
        lr_doc_list[i].update()
