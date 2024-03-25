"""
  Unit tests for service used by following routes:
  /import/local-csv
  /import/gcs-csv
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
import ingest_csv
from testing.testing_objects import FAKE_COMPETENCIES_ARRAY, FAKE_SKILLS_ARRAY
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_csv_ingestion_api(clean_firestore, mocker):
  request_dict = {"competency_uri": "fake-uri", "skill_uri": "fake-uri"}
  expected_response = {
      "success": True,
      "message": "Imported 2 domains, 2 subdomains, 5 competencies 1 skills",
      "data": {}
  }
  mocker.patch(
      "ingest_csv.parse_and_validate_competency_csv",
      return_value=FAKE_COMPETENCIES_ARRAY)
  mocker.patch(
      "ingest_csv.parse_and_validate_skill_csv", return_value=FAKE_SKILLS_ARRAY)
  response = ingest_csv.ingest_csv(request_dict)
  assert expected_response == response, "Expected response not same"
