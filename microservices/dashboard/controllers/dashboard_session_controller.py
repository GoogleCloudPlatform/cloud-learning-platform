"""
    Utility methods for Session management
"""
import time
import tornado.ioloop

from typing import Union

from config import ACTIVITY_ID, COLLECTION, DATABASE_PREFIX
from services.firestore_service import get_document_by_id, \
  insert_document, check_session_exists, update_document
from services.notes_service import is_archived_the_session_notes
from services.course_ingestion_service import fetch_competency, \
  fetch_subcompetency, get_course
from utils.exception_handler import InvalidSessionIdError
from common.utils.logging_handler import Logger
from common.utils.cache_service import set_key, get_key, delete_key


# pylint: disable= consider-using-f-string
def get_default_session_obj():
  """
        Sets default values to session_object and Returns it
        Args:
            None
        Returns:
            default session obj: Dict
    """
  session_obj = {
    "completed_percentage": 0,
    "is_active": True,
    "start_time": time.time(),
    "activity_id": ACTIVITY_ID
  }
  return session_obj


def type_mapping(comp_type, doc):
  """
        Sets type to doc and Returns it
        Args:
            None
        Returns:
            default obj: Dict
    """
  if comp_type == "Units":
    doc["type"] = "Modules"
    return doc
  elif comp_type == "competency":
    doc["type"] = "Subcompetency"
    return doc
  doc["type"] = "Subcompetency"
  return doc


async def get_course_details(ref_details):
  """
        Fetches 3 level data from firestore and Return as a list
        Args:
            doc_path: String
        Returns:
            course_details: Dict
    """
  temp_ref = {
    "course_id": ref_details["course_ref"].split("/")[1],
    "competency_id": ref_details["competency_ref"].split("/")[1],
    "subcompetency_id": ref_details["subcompetency_ref"].split("/")[1]
  }
  subcompetency_det = await tornado.ioloop.IOLoop.current().run_in_executor(
    None, fetch_subcompetency, temp_ref)
  del temp_ref["subcompetency_id"]

  competency_det = await tornado.ioloop.IOLoop.current().run_in_executor(
    None, fetch_competency, temp_ref)
  course_det = await tornado.ioloop.IOLoop.current().run_in_executor(
    None, get_course, temp_ref["course_id"])

  # TODO if "type" present in db, remove this
  subcompetency_det = type_mapping(competency_det["data"]["type"],
                                   subcompetency_det["data"])

  course_details = [{
    "level0": course_det["data"]
  }, {
    "level1": competency_det["data"]
  }, {
    "level2": subcompetency_det
  }]
  return course_details


def manage_session_creation(user_id, context_ref, body):
  """
        Takes SubCompetency or Modules details from request body and
        creates a new session for user, finally Returns session details
        including session_id
        Args:
            user_id: String
            context_ref: Dict
        Returns:
            session details: Dict
    """
  session_data = {
    **get_default_session_obj(), "user_id": user_id,
    "context_ref": context_ref,
    "competency_ref": body["competency_ref"],
    "course_ref": body["course_ref"]
  }

  session_id = insert_document(COLLECTION, session_data)
  session_data["session_id"] = session_id
  session_data["context_ref"] = context_ref
  return session_data


async def manage_session_retrieval(session_id, user_id):
  """
        Fetches a session document from COLLECTION_NAME using session_id
        and Returns it,Throws error if no session found or that session
        doesn"t belong to that user
        Args:
            session_id: String
            user_id: String
        Returns:
            session details: Dict
    """
  Logger.info("Initiating Firestore Connection")
  session_data = get_document_by_id(COLLECTION, session_id).to_dict()
  if session_data is None or session_data["user_id"] != user_id:
    raise InvalidSessionIdError("INVALID_SESSION_ID")

  ref_details = {
    "competency_ref": session_data["competency_ref"],
    "course_ref": session_data["course_ref"],
    "subcompetency_ref": session_data["context_ref"]
  }
  doc_path = session_data["context_ref"]
  course_details = get_key(doc_path)
  if course_details is None:
    course_details = await get_course_details(ref_details)
    cached_status = set_key(doc_path, course_details, 7200)
    Logger.info(
      "Storing course details in cache status {}".format(cached_status))
  session_data["course_details"] = course_details
  return session_data


def manage_session_update(req_body, user_id):
  """
        Takes session_id, completed_percentage, is_active from req body
        and updates completed_percentage, ia_active in session details
        Args:
            req_body: Dict
            user_id: str
        Returns:
            update_resp: Dict
    """
  session_id = req_body["session_id"]
  if "session_id" in req_body:
    del req_body["session_id"]
  update_resp = update_document(COLLECTION, session_id, req_body)
  sess_data = get_document_by_id(COLLECTION, session_id).to_dict()
  sub_comp_id = sess_data["context_ref"].split("/")[1]
  delete_key(sub_comp_id)
  if "is_active" in req_body.keys():
    if not req_body["is_active"]:
      is_archived_the_session_notes(session_id=session_id, user_id=user_id)
  return update_resp


def manage_session(req_body, user_id) -> Union[dict, str]:
  """
  This method handles 3 scenarios.
  1. Create a New Session if the doesn't exist already and returns session
  details.
  2. If already created session is not completed, return that session details.
  3. Marks 100% completed session as inactive(is_active=False) and if the user
  tries to restart the session, it will create new session.
  param req_body: dict
  param user_id: str
  return: dict/str
  """
  context_ref = f"{DATABASE_PREFIX}sub_competencies/{req_body['id']}" if \
    DATABASE_PREFIX != "" else f"sub_competencies/{req_body['id']}"

  body = {
    "competency_ref": req_body["ref_details"]["competency_ref"],
    "course_ref": req_body["ref_details"]["course_ref"]
  }

  session_filter = {
    "competency_ref": req_body["ref_details"]["competency_ref"],
    "course_ref": req_body["ref_details"]["course_ref"],
    "context_ref": context_ref,
    "user_id": user_id,
    "is_active": True
  }

  previous_sessions = check_session_exists(COLLECTION, session_filter)

  if not previous_sessions:
    return manage_session_creation(user_id=user_id, context_ref=context_ref,
                                   body=body)

  elif previous_sessions:
    ses_data = previous_sessions[0].to_dict()
    if ses_data["completed_percentage"] < 100:
      res = {"session_id": previous_sessions[0].id, **ses_data}

    elif ses_data["completed_percentage"] >= 100:
      updated_data = {"is_active": False, "end_time": time.time()}
      is_archived_the_session_notes(session_id=previous_sessions[0].id,
                                    user_id=user_id)
      update_document(COLLECTION, previous_sessions[0].id, updated_data)
      return manage_session_creation(user_id=user_id, context_ref=context_ref,
                                     body=body)

    else:
      res = "Failed to fetch session details"

    return res

  else:
    return "Failed to fetch previous sessions"
