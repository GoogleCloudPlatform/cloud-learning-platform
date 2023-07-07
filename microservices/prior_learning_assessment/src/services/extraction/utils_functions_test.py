"""Unit Test for Utils Functions Script"""
# pylint: disable=unused-argument,redefined-outer-name,unused-import,wrong-import-position,invalid-name
import os
import sys
import pytest
from services.extraction import utils_functions

sys.path.append("../../../common/src")
from common.models import PriorExperience
from common.testing.firestore_emulator import (firestore_emulator,
                                               clean_firestore)

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["GOOGLE_CLOUD_PROJECT"] = "fake-project"


def test_standard_entity_mapping():
  expected_result = [{
    "entity": "competencies", "value": None,
    "extraction_confidence": None,
    "manual_extraction": False,
    "corrected_value": None
  },
    {
      "entity": "credits_earned",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "date_completed",
      "value": "Jun 15, 2018",
      "extraction_confidence": 0.83,
      "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "description",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "experience_title",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "name",
      "value": "John Smith",
      "extraction_confidence": 0.9,
      "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "organization",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "skills",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "url",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None
    }]

  desired_entities_list = [{
    "entity": "Name", "value": "John Smith",
    "extraction_confidence": 0.9,
    "manual_extraction": False,
    "corrected_value": None,
    "value_coordinates": [0.2134, 0.1218, 0.2851, 0.1218, 0.2851, 0.1341,
                          0.2134, 0.1341],
    "key_coordinates": [0.0466, 0.1222, 0.0832, 0.1222,
                        0.0832, 0.1345, 0.0466, 0.1345], "page_no": 1,
    "page_width": 1757,
    "page_height": 2275
  },
    {
      "entity": "Organization",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None,
      "value_coordinates": None,
      "key_coordinates": None,
      "page_no": None,
      "page_width": None,
      "page_height": None
    },
    {
      "entity": "Experience Title",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None,
      "value_coordinates": None,
      "key_coordinates": None,
      "page_no": None,
      "page_width": None,
      "page_height": None
    },
    {
      "entity": "Date Graduated",
      "value": "Jun 15, 2018",
      "extraction_confidence": 0.83,
      "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.6915, 0.1235, 0.782,
                                                     0.1235, 0.782, 0.1336,
                                                     0.6915, 0.1336],
      "key_coordinates": [0.4731,
                          0.1218, 0.5875, 0.1218, 0.5875, 0.1349, 0.4731,
                          0.1349], "page_no": 1,
      "page_width": 1757, "page_height": 2275},
    {
      "entity": "Credits Earned",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None,
      "value_coordinates": None,
      "key_coordinates": None,
      "page_no": None,
      "page_width": None,
      "page_height": None
    },
    {
      "entity": "Description",
      "value": None,
      "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None,
      "value_coordinates": None,
      "key_coordinates": None,
      "page_no": None,
      "page_width": None,
      "page_height": None
    },
    {
      "entity": "URL",
      "value": None, "extraction_confidence": None,
      "manual_extraction": False,
      "corrected_value": None,
      "value_coordinates": None,
      "key_coordinates": None, "page_no": None,
      "page_width": None, "page_height": None},
    {
      "entity": "Competencies", "value": None,
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None,
      "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None},
    {
      "entity": "Skills", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None,
      "value_coordinates": None, "key_coordinates": None, "page_no": None,
      "page_width": None, "page_height": None
    }]

  parser_name = "form_parser"

  result = utils_functions.standard_entity_mapping(desired_entities_list,
                                                   parser_name)
  assert result == expected_result


def test_get_json_format_for_processing():
  expected_result = [{
    "url": {"text": None, "score": None},
    "skills": {"text": None, "score": None},
    "organization": {"text": None, "score": None},
    "name": {"text": "John Smith", "score": 0.9},
    "experience_title": {"text": None, "score": None},
    "description": {"text": None, "score": None},
    "date_completed": {"text": "Jun 15, 2018", "score": 0.83},
    "credits_earned": {"text": None, "score": None},
    "competencies": {"text": None, "score": None}
  }]

  input_json = [{
    "entity": "competencies", "value": None, "extraction_confidence": None,
    "manual_extraction": False, "corrected_value": None
  },
    {
      "entity": "credits_earned", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "date_completed", "value": "Jun 15, 2018",
      "extraction_confidence": 0.83, "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "description", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "experience_title", "value": None,
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "name", "value": "John Smith", "extraction_confidence": 0.9,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "organization", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "skills", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "url", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    }]

  result = utils_functions.get_json_format_for_processing(input_json)
  assert result == expected_result


