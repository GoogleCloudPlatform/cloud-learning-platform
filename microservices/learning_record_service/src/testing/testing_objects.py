"""Objects for Unit Testing"""

TEST_LEARNER = {
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
        "telephone_number_type": "Work",
        "primary_telephone_number_indicator": "Yes",
        "telephone_number": "",
        "telephone_do_not_publish_indicator": "Yes",
        "telephone_number_listed_status": "Listed",
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

TEST_USER = {
    "first_name": "steve",
    "last_name": "jobs",
    "email": "steve.jobs@example.com",
    "status": "active",
    "user_type": "learner",
    "user_type_ref": "learner/123",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0
}

TEST_LEARNER_PROFILE = {
    "learner_id": "",
    "learning_goals": [
        "Develop Communication Skills",
        "Teamwork"
    ],
    "learning_constraints": {
        "weekly_study_time": 0
    },
    "learning_preferences": {},
    "patterns_of_participation": {},
    "employment_status": "Unemployed",
    "potential_career_fields": [],
    "personal_goals": "",
    "employment_history": {},
    "education_history": {},
    "account_settings": {},
    "contact_preferences": {
        "email": False,
        "phone": False
    },
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

TEST_AGENT = {
    "object_type": "Agent",
    "name": "example agent",
    "mbox": "mailto:test_agent@example.org",
    "mbox_sha1sum": "SHA-123",
    "open_id": "",
    "account_homepage": "",
    "account_name": "test_account_name",
    "members": [],
    "user_id": "user_id_1234"
}

TEST_VERB = {
    "name": "started",
    "url": "Test Verb URL",
    "canonical_data": {}
}

TEST_EVENT = {
    "object_type": "activities",
    "timestamp": "2022-09-30T10:25:05.864Z",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "actor": {
        "uuid": "e8oKpDUSBSmGb8eqeBIG",
        "object_type": "agent",
        "name": "Learner1",
        "mbox": "mailto:gautam.patidar@quantiphi.com",
        "mbox_sha1sum": "",
        "open_id": "",
        "account_homepage": "",
        "account_name": "",
        "members": [],
        "user_id": "wUoamuf1DAUGRLCcqZwOqVkRT3h1"
    },
    "verb": {
        "uuid": "Cw574DIr4Lh1Sb0EAMJt",
        "name": "started",
        "url": "",
        "canonical_data": {}
    },
    "object": {
        "uuid": "0idJJWYLtKrDVYjHnkBI",
        "name": "Sequencing 1",
        "authority": "Sample Authority",
        "canonical_data": {
            "name": "Sequencing 1",
            "type": "learning_resources",
            "uuid": "0idJJWYLtKrDVYjHnkBI"
        }
    }
}

TEST_CURRICULUM_PATHWAY = {
    "name": "Kubernetes",
    "display_name": "Kubernetes",
    "description": "",
    "author": "TestUser",
    "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
    },
    "child_nodes": {
        "learning_experiences": [],
        "curriculum_pathways": []
    },
    "parent_nodes": {
        "learning_opportunities": [],
        "curriculum_pathways": []
    },
    "metadata": {}
}

TEST_LEARNING_EXPERIENCE = {
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
        "assessment_items": []
    },
    "parent_nodes": {
        "learning_opportunities": [],
        "curriculum_pathways": []
    },
    "metadata": {}
}

TEST_LEARNING_OBJECT = {
    "name": "Online presentation",
    "display_name": "Online presentation",
    "description": "Details on ppt",
    "author": "TestUser",
    "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
    },
    "child_nodes": {
        "learning_objects": [],
        "learning_resources": [],
        "assessment_items": []
    },
    "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
    },
    "metadata": {}
}

TEST_LEARNING_RESOURCE = {
    "uuid": "id",
    "name": "name",
    "display_name": "display_name",
    "description": "description",
    "type": "html",
    "resource_path": "test path",
    "lti_content_item_id": "",
    "course_category": ["Mathematics", "Calculus"],
    "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
    },
    "parent_nodes": {
        "learning_objects": []
    },
    "child_nodes": {
        "concepts": []
    },
    "is_archived": True,
    "is_deleted": False,
    "version": 1,
    "metadata": {}
}

TEST_ASSESSMENT_ITEM = {
    "name":
        "Short name or label for the assessment item.",
    "question":
        "Assessment item question",
    "answer":
        "Answer for the question",
    "context":
        "Context from which the question was created",
    "options": [],
    "question_type":
        "Type of question",
    "activity_type":
        "Type of activity",
    "use_type":
        "Summative",
    "metadata": {},
    "author":
        "A person or organization chiefly responsible for the intellectual "
        "or artistic content of this assessment item",
    "difficulty":
        1,
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
    "assessment_reference": {},
    "achievements": []
}

TEST_SKILL = {
    "uuid": "",
    "name":
        "Operating Systems",
    "description":
        "Explain the purpose of operating systems",
    "keywords": [],
    "author": "",
    "creator": "",
    "alignments": {
        "standard_alignment": "",
        "credential_alignment": "",
        "skill_alignment": {
            "emsi": {
                "aligned": [],
                "suggested": []
            }
        },
        "knowledge_alignment": {},
        "role_alignment": {},
        "organizational_alignment": ""
    },
    "organizations": [],
    "certifications": [],
    "occupations": {
        "occupations_major_group": "",
        "occupations_minor_group": "",
        "broad_occupation": "",
        "detailed_occupation": ""
    },
    "onet_job":
        "",
    "type": {
        "id": "",
        "name": ""
    },
    "parent_nodes": {"competencies": []},
    "reference_id":
        "",
    "source_uri":
        "",
    "source_name":
        "snhu"
}

TEST_ACHIEVEMENT = {
    "type": "course equate",
    "name": "Nursing",
    "description": "",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "associations": {
      "exact_match_of": [],
      "exemplar": [],
      "has_skill_level": [],
      "is_child_of": [],
      "is_parent_of": [],
      "is_part_of": [],
      "is_peer_of": [],
      "is_related_to": [],
      "precedes": [],
      "replaced_by": []
    },
    "credits_available": 0,
    "field_of_study": "",
"metadata": {"design_config" : {
                           "shape" : "",
                           "theme": "",
                           "illustration": ""
}},
    "image": "",
    "result_descriptions": [],
    "tags": [],
    "timestamp": ""
}

