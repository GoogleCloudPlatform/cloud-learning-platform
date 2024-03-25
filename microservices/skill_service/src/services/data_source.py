"""
  Service for Creating, Updating and Deleting data sources:
"""
from common.models import DataSource
from common.utils.errors import ResourceNotFoundException
# pylint: disable = broad-except


def get_data_sources(object_type):
  """
  Method to get data source from firestore for the object_type.
  If object_type is None, it will return list of all docs in DataSource
  collection from firestore.
  Args:
    object_type (str): type of object eg. skill, role, etc.
  Returns:
    data_sources (dict): Object Type, its sources and corresponding
                            index id in matching engine
  """
  response = []
  if object_type:
    data_source_obj = DataSource.find_by_type(object_type)
    response.append(
      {
        "type": data_source_obj.type,
        "source": data_source_obj.source,
        "matching_engine_index_id": data_source_obj.matching_engine_index_id
      })
  else:
    data_source_collection = DataSource.collection.fetch()
    for data_source in data_source_collection:
      response.append(
        {
          "type": data_source.type,
          "source": data_source.source,
          "matching_engine_index_id": data_source.matching_engine_index_id
        })
  return response


def upsert_data_source_doc(object_type, input_source):
  """This function will add the data source for given input object to firestore
  if it does not exist. If document for exist then it will update the doc with
  its sources.

  Args:
      obj_type (str): input object type for which data source doc to be created
      input_source: (str) - new source to be updated/inserted

  Raises:
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      message: (str) - Successfully created the data sources
  """
  try:
    existing_source = DataSource.find_by_type(object_type)
    if existing_source:
      source_fields = existing_source.get_fields()
      source_list = source_fields["source"]
      if input_source not in source_list:
        source_list.append(input_source)
      setattr(existing_source, "source", source_list)
      existing_source.update()
      source_fields = existing_source.get_fields(reformat_datetime=True)
      return {
          "success": True,
          "message": "Successfully updated the data source",
          "data": source_fields
      }

  except ResourceNotFoundException:
    new_data_source = DataSource()
    new_data_source.type = object_type
    new_data_source.source = [input_source]
    new_data_source.matching_engine_index_id = {}
    new_data_source.save()
    source_fields = new_data_source.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully created the data source",
        "data": source_fields
    }

  except Exception as e:
    response = {"success": False, "message": str(e), "data": {}}
    return response


def update_data_source_fields(object_type, input_source, matching_engine_id):
  """Updates matching_engine_index_id fields of data source document for given
    object type and its source.

  Args:
      object_type: (str) - object for which field is to be updated
      input_source: (str) - new source to be updated
      matching_engine_id: (str) - new matching engine ID to be updated

  Raises:
      ResourceNotFoundException: If the data source does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      message: (str) - Success/Failure & updated fields
  """
  try:
    if input_source.startswith(object_type):
      input_source = input_source.replace(object_type + "_", "")
    existing_source = DataSource.find_by_type(object_type)
    source_fields = existing_source.get_fields()
    source_list = source_fields["source"]
    index_id_dict = source_fields["matching_engine_index_id"]
    if input_source not in source_list:
      source_list.append(input_source)
      setattr(existing_source, "source", source_list)
    index_id_dict[input_source] = matching_engine_id
    setattr(existing_source, "matching_engine_index_id", index_id_dict)
    existing_source.update()
    source_fields = existing_source.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully updated the data source",
        "data": source_fields
    }

  except ResourceNotFoundException:
    index_id_dict = {}
    index_id_dict[input_source] = matching_engine_id
    new_data_source = DataSource()
    new_data_source.type = object_type
    new_data_source.source = [input_source]
    new_data_source.matching_engine_index_id = index_id_dict
    new_data_source.save()
    source_fields = new_data_source.get_fields(reformat_datetime=True)
    return {
        "success": True,
        "message": "Successfully update the data source",
        "data": source_fields
    }

  except Exception as e:
    response = {"success": False, "message": str(e), "data": {}}
    return response


def delete_data_source(obj_type, input_source=None, matching_engine_id=None):
  """Deletes either source and index or source or whole document from
    firestore for given type from data_sources collection depending on input

  Args:
      obj_type (str): type of object for which doc is to be deleted
      input_source (str): source for which index id and source to delete
      matching_engine_id (str): index id to be deleted
  Raises:
      ResourceNotFoundException: If the doc for given obj_type does not exist
      Exception: 500 Internal Server Error if something goes wrong

  Returns:
      response: Success/Fail Message
  """
  try:
    existing_source = DataSource.find_by_type(obj_type)
    source_fields = existing_source.get_fields()
    source_list = source_fields["source"]
    index_id_dict = source_fields["matching_engine_index_id"]

    if matching_engine_id: #Delete only matching engine ID
      for key, value in index_id_dict.items():
        if value == matching_engine_id:
          source = key
          break
      if source:
        del index_id_dict[source]
      setattr(existing_source, "matching_engine_index_id", index_id_dict)
      existing_source.update()

    elif input_source: #delete source and matching engine ID
      if input_source in source_list:
        source_list.remove(input_source)
      setattr(existing_source, "source", source_list)
      if input_source in index_id_dict.keys():
        del index_id_dict[input_source]
      setattr(existing_source, "matching_engine_index_id", index_id_dict)
      existing_source.update()

    else: #delete entire document for given obj_type
      DataSource.collection.delete(existing_source.key)

    return {"success": True, "message": "Successfully deleted the data source"}

  except ResourceNotFoundException as e:
    response = {"success": False, "message": str(e), "data": {}}
    return response

  except Exception as e:
    response = {"success": False, "message": str(e), "data": {}}
    return response
