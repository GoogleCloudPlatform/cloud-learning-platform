"""Unit Test for Extract Entities script"""

from unittest import mock
with mock.patch("google.cloud.storage.Client",
side_effect = mock.MagicMock()) as mok:
  with mock.patch("google.cloud.documentai_v1.DocumentProcessorServiceClient",
    side_effect = mock.MagicMock()) as mok:
    from services.extraction import extract_entities



def test_extract_entities(mocker):
  expected_result = [
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "13120 American Literature (Honors)",
              "score": 1.0
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": "0.50",
              "score": 1.0
          },
          "competencies": {
              "text": None,
              "score": None
          }
      },
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "43410 Geometry",
              "score": 1.0
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": "0.50",
              "score": 1.0
          },
          "competencies": {
              "text": None,
              "score": None
          }
      },
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "23610 United States History (Honors)",
              "score": 1.0
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": "0.50",
              "score": 1.0
          },
          "competencies": {
              "text": None,
              "score": None
          }
      },
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "33110 Environmental Science",
              "score": 1.0
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": "0.50",
              "score": 1.0
          },
          "competencies": {
              "text": None,
              "score": None
          }
      },
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "53820- Spanish",
              "score": 1.0
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": "0.50",
              "score": 1.0
          },
          "competencies": {
              "text": None,
              "score": None
          }
      },
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "91510 Art",
              "score": 1.0
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": "0.25",
              "score": 1.0
          },
          "competencies": {
              "text": None,
              "score": None
          }
      },
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "99210 Health",
              "score": 1.0
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": "0.50",
              "score": 1.0
          },
          "competencies": {
              "text": None,
              "score": None
          }
      },
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "Semester GPA",
              "score": 0.99
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": None,
              "score": None
          },
          "competencies": {
              "text": None,
              "score": None
          }
      },
      {
          "url": {
              "text": None,
              "score": None
          },
          "skills": {
              "text": None,
              "score": None
          },
          "organization": {
              "text": None,
              "score": None
          },
          "name": {
              "text": "John Smith",
              "score": 0.9
          },
          "experience_title": {
              "text": "Cumulative GPA",
              "score": 1.0
          },
          "description": {
              "text": None,
              "score": None
          },
          "date_completed": {
              "text": "Jun 15, 2018", "score": 0.83
          },
          "credits_earned": {
              "text": "9.75",
              "score": 1.0
          },
          "competencies": {
              "text": None,
              "score": None
          }
      }
  ]

  gcs_doc_path_list = [
              "gs://aitutor-dev/pla/user-transcripts/Sample_Transcript.pdf"
              ]
  doc_class = "transcripts"
  context = "generic"

  mocker.patch("services.extraction.extract_entities.form_parser_extraction",
    return_value = [
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
                "value": "13120 American Literature (Honors)",
                "extraction_confidence": 0.99988645,
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
                "value": "0.50",
                "extraction_confidence": 0.99976027,
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
        ],
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
                "value": "43410 Geometry",
                "extraction_confidence": 0.99990773,
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
                "value": "0.50",
                "extraction_confidence": 0.99978155,
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
        ],
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
                "value": "23610 United States History (Honors)",
                "extraction_confidence": 0.99992675,
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
                "value": "0.50",
                "extraction_confidence": 0.99980056,
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
        ],
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
                "value": "33110 Environmental Science",
                "extraction_confidence": 0.99986404,
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
                "value": "0.50",
                "extraction_confidence": 0.99973786,
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
        ],
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
                "value": "53820- Spanish",
                "extraction_confidence": 0.9998619,
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
                "value": "0.50",
                "extraction_confidence": 0.99973571,
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
        ],
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
                "value": "91510 Art",
                "extraction_confidence": 0.99993157,
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
                "value": "0.25",
                "extraction_confidence": 0.99980539,
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
        ],
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
                "value": "99210 Health",
                "extraction_confidence": 0.99973142,
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
                "value": "0.50",
                "extraction_confidence": 0.99960518,
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
        ],
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
                "value": "Semester GPA",
                "extraction_confidence": 0.99401909,
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
        ],
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
                "value": "Cumulative GPA",
                "extraction_confidence": 0.99953663,
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
                "value": "9.75",
                "extraction_confidence": 0.99941039,
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
    )
  result = extract_entities.extract_entities(gcs_doc_path_list, doc_class,
                                            context)
  assert result == expected_result
