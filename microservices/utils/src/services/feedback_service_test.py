"""
    Utility methods to execute unit tests for feedback_controller.py
"""
import unittest
from unittest import mock

with mock.patch("google.cloud.logging.Client",
  side_effect = mock.MagicMock()) as mok:
  with mock.patch("google.cloud.secretmanager.SecretManagerServiceClient",
    side_effect = mock.MagicMock()) as mok:
    from services import feedback_service

TEST_DOCUMENT = mock.MagicMock()
TEST_DICT = {"question_ref": "TEST_DICT"}
TEST_DOCUMENT.to_dict.return_value = TEST_DICT
TEST_DOCUMENT.reference.path = "TEST"
TEST_DOCUMENTS_LIST = [TEST_DOCUMENT] * 2


class FeedbackControllerTest(unittest.TestCase):

  @mock.patch.object(
      feedback_service,
      "get_documents",
      autospec=True,
      return_value=TEST_DOCUMENTS_LIST)
  def test_get_feedback_options_returns_dictionary(self, _):
    actual = feedback_service.get_feedback_options("TEST_COLLECTION_PATH")
    expected_value = {
        "items": [{
            "question_ref": "TEST"
        }, {
            "question_ref": "TEST"
        }]
    }
    self.assertEqual(actual, expected_value)

  @mock.patch.object(
      feedback_service, "get_documents", autospec=True, return_value=1)
  def test_get_feedback_options_raises_error(self, _):
    self.assertRaises(
        Exception,
        feedback_service.get_feedback_options("TEST_COLLECTION_PATH"))

  @mock.patch.object(feedback_service, "get_session_response", autospec=True)
  @mock.patch.object(
      feedback_service,
      "save_feedback_doc",
      autospec=True,
      return_value="TEST")
  def test_save_feedback_returns_doc_id_with_empty_use_session_id(
      self, mock_save_feedback_doc, _):
    test_req_data = {"session_id": "", "context_ref": "", "token": ""}
    actual = feedback_service.save_feedback("TEST_COLLECTION_PATH",
                                               "TEST_SUB_COLLECTION",
                                               test_req_data, "TEST_USER_ID")
    expected_value = "TEST"
    mock_save_feedback_doc.assert_called_once_with("TEST_COLLECTION_PATH",
                                                   "TEST_SUB_COLLECTION",
                                                   test_req_data,
                                                   "TEST_USER_ID")
    self.assertEqual(actual, expected_value)

  @mock.patch.object(
      feedback_service,
      "get_session_response",
      autospec=True,
      return_value={"message": "INVALID_SESSION_ID"})
  @mock.patch.object(
      feedback_service,
      "save_feedback_doc",
      autospec=True,
      return_value="TEST")
  def test_save_feedback_returns_doc_id_with_invalid_session_id(
      self, _, mock_get_session_response):
    test_req_data = {"session_id": "TEST", "context_ref": "TEST", "token": ""}
    expected_test_req_data = {"context_ref": ""}
    actual = feedback_service.save_feedback("TEST_COLLECTION_PATH",
                                               "TEST_SUB_COLLECTION",
                                               test_req_data, "TEST_USER_ID")
    mock_get_session_response.assert_called_once_with("TEST", "")
    expected_value = "TEST"
    self.assertEqual(actual, expected_value)
    self.assertEqual(test_req_data, expected_test_req_data)

  @mock.patch.object(
      feedback_service,
      "get_session_response",
      autospec=True,
      return_value={
          "message": "NOT_INVALID_SESSION",
          "data": {
              "context_ref": "TEST"
          }
      })
  @mock.patch.object(
      feedback_service,
      "save_feedback_doc",
      autospec=True,
      return_value="TEST")
  def test_save_feedback_returns_doc_id(self, _, mock_get_session_response):
    test_req_data = {"session_id": "TEST", "context_ref": "TEST", "token": ""}
    expected_test_req_data = {"context_ref": "TEST"}
    actual = feedback_service.save_feedback("TEST_COLLECTION_PATH",
                                               "TEST_SUB_COLLECTION",
                                               test_req_data, "TEST_USER_ID")
    mock_get_session_response.assert_called_once_with("TEST", "")
    expected_value = "TEST"
    self.assertEqual(actual, expected_value)
    self.assertEqual(test_req_data, expected_test_req_data)

  def test_save_feedback_raises_error(self):
    self.assertRaises(
        Exception,
        feedback_service.save_feedback("TEST_COLLECTION_PATH",
                                          "TEST_SUB_COLLECTION", Exception,
                                          "TEST_USER_ID"))

  @mock.patch.object(
      feedback_service,
      "save_inline_feedback_doc",
      autospec=True,
      return_value="TEST")
  def test_save_inline_feedback_returns_doc_id(self,
                                               mock_save_inline_feedback_doc):
    actual = feedback_service.save_inline_feedback("TEST_COLLECTION_PATH",
                                                      "TEST_SUB_COLLECTION",
                                                      "TEST_REQ_DATA",
                                                      "TEST_USER_ID")
    mock_save_inline_feedback_doc.assert_called_once_with(
        "TEST_COLLECTION_PATH", "TEST_SUB_COLLECTION", "TEST_REQ_DATA",
        "TEST_USER_ID")
    expected_value = "TEST"
    self.assertEqual(actual, expected_value)

  @mock.patch.object(
      feedback_service,
      "save_inline_feedback_doc",
      autospec=True,
      side_effect=Exception("TEST"))
  def test_save_inline_feedback_raises_error(self, _):
    self.assertRaises(
        Exception,
        feedback_service.save_inline_feedback("TEST_COLLECTION_PATH",
                                                 "TEST_SUB_COLLECTION",
                                                 "TEST_REQ_DATA",
                                                 "TEST_USER_ID"))
