""" Schema examples and test objects for unit test """

### PRIOR EXPERIENCE EXAMPLES ###

BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE = {
  "organization": "TPSI",
  "experience_title": "Fundamentals of Accounting",
  "date_completed": "2020-09-15T00:00:00",
  "credits_earned": 6,
  "description": "",
  "url": "",
  "competencies": ["Fields", "Applied Statistics"],
  "skills": ["Accounts", "Mathematics"],
  "documents": [],
  "cpl": 6,
  "is_flagged": False,
  "metadata": {},
  "alignments": {},
  "type_of_experience": "Transcripts",
  "validation_type": {"email": "verification@mail.com",
                      "website": "www.quickverficiation.com"},
  "terms": [
      {
          "end_date": {
              "day": "12",
              "month": "04",
              "year": "2020"
          },
          "transfer_courses": [
              {
                  "course_title": "Coding",
                  "course_code": "COD",
                  "credits": "3",
                  "grade": "B-"
              },
              {
                  "course_title": "Economics",
                  "course_code": "ECO",
                  "credits": "2",
                  "grade": "A"
              }
          ]
      },
      {
          "end_date": {
              "day": "04",
              "month": "08",
              "year": "2014"
          },
          "transfer_courses": [
              {
                  "course_title": "Math",
                  "course_code": "MTH",
                  "credits": "2",
                  "grade": "B+"
              },
              {
                  "course_title": "Accounts",
                  "course_code": "ACC",
                  "credits": "2",
                  "grade": "A-"
              }
          ]
      }
  ]
}

FULL_PRIOR_EXPERIENCE_MODEL_EXAMPLE = {
  "uuid": "44qxEpc35pVMb6AkZGbi",
  "id_number": 10001,
  "progress": 0,
  "is_archived": False,
  "is_flagged": False,
  **BASIC_PRIOR_EXPERIENCE_MODEL_EXAMPLE,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

BASIC_PLA_RECORD_MODEL_EXAMPLE = {
  "title": "PLA Title",
  "user_id": "user_1234",
  "type": "draft",
  "assessor_name": "Request_user",
  "description": "",
  "status": "In progress",
  "prior_experiences": [],
  "approved_experiences": []
}

FULL_PLA_RECORD_MODEL_EXAMPLE = {
  "uuid": "absde1234",
  **BASIC_PLA_RECORD_MODEL_EXAMPLE,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

UPDATE_PLA_RECORD_MODEL_EXAMPLE = {
    **BASIC_PLA_RECORD_MODEL_EXAMPLE, "is_archived": False
}

EXTRACTION_INPUT_EXAMPLE={
  "doc_class": str,
  "document_type": str,
  "context": str,
  "gcs_url": str
}

BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE = {
  "title": "Fundamentals of Accounting",
  "description": "",
  "organization": "TPSI",
  "type": "Transcripts",
  "student_type": "Graduate",
  "class_level": "Mid level",
  "credits_range": {
    "upper_limit": 20,
    "lower_limit": 5},
  "status": "Active",
  "metadata": {}
}

FULL_APPROVED_EXPERIENCE_MODEL_EXAMPLE = {
  "uuid": "44qxEpc35pVMb6AkZGbi",
  **BASIC_APPROVED_EXPERIENCE_MODEL_EXAMPLE,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}
