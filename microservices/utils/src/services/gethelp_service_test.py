"""
    Utility methods to execute unit tests for gethelp_controller.py
"""
import unittest
from unittest import mock

from services import gethelp_service


class GetHelpControllerTest(unittest.TestCase):

  @mock.patch.object(gethelp_service, "get_paginated_topic_documents")
  def test_get_help_faqs_return_dict(self, mock_gethelp_controller):
    mock_doc = mock.MagicMock()
    mock_gethelp_controller.return_value = [mock_doc, mock_doc]
    mock_doc.to_dict.return_value = "TEST"
    actual = gethelp_service.get_help_faqs("TEST_COLLECTION_PATH",
                                              "TEST_TOPIC", 1)
    print(actual)
    expected_value = {"items": ["TEST", "TEST"]}
    self.assertEqual(actual, expected_value)

  @mock.patch.object(
      gethelp_service, "get_paginated_topic_documents", return_value=1)
  def test_get_help_faqs_raises_exception(self, _):
    self.assertRaises(
        Exception,
        gethelp_service.get_help_faqs("TEST_COLLECTION_PATH", "TEST_TOPIC",
                                         1))

  @mock.patch.object(gethelp_service, "get_paginated_documents")
  def test_get_topics_return_dict(self, mock_gethelp_controller):
    mock_doc = mock.MagicMock()
    mock_gethelp_controller.return_value = [mock_doc, mock_doc]
    mock_doc.to_dict.return_value = "TEST"
    actual = gethelp_service.gettopics("TEST_COLLECTION_PATH", 1)
    expected_value = {"items": ["TEST", "TEST"]}
    self.assertEqual(actual, expected_value)

  @mock.patch.object(
      gethelp_service, "get_paginated_documents", return_value=1)
  def test_get_topics_raises_exception(self, _):
    self.assertRaises(Exception,
                      gethelp_service.gettopics("TEST_COLLECTION_PATH", 1))
