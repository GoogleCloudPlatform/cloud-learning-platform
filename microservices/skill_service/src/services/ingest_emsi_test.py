"""
  Unit test for service used by emsi data ingestion route
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
from unittest.mock import Mock
import ingest_emsi
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_import_from_emsi(clean_firestore, mocker):
  skill = [{
      "id": "KS120P86XDXZJT3B7KVJ",
      "infoUrl": "https://skills.emsidata.com/skills/KS120P86XDXZJT3B7KVJ",
      "name": "(American Society For Quality) ASQ Certified",
      "tags": [],
      "type": {
          "id": "ST3",
          "name": "Certification"
      }
  }]
  expected_response = {
      "success": True,
      "message": "Imported 1 skills",
      "data": {}
  }

  fetch_skills_return_value = skill
  mocker.patch("ingest_emsi.auth_emsi", return_value="fake_token")
  mocker.patch(
      "ingest_emsi.fetch_emsi_skills", return_value=fetch_skills_return_value)

  # import 1 skil to check the output
  requests = Mock()
  mock_response = Mock()
  mock_response.json.return_value = skill
  mock_response.status_code = 200
  requests.get = Mock(return_value=mock_response)

  response = ingest_emsi.ingest_emsi(size=1)
  assert expected_response == response, "Expected response not same"
