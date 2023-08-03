"""
Sample objects for the schema
"""

### xAPI STATEMENT EXAMPLES ###
AGENT_XAPI_EXAMPLE = {
    "uuid": "2ivy523v5y6ynefn7a",
    "object_type": "agent",
    "name": "Learner1",
    "mbox": "mailto:test_agent@example.org",
    "mbox_sha1sum": "",
    "open_id": "",
    "account_homepage": "",
    "account_name": "",
    "members": [],
    "user_id": "2ivy523v5y6ynefn7a"
}

VERB_XAPI_EXAMPLE = {
    "uuid": "v1bv9an0sf1n2u08na",
    "name": "Random verb name",
    "url": "http://example.com/xapi/verbs#verb1",
    "canonical_data": {}
}

ACTIVITY_XAPI_EXAMPLE = {
    "uuid": "1bcv1629rbcayb8gs",
    "name": "Activity1",
    "authority": "Sample Authority",
    "canonical_data": {
        "name": "Activity1",
        "type": "learning_experiences",
        "uuid": "oTkwe45fsrdfjhin",
        "hierarchy": {}
    }
}

BASIC_EXISTING_LEARNING_EXPERIENCE_EXAMPLE = {
    "uuid": "0Ad4YGZbFOyhTdN6fkis",
    "name": "Kubernetes",
    "description": "",
    "author": "TestUser",
    "alignments": {
        "skill_alignments": [],
        "competency_alignments": []
    },
    "child_nodes": {
        "learning_objects": [],
        "assessments": []
    },
    "parent_nodes": {
        "curriculum_pathways": [],
        "learning_opportunities": []
    },
    "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "0Ad4YGZbFOyhTdN6fkis",
    "is_archived": False,
    "is_deleted": False,
    "metadata": {},
    "created_time": "2022-08-22 12:00:41.206138+00:00",
    "last_modified_time": "2022-08-22 12:00:47.904918+00:00",
    "created_by": "",
    "last_modified_by": ""
}

ACTIVITY_XAPI_RESPONSE_EXAMPLE = {
    "uuid": "1bcv1629rbcayb8gs",
    "name": "Activity1",
    "authority": "Sample Authority",
    "canonical_data": {
        "name": "Activity1",
        "type": "learning_experiences",
        "uuid": "oTkwe45fsrdfjhin",
        "hierarchy": {},
        "existing_document": {
            **BASIC_EXISTING_LEARNING_EXPERIENCE_EXAMPLE
        }
    }
}

BASIC_XAPI_STATEMENT = {
    "actor": {
        **AGENT_XAPI_EXAMPLE
    },
    "verb": {
        **VERB_XAPI_EXAMPLE
    },
    "object": {
        **ACTIVITY_XAPI_EXAMPLE
    },
    "session_id": "yS2BlJTWD9yQYqwVuDpI",
    "object_type": "activities",
    "timestamp": "2022-08-26 12:29:50.1353 UTC",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "result_success": True,
    "result_completion": True,
    "result_score_raw": 80,
    "result_score_min": 0,
    "result_score_max": 100
}

FULL_XAPI_STATEMENT = {
    "uuid": "brv1iob9vsm24s1chn",
    "actor": {
        **AGENT_XAPI_EXAMPLE
    },
    "verb": {
        **VERB_XAPI_EXAMPLE
    },
    "object": {
        **ACTIVITY_XAPI_RESPONSE_EXAMPLE
    },
    "session_id": "yS2BlJTWD9yQYqwVuDpI",
    "object_type": "activities",
    "timestamp": "2022-08-26 12:29:50.1353 UTC",
    "stored": "2022-08-26 12:29:50.1353 UTC",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "result_success": True,
    "result_completion": True,
    "result_score_raw": 80,
    "result_score_min": 0,
    "result_score_max": 100
}

