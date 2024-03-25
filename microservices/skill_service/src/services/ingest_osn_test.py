"""
  Unit tests for service used by following routes:
  /import/osn
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
import ingest_osn
from testing.testing_objects import FAKE_OSN_SKILLS_ARRAY
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_osn_csv_ingestion_api(clean_firestore, mocker):
  request_dict = {"skill_uri": "fake-uri"}
  expected_response = {
      "success": True,
      "message": "Imported 1 skills",
      "data": {}
  }
  mocker.patch(
      "ingest_osn.parse_and_validate_osn_csv",
      return_value=FAKE_OSN_SKILLS_ARRAY)
  response = ingest_osn.ingest_osn_csv(request_dict)
  assert expected_response == response, "Expected response not same"
