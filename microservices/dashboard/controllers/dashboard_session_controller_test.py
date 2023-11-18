"""
    utility methods to execute unit tests for module
    dashboard_session_controller.py
"""
# pylint: disable=wrong-import-position
import mock
import time
import uuid
from config import ACTIVITY_ID
import sys

sys.path.append("../../common/src")
from controllers.dashboard_session_controller import (get_default_session_obj,
                                                      manage_session_creation,
                                                      manage_session_update)

body = {
  "competency_ref": "Sub-Competency",
  "course_ref": "socialogy",
  "context_ref": "sub_competencies/1234qwqeer"
}


class MockDocumentReference:

  def __init__(self, path):
    self.path = path

  def to_str(self):
    return self.path


class MockDocumentSnapshot:

  def __init__(self, data):
    self.data = data

  def to_dict(self):
    return dict(self.data)


class MockSessionDoc:

  def __init__(self):
    self.data = body

  def to_dict(self):
    return dict(self.data)

def test_get_default_session_obj():
  session_obj = get_default_session_obj()
  assert session_obj is not None
  assert session_obj["completed_percentage"] == 0
  assert session_obj["is_active"] is True
  assert session_obj["start_time"] > 0
  assert session_obj["activity_id"] == ACTIVITY_ID


@mock.patch("controllers.dashboard_session_controller.insert_document")
@mock.patch("controllers.dashboard_session_controller.get_default_session_obj")
def test_manage_session_creation(mock_session_obj, mock_insert_document):
  # arrange
  default_obj = {
    "completed_percentage": 0,
    "is_active": True,
    "start_time": time.time(),
    "activity_id": ACTIVITY_ID
  }
  mock_session_obj.return_value = default_obj
  user_id = str(uuid.uuid4())
  doc_id = str(uuid.uuid4())
  path = "level0/abc/level1/pqr/level2/xyz"
  mock_insert_document.return_value = doc_id
  context_ref = MockDocumentReference(path).to_str()
  # action
  session_data = manage_session_creation(user_id, context_ref, body)

  # assert
  assert session_data is not None
  assert session_data["session_id"] == doc_id
  assert session_data["user_id"] == user_id
  assert session_data["context_ref"] == path


@mock.patch("controllers.dashboard_session_controller.update_document")
@mock.patch("controllers.dashboard_session_controller.get_document_by_id")
@mock.patch("controllers.dashboard_session_controller.delete_key")
@mock.patch(
  "controllers.dashboard_session_controller.is_archived_the_session_notes")
def test_manage_session_update(mock_update_document, mock_get_document_by_id,
                               mock_delete_key,
                               mock_is_archived_the_session_notes):
  # arrange
  req_body = {"session_id": str(uuid.uuid4()), "is_active": False}
  user_id = "q1w23eewwewe"
  mock_is_archived_the_session_notes.return_value = {
    "is_active": False,
    "is_deleted": True,
    "updated_at": time.time()
  }
  mock_update_document.return_value = {
    "is_active": False,
    "updated_at": time.time()
  }
  mock_get_document_by_id.return_value = MockSessionDoc()
  mock_delete_key.return_value = MockSessionDoc()
  # action
  update_resp = manage_session_update(req_body, user_id)
  # assert
  assert update_resp is not None
  assert update_resp["is_active"] is False
  assert update_resp["updated_at"] > 0
