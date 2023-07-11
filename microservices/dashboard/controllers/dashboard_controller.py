"""
    Utility methods for Dashboard operations
"""
from tornado.gen import multi
import tornado.ioloop
from config import COLLECTION
from services.level_mapping_service import get_level_mapping
from services.firestore_service import get_documents, \
  get_document_by_id, get_leaf_document, check_session_exists
from utils.exception_handler import InvalidContextError
from common.utils.logging_handler import Logger


# pylint: disable=Catching too general exception Exception (broad-except)
# pylint: disable= consider-using-f-string
def get_document_list(collection_name, add_ref=False):
  """
            Returns list of all documents from collection passed in parameter
            Args:
                collection_name: String
                add_ref: Boolean(default False)
            Returns:
                doc_list: List of Dict
        """
  doc_list = list(get_documents(collection_name))
  if add_ref:
    return_list = list(
      map(lambda x: {
        **x.to_dict(), "context_ref": x.reference
      }, doc_list))
  else:
    return_list = list(map(lambda x: x.to_dict(), doc_list))
  return return_list


def remove_context_ref(doc):
  """
            Deletes context_ref key from object passed in paramater
            Args:
                doc: Dict
            Returns:
                doc: Dict
        """
  del doc["context_ref"]
  return doc


def add_context_path(doc):
  """
            Changes type of context_ref from DocumentReference to String
            Args:
                doc: Dict
            Returns:
                doc: Dict
        """
  doc["context_ref"] = doc["context_ref"]
  return doc


async def get_session_details(doc_list, req_body, user_id):
  """
            For every sub-competency/module in doc_list, checks if there is any
            active session associated, then adds session_details to that
            subcompetency/module else adds session_details as null
            and Returns same doc_list
            Args:
                doc_list: List of Dict
                req_body: Dict
                user_id: String
            Returns:
                doc_list: List of Dict

  """
  return_list = []
  course_ref = "course/{}".format(req_body["course_id"])
  competency_ref = "competencies/{}".format(req_body["competency_id"])
  session_filters = {"user_id": user_id, "is_active": True,
                     "course_ref": course_ref, "competency_ref": competency_ref}
  try:
    sessions = await multi([
      tornado.ioloop.IOLoop.current().run_in_executor(
        None, check_session_exists, COLLECTION, {
          **session_filters, "context_ref":
            "sub_competencies/{}".format(doc["id"])
        }) for doc in doc_list
    ])
  except Exception as e:
    Logger.error(f"No Sub-Competencies are found for this competency {e}")
    return []

  if "completed" in req_body.keys() and req_body["completed"] is True:
    idx = 0
    for doc in doc_list:
      if sessions[idx] and \
        sessions[idx][0].to_dict()["completed_percentage"] >= 100:
        doc["session_details"] = {
          **add_context_path(sessions[idx][0].to_dict()),
          "session_id": sessions[idx][0].id
        }
        return_list.append(doc)
      idx += 1

  elif "completed" in req_body.keys() and req_body["completed"] is False:
    idx = 0
    for doc in doc_list:
      if sessions[idx]:
        session_details = sessions[idx][0].to_dict()
        if session_details["completed_percentage"] < 100:
          doc["session_details"] = {
            **add_context_path(session_details), "session_id":
              sessions[idx][0].id
          }
          return_list.append(doc)
      else:
        doc["session_details"] = None
        return_list.append(doc)
      idx += 1

  else:
    idx = 0
    for doc in doc_list:
      if sessions[idx]:
        session_details = sessions[idx][0].to_dict()
        doc["session_details"] = {
          **add_context_path(session_details), "session_id":
            sessions[idx][0].id
        }
        return_list.append(doc)
      else:
        doc["session_details"] = None
        return_list.append(doc)
      idx += 1

  return return_list


async def get_dashboard_items(req_body, user_id):
  """
            This method handles all the 3 cases of context coming from LMS
            and Returns 3 level hierarchy data of dashboard accordingly
            Args:
                req_body: Dict
                user_id: String
            Returns:
                dashboard_items: Dict
        """
  level = get_level_mapping(req_body["type"])
  context_filters = {
    "label": req_body["label"],
    "type": req_body["type"],
    "title": req_body["title"]
  }
  return_obj = {}
  if level == "level0":
    doc_list = list(get_leaf_document(level, context_filters))
    if len(doc_list) == 0:
      raise InvalidContextError("Invalid Context")
    doc = doc_list[0].to_dict()
    doc["level1"] = get_document_list("level0/{}/level1".format(doc_list[0].id))
    return_obj["level0"] = []
    return_obj["level0"].append(doc)
  else:
    doc_list = list(get_leaf_document(level, context_filters))
    if len(doc_list) == 0:
      raise InvalidContextError("Invalid Context")
    context_ref = doc_list[0].reference
    path = context_ref.path.split("/")
    path_list = path if level == "level1" else path[0:-2]
    path = "/".join(path_list)
    level0_data, level1_data, level2_data = await multi([
      tornado.ioloop.IOLoop.current().run_in_executor(None,
                                                      get_document_by_id,
                                                      path_list[0],
                                                      path_list[1]),
      tornado.ioloop.IOLoop.current().run_in_executor(
        None, get_document_by_id, "/".join(path_list[0:3]), path_list[3]),
      tornado.ioloop.IOLoop.current().run_in_executor(
        None, get_document_list, "{}/level2".format(path), True)
    ])

    level0_data = [level0_data.to_dict()]
    level1_data = [level1_data.to_dict()]
    level2_data = await get_session_details(level2_data, req_body, user_id)
    level1_data[0]["level2"] = level2_data
    level0_data[0]["level1"] = level1_data
    return_obj["level0"] = level0_data
  return {**return_obj, "context": req_body}
