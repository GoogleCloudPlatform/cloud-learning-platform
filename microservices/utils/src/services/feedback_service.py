"""Utility methods to handle feedback data"""
from services.firestore_service import get_documents,\
    save_feedback_doc, save_inline_feedback_doc
from services.session_service import get_session_response
from common.utils.logging_handler import Logger


def get_feedback_options(collection_path):
  """Method to handle fetched feedback data"""
  try:
    docs = get_documents(collection_path)
    return_list = []
    for doc in docs:
      data = doc.to_dict()
      data["question_ref"] = doc.reference.path
      return_list.append(data)
    return {"items": return_list}
  except Exception as err:  # pylint: disable=broad-except
    return err


def save_feedback(collection_path, sub_collection, req_data, user_id):
  """Method which handles saving feedback"""
  try:
    if req_data["session_id"] != "":
      session_response = get_session_response(req_data["session_id"],
                                              req_data["token"])
      if session_response["message"] == "INVALID_SESSION_ID":
        req_data["context_ref"] = ""
      else:
        req_data["context_ref"] =\
            session_response["data"]["context_ref"]
    else:
      req_data["context_ref"] = ""
    del req_data["session_id"]
    del req_data["token"]
    doc_id = save_feedback_doc(collection_path, sub_collection, req_data,
                               user_id)
    return doc_id

  except Exception as err:  # pylint: disable=broad-except
    Logger.info(err)
    return err


def save_inline_feedback(collection_path, sub_collection, req_data, user_id):
  """
    Method which handles data in saving
    inline feedback
    """
  try:
    doc_id = save_inline_feedback_doc(collection_path, sub_collection, req_data,
                                      user_id)
    return doc_id

  except Exception as err:  # pylint: disable=broad-except
    return err
