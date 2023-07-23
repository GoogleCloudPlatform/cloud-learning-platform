"""
    Utility methods to execute unit tests for activity_controller.py
"""
import unittest
from unittest import mock

from services import activity_service


class ActivityControllerTest(unittest.TestCase):

  @mock.patch.object(activity_service, "get_documents", autospec=True)
  def test_get_activity_list_with_multiple_documents_return_list(
      self, mock_get_documents):
    mock_dict = mock.MagicMock()
    mock_dict.to_dict.return_value = "TEST"
    mock_get_documents.return_value = [mock_dict, mock_dict]
    actual_activity_list = activity_service.get_activity_list()
    print(actual_activity_list)
    expected_activity_list = ["TEST", "TEST"]
    self.assertEqual(actual_activity_list, expected_activity_list)

  @mock.patch.object(
      activity_service, "get_documents", autospec=True, return_value="")
  def test_get_activity_list_with_no_document_raise_exception(self, _):
    with self.assertRaises(Exception):
      activity_service.get_activity_list()
