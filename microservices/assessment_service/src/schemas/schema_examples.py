""" Schema examples and test objects for unit test """
# pylint: disable = line-too-long

### ASSESSMENT ITEMS EXAMPLES ###
BASIC_ASSESSMENT_EXAMPLE = {
    "name": "Assessment 1",
    "type": "practice",
    "order": 1,
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {},
    "max_attempts": 3,
    "pass_threshold": 0.7,
    "achievements": [],
    "alignments": {},
    "references": {},
    "parent_nodes": {
        "learning_objects":[],
        "learning_experiences":[]
    },
    "child_nodes": {},
    "prerequisites": {},
    "metadata": {},
    "alias": "assessment"
}

UPDATE_ASSESSMENT_EXAMPLE = {**BASIC_ASSESSMENT_EXAMPLE}
FULL_ASSESSMENT_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_ASSESSMENT_EXAMPLE,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

### ASSESSMENT ITEMS EXAMPLES ###
BASIC_ASSESSMENT_ITEM_EXAMPLE = {
    "name": "Short name or label for the assessment item.",
    "question": "Assessment item question",
    "answer": "Answer for the question",
    "context": "Context from which the question was created",
    "options": [],
    "question_type": "Type of question",
    "assessment_type": "Type of activity",
    "use_type": "Field to distinguish the type of assessment profile (Formative/Summative)",
    "metadata": {},
    "author": "A person or organization chiefly responsible for the intellectual or artistic content of this assessment item",
    "difficulty": 1,
    "alignments": {},
    "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
    },
    "references": {
        "competencies": [],
        "skills": []
    },
    "child_nodes": {},
    "assessment_reference": {
        "activity_id": "",
        "activity_template_id": "",
        "source": "learnosity"
    },
    "achievements": [],
    "pass_threshold": 1,
    "is_flagged": False,
    "comments": ""
}

UPDATE_ASSESSMENT_ITEM_EXAMPLE = {**BASIC_ASSESSMENT_ITEM_EXAMPLE}

FULL_ASSESSMENT_ITEM_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_ASSESSMENT_ITEM_EXAMPLE,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

### ASSESSMENT ITEMS EXAMPLES ###
BASIC_RUBRIC_EXAMPLE = {
    "name": "Short name or label for the rubric.",
    "description": "Full text description of the rubric.",
    "author": "Author name",
    "parent_nodes": {},
    "child_nodes": {},
    "performance_indicators": {}
}

UPDATE_RUBRIC_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_RUBRIC_EXAMPLE
}

FULL_RUBRIC_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_RUBRIC_EXAMPLE, "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

### RUBRIC CRITERION EXAMPLES ###
BASIC_RUBRIC_CRITERION_EXAMPLE = {
    "name": "Short name or label for the rubric criterion.",
    "description": "Full text description of the rubric criterion.",
    "author": "Author name",
    "parent_nodes": {}
}
FULL_RUBRIC_CRITERION_EXAMPLE = {
    "uuid": "as98457a3sdjgkjsdfh",
    **BASIC_RUBRIC_CRITERION_EXAMPLE
}
UPDATE_RUBRIC_CRITERION_EXAMPLE = {
    "uuid": "as98457a3sdjgkjsdfh",
    **BASIC_RUBRIC_CRITERION_EXAMPLE,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

UPLOAD_SUBMITTED_ASSESSMENT_EXAMPLE = {
    "assessment_id": "id_1",
    "learner_id": "learner_1"
}

SUBMITTED_ASSESSMENT_EXAMPLE = {
    "assessment_id": "assessment1",
    "learner_id": "learner1",
    "learner_session_id": "learner_session_id1",
    "attempt_no": 1,
    "submission_gcs_paths": []
}

UPDATE_SUBMITTED_ASSESSMENT_EXAMPLE = {"pass_status": True}

FULL_SUBMITTED_ASSESSMENT_EXAMPLE = {
    "assessment_id": "assessment id",
    "learner_id": "learner who submitted the assessment",
    "assessor_id": "accessor who will access the assessment",
    "type": "type of assessment",
    "plagiarism_score": 0.8,
    "plagiarism_report_path": "gcs path to turnitin report",
    "result": "final result of the assessment",
    "pass_status": True,
    "status": "evaluated",
    "is_flagged": False,
    "timer_start_time": "Time at which the timer was resumed",
    "attempt_no": 3,
    "learner_session_id": "Session id for learnosity",
    "uuid": "firestore id of submitted assessment",
    "created_time": "Time at which the submission was created",
    "last_modified_time": "Time at which the submission was updated"
}

BASIC_LEARNING_OBJECT_EXAMPLE = {
    "name": "Online presentation",
    "display_name": "Online presentation",
    "description": "testing out online ppt",
    "is_optional": False,
    "type": "learning_module",
    "author": "TestUser",
    "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
    },
    "references": {
        "skills": [],
        "competencies": []
    },
    "child_nodes": {
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
    },
    "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
    },
    "metadata": {
        "design_config": {
            "illustration": "",
            "theme": ""
        }
    },
    "achievements": [],
    "completion_criteria": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
    },
    "prerequisites": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
    },
    "is_locked": False,
    "is_hidden": False,
    "duration": 15,
    "equivalent_credits": 0,
    "alias": "module",
    "order": 1
}

