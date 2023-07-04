"""
    utility methods to execute unit tests for module dashboard_controller.py
"""
# pylint: disable=wrong-import-position
import pytest
import mock
import time
import sys

sys.path.append("../../common/src")
with mock.patch("google.cloud.logging.Client",
side_effect=mock.MagicMock()) as mok:
  from controllers.dashboard_controller import (get_document_list,
                                                remove_context_ref,
                                                get_session_details,
                                                get_dashboard_items)

context_ref = "level0/abc/level1/pqr/level2/xyz"
user_id = "BU3ol5C50OVWbhcwj1eXEByjzyQ2"
docs = [{
  "id": "12345",
  "is_active": True,
  "start_time": time.time()},
  {
    "id": "12345",
    "is_active": True,
    "completed_percentage": 0,
    "start_time": time.time()},
  {
    "id": "12345",
    "is_active": False,
    "completed_percentage": 100,
    "start_time": time.time()
  }]


class MockReference:

  def __init__(self, path):
    self.path = path


class MockDocumentReference:

  def __init__(self, data, path, reference=None):
    self.data = data
    self.path = path
    self.reference = reference

  def to_dict(self):
    return dict(self.data)


class MockLeapDocument:

  def __init__(self, data, path, reference=None, leap_id=None):
    self.data = data
    self.path = path
    self.reference = reference
    self.id = leap_id

  def to_dict(self):
    return dict(self.data)


class SessionDetails:

  def __init__(self, data, ses_id=None):
    self.data = data
    self.id = ses_id

  def to_dict(self):
    return dict(self.data)


class DocById:

  def __init__(self, data):
    self.data = data

  def to_dict(self):
    return dict(self.data)


def get_leap_doc():
  """Function to get leap document"""
  yield MockLeapDocument(
    docs[0],
    path=context_ref,
    reference=MockReference(context_ref),
    leap_id=user_id)
  yield MockLeapDocument(
    docs[0],
    path=context_ref,
    reference=MockReference(context_ref),
    leap_id=user_id)
  yield MockLeapDocument(
    docs[0],
    path=context_ref,
    reference=MockReference(context_ref),
    leap_id=user_id)


def get_docs():
  yield MockDocumentReference(docs[0], context_ref)
  yield MockDocumentReference(docs[0], context_ref)
  yield MockDocumentReference(docs[0], context_ref)


def get_docs_with_ref():
  yield MockDocumentReference(docs[0], context_ref, context_ref)
  yield MockDocumentReference(docs[0], context_ref, context_ref)
  yield MockDocumentReference(docs[0], context_ref, context_ref)


@pytest.mark.parametrize("doc", [{
  "context_ref": context_ref},
  {
    "is_active": True,
    "context_ref": ""
  }])
def test_remove_context_ref(doc):
  doc = remove_context_ref(doc)
  assert "context_ref" not in doc


@mock.patch("controllers.dashboard_controller.get_documents")
def test_get_document_list(mock_get_documents):
  # arrange
  collection_name = "sessions"
  mock_get_documents.return_value = get_docs()
  # action
  doc_list = get_document_list(collection_name)
  # assert
  assert len(doc_list) == 3
  assert "context_ref" not in doc_list[0]
  assert "context_ref" not in doc_list[1]
  assert "context_ref" not in doc_list[2]


@mock.patch("controllers.dashboard_controller.get_documents")
def test_get_document_list_add_ref(mock_get_documents):
  # arrange
  collection_name = "sessions"
  mock_get_documents.return_value = get_docs_with_ref()
  # action
  doc_list = get_document_list(collection_name, True)
  # assert
  assert len(doc_list) == 3
  assert "context_ref" in doc_list[0]
  assert "context_ref" in doc_list[1]
  assert "context_ref" in doc_list[2]


@pytest.mark.asyncio
@pytest.mark.parametrize("request_body", [
  {
    "competency_id": "1121212",
    "completed": False,
    "course_id": "123",
    "subcompetency_id": ""
  }])
@mock.patch("controllers.dashboard_controller.check_session_exists")
@mock.patch("controllers.dashboard_controller.COLLECTION")
async def test_get_session_details(mock_check_session_exists, mock_collection,
                                   request_body):
  doc_list = docs
  mock_check_session_exists.side_effect = [[], [], []]
  mock_collection.side_effect = mock_check_session_exists
  result = await get_session_details(doc_list, request_body, user_id)
  assert result[0]["session_details"] is None


@pytest.mark.asyncio
@pytest.mark.parametrize("request_body", [{
  "competency_id": "1121212",
  "completed": False,
  "course_id": "123",
  "subcompetency_id": ""
  }])
@mock.patch("controllers.dashboard_controller.check_session_exists")
@mock.patch("controllers.dashboard_controller.COLLECTION")
async def test_get_session_details_not_completed_with_session(
  mock_check_session_exists, mock_collection, request_body):
  doc_list = docs
  data = {
    "start_time": 1622026257.0947058,
    "context_ref": MockReference(context_ref),
    "is_active": True,
    "user_id": "BU3ol5C50OVWbhcwj1eXEByjzyQ2",
    "activity_id": "teachme",
    "completed_percentage": 0
  }
  result_series = SessionDetails(data=data, ses_id=user_id)
  mock_check_session_exists.side_effect = [[result_series], [], []]
  mock_collection.side_effect = mock_check_session_exists
  result = await get_session_details(doc_list, request_body, user_id)
  assert result[0]["session_details"] is not None
  assert result[1]["session_details"] is None
  assert result[2]["session_details"] is None


