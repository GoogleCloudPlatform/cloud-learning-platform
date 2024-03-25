"""
  Unit tests for generic csv ingestion service
"""
# disabling pylint rules that conflict with pytest fixtures
# pylint: disable=unused-argument,redefined-outer-name,unused-import
import os
import pytest
import ingest_generic_csv
from testing.testing_objects import (
    TEST_GENERIC_SKILLS_ARRAY, TEST_GENERIC_SKILLS_ARRAY_NEGATIVE_1,
    TEST_GENERIC_SKILLS_ARRAY_NEGATIVE_2, TEST_GENERIC_SKILLS_ARRAY_NEGATIVE_3,
    TEST_GENERIC_COMPETENCY_ARRAY, TEST_GENERIC_COMPETENCY_ARRAY_NEGATIVE_1,
    TEST_GENERIC_COMPETENCY_ARRAY_NEGATIVE_2,
    TEST_GENERIC_COMPETENCY_ARRAY_NEGATIVE_3,
    TEST_GENERIC_CATEGORY_ARRAY_NEGATIVE_1,
    TEST_GENERIC_CATEGORY_ARRAY_NEGATIVE_2,
    TEST_GENERIC_CATEGORY_ARRAY_NEGATIVE_3, TEST_GENERIC_CATEGORY_ARRAY,
    TEST_GENERIC_SUBDOMAIN_ARRAY, TEST_GENERIC_SUBDOMAIN_ARRAY_NEGATIVE_1,
    TEST_GENERIC_SUBDOMAIN_ARRAY_NEGATIVE_2,
    TEST_GENERIC_SUBDOMAIN_ARRAY_NEGATIVE_3, TEST_GENERIC_DOMAIN_ARRAY,
    TEST_GENERIC_DOMAIN_ARRAY_NEGATIVE_1, TEST_GENERIC_DOMAIN_ARRAY_NEGATIVE_2,
    TEST_GENERIC_DOMAIN_ARRAY_NEGATIVE_3)
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


