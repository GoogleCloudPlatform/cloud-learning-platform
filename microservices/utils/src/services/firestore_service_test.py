"""Test cases for firestore service. """
import unittest
from unittest import mock
import uuid

from services import firestore_service

TEST_UUID = uuid.uuid4()


class FirestoreServicesTest(unittest.TestCase):

  @mock.patch.object(
      firestore_service, "uuid4", autospec=True, return_value=TEST_UUID)
  def test_get_doc_id(self, mock_uuid4):
    """Duplicate test case for firestore get doc id."""
    # Run.
    test_doc_id = firestore_service.get_doc_id()

    # Assert.
    mock_uuid4.assert_called_once()
    assert test_doc_id == str(TEST_UUID)

  @mock.patch("google.auth")
  @mock.patch("services.firestore_service.firestore.Client")
  def test_get_firestore_instance(self, mock_firestore, mock_auth_client):
    """Duplicate test case for firestore get firestore instance."""
    # Assign.
    mock_firestore.return_value = "TEST_DB"
    mock_auth_client.default.return_value = ["test_cred", "test_project"]

    # Run.
    test_firestore_instance = firestore_service.get_firestore_instance()

    # Assert.
    mock_firestore.assert_called_once_with(
        project="test_project", credentials="test_cred")
    assert test_firestore_instance == "TEST_DB"

  @mock.patch("services.firestore_service.get_firestore_instance")
  def test_get_documents(self, mock_firestore_service):
    """Duplicate test case for firestore get documents."""
    # Assign.
    mock_firestore_service().collection.return_value = mock.MagicMock()
    mock_firestore_service().collection().get.return_value = "TEST_DOCS"
    expected_value = "TEST_DOCS"

    # Run.
    actual = firestore_service.get_documents("TEST_COLLECTION_NAME")

    # Assert.
    mock_firestore_service().collection.assert_called_with(
        "TEST_COLLECTION_NAME")
    self.assertEqual(actual, expected_value)

  @mock.patch("services.firestore_service.get_firestore_instance")
  def test_get_paginated_topic_documents(self, mock_firestore_service):

    # Assign.
    mock_firestore_service().collection.return_value = mock.MagicMock()
    mock_firestore_service().collection().where(
    ).limit.return_value = mock.MagicMock()
    mock_firestore_service().collection().where().limit(
    ).offset = mock.MagicMock()
    mock_firestore_service().collection().where.return_value = mock.MagicMock()
    mock_firestore_service().collection().where().limit().offset(
    ).get.return_value = "TEST_DOCS"
    expected_value = "TEST_DOCS"

    # Run.
    actual = firestore_service.get_paginated_topic_documents(
        "TEST_COLLECTION_NAME", "TEST_TOPIC", 1)

    # Assert.
    mock_firestore_service().collection.assert_called_with(
        "TEST_COLLECTION_NAME")
    mock_firestore_service().collection().where.assert_called_with(
        "topic", "==", "TEST_TOPIC")
    mock_firestore_service().collection().where().limit.assert_called_with(10)
    mock_firestore_service().collection().where().limit(
    ).offset.assert_called_with(0)
    self.assertEqual(actual, expected_value)

  @mock.patch("services.firestore_service.get_firestore_instance")
  def test_get_paginated_documents(self, mock_firestore_service):
    # Assign.
    mock_firestore_service().collection.return_value = mock.MagicMock()
    mock_firestore_service().collection().limit.return_value = mock.MagicMock()
    mock_firestore_service().collection().limit(
    ).offset.return_value = mock.MagicMock()
    mock_firestore_service().collection().limit().offset(
    ).get.return_value = "TEST_DOCS"
    expected_value = "TEST_DOCS"

    # Run.
    actual = firestore_service.get_paginated_documents("TEST_COLLECTION_NAME",
                                                       1)

    # Assert.
    mock_firestore_service().collection.assert_called_with(
        "TEST_COLLECTION_NAME")
    mock_firestore_service().collection().limit.assert_called_with(10)
    mock_firestore_service().collection().limit().offset.assert_called_with(0)
    self.assertEqual(actual, expected_value)

  @mock.patch("services.firestore_service.get_firestore_instance")
  @mock.patch("services.firestore_service.get_doc_id")
  def test_save_feedback_doc(self, mock_doc_id, mock_firestore_service):
    # Assign.
    mock_firestore_service().collection.return_value = mock.MagicMock()
    mock_firestore_service().collection(
    ).document.return_value = mock.MagicMock()
    mock_firestore_service().collection().document(
    ).collection.return_value = mock.MagicMock()
    mock_firestore_service().collection().document().collection(
    ).document.return_value = mock.MagicMock()
    mock_firestore_service().collection().format().document().collection(
    ).document().set.return_value = "TEST_SAVE"
    mock_doc_id.return_value = "TEST_DOC_ID"
    expected_value = "TEST_DOC_ID"

    # Run.
    actual = firestore_service.save_feedback_doc("TEST_COLLECTION",
                                                 "TEST_SUBCOLLECTION",
                                                 "TEST_DATA", "TEST_USER_ID")

    # Assert.
    mock_firestore_service().collection.assert_called_with("TEST_COLLECTION")
    mock_firestore_service().collection().document.assert_called_with(
        "TEST_USER_ID")
    mock_firestore_service().collection().document(
    ).collection.assert_called_with("TEST_SUBCOLLECTION")
    mock_firestore_service().collection().document().collection(
    ).document.assert_called_with("TEST_DOC_ID")
    mock_firestore_service().collection().document().collection().document(
    ).set.assert_called_with("TEST_DATA")
    self.assertEqual(actual, expected_value)

  @mock.patch("services.firestore_service.get_firestore_instance")
  @mock.patch("services.firestore_service.get_doc_id")
  def test_save_inline_feedback_doc(self, mock_doc_id, mock_firestore_service):
    # Assign.
    mock_firestore_service().collection.return_value = mock.MagicMock()
    mock_firestore_service().collection(
    ).document.return_value = mock.MagicMock()
    mock_firestore_service().collection().document(
    ).collection.return_value = mock.MagicMock()
    mock_firestore_service().collection().document().collection(
    ).document.return_value = mock.MagicMock()
    mock_firestore_service().collection().document().collection().document(
    ).set.return_value = "TEST_SAVE"
    mock_doc_id.return_value = "TEST_DOC_ID"
    expected_value = "TEST_DOC_ID"

    # Run.
    actual = firestore_service.save_inline_feedback_doc("TEST_COLLECTION",
                                                        "TEST_SUBCOLLECTION",
                                                        "TEST_DATA",
                                                        "TEST_USER_ID")

    # Assert.
    mock_firestore_service().collection.assert_called_with("TEST_COLLECTION")
    mock_firestore_service().collection().document.assert_called_with(
        "TEST_USER_ID")
    mock_firestore_service().collection().document(
    ).collection.assert_called_with("TEST_SUBCOLLECTION")
    mock_firestore_service().collection().document().collection(
    ).document.assert_called_with("TEST_DOC_ID")
    mock_firestore_service().collection().document().collection().document(
    ).set.assert_called_with("TEST_DATA")
    self.assertEqual(actual, expected_value)

  @mock.patch("services.firestore_service.get_firestore_instance")
  def test_update_feedback(self, mock_firestore_service):
    # Assign.
    mock_firestore_service().collection.return_value = mock.MagicMock()
    mock_firestore_service().collection(
    ).document.return_value = mock.MagicMock()
    mock_firestore_service().collection().document(
    ).collection.return_value = mock.MagicMock()
    mock_doc_ref = mock.MagicMock()
    mock_doc_ref.id = "TEST_ID"
    mock_firestore_service().collection().document().collection(
    ).document.return_value = mock_doc_ref
    expected_value = "TEST_ID"

    # Run.
    actual = firestore_service.update_feedback("TEST_COLLECTION",
                                               "TEST_SUBCOLLECTION",
                                               "TEST_DOC_ID", "TEST_DATA",
                                               "TEST_USER_ID")

    # Assert.
    mock_firestore_service().collection.assert_called_with("TEST_COLLECTION")
    mock_firestore_service().collection().document.assert_called_with(
        "TEST_USER_ID")
    mock_firestore_service().collection().document(
    ).collection.assert_called_with("TEST_SUBCOLLECTION")
    mock_firestore_service().collection().document().collection(
    ).document.assert_called_with("TEST_DOC_ID")
    self.assertEqual(actual, expected_value)

  @mock.patch("services.firestore_service.get_firestore_instance")
  def test_check_user_feedback(self, mock_firestore_service):
    # Assign.
    mock_firestore_service().collection.return_value = mock.MagicMock()
    mock_firestore_service().collection(
    ).document.return_value = mock.MagicMock()
    mock_firestore_service().collection().document(
    ).collection.return_value = mock.MagicMock()
    mock_firestore_service().collection().document().collection(
    ).get.return_value = "TEST_FEEDBACK"
    expected_value = "TEST_FEEDBACK"

    # Run.
    actual = firestore_service.check_user_feedback("TEST_COLLECTION",
                                                   "TEST_SUBCOLLECTION",
                                                   "TEST_USER_ID")

    # Assert.
    mock_firestore_service().collection.assert_called_with("TEST_COLLECTION")
    mock_firestore_service().collection().document.assert_called_with(
        "TEST_USER_ID")
    mock_firestore_service().collection().document(
    ).collection.assert_called_with("TEST_SUBCOLLECTION")
    self.assertEqual(actual, expected_value)
