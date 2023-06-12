"""Tests for session_service."""

import unittest
from unittest import mock

from services import session_service

#pylint: disable=unnecessary-dunder-call
class SessionServiceTest(unittest.TestCase):
  """Test class for Session Service."""

  @mock.patch("services.session_service.SERVICES")
  @mock.patch("services.session_service.requests")
  def test_get_session_response(self, mock_request, mock_services):
    """testing get session response from session service."""
    # Assign.
    mock_services.__getitem__(
        "dashboard").__getitem__.return_value = "TEST_SERVICES"
    mock_request.get().json.return_value = "TEST_JSON"
    expected_value = "TEST_JSON"

    # Run.
    actual = session_service.get_session_response("TEST_SESSION_ID",
                                                  "TEST_TOKEN")
    # Assert.
    mock_request.get.assert_called_with(
        headers={
            "Content-Type": "application/json",
            "Authorization": "TEST_TOKEN"
        },
        params={"id": "TEST_SESSION_ID"},
        url="http://TEST_SERVICES:TEST_SERVICES/dashboard/api/v1/session",
        timeout=60)
    self.assertEqual(actual, expected_value)