def test_correct_json_format_for_db():
  expected_result = [{
    "entity": "competencies", "value": {"text": None, "score": None},
    "extraction_confidence": None, "manual_extraction": False,
    "corrected_value": None
  },
    {
      "entity": "credits_earned", "value": {"text": None, "score": None},
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "date_completed", "value": {"text": "Jun 15, 2018",
                                            "score": 0.83},
      "extraction_confidence": 0.83,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "description", "value": {"text": None, "score": None},
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "experience_title", "value": {"text": None, "score": None},
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "name", "value": "TEXTSCORE", "extraction_confidence": 0.9,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "organization", "value": {"text": None, "score": None},
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "skills",
      "value": {"text": None, "score": None},
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "url", "value": {"text": None, "score": None},
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None
    }]

  output_dict = [{
    "url": {"text": None, "score": None},
    "skills": {"text": None, "score": None},
    "organization": {"text": None, "score": None},
    "name": "TEXTSCORE", "experience_title": {"text": None, "score": None},
    "description": {"text": None, "score": None},
    "date_completed": {"text": "Jun 15, 2018", "score": 0.83},
    "credits_earned": {"text": None, "score": None},
    "competencies": {"text": None, "score": None}
  }]
  input_json = [{
    "entity": "competencies", "value": None, "extraction_confidence": None,
    "manual_extraction": False, "corrected_value": None
  },
    {
      "entity": "credits_earned", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "date_completed", "value": "Jun 15, 2018",
      "extraction_confidence": 0.83, "manual_extraction": False,
      "corrected_value": None
    },
    {
      "entity": "description", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "experience_title", "value": None,
      "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "name", "value": "John Smith", "extraction_confidence": 0.9,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "organization", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "skills", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    },
    {
      "entity": "url", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None
    }]

  result = utils_functions.correct_json_format_for_db(output_dict, input_json)
  assert result == expected_result


def test_get_doc_type():
  expected_result = ["pdf"]
  gcs_uri_list = ["gs://aitutor-dev/pla/user-transcripts/Sample_Transcript.pdf"]
  result = utils_functions.get_doc_type(gcs_uri_list)
  assert result == expected_result


# pylint: disable=pointless-string-statement
def test_form_parser_entities_mapping():
  expected_result = [
    [
      {
        "entity": "Name",
        "value": "John Smith",
        "extraction_confidence": 0.9,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": [
          0.2134,
          0.1218,
          0.2851,
          0.1218,
          0.2851,
          0.1341,
          0.2134,
          0.1341
        ],
        "key_coordinates": [
          0.0466,
          0.1222,
          0.0832,
          0.1222,
          0.0832,
          0.1345,
          0.0466,
          0.1345
        ],
        "page_no": 1,
        "page_width": 1757,
        "page_height": 2275
      },
      {
        "entity": "Organization",
        "value": None,
        "extraction_confidence": None,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": None,
        "key_coordinates": None,
        "page_no": None,
        "page_width": None,
        "page_height": None
      },
      {
        "entity": "Experience Title",
        "value": None,
        "extraction_confidence": None,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": None,
        "key_coordinates": None,
        "page_no": None,
        "page_width": None,
        "page_height": None
      },
      {
        "entity": "Date Graduated",
        "value": "Jun 15, 2018",
        "extraction_confidence": 0.83,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": [
          0.6915,
          0.1235,
          0.782,
          0.1235,
          0.782,
          0.1336,
          0.6915,
          0.1336
        ],
        "key_coordinates": [
          0.4731,
          0.1218,
          0.5875,
          0.1218,
          0.5875,
          0.1349,
          0.4731,
          0.1349
        ],
        "page_no": 1,
        "page_width": 1757,
        "page_height": 2275
      },
      {
        "entity": "Credits Earned",
        "value": None,
        "extraction_confidence": None,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": None,
        "key_coordinates": None,
        "page_no": None,
        "page_width": None,
        "page_height": None
      },
      {
        "entity": "Description",
        "value": None,
        "extraction_confidence": None,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": None,
        "key_coordinates": None,
        "page_no": None,
        "page_width": None,
        "page_height": None
      },
      {
        "entity": "URL",
        "value": None,
        "extraction_confidence": None,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": None,
        "key_coordinates": None,
        "page_no": None,
        "page_width": None,
        "page_height": None
      },
      {
        "entity": "Competencies",
        "value": None,
        "extraction_confidence": None,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": None,
        "key_coordinates": None,
        "page_no": None,
        "page_width": None,
        "page_height": None
      },
      {
        "entity": "Skills",
        "value": None,
        "extraction_confidence": None,
        "manual_extraction": False,
        "corrected_value": None,
        "value_coordinates": None,
        "key_coordinates": None,
        "page_no": None,
        "page_width": None,
        "page_height": None
      }
    ]
  ]

  form_parser_entity_list = [
    {
      "key": "RPS ID",
      "key_coordinates": [
        0.0467,
        0.1358,
        0.1015,
        0.1358,
        0.1015,
        0.1464,
        0.0467,
        0.1464
      ],
      "value": "12345",
      "value_coordinates": [
        0.2117,
        0.1354,
        0.2493,
        0.1354,
        0.2493,
        0.1473,
        0.2117,
        0.1473
      ],
      "key_confidence": 0.95,
      "value_confidence": 0.95,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Name",
      "key_coordinates": [
        0.0466,
        0.1222,
        0.0832,
        0.1222,
        0.0832,
        0.1345,
        0.0466,
        0.1345
      ],
      "value": "John Smith",
      "value_coordinates": [
        0.2134,
        0.1218,
        0.2851,
        0.1218,
        0.2851,
        0.1341,
        0.2134,
        0.1341
      ],
      "key_confidence": 0.9,
      "value_confidence": 0.9,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Gender",
      "key_coordinates": [
        0.0461,
        0.1613,
        0.0995,
        0.1613,
        0.0995,
        0.1714,
        0.0461,
        0.1714
      ],
      "value": "Male",
      "value_coordinates": [
        0.21,
        0.1609,
        0.2396,
        0.1609,
        0.2396,
        0.1705,
        0.21,
        0.1705
      ],
      "key_confidence": 0.85,
      "value_confidence": 0.85,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Date Graduated",
      "key_coordinates": [
        0.4731,
        0.1218,
        0.5875,
        0.1218,
        0.5875,
        0.1349,
        0.4731,
        0.1349
      ],
      "value": "Jun 15, 2018",
      "value_coordinates": [
        0.6915,
        0.1235,
        0.782,
        0.1235,
        0.782,
        0.1336,
        0.6915,
        0.1336
      ],
      "key_confidence": 0.83,
      "value_confidence": 0.83,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Guardian",
      "key_coordinates": [
        0.473,
        0.1345,
        0.5407,
        0.1345,
        0.5407,
        0.1477,
        0.473,
        0.1477
      ],
      "value": "Julie Smith",
      "value_coordinates": [
        0.6927,
        0.1354,
        0.7712,
        0.1354,
        0.7712,
        0.1477,
        0.6927,
        0.1477
      ],
      "key_confidence": 0.79,
      "value_confidence": 0.79,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Birthdate",
      "key_coordinates": [
        0.0478,
        0.1473,
        0.1228,
        0.1473,
        0.1228,
        0.1591,
        0.0478,
        0.1591
      ],
      "value": "Apr 12, 2001",
      "value_coordinates": [
        0.2112,
        0.1464,
        0.3005,
        0.1464,
        0.3005,
        0.1596,
        0.2112,
        0.1596
      ],
      "key_confidence": 0.79,
      "value_confidence": 0.79,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Non-Credit Requirements",
      "key_coordinates": [
        0.473,
        0.182,
        0.6489,
        0.182,
        0.6489,
        0.1952,
        0.473,
        0.1952
      ],
      "value": "40 Hours of Service Learning Hours Driver Education "
               "Constitution (Public Law 195) Consumer Education",
      "value_coordinates": [
        0.4735,
        0.1934,
        0.7285,
        0.1934,
        0.7285,
        0.2378,
        0.4735,
        0.2378
      ],
      "key_confidence": 0.78,
      "value_confidence": 0.78,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Fine Arts",
      "key_coordinates": [
        0.2264,
        0.1938,
        0.2985,
        0.1938,
        0.2985,
        0.2062,
        0.2264,
        0.2062
      ],
      "value": "English 2",
      "value_coordinates": [
        0.062,
        0.1943,
        0.2203,
        0.1943,
        0.2203,
        0.2075,
        0.062,
        0.2075
      ],
      "key_confidence": 0.62,
      "value_confidence": 0.62,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Unweighted GPA",
      "key_coordinates": [
        0.1242,
        0.7284,
        0.2369,
        0.7284,
        0.2369,
        0.7407,
        0.1242,
        0.7407
      ],
      "value": "3.08/4.00 Cumulative",
      "value_coordinates": [
        0.0478,
        0.7284,
        0.3443,
        0.7284,
        0.3443,
        0.7407,
        0.0478,
        0.7407
      ],
      "key_confidence": 0.57,
      "value_confidence": 0.57,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Address",
      "key_coordinates": [
        0.473,
        0.1473,
        0.5343,
        0.1473,
        0.5343,
        0.1596,
        0.473,
        0.1596
      ],
      "value": "123 Maple St",
      "value_coordinates": [
        0.691,
        0.1468,
        0.782,
        0.1468,
        0.782,
        0.16,
        0.691,
        0.16
      ],
      "key_confidence": 0.54,
      "value_confidence": 0.54,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Cumulative",
      "key_coordinates": [
        0.0472,
        0.716,
        0.1425,
        0.716,
        0.1425,
        0.7279,
        0.0472,
        0.7279
      ],
      "value": "3.15/4.00 Weighted GPA",
      "value_coordinates": [
        0.1298,
        0.716,
        0.3438,
        0.716,
        0.3438,
        0.7279,
        0.1298,
        0.7279
      ],
      "key_confidence": 0.48,
      "value_confidence": 0.48,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Date",
      "key_coordinates": [
        0.045,
        0.0998,
        0.0772,
        0.0998,
        0.0772,
        0.1143,
        0.045,
        0.1143
      ],
      "value": "Issued: August 3, 2017",
      "value_coordinates": [
        0.0848,
        0.0985,
        0.251,
        0.0985,
        0.251,
        0.1138,
        0.0848,
        0.1138
      ],
      "key_confidence": 0.46,
      "value_confidence": 0.46,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Class Rank",
      "key_coordinates": [
        0.0478,
        0.7543,
        0.124,
        0.7543,
        0.124,
        0.767,
        0.0478,
        0.767
      ],
      "value": "3/10",
      "value_coordinates": [
        0.2772,
        0.7543,
        0.3085,
        0.7543,
        0.3085,
        0.7644,
        0.2772,
        0.7644
      ],
      "key_confidence": 0.46,
      "value_confidence": 0.46,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Cumulative GPA",
      "key_coordinates": [
        0.6719,
        0.5033,
        0.7848,
        0.5033,
        0.7848,
        0.5136,
        0.6719,
        0.5136
      ],
      "value": "2.73 6.50",
      "value_coordinates": [
        0.7928,
        0.5033,
        0.8884,
        0.5033,
        0.8884,
        0.513,
        0.7928,
        0.513
      ],
      "key_confidence": 0.44,
      "value_confidence": 0.44,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "HS Units Earned",
      "key_coordinates": [
        0.0467,
        0.7407,
        0.1625,
        0.7407,
        0.1625,
        0.7534,
        0.0467,
        0.7534
      ],
      "value": "13.25",
      "value_coordinates": [
        0.2795,
        0.7424,
        0.3153,
        0.7424,
        0.3153,
        0.7516,
        0.2795,
        0.7516
      ],
      "key_confidence": 0.41,
      "value_confidence": 0.41,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "3 Mathematics",
      "key_coordinates": [
        0.0501,
        0.207,
        0.1453,
        0.207,
        0.1453,
        0.2171,
        0.0501,
        0.2171
      ],
      "value": "2 Physical",
      "value_coordinates": [
        0.2157,
        0.2057,
        0.2886,
        0.2057,
        0.2886,
        0.218,
        0.2157,
        0.218
      ],
      "key_confidence": 0.36,
      "value_confidence": 0.36,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "3 Social Science",
      "key_coordinates": [
        0.0484,
        0.2277,
        0.1765,
        0.2277,
        0.1765,
        0.2385,
        0.0484,
        0.2385
      ],
      "value": "2 Career",
      "value_coordinates": [
        0.2157,
        0.2268,
        0.2743,
        0.2268,
        0.2743,
        0.2404,
        0.2157,
        0.2404
      ],
      "key_confidence": 0.32,
      "value_confidence": 0.32,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "GPA",
      "key_coordinates": [
        0.3045,
        0.5033,
        0.3306,
        0.5033,
        0.3306,
        0.5131,
        0.3045,
        0.5131
      ],
      "value": "Cumulative 2.69 3.25",
      "value_coordinates": [
        0.222,
        0.5033,
        0.4377,
        0.5033,
        0.4377,
        0.513,
        0.222,
        0.513
      ],
      "key_confidence": 0.32,
      "value_confidence": 0.32,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Fall",
      "key_coordinates": [
        0.0461,
        0.2971,
        0.0768,
        0.2971,
        0.0768,
        0.3067,
        0.0461,
        0.3067
      ],
      "value": "2013: 89/95",
      "value_coordinates": [
        0.0854,
        0.2967,
        0.1668,
        0.2967,
        0.1668,
        0.3064,
        0.0854,
        0.3064
      ],
      "key_confidence": 0.24,
      "value_confidence": 0.24,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "3 Science",
      "key_coordinates": [
        0.0495,
        0.2176,
        0.1162,
        0.2176,
        0.1162,
        0.2268,
        0.0495,
        0.2268
      ],
      "value": "1 Technology",
      "value_coordinates": [
        0.2157,
        0.2163,
        0.3039,
        0.2163,
        0.3039,
        0.2295,
        0.2157,
        0.2295
      ],
      "key_confidence": 0.24,
      "value_confidence": 0.24,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "4 World Languages",
      "key_coordinates": [
        0.0478,
        0.2374,
        0.1775,
        0.2374,
        0.1775,
        0.2514,
        0.0478,
        0.2514
      ],
      "value": "A minimum of 24 total credits is required for a diploma",
      "value_coordinates": [
        0.0489,
        0.2497,
        0.2669,
        0.2497,
        0.2669,
        0.2738,
        0.0489,
        0.2738
      ],
      "key_confidence": 0.2,
      "value_confidence": 0.2,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    },
    {
      "key": "Physical",
      "key_coordinates": [
        0.2251,
        0.2021,
        0.2975,
        0.2021,
        0.2975,
        0.218,
        0.2251,
        0.218
      ],
      "value": "Education",
      "value_coordinates": [
        0.296,
        0.2057,
        0.3625,
        0.2057,
        0.3625,
        0.218,
        0.296,
        0.218
      ],
      "key_confidence": 0.12,
      "value_confidence": 0.12,
      "page_no": 1,
      "page_width": 1757,
      "page_height": 2275
    }
  ]

  mapping_dict = {
    "default_entities": {
      "Name": [
        "Name"
      ],
      "Organization": [
        "Organization",
        "University"
      ],
      "Experience Title": [
        "Experience Title"
      ],
      "Date Graduated": [
        "Date Graduated"
      ],
      "Credits Earned": [
        "Credits Earned"
      ],
      "Description": [
        "Description"
      ],
      "URL": [
        "URL"
      ],
      "Competencies": [
        "Competencies"
      ],
      "Skills": [
        "Skills"
      ]
    }
  }

  form_parser_text = "Legacy Academy of Excellence Charter School 4029 "
  "Prairie Road Rockford, IL 61102 www.legacyacademy.com Legacy Academy of "
  "Excellence Charter School Legacy An International Baccalaureate MYP World "
  "School High School Transcript of Student Progress Middle Years Programme "
  "Date Issued: August 3, 2017 Name: John Smith Date Graduated: RPS ID: "
  "12345 Guardian: Birthdate: Apr 12, 2001 Address: Gender: Male Jun 15, "
  "2018 Julie Smith 123 Maple St Rockford, IL 61101 Requirements 4 English "
  "2 Fine Arts 3 Mathematics 2 Physical Education 3 Science 1 Technology 3 "
  "Social Science 2 Career Education 4 World Languages A minimum of 24 total "
  "credits is required for a diploma Non-Credit Requirements 40 Hours of "
  "Service Learning Hours Driver Education Constitution (Public Law 195) "
  "Consumer Education Attendance Fall 2013: 89/95 Spring 2014: 92/95 Grade "
  "A B C D F S-Modified 2 2 1 1 0 Weighted Credit Value Reg Honors "
  "Advanced/Telescopic 5 6 3 4 5 2 3 4 1 0 Freshman Year First Semester "
  "Course Grade 13110 Survey of Literature B 53810 Spanish A 43310 Algebra 1 B "
  "23110 World Cultures A 99010 - Physical Education C 33110 Environmental "
  "Science F 62210 Design B Semester GPA Cumulative GPA 2.69 Credits 0.50 "
  "0.50 0.50 0.50 0.50 0.50 0.25 Second Semester Course Grade 13110 Survey of "
  "Literature D 23110 World Cultures B 33110 Environmental Science A 43310 "
  "Algebra 1 B 53810- Spanish A 99010 - Physical Education D 91510 Art A "
  "Semester GPA Cumulative GPA 2.73 Credits 0.50 0.50 0.50 0.50 0.50 0.50 "
  "0.25 3.25 6.50 Grade B B B First Semester Course 13120 American Literature "
  "43410 Geometry 23610 United States History 33110 Environmental Science "
  "53820- Spanish 91510 Art 99020- Physical Education Semester GPA Cumulative "
  "GPA Sophomore Year Second Semester Credits Course Grade 0.50 13120 American "
  "Literature (Honors) B 0.50 43410 Geometry A 0.50 23610 United States "
  "History (Honors) B 0.50 33110 Environmental Science B 0.50 53820- Spanish "
  "A 0.25 91510 Art A 0.50 99210 Health A Semester GPA 9.75 Cumulative GPA "
  "3.15 Credits 0.50 0.50 0.50 0.50 0.50 0.50 0.50 B A A B 2.90 13.25 "
  "Standardized Scores 3.15/4.00 3.08/4.00 13.25 3/10 Academic Information "
  "Cumulative Weighted GPA Cumulative Unweighted GPA HS Units Earned Class "
  "Rank Notes/Activities Public Speaking Advisory Habits of Mind PBIS Seal: "
  "Executive Director 1 of 1"
  json_folder = "bepjncdojl"

  result_1, result_2 = utils_functions.form_parser_entities_mapping(
    form_parser_entity_list, mapping_dict, form_parser_text, json_folder)
  assert result_1 == expected_result
  assert result_2 is False


