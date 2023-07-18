""" Developer APIs """
import os
import traceback
from google.cloud import firestore
from fastapi import APIRouter
from config import ERROR_RESPONSES
from schemas.developer_api_schema import BasicUpdateModel
from common.utils.logging_handler import Logger
from common.utils.http_exceptions import InternalServerError

router = APIRouter(tags=["Developer API"], responses=ERROR_RESPONSES)

project_id = os.getenv("GCP_PROJECT", "aitutor-dev")


@router.put("/update-fields", include_in_schema=False)
def update_collection_fields(request: BasicUpdateModel):
  """
  Update fields of a given collection 

  Args:
    collection_name (str): Name of the collection
    fields(list): list of fields

  """
  try:
    fields = request.fields
    collection_name = request.collection_name

    db = firestore.Client(project=project_id)
    datamodel_ref = db.collection(collection_name)

    result = {}
    for field in fields:
      field = field.dict()
      key = field["key"]

      updated_fields = []
      if field["existing_value"] is not None:
        docs = datamodel_ref.where(field["key"], "==", field[
                                            "existing_value"]).stream()
      else:
        docs = datamodel_ref.stream()

      #delete field
      if field["delete_key"] is True:
        Logger.info(f"Deleting field {key}")
        for doc in docs:
          doc = doc.to_dict()
          datamodel_ref.document(doc["uuid"]).update({
                                  key: firestore.DELETE_FIELD})
          updated_fields.append(doc["uuid"])
        result[key] = updated_fields

      #update field
      else:
        Logger.info(f"Updating field {key}")
        for doc in docs:
          doc = doc.to_dict()
          doc[key] = field["new_value"]
          datamodel_ref.document(doc["uuid"]).set(doc)
          updated_fields.append(doc["uuid"])
        result[key] = updated_fields

    return {
        "success": True,
        "message": f"Successfully updated the DataModel {collection_name}",
        "data": result
    }
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