### ACTIVITY EXAMPLES ###
BASIC_ACTIVITY_EXAMPLE = {
    "name": "Activity1",
    "authority": "author 1",
    "canonical_data": {}
}

FULL_ACTIVITY_EXAMPLE = {
    **BASIC_ACTIVITY_EXAMPLE, "uuid": "YHftjfGFGJHKJ45fgdthyj",
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

### ACTIVITY STATE EXAMPLES ###
BASIC_ACTIVITY_STATE_MODEL_EXAMPLE = {
    "agent_id": "e05aa883-acaf-40ad-bf54-02c8ce485fb0",
    "activity_id": "12345678-1234-5678-1234-567812345678",
    "canonical_data": {}
}

FULL_ACTIVITY_STATE_MODEL_EXAMPLE = {
    "uuid": "1Tusjz6W1JI2aFr4SiIw",
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00",
    **BASIC_ACTIVITY_STATE_MODEL_EXAMPLE
}

### AGENT MODEL EXAMPLES ###
BASIC_AGENT_SCHEMA_EXAMPLE = {
    "object_type": "agent",
    "name": "example agent",
    "mbox": "mailto:test_agent@example.org",
    "mbox_sha1sum": "SHA-123",
    "open_id": "opne_id_1234",
    "account_homepage": "homepage",
    "account_name": "test_account_name",
    "members": [],
    "user_id": "user_id_1234"
}

#We can add feilds for archival in the updated schema if necessary
UPDATE_AGENT_SCHEMA_EXAMPLE = {**BASIC_AGENT_SCHEMA_EXAMPLE}

FULL_AGENT_SCHEMA_EXAMPLE = {
    "uuid":
        "abscdedfgi123",
    **BASIC_AGENT_SCHEMA_EXAMPLE, "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}

### VERB EXAMPLES ###
BASIC_VERB_MODEL_EXAMPLE = {
    "name": "Random verb name",
    "url": "Random verb URL",
    "canonical_data": {}
}

FULL_VERB_MODEL_EXAMPLE = {
    "uuid":
        "44qxEpc35pVMb6AkZGbi",
    **BASIC_VERB_MODEL_EXAMPLE, "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}

BASIC_LEARNING_EXPERIENCE_EXAMPLE = {
    "name": "Kubernetes",
    "display_name": "Kubernetes",
    "description": "",
    "author": "TestUser",
    "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
    },
    "child_nodes": {
        "learning_objects": [],
        "assessments": []
    },
    "parent_nodes": {
        "learning_opportunities": [],
        "curriculum_pathways": []
    },
    "metadata": {},
    "assessment_reference": "/learnosity/52f3fc394d81"
}

TEST_USER = {
    "first_name": "steve",
    "last_name": "jobs",
    "email": "steve.jobs@example.com",
    "status": "active",
    "user_type": "learner",
    "user_type_ref": "learner/123",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "user_id": "user_id_1234"
}

BASIC_SESSION_EXAMPLE = {
    "user_id": "User ID",
    "parent_session_id": None,
    "session_data": None
}

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
    "backup_email_address":"jon.doe2@gmail.com",
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

BASIC_LEARNER_PROFILE_EXAMPLE = {
    "learning_goals": ["Develop Communication Skills", "Teamwork"],
    "learning_constraints": {"weekly_study_time": 0},
    "learning_preferences": {},
    "patterns_of_participation": {},
    "employment_status": "Unemployed",
    "potential_career_fields":  [],
    "personal_goals": "",
    "employment_history": {},
    "education_history": {},
    "account_settings": {},
    "contact_preferences": {"email":False, "phone":False},
    "attestation_object": {},
    "enrollment_information": {},
    "progress": {
        "curriculum_pathways": {},
        "learning_experiences": {},
        "learning_objects": {},
        "learning_resources": {},
        "assessment_items": {}
    },
    "achievements": [],
    "tagged_skills": [],
    "tagged_competencies": [],
    "mastered_skills": [],
    "mastered_competencies": []
}