def test_check_duplicate_keys():
  expected_result = True

  dictme = {
    "Name": ["Name"], "Organization": ["Organization"],
    "Experience Title": ["Experience Title"],
    "Date Graduated": ["Date Graduated"], "Credits Earned": ["Credits Earned"],
    "Description": ["Description"], "URL": ["URL"],
    "Competencies": ["Competencies"], "Skills": ["Skills"]
  }

  without_noise = [{
    "key": "RPS ID", "key_coordinates": [0.0467, 0.1358, 0.1015, 0.1358,
                                         0.1015, 0.1464, 0.0467, 0.1464],
    "value": "12345",
    "value_coordinates": [0.2117, 0.1354, 0.2493, 0.1354, 0.2493, 0.1473,
                          0.2117, 0.1473], "key_confidence": 0.95,
    "value_confidence": 0.95,
    "page_no": 1, "page_width": 1757, "page_height": 2275
  },
    {
      "key": "Name", "key_coordinates": [0.0466, 0.1222, 0.0832, 0.1222,
                                         0.0832, 0.1345, 0.0466, 0.1345],
      "value": "John Smith",
      "value_coordinates": [0.2134, 0.1218, 0.2851, 0.1218, 0.2851, 0.1341,
                            0.2134, 0.1341], "key_confidence": 0.9,
      "value_confidence": 0.9,
      "page_no": 1, "page_width": 1757, "page_height": 2275
    },
    {
      "key": "Gender", "key_coordinates": [0.0461, 0.1613, 0.0995, 0.1613,
                                           0.0995, 0.1714, 0.0461, 0.1714],
      "value": "Male",
      "value_coordinates": [0.21, 0.1609, 0.2396, 0.1609, 0.2396, 0.1705, 0.21,
                            0.1705], "key_confidence": 0.85,
      "value_confidence": 0.85, "page_no": 1,
      "page_width": 1757, "page_height": 2275}]

  result = utils_functions.check_duplicate_keys(dictme, without_noise)
  assert result == expected_result