@pytest.mark.asyncio
@pytest.mark.parametrize("request_body", [{
  "competency_id": "1121212",
  "completed": False,
  "course_id": "123",
  "subcompetency_id": ""
  }])
@mock.patch("controllers.dashboard_controller.check_session_exists")
@mock.patch("controllers.dashboard_controller.COLLECTION")
async def test_get_session_details_without_session(mock_check_session_exists,
                                                   mock_collection,
                                                   request_body):
  doc_list = docs
  mock_check_session_exists.side_effect = [[], [], []]
  mock_collection.side_effect = mock_check_session_exists
  result = await get_session_details(doc_list, request_body, user_id)
  assert result[0]["session_details"] is None
  assert result[1]["session_details"] is None
  assert result[2]["session_details"] is None


@pytest.mark.asyncio
@pytest.mark.parametrize("collection_name", [{
  "collection_name": "session"},
  {
  "collection_name": "sessions"
  }])
@mock.patch("controllers.dashboard_controller.get_leaf_document")
@mock.patch("controllers.dashboard_controller.get_documents")
@mock.patch("controllers.dashboard_controller.get_level_mapping")
async def test_get_dashboard_items_level_0_success(mock_get_level_mapping,
                                                   mock_get_leap_document,
                                                   mock_get_documents,
                                                   collection_name):
  request_body = {
    "id": "",
    "label": "PV001",
    "type": "http://purl.imsglobal.org/vocab/lis/v2/course",
    "title": "PV001: History and Evolution of the Early",
    "completed": False
  }
  mock_get_level_mapping.return_value = "level0"
  mock_get_documents.return_value = get_leap_doc()
  doc = get_document_list(collection_name, add_ref=True)
  mock_get_leap_document.return_value = doc
  result = await get_dashboard_items(request_body, user_id)
  assert len(result) == 2
  assert result["level0"][0]["is_active"] is True


@pytest.mark.asyncio
@pytest.mark.parametrize("collection_name", [{
  "collection_name": "session"},
  {
  "collection_name": "sessions"
  }])
@mock.patch("controllers.dashboard_controller.get_session_details")
@mock.patch("controllers.dashboard_controller.get_document_by_id")
@mock.patch("controllers.dashboard_controller.get_leaf_document")
@mock.patch("controllers.dashboard_controller.get_documents")
@mock.patch("controllers.dashboard_controller.get_level_mapping")
async def test_get_dashboard_items_level_1_success(
  mock_get_level_mapping, mock_get_leap_document, mock_get_documents,
  mock_get_document_by_id, mock_get_session_details, collection_name):
  request_body = {
    "id": "",
    "label": "PV001",
    "type": "http://purl.imsglobal.org/vocab/lis/v2/course",
    "title": "PV001: History and Evolution of the Early",
    "completed": False
  }
  mock_get_level_mapping.return_value = "level1"
  mock_get_documents.return_value = get_leap_doc()
  doc = get_document_list(collection_name, add_ref=True)
  mock_get_leap_document.return_value = doc
  mock_get_document_by_id.return_value = DocById(docs[0])
  data = {
    "start_time": 1622026257.0947058,
    "context_ref": MockReference(context_ref),
    "is_active": True,
    "user_id": "BU3ol5C50OVWbhcwj1eXEByjzyQ2",
    "activity_id": "teachme",
    "completed_percentage": 0
  }
  result_series = SessionDetails(data=data, ses_id=user_id)
  mock_get_session_details.return_value = [[result_series], [], []]
  result = await get_dashboard_items(request_body, user_id)
  assert result["context"] == request_body


@pytest.mark.asyncio
@pytest.mark.parametrize("collection_name", [{
  "collection_name": "session"},
  {
  "collection_name": "sessions"
  }])
@mock.patch("controllers.dashboard_controller.get_session_details")
@mock.patch("controllers.dashboard_controller.get_document_by_id")
@mock.patch("controllers.dashboard_controller.get_leaf_document")
@mock.patch("controllers.dashboard_controller.get_documents")
@mock.patch("controllers.dashboard_controller.get_level_mapping")
async def test_get_dashboard_items_level_1_success_without_session(
  mock_get_level_mapping, mock_get_leap_document, mock_get_documents,
  mock_get_document_by_id, mock_get_session_details, collection_name):
  request_body = {
    "id": "",
    "label": "PV001",
    "type": "http://purl.imsglobal.org/vocab/lis/v2/course",
    "title": "PV001: History and Evolution of the Early",
    "completed": False
  }
  mock_get_level_mapping.return_value = "level1"
  mock_get_documents.return_value = get_leap_doc()
  doc = get_document_list(collection_name, add_ref=True)
  mock_get_leap_document.return_value = doc
  mock_get_document_by_id.return_value = DocById(docs[0])
  mock_get_session_details.return_value = [[], [], []]
  result = await get_dashboard_items(request_body, user_id)
  assert result["context"] == request_body
