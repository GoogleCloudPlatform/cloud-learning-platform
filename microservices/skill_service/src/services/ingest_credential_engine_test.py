"""
  Unit test for service used by credential engine data ingestion route
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
from testing.test_config import TEST_IMPORT_URLS
from ingest_credential_engine import ingest_credential_engine
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_import_from_credential_engine(clean_firestore):
  expected_response = {
      "success": True,
      "message": "Data ingestion complete",
      "data": {}
  }
  req_data = TEST_IMPORT_URLS
  response = ingest_credential_engine(req_data)
  assert expected_response == response, "Expected response not same"