@pytest.mark.parametrize("text, expected_result", [
  ("4.0", True), ("4", False)])
def test_check_int(text, expected_result):
  result = utils_functions.check_int(text)
  assert result == expected_result


@pytest.mark.parametrize("text, expected_result", [
  ("!@#Test string$%^", "Test string"), ("Test string", "Test string")])
def test_clean_form_parser_keys(text, expected_result):
  result = utils_functions.clean_form_parser_keys(text)
  assert result == expected_result


@pytest.mark.parametrize("text, expected_result", [
  ("  Test string  ", "Test string"), (" Test string ", "Test string")])
def test_strip_value(text, expected_result):
  result = utils_functions.strip_value(text)
  assert result == expected_result


@pytest.mark.parametrize("pattern, expected_result", [
  (r"What is your gender\?\n\d\.(.*?)\n\d", None),
  (r"What is your graduation date\?\n\d\.(.*?)\((mm/dd/yyyy)", None)])
def test_pattern_based_entities(pattern, expected_result):
  parser_data = {"text": "Legacy Academy of Excellence Charter School 4029 "
                         "Prairie Road Rockford, IL 61102 www.legacyacademy.com Legacy Academy of "
                         "Excellence Charter School Legacy An International Baccalaureate MYP World "
                         "School High School Transcript of Student Progress Middle Years Programme "
                         "Date Issued: August 3, 2017 Name: John Smith Date Graduated: RPS ID: "
                         "12345 Guardian: Birthdate: Apr 12, 2001 Address: Gender: Male Jun 15, "
                         "2018 Julie Smith 123 Maple St Rockford, IL 61101 Requirements 4 English "
                         "2 Fine Arts 3 Mathematics 2 Physical Education 3 Science 1 Technology 3 "
                         "Social Science 2 Career Education 4 World Languages A minimum of 24 total "
                         "credits is required for a diploma Non-Credit Requirements 40 Hours of "
                         "Service Learning Hours Driver Education Constitution (Public Law 195) "
                         "Consumer Education Attendance Fall 2013: 89/95 Spring 2014: 92/95 Grade "
                         "A B C D F S-Modified 2 2 1 1 0 Weighted Credit Value Reg Honors "
                         "Advanced/Telescopic 5 6 3 4 5 2 3 4 1 0 Freshman Year First Semester "
                         "Course Grade 13110 Survey of Literature B 53810 Spanish A 43310 Algebra 1 B "
                         "23110 World Cultures A 99010 - Physical Education C 33110 Environmental "
                         "Science F 62210 Design B Semester GPA Cumulative GPA 2.69 Credits 0.50 "
                         "0.50 0.50 0.50 0.50 0.50 0.25 Second Semester Course Grade 13110 Survey of "
                         "Literature D 23110 World Cultures B 33110 Environmental Science A 43310 "
                         "Algebra 1 B 53810- Spanish A 99010 - Physical Education D 91510 Art A "
                         "Semester GPA Cumulative GPA 2.73 Credits 0.50 0.50 0.50 0.50 0.50 0.50 "
                         "0.25 3.25 6.50 Grade B B B First Semester Course 13120 American Literature "
                         "43410 Geometry 23610 United States History 33110 Environmental Science "
                         "53820- Spanish 91510 Art 99020- Physical Education Semester GPA Cumulative "
                         "GPA Sophomore Year Second Semester Credits Course Grade 0.50 13120 American "
                         "Literature (Honors) B 0.50 43410 Geometry A 0.50 23610 United States "
                         "History (Honors) B 0.50 33110 Environmental Science B 0.50 53820- Spanish "
                         "A 0.25 91510 Art A 0.50 99210 Health A Semester GPA 9.75 Cumulative GPA "
                         "3.15 Credits 0.50 0.50 0.50 0.50 0.50 0.50 0.50 B A A B 2.90 13.25 "
                         "Standardized Scores 3.15/4.00 3.08/4.00 13.25 3/10 Academic Information "
                         "Cumulative Weighted GPA Cumulative Unweighted GPA HS Units Earned Class "
                         "Rank Notes/Activities Public Speaking Advisory Habits of Mind PBIS Seal: "
                         "Executive Director 1 of 1"}
  result = utils_functions.pattern_based_entities(parser_data, pattern)
  assert result == expected_result


