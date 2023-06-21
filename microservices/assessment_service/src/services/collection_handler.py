"""Functions to fetch the collection using
the UUID of the object
"""
import traceback
from common.utils.collection_references import collection_references
from common.utils.errors import (ResourceNotFoundException)
from common.utils.logging_handler import Logger

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
    for key, _ in document.items():
      if key == "references" and document.get(key, {}):
        for ref_key, ref_val in document.get(key, {}).items():
          try:
            if ref_key in ["competencies", "skills"]:
              document[key][ref_key] = [
                cls.get_document_from_collection(
                ref_key, doc_id) for doc_id in ref_val
            ]
          except ResourceNotFoundException as e:
            Logger.error(e)
            Logger.error(traceback.print_exc())
    return document
