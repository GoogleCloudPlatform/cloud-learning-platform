"""
  Tests for User endpoints
"""
import os
import mock
from testing.test_config import BASE_URL
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
from common.testing.client_with_emulator import client_with_emulator
from common.testing.firestore_emulator import firestore_emulator, clean_firestore
from schemas.schema_examples import (
  INPUT_REPLAY_NOTIFICATION_EXAMPLE)
os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"

API_URL = f"{BASE_URL}/lms-notifications/replay"

SUCCESS_RESPONSE = {"status": "Success"}
mock_input = INPUT_REPLAY_NOTIFICATION_EXAMPLE.copy()


def test_replay_notifications(client_with_emulator):
  with mock.patch("routes.lms_notification.Logger"):
    with mock.patch("routes.lms_notification.publish_messages"):
      response = client_with_emulator.post(API_URL,
                                           json={
                                               "start_date":
                                               "2023-07-26T00:00:00+00:00",
                                               "end_date":
                                               "2023-07-28T00:00:00+00:00"
                                           })
  assert response.status_code == 202, "Status 202"

def test_replay_notifications_negative(client_with_emulator):
  negative_input = {
    "start_date":"2023-07-26", # incorrect, not datetime 
    "end_date":"2023-07-28T00:00:00+00:00" # correct, datetime
  }
  with mock.patch("routes.lms_notification.Logger"):
    with mock.patch("routes.lms_notification.publish_messages"):
      response = client_with_emulator.post(API_URL, json=negative_input)
  assert response.status_code == 422, "Status 422"