def test_derived_entities_extraction():
  expected_result = {
    "What is your graduation date?": {
      "entity": "What is your graduation date?", "value": None,
      "extraction_confidence": None, "manual_extraction": True,
      "corrected_value": None, "value_coordinates": None,
      "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None},
    "What is your gender?": {
      "entity": "What is your gender?", "value": None,
      "extraction_confidence": None, "manual_extraction": True,
      "corrected_value": None, "value_coordinates": None,
      "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}
  }

  parser_data = {"text": "Legacy Academy of Excellence Charter School 4029 "
                         "Prairie Road Rockford, IL 61102 www.legacyacademy.com Legacy Academy of "
                         "Excellence Charter School Legacy An International Baccalaureate MYP World "
                         "School High School Transcript of Student Progress Middle Years Programme "
                         "Date Issued: August 3, 2017 Name: John Smith Date Graduated: RPS ID: "
                         "12345 Guardian: Birthdate: Apr 12, 2001 Address: Gender: Male Jun 15, "
                         "2018 Julie Smith 123 Maple St Rockford, IL 61101 Requirements 4 English "
                         "2 Fine Arts 3 Mathematics 2 Physical Education 3 Science 1 Technology 3 "
                         "Social Science 2 Career Education 4 World Languages A minimum of 24 total "
                         "credits is required for a diploma Non-Credit Requirements 40 Hours of "
                         "Service Learning Hours Driver Education Constitution (Public Law 195) "
                         "Consumer Education Attendance Fall 2013: 89/95 Spring 2014: 92/95 Grade "
                         "A B C D F S-Modified 2 2 1 1 0 Weighted Credit Value Reg Honors "
                         "Advanced/Telescopic 5 6 3 4 5 2 3 4 1 0 Freshman Year First Semester "
                         "Course Grade 13110 Survey of Literature B 53810 Spanish A 43310 Algebra 1 B "
                         "23110 World Cultures A 99010 - Physical Education C 33110 Environmental "
                         "Science F 62210 Design B Semester GPA Cumulative GPA 2.69 Credits 0.50 "
                         "0.50 0.50 0.50 0.50 0.50 0.25 Second Semester Course Grade 13110 Survey of "
                         "Literature D 23110 World Cultures B 33110 Environmental Science A 43310 "
                         "Algebra 1 B 53810- Spanish A 99010 - Physical Education D 91510 Art A "
                         "Semester GPA Cumulative GPA 2.73 Credits 0.50 0.50 0.50 0.50 0.50 0.50 "
                         "0.25 3.25 6.50 Grade B B B First Semester Course 13120 American Literature "
                         "43410 Geometry 23610 United States History 33110 Environmental Science "
                         "53820- Spanish 91510 Art 99020- Physical Education Semester GPA Cumulative "
                         "GPA Sophomore Year Second Semester Credits Course Grade 0.50 13120 American "
                         "Literature (Honors) B 0.50 43410 Geometry A 0.50 23610 United States "
                         "History (Honors) B 0.50 33110 Environmental Science B 0.50 53820- Spanish "
                         "A 0.25 91510 Art A 0.50 99210 Health A Semester GPA 9.75 Cumulative GPA "
                         "3.15 Credits 0.50 0.50 0.50 0.50 0.50 0.50 0.50 B A A B 2.90 13.25 "
                         "Standardized Scores 3.15/4.00 3.08/4.00 13.25 3/10 Academic Information "
                         "Cumulative Weighted GPA Cumulative Unweighted GPA HS Units Earned Class "
                         "Rank Notes/Activities Public Speaking Advisory Habits of Mind PBIS Seal: "
                         "Executive Director 1 of 1"}

  derived_entities = {
    "What is your graduation date?": {
      "rule": "What is your graduation date\\?\\n\\d\\.(.*?)\\((mm/dd/yyyy)"
    },
    "What is your gender?": {
      "rule": "What is your gender\\?\\n\\d\\.(.*?)\\n\\d"}
  }

  result = utils_functions.derived_entities_extraction(parser_data,
                                                       derived_entities)
  assert result == expected_result


def test_separate_out_PE():
  expected_result = [[
    {"entity": "Name", "value": "John Smith", "extraction_confidence": 0.9,
     "manual_extraction": False, "corrected_value": None,
     "value_coordinates": [0.2134, 0.1218, 0.2851, 0.1218, 0.2851, 0.1341,
                           0.2134, 0.1341],
     "key_coordinates": [0.0466, 0.1222, 0.0832, 0.1222,
                         0.0832, 0.1345, 0.0466, 0.1345], "page_no": 1,
     "page_width": 1757,
     "page_height": 2275}, {"entity": "Organization", "value": None,
                            "extraction_confidence": None,
                            "manual_extraction": False,
                            "corrected_value": None, "value_coordinates": None,
                            "key_coordinates": None,
                            "page_no": None, "page_width": None,
                            "page_height": None},
    {"entity": "Experience Title",
     "value": "13120 American Literature (Honors)",
     "extraction_confidence": 0.99988645, "manual_extraction": False,
     "corrected_value": None, "value_coordinates": None,
     "key_coordinates": None,
     "page_no": None, "page_width": None, "page_height": None},
    {"entity": "Date Graduated", "value": "Jun 15, 2018",
     "extraction_confidence": 0.83, "manual_extraction": False,
     "corrected_value": None, "value_coordinates": [0.6915, 0.1235, 0.782,
                                                    0.1235, 0.782, 0.1336,
                                                    0.6915, 0.1336],
     "key_coordinates": [0.4731, 0.1218,
                         0.5875, 0.1218, 0.5875, 0.1349, 0.4731, 0.1349],
     "page_no": 1,
     "page_width": 1757, "page_height": 2275}, {"entity": "Credits Earned",
                                                "value": "0.50",
                                                "extraction_confidence": 0.99976027,
                                                "manual_extraction": False,
                                                "corrected_value": None,
                                                "value_coordinates": None,
                                                "key_coordinates": None,
                                                "page_no": None,
                                                "page_width": None,
                                                "page_height": None},
    {"entity": "Description",
     "value": None, "extraction_confidence": None, "manual_extraction": False,
     "corrected_value": None, "value_coordinates": None,
     "key_coordinates": None,
     "page_no": None, "page_width": None, "page_height": None},
    {"entity": "URL", "value": None, "extraction_confidence": None,
     "manual_extraction": False, "corrected_value": None,
     "value_coordinates": None, "key_coordinates": None, "page_no": None,
     "page_width": None, "page_height": None}, {"entity": "Competencies",
                                                "value": None,
                                                "extraction_confidence": None,
                                                "manual_extraction": False,
                                                "corrected_value": None,
                                                "value_coordinates": None,
                                                "key_coordinates": None,
                                                "page_no": None,
                                                "page_width": None,
                                                "page_height": None}, {
      "entity": "Skills", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None,
      "value_coordinates": None, "key_coordinates": None, "page_no": None,
      "page_width": None, "page_height": None}], [{"entity": "Name",
                                                   "value": "John Smith",
                                                   "extraction_confidence": 0.9,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": [0.2134,
                                                                         0.1218,
                                                                         0.2851,
                                                                         0.1218,
                                                                         0.2851,
                                                                         0.1341,
                                                                         0.2134,
                                                                         0.1341],
                                                   "key_coordinates": [0.0466,
                                                                       0.1222,
                                                                       0.0832,
                                                                       0.1222,
                                                                       0.0832,
                                                                       0.1345,
                                                                       0.0466,
                                                                       0.1345],
                                                   "page_no": 1,
                                                   "page_width": 1757,
                                                   "page_height": 2275},
                                                  {"entity": "Organization",
                                                   "value": None,
                                                   "extraction_confidence": None,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": None,
                                                   "key_coordinates": None,
                                                   "page_no": None,
                                                   "page_width": None,
                                                   "page_height": None},
                                                  {"entity": "Experience Title",
                                                   "value": "43410 Geometry",
                                                   "extraction_confidence": 0.99990773,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": None,
                                                   "key_coordinates": None,
                                                   "page_no": None,
                                                   "page_width": None,
                                                   "page_height": None},
                                                  {"entity": "Date Graduated",
                                                   "value": "Jun 15, 2018",
                                                   "extraction_confidence": 0.83,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": [0.6915,
                                                                         0.1235,
                                                                         0.782,
                                                                         0.1235,
                                                                         0.782,
                                                                         0.1336,
                                                                         0.6915,
                                                                         0.1336],
                                                   "key_coordinates": [0.4731,
                                                                       0.1218,
                                                                       0.5875,
                                                                       0.1218,
                                                                       0.5875,
                                                                       0.1349,
                                                                       0.4731,
                                                                       0.1349],
                                                   "page_no": 1,
                                                   "page_width": 1757,
                                                   "page_height": 2275},
                                                  {"entity": "Credits Earned",
                                                   "value": "0.50",
                                                   "extraction_confidence": 0.99978155,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": None,
                                                   "key_coordinates": None,
                                                   "page_no": None,
                                                   "page_width": None,
                                                   "page_height": None},
                                                  {"entity": "Description",
                                                   "value": None,
                                                   "extraction_confidence": None,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": None,
                                                   "key_coordinates": None,
                                                   "page_no": None,
                                                   "page_width": None,
                                                   "page_height": None},
                                                  {"entity": "URL",
                                                   "value": None,
                                                   "extraction_confidence": None,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": None,
                                                   "key_coordinates": None,
                                                   "page_no": None,
                                                   "page_width": None,
                                                   "page_height": None},
                                                  {"entity": "Competencies",
                                                   "value": None,
                                                   "extraction_confidence": None,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": None,
                                                   "key_coordinates": None,
                                                   "page_no": None,
                                                   "page_width": None,
                                                   "page_height": None},
                                                  {"entity": "Skills",
                                                   "value": None,
                                                   "extraction_confidence": None,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": None,
                                                   "key_coordinates": None,
                                                   "page_no": None,
                                                   "page_width": None,
                                                   "page_height": None}],
    [{"entity": "Name", "value": "John Smith",
      "extraction_confidence": 0.9, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.2134, 0.1218, 0.2851,
                                                     0.1218, 0.2851, 0.1341,
                                                     0.2134, 0.1341],
      "key_coordinates": [0.0466,
                          0.1222, 0.0832, 0.1222, 0.0832, 0.1345, 0.0466,
                          0.1345], "page_no": 1,
      "page_width": 1757, "page_height": 2275}, {"entity": "Organization",
                                                 "value": None,
                                                 "extraction_confidence": None,
                                                 "manual_extraction": False,
                                                 "corrected_value": None,
                                                 "value_coordinates": None,
                                                 "key_coordinates": None,
                                                 "page_no": None,
                                                 "page_width": None,
                                                 "page_height": None},
     {"entity": "Experience Title",
      "value": "23610 United States History (Honors)",
      "extraction_confidence": 0.99992675, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None,
      "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "Date Graduated",
                             "value": "Jun 15, 2018",
                             "extraction_confidence": 0.83,
                             "manual_extraction": False,
                             "corrected_value": None,
                             "value_coordinates": [0.6915, 0.1235, 0.782,
                                                   0.1235, 0.782, 0.1336,
                                                   0.6915, 0.1336],
                             "key_coordinates": [0.4731, 0.1218, 0.5875, 0.1218,
                                                 0.5875, 0.1349, 0.4731,
                                                 0.1349], "page_no": 1,
                             "page_width": 1757,
                             "page_height": 2275},
     {"entity": "Credits Earned", "value": "0.50",
      "extraction_confidence": 0.99980056, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None,
      "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "Description", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates": None, "page_no": None,
                             "page_width": None,
                             "page_height": None},
     {"entity": "URL", "value": None,
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None,
      "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "Competencies", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates": None, "page_no": None,
                             "page_width": None,
                             "page_height": None},
     {"entity": "Skills", "value": None,
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None,
      "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}], [{"entity": "Name", "value": "John Smith",
                               "extraction_confidence": 0.9,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": [0.2134, 0.1218, 0.2851,
                                                     0.1218, 0.2851, 0.1341,
                                                     0.2134, 0.1341],
                               "key_coordinates": [0.0466,
                                                   0.1222, 0.0832, 0.1222,
                                                   0.0832, 0.1345, 0.0466,
                                                   0.1345], "page_no": 1,
                               "page_width": 1757, "page_height": 2275},
                              {"entity": "Organization",
                               "value": None, "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": None,
                               "key_coordinates": None, "page_no": None,
                               "page_width": None,
                               "page_height": None},
                              {"entity": "Experience Title", "value":
                                "33110 Environmental Science",
                               "extraction_confidence": 0.99986404,
                               "manual_extraction": False,
                               "corrected_value": None, "value_coordinates":
                                 None, "key_coordinates": None, "page_no": None,
                               "page_width": None,
                               "page_height": None},
                              {"entity": "Date Graduated", "value":
                                "Jun 15, 2018", "extraction_confidence": 0.83,
                               "manual_extraction":
                                 False, "corrected_value": None,
                               "value_coordinates": [0.6915, 0.1235,
                                                     0.782, 0.1235, 0.782,
                                                     0.1336, 0.6915, 0.1336],
                               "key_coordinates": [0.4731,
                                                   0.1218, 0.5875, 0.1218,
                                                   0.5875, 0.1349, 0.4731,
                                                   0.1349], "page_no": 1,
                               "page_width": 1757, "page_height": 2275},
                              {"entity": "Credits Earned",
                               "value": "0.50",
                               "extraction_confidence": 0.99973786,
                               "manual_extraction": False,
                               "corrected_value": None, "value_coordinates":
                                 None, "key_coordinates": None, "page_no": None,
                               "page_width": None,
                               "page_height": None},
                              {"entity": "Description", "value": None,
                               "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": None, "key_coordinates":
                                 None, "page_no": None, "page_width": None,
                               "page_height": None},
                              {"entity": "URL", "value": None,
                               "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None, "value_coordinates":
                                 None, "key_coordinates": None, "page_no": None,
                               "page_width": None,
                               "page_height": None},
                              {"entity": "Competencies", "value": None,
                               "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": None, "key_coordinates":
                                 None, "page_no": None, "page_width": None,
                               "page_height": None},
                              {"entity": "Skills", "value": None,
                               "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None, "value_coordinates":
                                 None, "key_coordinates": None, "page_no": None,
                               "page_width": None,
                               "page_height": None}],
    [{"entity": "Name", "value": "John Smith",
      "extraction_confidence": 0.9, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.2134, 0.1218, 0.2851,
                                                     0.1218, 0.2851, 0.1341,
                                                     0.2134, 0.1341],
      "key_coordinates": [0.0466,
                          0.1222, 0.0832, 0.1222, 0.0832, 0.1345, 0.0466,
                          0.1345], "page_no": 1,
      "page_width": 1757, "page_height": 2275}, {"entity": "Organization",
                                                 "value": None,
                                                 "extraction_confidence": None,
                                                 "manual_extraction": False,
                                                 "corrected_value": None,
                                                 "value_coordinates": None,
                                                 "key_coordinates":
                                                   None, "page_no": None,
                                                 "page_width": None,
                                                 "page_height": None},
     {"entity": "Experience Title", "value": "53820- Spanish",
      "extraction_confidence": 0.9998619, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None, "key_coordinates":
        None, "page_no": None, "page_width": None, "page_height": None},
     {"entity": "Date Graduated", "value": "Jun 15, 2018",
      "extraction_confidence": 0.83, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.6915, 0.1235, 0.782,
                                                     0.1235, 0.782, 0.1336,
                                                     0.6915, 0.1336],
      "key_coordinates": [0.4731,
                          0.1218, 0.5875, 0.1218, 0.5875, 0.1349, 0.4731,
                          0.1349], "page_no": 1,
      "page_width": 1757, "page_height": 2275}, {"entity": "Credits Earned",
                                                 "value": "0.50",
                                                 "extraction_confidence": 0.99973571,
                                                 "manual_extraction":
                                                   False,
                                                 "corrected_value": None,
                                                 "value_coordinates": None,
                                                 "key_coordinates": None,
                                                 "page_no": None,
                                                 "page_width": None,
                                                 "page_height": None},
     {"entity": "Description", "value": None,
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None, "key_coordinates":
        None, "page_no": None, "page_width": None, "page_height": None},
     {"entity": "URL", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
        None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "Competencies", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates":
                               None, "page_no": None, "page_width": None,
                             "page_height": None},
     {"entity": "Skills", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
        None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}], [{"entity": "Name", "value": "John Smith",
                               "extraction_confidence": 0.9,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": [0.2134, 0.1218, 0.2851,
                                                     0.1218, 0.2851, 0.1341,
                                                     0.2134, 0.1341],
                               "key_coordinates": [0.0466,
                                                   0.1222, 0.0832, 0.1222,
                                                   0.0832, 0.1345, 0.0466,
                                                   0.1345], "page_no": 1,
                               "page_width": 1757, "page_height": 2275},
                              {"entity": "Organization",
                               "value": None, "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": None, "key_coordinates":
                                 None, "page_no": None, "page_width": None,
                               "page_height": None},
                              {"entity": "Experience Title",
                               "value": "91510 Art",
                               "extraction_confidence": 0.99993157,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": None, "key_coordinates":
                                 None, "page_no": None, "page_width": None,
                               "page_height": None},
                              {"entity": "Date Graduated",
                               "value": "Jun 15, 2018",
                               "extraction_confidence": 0.83,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": [0.6915, 0.1235, 0.782,
                                                     0.1235, 0.782, 0.1336,
                                                     0.6915, 0.1336],
                               "key_coordinates": [0.4731,
                                                   0.1218, 0.5875, 0.1218,
                                                   0.5875, 0.1349, 0.4731,
                                                   0.1349], "page_no": 1,
                               "page_width": 1757, "page_height": 2275},
                              {"entity": "Credits Earned",
                               "value": "0.25",
                               "extraction_confidence": 0.99980539,
                               "manual_extraction":
                                 False, "corrected_value": None,
                               "value_coordinates": None,
                               "key_coordinates": None, "page_no": None,
                               "page_width": None,
                               "page_height": None},
                              {"entity": "Description", "value": None,
                               "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": None, "key_coordinates":
                                 None, "page_no": None, "page_width": None,
                               "page_height": None},
                              {"entity": "URL", "value": None,
                               "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None, "value_coordinates":
                                 None, "key_coordinates": None, "page_no": None,
                               "page_width": None,
                               "page_height": None},
                              {"entity": "Competencies", "value": None,
                               "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None,
                               "value_coordinates": None, "key_coordinates":
                                 None, "page_no": None, "page_width": None,
                               "page_height": None},
                              {"entity": "Skills", "value": None,
                               "extraction_confidence": None,
                               "manual_extraction": False,
                               "corrected_value": None, "value_coordinates":
                                 None, "key_coordinates": None, "page_no": None,
                               "page_width": None,
                               "page_height": None}],
    [{"entity": "Name", "value": "John Smith",
      "extraction_confidence": 0.9, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.2134, 0.1218, 0.2851,
                                                     0.1218, 0.2851, 0.1341,
                                                     0.2134, 0.1341],
      "key_coordinates": [0.0466,
                          0.1222, 0.0832, 0.1222, 0.0832, 0.1345, 0.0466,
                          0.1345], "page_no": 1,
      "page_width": 1757, "page_height": 2275}, {"entity": "Organization",
                                                 "value": None,
                                                 "extraction_confidence": None,
                                                 "manual_extraction": False,
                                                 "corrected_value": None,
                                                 "value_coordinates": None,
                                                 "key_coordinates":
                                                   None, "page_no": None,
                                                 "page_width": None,
                                                 "page_height": None},
     {"entity": "Experience Title", "value": "99210 Health",
      "extraction_confidence": 0.99973142, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None, "key_coordinates":
        None, "page_no": None, "page_width": None, "page_height": None},
     {"entity": "Date Graduated", "value": "Jun 15, 2018",
      "extraction_confidence": 0.83, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.6915, 0.1235, 0.782,
                                                     0.1235, 0.782, 0.1336,
                                                     0.6915, 0.1336],
      "key_coordinates": [0.4731,
                          0.1218, 0.5875, 0.1218, 0.5875, 0.1349, 0.4731,
                          0.1349], "page_no": 1,
      "page_width": 1757, "page_height": 2275}, {"entity": "Credits Earned",
                                                 "value": "0.50",
                                                 "extraction_confidence": 0.99960518,
                                                 "manual_extraction":
                                                   False,
                                                 "corrected_value": None,
                                                 "value_coordinates": None,
                                                 "key_coordinates": None,
                                                 "page_no": None,
                                                 "page_width": None,
                                                 "page_height": None},
     {"entity": "Description", "value": None,
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None,
      "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "URL", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates":
                               None, "page_no": None, "page_width": None,
                             "page_height": None},
     {"entity": "Competencies", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
        None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "Skills", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates":
                               None, "page_no": None, "page_width": None,
                             "page_height": None}],
    [{"entity": "Name", "value": "John Smith", "extraction_confidence": 0.9,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
        [0.2134, 0.1218, 0.2851, 0.1218, 0.2851, 0.1341, 0.2134, 0.1341],
      "key_coordinates": [0.0466, 0.1222, 0.0832, 0.1222, 0.0832, 0.1345,
                          0.0466, 0.1345], "page_no": 1, "page_width": 1757,
      "page_height": 2275},
     {"entity": "Organization", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
        None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "Experience Title", "value":
      "Semester GPA", "extraction_confidence": 0.99401915, "manual_extraction":
                               False, "corrected_value": None,
                             "value_coordinates": None,
                             "key_coordinates": None, "page_no": None,
                             "page_width": None,
                             "page_height": None},
     {"entity": "Date Graduated", "value":
       "Jun 15, 2018", "extraction_confidence": 0.83,
      "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.6915, 0.1235, 0.782,
                                                     0.1235, 0.782, 0.1336,
                                                     0.6915, 0.1336],
      "key_coordinates": [0.4731,
                          0.1218, 0.5875, 0.1218, 0.5875, 0.1349, 0.4731,
                          0.1349], "page_no": 1,
      "page_width": 1757, "page_height": 2275}, {"entity": "Credits Earned",
                                                 "value": None,
                                                 "extraction_confidence": None,
                                                 "manual_extraction": False,
                                                 "corrected_value": None,
                                                 "value_coordinates": None,
                                                 "key_coordinates":
                                                   None, "page_no": None,
                                                 "page_width": None,
                                                 "page_height": None},
     {"entity": "Description", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
        None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "URL", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates":
                               None, "page_no": None, "page_width": None,
                             "page_height": None},
     {"entity": "Competencies", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
        None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None}, {"entity": "Skills", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates":
                               None, "page_no": None, "page_width": None,
                             "page_height": None}], [{
      "entity": "Name", "value": "John Smith", "extraction_confidence": 0.9,
      "manual_extraction": False, "corrected_value": None,
      "value_coordinates": [0.2134, 0.1218, 0.2851, 0.1218, 0.2851, 0.1341,
                            0.2134, 0.1341],
      "key_coordinates": [0.0466, 0.1222, 0.0832, 0.1222,
                          0.0832, 0.1345, 0.0466, 0.1345], "page_no": 1,
      "page_width": 1757,
      "page_height": 2275}, {"entity": "Organization", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates":
                               None, "page_no": None, "page_width": None,
                             "page_height": None}, {
      "entity": "Experience Title", "value": "Cumulative GPA",
      "extraction_confidence": 0.99953663, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None, "key_coordinates":
        None, "page_no": None, "page_width": None, "page_height": None}, {
      "entity": "Date Graduated", "value": "Jun 15, 2018",
      "extraction_confidence": 0.83, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.6915, 0.1235,
                                                     0.782, 0.1235, 0.782,
                                                     0.1336, 0.6915, 0.1336],
      "key_coordinates":
        [0.4731, 0.1218, 0.5875, 0.1218, 0.5875, 0.1349, 0.4731, 0.1349],
      "page_no": 1, "page_width": 1757, "page_height": 2275}, {"entity":
                                                                 "Credits Earned",
                                                               "value": "9.75",
                                                               "extraction_confidence": 0.99941039,
                                                               "manual_extraction": False,
                                                               "corrected_value": None,
                                                               "value_coordinates":
                                                                 None,
                                                               "key_coordinates": None,
                                                               "page_no": None,
                                                               "page_width": None,
                                                               "page_height": None},
      {"entity": "Description", "value": None,
       "extraction_confidence": None, "manual_extraction": False,
       "corrected_value": None, "value_coordinates": None, "key_coordinates":
         None, "page_no": None, "page_width": None, "page_height": None}, {
        "entity": "URL", "value": None, "extraction_confidence": None,
        "manual_extraction": False, "corrected_value": None,
        "value_coordinates": None, "key_coordinates": None, "page_no": None,
        "page_width": None, "page_height": None}, {"entity": "Competencies",
                                                   "value": None,
                                                   "extraction_confidence": None,
                                                   "manual_extraction": False,
                                                   "corrected_value": None,
                                                   "value_coordinates": None,
                                                   "key_coordinates":
                                                     None, "page_no": None,
                                                   "page_width": None,
                                                   "page_height": None},
      {"entity": "Skills", "value": None, "extraction_confidence": None,
       "manual_extraction": False, "corrected_value": None, "value_coordinates":
         None, "key_coordinates": None, "page_no": None, "page_width": None,
       "page_height": None}]]

  extracted_entities = [
    {
      "entity": "Name", "value": "John Smith", "extraction_confidence": 0.9,
      "manual_extraction": False, "corrected_value": None,
      "value_coordinates": [0.2134, 0.1218, 0.2851, 0.1218, 0.2851, 0.1341,
                            0.2134, 0.1341],
      "key_coordinates": [0.0466, 0.1222, 0.0832, 0.1222,
                          0.0832, 0.1345, 0.0466, 0.1345], "page_no": 1,
      "page_width": 1757,
      "page_height": 2275}, {"entity": "Organization", "value": None,
                             "extraction_confidence": None,
                             "manual_extraction": False,
                             "corrected_value": None, "value_coordinates": None,
                             "key_coordinates": None, "page_no": None,
                             "page_width": None,
                             "page_height": None},
    {"entity": "Experience Title", "value": None,
     "extraction_confidence": None, "manual_extraction": False,
     "corrected_value": None, "value_coordinates": None, "key_coordinates":
       None, "page_no": None, "page_width": None, "page_height": None
     },
    {
      "entity": "Date Graduated", "value": "Jun 15, 2018",
      "extraction_confidence": 0.83, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": [0.6915, 0.1235, 0.782,
                                                     0.1235, 0.782, 0.1336,
                                                     0.6915, 0.1336],
      "key_coordinates": [0.4731,
                          0.1218, 0.5875, 0.1218, 0.5875, 0.1349, 0.4731,
                          0.1349], "page_no": 1,
      "page_width": 1757, "page_height": 2275}, {"entity": "Credits Earned",
                                                 "value": None,
                                                 "extraction_confidence": None,
                                                 "manual_extraction": False,
                                                 "corrected_value": None,
                                                 "value_coordinates": None,
                                                 "key_coordinates":
                                                   None, "page_no": None,
                                                 "page_width": None,
                                                 "page_height": None
                                                 },
    {
      "entity": "Description", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
      None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None
    },
    {
      "entity": "URL", "value": None,
      "extraction_confidence": None, "manual_extraction": False,
      "corrected_value": None, "value_coordinates": None, "key_coordinates":
      None, "page_no": None, "page_width": None, "page_height": None
    },
    {
      "entity": "Competencies", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
      None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None
    },
    {
      "entity": "Skills", "value": None, "extraction_confidence": None,
      "manual_extraction": False, "corrected_value": None, "value_coordinates":
      None, "key_coordinates": None, "page_no": None, "page_width": None,
      "page_height": None
    },
    {
      "entity": "experience_title", "value":
      ["13120 American Literature (Honors)", "43410 Geometry",
       "23610 United States History (Honors)", "33110 Environmental Science",
       "53820- Spanish", "91510 Art", "99210 Health", "Semester GPA",
       "Cumulative GPA"],
      "extraction_confidence": [0.99988645, 0.99990773, 0.99992675, 0.99986404,
                                0.9998619, 0.99993157, 0.99973142, 0.99401915,
                                0.99953663]
    },
    {
      "entity": "credits_earned", "value": ["0.50", "0.50", "0.50", "0.50",
                                            "0.50", "0.25", "0.50", None,
                                            "9.75", "0.50", "0.50", "0.50",
                                            "0.50",
                                            "0.50", "0.50", "0.50", None,
                                            "13.25"], "extraction_confidence":
      [0.99976027, 0.99978155, 0.99980056, 0.99973786, 0.99973571, 0.99980539,
       0.99960518, None, 0.99941039, 0.99985754, 0.99987876, 0.99989784,
       0.99983513, 0.99983299, 0.99990261, 0.99970245, None, 0.99950767]
    }]

  result = utils_functions.separate_out_PE(extracted_entities)
  assert result == expected_result


