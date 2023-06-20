"""Common functionalities for various data models"""
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler

class CommonAPIHandler:
  """Class containing common functions used by various data models"""

  @classmethod
  def update_document(cls, collection, uuid, request_body):
    """Updates the document with given uuid"""
    existing_doc_object = collection.find_by_uuid(uuid)
    existing_doc_object_dict = existing_doc_object.get_fields()
    update_fields = [key for key in existing_doc_object_dict.keys()\
       if isinstance(existing_doc_object_dict[key], dict)]
    for field in update_fields:
      if request_body[field] is None:
        request_body[field] = existing_doc_object_dict[field]
      else:
        for key, val in request_body[field].items():
          if val is None:
            request_body[field][key] = \
              existing_doc_object_dict[field][key]
    ParentChildNodesHandler.compare_and_update_nodes_references(
        request_body, existing_doc_object_dict, collection)
    for key, value in request_body.items():
      if value is not None:
        setattr(existing_doc_object, key, value)
      existing_doc_object.update()

    updated_doc_fields = \
        existing_doc_object.get_fields(reformat_datetime=True)

    return updated_doc_fields

  @classmethod
  def update_and_create_version(cls, collection, uuid, request_body):
    """
      Creates a new version of the document for the given uuid
      and update references
    """
    existing_doc_object = collection.find_by_uuid(uuid)
    existing_doc_object_dict = existing_doc_object.get_fields()
    update_fields = [key for key in existing_doc_object_dict.keys()\
       if isinstance(existing_doc_object_dict[key], dict)]
    for field in update_fields:
      if request_body[field] is None:
        request_body[field] = existing_doc_object_dict[field]
      else:
        for key, val in request_body[field].items():
          if val is None:
            request_body[field][key] = \
              existing_doc_object_dict[field][key]
    # Creating a versioned doc
    versioned_doc = collection()
    versioned_doc = versioned_doc.from_dict(existing_doc_object_dict)

    # Code to find the correct version number
    collection_manager = collection.collection
    collection_manager = collection_manager.filter(
        "root_version_uuid", "==",
        existing_doc_object.root_version_uuid)
    documents = collection_manager.order("-version").fetch(1)
    latest_document = [i.get_fields(reformat_datetime=True) for i in documents
                      ][0]
    versioned_doc.version = latest_document["version"] + 1
    versioned_doc.parent_version_uuid = uuid

    ParentChildNodesHandler.validate_parent_child_nodes_references(request_body)
    for key, value in request_body.items():
      if value is not None:
        setattr(versioned_doc, key, value)
    versioned_doc.save()
    versioned_doc.uuid = versioned_doc.id
    versioned_doc.update()
    updated_doc_fields = versioned_doc.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        updated_doc_fields, collection, operation="add")
    ParentChildNodesHandler.update_parent_references(
        updated_doc_fields, collection, operation="add")
    return updated_doc_fields

  @classmethod
  def create_copy(cls, collection, uuid):
    """Function to create COPY of a documnent"""
    doc = collection.find_by_uuid(uuid)
    doc_dict = doc.get_fields\
      (reformat_datetime=True)
    del doc_dict["uuid"]
    del doc_dict["created_time"]
    del doc_dict["last_modified_time"]
    if doc_dict.get("last_published_on") is not None:
      del doc_dict["last_published_on"]
    ParentChildNodesHandler.validate_parent_child_nodes_references(doc_dict)
    doc_dict["version"] = 1

    copy_doc = collection()
    copy_doc = copy_doc.from_dict(doc_dict)
    copy_doc.uuid = ""
    copy_doc = cls.check_item_is_locked(copy_doc)

    copy_doc.save()
    copy_doc.uuid = copy_doc.id
    copy_doc.root_version_uuid = \
      copy_doc.id
    copy_doc.update()
    copy_doc_fields = copy_doc.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        copy_doc_fields, collection, operation="add")
    ParentChildNodesHandler.update_parent_references(
        copy_doc_fields, collection, operation="add")
    return copy_doc_fields

  @classmethod
  def check_item_is_locked(cls, item):
    """Function to assign is_locked flag to items
    in Learning Hierarchy upon creation"""
    item.is_locked = False
    if item.prerequisites:
      for prereq_level in item.prerequisites:
        if item.prerequisites[prereq_level]:
          item.is_locked = True
          break
    return item

  @classmethod
  def create_versioned_document(cls, collection, uuid, request_body):
    """
      Creates a new version of the document for the given uuid
      without updating the references
    """
    existing_doc_object = collection.find_by_uuid(uuid)
    existing_doc_object_dict = existing_doc_object.get_fields()

    update_fields = [key for key in existing_doc_object_dict.keys()\
       if isinstance(existing_doc_object_dict[key], dict)]
    for field in update_fields:
      if request_body.get(field) is None:
        request_body[field] = existing_doc_object_dict[field]
      else:
        for key, val in request_body[field].items():
          if val is None:
            request_body[field][key] = \
              existing_doc_object_dict[field][key]

    # Creating a versioned doc
    versioned_doc = collection()
    versioned_doc = versioned_doc.from_dict(existing_doc_object_dict)

    # Code to find the correct version number
    collection_manager = collection.collection
    collection_manager = collection_manager.filter(
        "root_version_uuid", "==",
        existing_doc_object.root_version_uuid)
    documents = collection_manager.order("-version").fetch(1)
    latest_document = [i.get_fields(reformat_datetime=True) for i in documents
                      ][0]
    versioned_doc.version = latest_document["version"] + 1
    versioned_doc.parent_version_uuid = uuid
    for key, value in request_body.items():
      if value is not None:
        setattr(versioned_doc, key, value)
    versioned_doc.save()
    versioned_doc.uuid = versioned_doc.id
    versioned_doc.is_implicit = True
    versioned_doc.update()
    updated_doc_fields = versioned_doc.get_fields(reformat_datetime=True)

    return updated_doc_fields

  @classmethod
  def remove_uuid_from_prerequisites(cls, collection, key, uuid):
    """
    This method removes the given 'uuid' from the given 'key' field in
    prerequisites of all the documents in the given 'collection'.
    """
    docs = collection.collection.fetch()
    for doc in docs:
      doc_dict = doc.to_dict()
      prerequisites = doc_dict.get("prerequisites", {})
      if prerequisites:
        key_field = prerequisites.get(key, [])
        if key_field and uuid in key_field:
          doc.prerequisites[key].remove(uuid)
          doc.update()