#HUMAN GRADED ASSESSMENTS
BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE = {
  "name": "Assessment 1",
  "type": "practice",
  "order": 1,
  "author_id": "author_id",
  "instructor_id": "instructor_id",
  "assessor_id": "assessor_id",
  "assessment_reference": {},
  "max_attempts": 3,
  "pass_threshold": 0.7,
  "achievements": [],
  "alignments": {},
  "references": {},
  "parent_nodes": {"assessments":[]},
  "child_nodes": {
  "rubrics":[
  {"name": "Short name or label for the rubric.",
    "description": "Full text description of the rubric.",
    "author": "Author name",
    "evaluation_criteria":{},
    "parent_nodes": {},
    "child_nodes": {
    "rubric_criteria":[
    {
    "name": "Short name or label for the rubric criterion.",
    "description": "Full text description of the rubric criterion.",
    "author": "Author name",
    "performance_indicators": [],
    "parent_nodes": {"rubrics":[]}}
    ]
    }
    }
    ]
    },
  "prerequisites": {},
  "metadata": {},
  "alias": "assessment",
  "resource_paths": ["resource paths"]
}

UPDATE_HUMAN_GRADED_ASSESSMENT_EXAMPLE = {**BASIC_ASSESSMENT_EXAMPLE}
FULL_HUMAN_GRADED_ASSESSMENT_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_HUMAN_GRADED_ASSESSMENT_EXAMPLE,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

### LEARNER EXAMPLES ###
BASIC_LEARNER_EXAMPLE = {
  "first_name": "Jon",
  "middle_name": "Jon",
  "last_name": "Doe",
  "suffix": "",
  "prefix": "",
  "preferred_name": "",
  "preferred_first_name": "",
  "preferred_middle_name": "",
  "preferred_last_name": "",
  "preferred_name_type": "PreferredName",
  "preferred_pronoun": "",
  "student_identifier": "",
  "student_identification_system": "",
  "personal_information_verification": "",
  "personal_information_type": "",
  "address_type": "",
  "street_number_and_name": "",
  "apartment_room_or_suite_number": "",
  "city": "",
  "state_abbreviation": "",
  "postal_code": "",
  "country_name": "",
  "country_code": "",
  "latitude": "",
  "longitude": "",
  "country_ansi_code": 10000,
  "address_do_not_publish_indicator": "Yes",
  "phone_number": {
    "mobile": {
      "phone_number_type": "Work",
      "primary_phone_number_indicator": "Yes",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
    },
    "telephone": {
      "phone_number_type": "Home",
      "primary_phone_number_indicator": "No",
      "phone_number": "",
      "phone_do_not_publish_indicator": "Yes",
      "phone_number_listed_status": "Listed"
    }
  },
  "email_address_type": "Work",
  "email_address": "jon.doe@gmail.com",
  "email_do_not_publish_indicator": "Yes",
  "backup_email_address": "jon.doe2@gmail.com",
  "birth_date": "",
  "gender": "NotSelected",
  "country_of_birth_code": "",
  "ethnicity": "",
  "employer_id": "test_employer_id",
  "employer": "",
  "employer_email": "testid@employer.com",
  "organisation_email_id": "jon.doe@foobar.com",
  "affiliation": ""
}
POST_LEARNER_PROFILE_EXAMPLE = {
  "learning_goals": ["Develop Communication Skills", "Teamwork"],
  "learning_constraints": {"weekly_study_time": 0},
  "learning_preferences": {},
  "patterns_of_participation": {},
  "employment_status": "Unemployed",
  "potential_career_fields": [],
  "personal_goals": "",
  "employment_history": {},
  "education_history": {},
  "account_settings": {},
  "contact_preferences": {"email": False, "phone": False},
  "attestation_object": {},
  "enrollment_information": {},
  "progress": {
    "curriculum_pathways": {},
    "learning_experiences": {},
    "learning_objects": {},
    "learning_resources": {},
    "assessments": {"wOI51RYsBOcL7x6TUCBr":{"name":"content_upload","num_attempts":4}}
  },
  "achievements": [],
  "tagged_skills": [],
  "tagged_competencies": [],
  "mastered_skills": [],
  "mastered_competencies": []
}

BASIC_LEARNER_PROFILE_EXAMPLE = {
  "learner_id": "Learner ID",
  **POST_LEARNER_PROFILE_EXAMPLE
}

BASIC_SKILL_EXAMPLE = {
  "name":
      "Regression Analysis one",
  "description":
      "Perform regression analysis to address an authentic problem",
  "keywords": ["regression", "analysis"],
  "author":
      "https://credentialengineregistry.org/resources/ce-0f0d84f5-5c32-4526-ad39-1db0adbdbe93",
  "creator":
      "https://credentialengineregistry.org/resources/ce-0f0d84f5-5c32-4526-ad39-1db0adbdbe93",
  "alignments": {
      "standard_alignment": {},
      "credential_alignment": {},
      "skill_alignment": {
          "emsi": {
              "aligned": [
                  {
                      "id": "124hsgxR77QKS8uS7Zgm",
                      "name": "Cyber Security",
                      "score": 1.0
                  }
              ],
              "suggested": []
          }
      },
      "knowledge_alignment": {},
      "role_alignment": {},
      "organizational_alignment": {}
  },
  "organizations": [],
  "certifications": [],
  "occupations": {
      "occupations_major_group": ["15-1212.00"],
      "occupations_minor_group": [],
      "broad_occupation": [],
      "detailed_occupation": []
  },
  "onet_job":
      "",
  "parent_nodes": {
      "competencies": [
          "MAT-243: Applied Statistics for Science, Technology, Engineering, and Mathematics (STEM)"]
  },
  "reference_id":
      "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
  "source_uri":
      "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
  "source_name":
      "Credentialengine"
}
