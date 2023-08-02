"""Module containing Testing Objects"""
DEL_KEYS = [
  "is_archived", "is_deleted", "uuid", "created_time",
  "last_modified_time", "created_by", "last_modified_by", "timezone"
]


TEST_USER = {
  "first_name": "steve",
  "last_name": "jobs",
  "email": "steve.jobs@example.com",
  "user_type": "learner",
  "user_groups": ["44qxEpc35pVMb6AkZGbi"],
  "status": "active",
  "is_registered": True,
  "failed_login_attempts_count": 0,
  "access_api_docs": False,
  "gaia_id": "F2GGRg5etyty",
  "photo_url" :"//lh3.googleusercontent.com/a/default-user"
}

TEST_ASSOCIATION_GROUP = {
    "name": "Association Group Name",
    "description": "Description for Association Group"
}

TEST_STAFF = {
  "first_name": "Ted",
  "last_name": "Turner",
  "preferred_name": "staff",
  "bio": "",
  "pronoun": "he/him/his",
  "email": "ted.turner@email.com",
  "phone_number": "0000000000",
  "shared_inboxes": "",
  "timezone": "",
  "office_hours": []
}

TEST_LEARNER = {
        "uuid": "tzlyrXWaSDC4n2XwQabX",
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
        "employer_email": "test@mail.com",
        "organisation_email_id": "jon.doe@foobar.com",
        "affiliation": "",
        "is_archived": False
    }

TEST_DISCIPLINE = {
    "name": "Kubernetes",
    "display_name": "Introduction to Kubernetes",
    "description": "",
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
        "learning_experiences": [],
        "curriculum_pathways": []
    },
    "parent_nodes": {
        "learning_opportunities": [],
        "curriculum_pathways": []
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
    "duration": 0,
    "is_optional": False,
    "equivalent_credits": 0,
    "order": 1,
    "alias": "discipline",
}