# check for empty value in required column
def test_generic_skill_csv_ingestion_negative_1(clean_firestore, mocker):
  request_dict = {"skill_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_SKILLS_ARRAY_NEGATIVE_1)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for missing required column
def test_generic_skill_csv_ingestion_negative_2(clean_firestore, mocker):
  request_dict = {"skill_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_SKILLS_ARRAY_NEGATIVE_2)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for unknown column
def test_generic_skill_csv_ingestion_negative_3(clean_firestore, mocker):
  request_dict = {"skill_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_SKILLS_ARRAY_NEGATIVE_3)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


def test_generic_skill_csv_ingestion(clean_firestore, mocker):
  request_dict = {"skill_uri": "fake-uri", "source_name": "emsi"}
  expected_response = {
      "success": True,
      "message": "Imported 2 skills",
      "data": {}
  }
  mocker.patch(
      "ingest_generic_csv.parse_csv", return_value=TEST_GENERIC_SKILLS_ARRAY)
  response = ingest_generic_csv.ingest_generic_csv(request_dict)
  assert expected_response == response, "Expected response not same"


# check for empty value in required column
def test_generic_competency_csv_ingestion_negative_1(clean_firestore, mocker):
  request_dict = {"competency_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_COMPETENCY_ARRAY_NEGATIVE_1)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for missing required column
def test_generic_competency_csv_ingestion_negative_2(clean_firestore, mocker):
  request_dict = {"competency_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_COMPETENCY_ARRAY_NEGATIVE_2)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for unknown column
def test_generic_competency_csv_ingestion_negative_3(clean_firestore, mocker):
  request_dict = {"competency_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_COMPETENCY_ARRAY_NEGATIVE_3)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


def test_generic_competency_csv_ingestion(clean_firestore, mocker):
  request_dict = {"competency_uri": "fake-uri", "source_name": "emsi"}
  expected_response = {
      "success": True,
      "message": "Imported 2 competencies",
      "data": {}
  }
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_COMPETENCY_ARRAY)
  response = ingest_generic_csv.ingest_generic_csv(request_dict)
  assert expected_response == response, "Expected response not same"


# check for empty value in required column
def test_generic_category_csv_ingestion_negative_1(clean_firestore, mocker):
  request_dict = {"category_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_CATEGORY_ARRAY_NEGATIVE_1)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for missing required column
def test_generic_category_csv_ingestion_negative_2(clean_firestore, mocker):
  request_dict = {"category_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_CATEGORY_ARRAY_NEGATIVE_2)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for unknown column
def test_generic_category_csv_ingestion_negative_3(clean_firestore, mocker):
  request_dict = {"category_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_CATEGORY_ARRAY_NEGATIVE_3)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


def test_generic_category_csv_ingestion(clean_firestore, mocker):
  request_dict = {"category_uri": "fake-uri", "source_name": "emsi"}
  expected_response = {
      "success": True,
      "message": "Imported 2 categories",
      "data": {}
  }
  mocker.patch(
      "ingest_generic_csv.parse_csv", return_value=TEST_GENERIC_CATEGORY_ARRAY)
  response = ingest_generic_csv.ingest_generic_csv(request_dict)
  assert expected_response == response, "Expected response not same"


# check for empty value in required column
def test_generic_sub_domain_csv_ingestion_negative_1(clean_firestore, mocker):
  request_dict = {"sub_domain_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_SUBDOMAIN_ARRAY_NEGATIVE_1)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for missing required column
def test_generic_sub_domain_csv_ingestion_negative_2(clean_firestore, mocker):
  request_dict = {"sub_domain_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_SUBDOMAIN_ARRAY_NEGATIVE_2)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for unknown column
def test_generic_sub_domain_csv_ingestion_negative_3(clean_firestore, mocker):
  request_dict = {"sub_domain_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_SUBDOMAIN_ARRAY_NEGATIVE_3)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


def test_generic_sub_domain_csv_ingestion(clean_firestore, mocker):
  request_dict = {"sub_domain_uri": "fake-uri", "source_name": "emsi"}
  expected_response = {
      "success": True,
      "message": "Imported 2 sub domains",
      "data": {}
  }
  mocker.patch(
      "ingest_generic_csv.parse_csv", return_value=TEST_GENERIC_SUBDOMAIN_ARRAY)
  response = ingest_generic_csv.ingest_generic_csv(request_dict)
  assert expected_response == response, "Expected response not same"


# check for empty value in required column
def test_generic_domain_csv_ingestion_negative_1(clean_firestore, mocker):
  request_dict = {"domain_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_DOMAIN_ARRAY_NEGATIVE_1)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for missing required column
def test_generic_domain_csv_ingestion_negative_2(clean_firestore, mocker):
  request_dict = {"domain_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_DOMAIN_ARRAY_NEGATIVE_2)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


# check for unknown column
def test_generic_domain_csv_ingestion_negative_3(clean_firestore, mocker):
  request_dict = {"domain_uri": "fake-uri", "source_name": "emsi"}
  mocker.patch(
      "ingest_generic_csv.parse_csv",
      return_value=TEST_GENERIC_DOMAIN_ARRAY_NEGATIVE_3)
  with pytest.raises(Exception):
    ingest_generic_csv.ingest_generic_csv(request_dict)


def test_generic_domain_csv_ingestion(clean_firestore, mocker):
  request_dict = {"domain_uri": "fake-uri", "source_name": "emsi"}
  expected_response = {
      "success": True,
      "message": "Imported 2 domains",
      "data": {}
  }
  mocker.patch(
      "ingest_generic_csv.parse_csv", return_value=TEST_GENERIC_DOMAIN_ARRAY)
  response = ingest_generic_csv.ingest_generic_csv(request_dict)
  assert expected_response == response, "Expected response not same"