def test_extract_entities_from_table_response():
  expected_result = [
    {
      "entity": "experience_title", "value":
      ["13120 American Literature (Honors)", "43410 Geometry",
       "23610 United States History (Honors)", "33110 Environmental Science",
       "53820- Spanish", "91510 Art", "99210 Health", "Semester GPA",
       "Cumulative GPA"], "extraction_confidence": [0.99988645, 0.99990773,
                                                    0.99992675, 0.99986404,
                                                    0.9998619, 0.99993157,
                                                    0.99973142, 0.99401915,
                                                    0.99953663]
    },
    {
      "entity": "credits_earned", "value": ["0.50", "0.50", "0.50", "0.50",
                                            "0.50", "0.25", "0.50", None,
                                            "9.75", "0.50", "0.50", "0.50",
                                            "0.50",
                                            "0.50", "0.50", "0.50", None,
                                            "13.25"], "extraction_confidence": [
      0.99976027, 0.99978155, 0.99980056, 0.99973786, 0.99973571, 0.99980539,
      0.99960518, None, 0.99941039, 0.99985754, 0.99987876, 0.99989784,
      0.99983513, 0.99983299, 0.99990261, 0.99970245, None, 0.99950767]
    }]
  table_response = [
    {
      "keys": ["Credits", "Course", "Credits"], "values": [["0.50", "0.50",
                                                            "0.50", "0.50",
                                                            "0.50", "0.25",
                                                            "0.50", None,
                                                            "9.75"],
                                                           [
                                                             "13120 American Literature (Honors)",
                                                             "43410 Geometry",
                                                             "23610 United States History (Honors)",
                                                             "33110 Environmental Science",
                                                             "53820- Spanish",
                                                             "91510 Art",
                                                             "99210 Health",
                                                             "Semester GPA",
                                                             "Cumulative GPA"],
                                                           ["0.50", "0.50",
                                                            "0.50", "0.50",
                                                            "0.50", "0.50",
                                                            "0.50", None,
                                                            "13.25"]],
      "confidence": [[0.99976027, 0.99978155,
                      0.99980056, 0.99973786, 0.99973571, 0.99980539,
                      0.99960518, None,
                      0.99941039],
                     [0.99988645, 0.99990773, 0.99992675, 0.99986404, 0.9998619,
                      0.99993157, 0.99973142, 0.99401915, 0.99953663],
                     [0.99985754, 0.99987876,
                      0.99989784, 0.99983513, 0.99983299, 0.99990261,
                      0.99970245, None,
                      0.99950767]]}]
  result = utils_functions.extract_entities_from_table_response(table_response)
  assert result == expected_result


def test_save_prior_experience_items(firestore_emulator, clean_firestore):
  extracted_items = [
    {
      "name": {
        "text": "John Smith",
        "score": 0.9
      },
      "skills": {
        "text": None,
        "score": None
      },
      "competencies": {
        "text": None,
        "score": None
      },
      "organization": {
        "text": None,
        "score": None
      },
      "experience_title": {
        "text": "13120 American Literature (Honors)",
        "score": 1
      },
      "date_completed": {
        "text": "Jun 15, 2018",
        "score": 0.83
      },
      "credits_earned": {
        "text": "0.50",
        "score": 1
      },
      "description": {
        "text": None,
        "score": None
      },
      "url": {
        "text": None,
        "score": None
      }
    }]
  utils_functions.save_prior_experience_items(extracted_items)

  prior_experiences = PriorExperience.collection.fetch()
  for prior_experience in prior_experiences:
    assert prior_experience.experience_title == \
           extracted_items[0]["experience_title"]["text"]
    assert prior_experience.credits_earned == \
           float(extracted_items[0]["credits_earned"]["text"])
    assert prior_experience.date_completed.strftime("%b %d, %Y") == \
           extracted_items[0]["date_completed"]["text"]
