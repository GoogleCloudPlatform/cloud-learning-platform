"""Functions to fetch the collection using
the UUID of the object
"""
from common.utils.collection_references import collection_references
from common.utils.errors import ResourceNotFoundException
from typing import Optional
from typing_extensions import Literal
# pylint:disable=line-too-long


class CollectionHandler:
  """
  Collection Handler fetch Collection using
  the UUID of the object
  """

  @classmethod
  def get_document_from_collection(cls, collection_type, doc_id, get_fields = True):
    """To get document from the collection using UUID"""
    try:
      collection = collection_references[collection_type]
      document = collection.find_by_uuid(doc_id)
      if get_fields:
        document_fields = document.get_fields(reformat_datetime=True)
        return document_fields
      return document
    except KeyError:
      return doc_id

  @classmethod
  def loads_field_data_from_collection(cls, document):
    """To fetch the document from the collection using UUID"""
    for key, val in document.items():
      if val:
        if isinstance(val, list):
          document[key] = [
              cls.get_document_from_collection(key, doc_id) for doc_id in val
          ]
        else:
          document[key] = cls.get_document_from_collection(key, val)
    return document

  @classmethod
  def update_many_to_many_relations(
      cls,
      collection_type,
      doc_id,
      doc_prop_name,
      referred_collection_type,
      referred_doc_ids,
      referred_doc_prop_name,
      update_referred_doc: Optional[bool] = False,
      validate_referred_ids: Optional[bool] = False,
      operation: Literal["add", "remove"] = "add"):
    """This function updates referred docs to a document
    Add/remove multiple reference docs to a document
    Example: Add multiple users to the group and update the users simultaniously
    Args:
      collection_type : Type of document to which referred docs should be added ("user_group")
      doc_id : Unique identifier of document to which referred docs should be added (user_group_id)
      doc_prop_name : name of the property in document in which referred docs should be added ("users")
      referred_collection_type : Type of referred docs ("users")
      referred_doc_ids : List of unique identifiers for referred docs (list of user_ids to add to group : [user_id])
      referred_doc_prop_name : name of the property in referred document in which document should be added ("user_groups")
      update_referred_doc : Boolean value to update the referred docs
      validate_referred_ids: Boolean value to vaildate the referred_doc_ids before hand
      operation: Type of action to be performed ("add")
    Returns:
        Updated document
    """
    collection = collection_references[collection_type]
    existing_doc = collection.find_by_uuid(doc_id)
    if validate_referred_ids:
      CollectionHandler.validate_documents(referred_collection_type,
                                           referred_doc_ids)
    doc_fields = existing_doc.get_fields()
    ref_docs = doc_fields.get(doc_prop_name) if doc_fields.get(
        doc_prop_name) else []
    not_found_docs = []
    for child_doc_id in referred_doc_ids:
      try:
        if operation == "add":
          if child_doc_id not in ref_docs:
            cls.update_ref_of_document(referred_collection_type, child_doc_id,
                                       referred_doc_prop_name, doc_id, "add")
            ref_docs.append(child_doc_id)
        else:
          if child_doc_id in ref_docs:
            ref_docs.remove(child_doc_id)
            if update_referred_doc:
              cls.update_ref_of_document(referred_collection_type, child_doc_id,
                                         referred_doc_prop_name, doc_id,
                                         "remove")
      except ResourceNotFoundException:
        not_found_docs.append(child_doc_id)
        #ToDo: return resource-not-found childs in error message
        pass
    setattr(existing_doc, doc_prop_name, ref_docs)
    existing_doc.update()
    doc_fields = existing_doc.get_fields(reformat_datetime=True)
    return doc_fields

  @classmethod
  def update_ref_of_document(cls,
                             collection_type,
                             doc_id,
                             doc_prop_name,
                             referred_doc_id,
                             operation: Literal["add", "remove"] = "add"):
    """Add/removes referred_doc_id to/from document of type collection_type
    Example: add user(user_id) to a user group
    Args:
      collection_type: Type of collection for which the updation to be done ("user_group")
      doc_id: Unique identifier of document to which referred_doc_id should be added or removed (user_group_id)
      doc_prop_name: Name of the property on which the updation is done ("users")
      referred_doc_id : Unique identifier of document which which is to be added/removed (user_id)
      operation : Action Type add or remove"""

    collection = collection_references[collection_type]
    existing_doc = collection.find_by_uuid(doc_id)
    doc_fields = existing_doc.get_fields()
    doc_prop_ids_list = doc_fields.get(doc_prop_name) if doc_fields.get(
        doc_prop_name) else []
    if operation == "add" and referred_doc_id not in doc_prop_ids_list:
      doc_prop_ids_list.append(referred_doc_id)
    elif operation == "remove" and referred_doc_id in doc_prop_ids_list:
      doc_prop_ids_list.remove(referred_doc_id)
    setattr(existing_doc, doc_prop_name, doc_prop_ids_list)
    existing_doc.update()
    doc_fields = existing_doc.get_fields(reformat_datetime=True)
    return doc_fields

  @classmethod
  def validate_documents(cls, collection_type, doc_ids):
    """validates the documents
    Args:
      collection_type: Type of collection
      doc_ids: List of Unique identifier of documents which are to be validated"""
    collection = collection_references[collection_type]
    for doc_id in doc_ids:
      collection.find_by_uuid(doc_id)

  @classmethod
  def remove_doc_from_all_references(cls, doc_to_remove, collection_type,
                                     doc_ids, doc_prop):
    """This function removes the document(doc_to_remove) from linked documents of type(collection_type)
    Example: remove user from all assigned groups
    Args:
      doc_to_remove : Unique identifier of the document to be removed (user_id)
      collection_type : Type of documents from which document should be removed ("usre_groups")
      doc_ids : List of Unique identifier of documents from which doc_to_remove should be removed (list of user_group_ids: [user_group_id])
      doc_prop : name of the property in document from which doc_to_remove should be removed ("users")
    """
    collection = collection_references[collection_type]
    for doc_id in doc_ids:
      try:
        doc = collection.find_by_uuid(doc_id)
        doc_fields = doc.get_fields()
        doc_prop_values = doc_fields.get(doc_prop)
        if doc_prop_values and doc_to_remove in doc_prop_values:
          doc_prop_values.remove(doc_to_remove)
        setattr(doc, doc_prop, doc_prop_values)
        doc.update()
      except ResourceNotFoundException:
        pass

  @classmethod
  def update_existing_references(cls, doc_id, collection_type, doc_prop_name,
                                 updated_refs, existing_refs):
    """ This function compares the updated_refs with the existing_refs and updates the final list of documents.
    It returns the final list of documents after updating the references of documents.
    Example: update groups of a user
    Args:
      doc_id : Unique identifier of the document for which updation is being done (user_id)
      collection_type : Type of the documents for which document should be updated ("user_groups)
      doc_prop_name : Name of the property of document to which the doc_id should be added/removed ("users")
      updated_refs : Updated List of Unique identifier of documents (list of user_group_ids)
      existing_refs : Existing List of Unique identifier of documents (list of user_group_ids)
    """
    value = existing_refs
    if isinstance(updated_refs,list):
      added_refs = list(set(updated_refs) - set(existing_refs))
      for group in added_refs:
        try:
          cls.update_ref_of_document(collection_type, group, doc_prop_name,
                                     doc_id, "add")
          value.append(group)
        except ResourceNotFoundException:
          #ToDo: return resource-not-found childs in error message if needed
          pass

      removed_refs = list(set(existing_refs) - set(updated_refs))
      for group in removed_refs:
        try:
          cls.update_ref_of_document(collection_type, group, doc_prop_name,
                                     doc_id, "remove")
          value.remove(group)
        except ResourceNotFoundException:
          #ToDo: return resource-not-found childs in error message if needed
          value.remove(group)

    return value

  @classmethod
  def get_document(cls, uuid, collection_name, doc_prop: Optional[str] = None):
    """Returns document with the UUID from the collection.
     If doc_prop is provided then returns particular filed of the document"""
    existing_doc = collection_references[collection_name].find_by_uuid(uuid)
    return existing_doc.get_fields(
    )[doc_prop] if doc_prop else existing_doc.get_fields()

  @classmethod
  def remove_del_doc_ref_from_collection(cls, collection_type, doc_prop,
                                         del_doc_id):
    """ This function removes the reference of the deleted doc from oter collections
    Example: remove user from user groups
    Args:
      collection_type : Type of documents from which document should be removed ("user_groups)
      doc_prop : Name of the property of document from which the del_doc_id should be removed ("users")
      del_doc_id : unique identifier of the document to be removed  (user_id)
    """
    collection = collection_references[collection_type]
    collection_manager = collection.collection
    collection_manager = collection_manager.filter(doc_prop, "array_contains",
                                                   del_doc_id).fetch()
    for doc in collection_manager:
      doc_fields = doc.get_fields(reformat_datetime=True)
      doc_prop_values = doc_fields.get("doc_prop") if doc_fields.get(
          "doc_prop") else []
      if del_doc_id in doc_prop_values:
        doc_prop_values.remove(del_doc_id)
      setattr(doc, doc_prop, doc_prop_values)
      doc.update()
