"""Testing objects file for behave e2e tests"""

E2E_SKILL_INDEX_ID = "1528620229771395072"

INDEX_ENDPOINT_ID = "4437945589052735488"


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
    "metadata": {
        "design_config":{
            "theme": "blue",
            "illustration": "U1C1"
        }
    },
    "order": 1,
    "alias": "unit"
}

TEST_LEARNING_EXPERIENCE = {
    "name": "Kubernetes",
    "display_name": "Kubernetes",
    "description": "",
    "author": "TestUser",
    "resource_path": "",
    "srl_resource_path": "",
    "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
    },
    "child_nodes": {
        "learning_objects": []
    },
    "parent_nodes": {
        "learning_opportunities": [],
        "curriculum_pathways": []
    },
    "metadata": {
        "design_config":{
            "theme": "blue",
            "illustration": "U1C1"
        }
    },
    "alias": "learning_experience",
    "order": 1
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
        "assessments": []
    },
    "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
    },
    "metadata": {
        "design_config":{
            "theme": "blue",
            "illustration": "U1C1"
        }
    },
    "order": 1,
    "type": "learning_module",
    "alias": "module",
}

TEST_UNIT_OVERVIEW_OBJECT = {
    "name": "Unit Overview",
    "display_name": "Unit Overview",
    "description": "Introduction",
    "author": "TestUser",
    "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
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
    "alias": "module",
    "order": 2,
    "type": "unit_overview",
    "metadata": {
        "design_config":{
            "theme": "blue",
            "illustration": "U1C1"
        }
    }
}

DOMAIN_OBJ_TEMPLATE = {
    "name": "Test domain",
    "description": "Test domain",
    "keywords": [],
    "child_nodes": {
        "sub_domains": []
    },
    "reference_id": "gstyr263s",
    "source_uri": "https://credentialengineregistry.org/resources/gstyr263s",
    "source_name": "Credentialengine"
}

SUB_DOMAIN_OBJ_TEMPLATE = {
    "name": "Test sub domain",
    "description": "Test sub domain",
    "keywords": [],
    "parent_nodes": {
        "domains": []
    },
    "child_nodes": {
        "categories": [],
        "competencies": []
    },
    "reference_id": "rteyfga67",
    "source_uri": "https://credentialengineregistry.org/resources/rteyfga67",
    "source_name": "Credentialengine"
}

CATEGORY_OBJ_TEMPLATE = {
    "name": "Test category",
    "description": "Test category",
    "keywords": [],
    "parent_nodes": {
        "sub_domains": []
    },
    "child_nodes": {
        "competencies": []
    },
    "reference_id": "feuhqooijcbv",
    "source_uri": "https://credentialengineregistry.org/resources/feuhqooijcbv",
    "source_name": "Credentialengine"
}

COMPETENCY_OBJ_TEMPLATE = {
    "name": "Test competency",
    "description": "Test competency",
    "keywords": [],
    "level": "2",
    "subject_code": "MAT",
    "course_code": "MAT-240",
    "course_title": "Applied Statistics",
    "alignments": {
        "standard_alignment": {},
        "credential_alignment": {},
        "skill_alignment": {
            "aligned": "Cyber Security"
        },
        "organizational_alignment": {},
        "competency_alignment": {},
        "o_net_alignment": {}
    },
    "occupations": {
        "occupations_major_group": ["15-1212.00"],
        "occupations_minor_group": [],
        "broad_occupation": [],
        "detailed_occupation": []
    },
    "parent_nodes": {
        "categories": [],
        "sub_domains": []
    },
    "child_nodes": {
        "skills": []
    },
    "reference_id": "f35gkqfwdft",
    "source_uri": "https://credentialengineregistry.org/resources/f35gkqfwdft",
    "source_name": "Credentialengine"
}

CONCEPT_OBJ_TEMPLATE = {
    "uuid": "id",
    "title": "title",
    "description": "description",
    "label": "Test label",
    "type": "concept",
    "is_valid": True,
    "parent_nodes": {
        "learning_resource": []
    },
    "child_nodes": {
        "sub_concepts": []
    },
    "child_type": "subconcepts",
    "alignments": {
        "organizational_alignment": ""
    },
    "is_archived": False,
    "is_deleted": False
}

SUBCONCEPT_OBJ_TEMPLATE = {
    "uuid": "id",
    "title": "title",
    "description": "description",
    "all_learning_resource": "",
    "label": "Test label",
    "type": "subconcept",
    "is_valid": True,
    "parent_nodes": {
        "concepts": []
    },
    "child_nodes": {
        "learning_objectives": []
    },
    "alignments": {
        "organizational_alignment": ""
    },
    "is_archived": False,
    "is_deleted": False
}

LEARNING_OBJECTIVE_OBJ_TEMPLATE = {
    "uuid": "id",
    "title": "title",
    "description": "description",
    "all_learning_resource": "",
    "label": "Test label",
    "type": "learning_objective",
    "is_valid": True,
    "parent_nodes": {
        "sub_concepts": []
    },
    "child_nodes": {
        "learning_units": []
    },
    "alignments": {
        "organizational_alignment": ""
    },
    "is_archived": False,
    "is_deleted": False
}

LEARNING_UNIT_OBJ_TEMPLATE = {
    "uuid": "id",
    "title": "title",
    "description": "description",
    "text": "",
    "label": "Test label",
    "type": "learning_resource",
    "is_valid": True,
    "parent_nodes": {
        "learning_objectives": []
    },
    "child_nodes": {},
    "alignments": {
        "organizational_alignment": ""
    },
    "is_archived": False,
    "is_deleted": False
}

LEARNING_CONTENT_OBJ_TEMPLATE = {
    "uuid": "id",
    "title": "title",
    "description": "description",
    "document_type": "",
    "label": "Test label",
    "type": "learning_resource",
    "child_nodes": {
        "concepts": []
    },
    "is_valid": True,
    "alignments": {
        "organizational_alignment": ""
    },
    "is_archived": False,
    "is_deleted": False
}

LEARNING_RESOURCE_OBJ_TEMPLATE = {
    "uuid": "id",
    "title": "title",
    "description": "description",
    "type": "html",
    "resource_path": "test_file.html",
    "lti_content_item_id": "",
    "course_category": ["Mathematics", "Calculus"],
    "alignments": {},
    "parent_nodes": {},
    "child_nodes": {},
    "is_achieved": True,
    "version": 1,
    "alias": "",
    "order": 1,
    "metadata": {
        "design_config":{
            "theme": "blue",
            "illustration": "U1C1"
        }
    }
}

SKILL_OBJ_TEMPLATE = {
    "name": "name",
    "description": "description",
    "keywords": [],
    "author": "test",
    "creator": "test",
    "alignments": {
        "standard_alignment": {},
        "credential_alignment": {},
        "skill_alignment": {},
        "knowledge_alignment": {},
        "role_alignment": {},
        "organizational_alignment": {}
    },
    "organizations": [],
    "certifications": [],
    "occupations": {
        "occupations_major_group": [],
        "occupations_minor_group": [],
        "broad_occupation": [],
        "detailed_occupation": []
    },
    "onet_job": "",
    "type": {
        "id": "",
        "name": ""
    },
    "parent_nodes": {
        "competencies": []
    },
    "reference_id": "12345",
    "source_uri": "https://emsi/resources/12345",
    "source_name": "e2e_wgu"
}

TEST_CONCEPT = {
    "title":
        "Idealism",
    "description":
        "The belief that a perfect life, situation, etc. can be achieved, even when this is not very likely",
    "label":
        "",
    "is_valid":
        True,
    "type":
        "concept",
    "parent_nodes": {
        "learning_resource": []
    },
    "child_nodes": {
        "sub_concepts": []
    },
    "alignments": {
        "skill_alignment": {
            "emsi": {
                "aligned": [{
                    "id": "124hsgxR77QKS8uS7Zgm",
                    "name": "Cyber Security",
                    "score": 1.0
                }],
                "suggested": []
            },
            "snhu": {
                "aligned": [],
                "suggested": []
            }
        },
        "role_alignment": {
            "onet": {
                "aligned": [],
                "suggested": []
            }
        },
        "organizational_alignment": "",
        "is_archived": False,
        "is_deleted": False
    }
}

TEST_SUBCONCEPT = {
    "title":
        "Essentialism",
    "description":
        "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods",
    "all_learning_resource":
        "",
    "parent_nodes": {
        "concepts": []
    },
    "child_nodes": {
        "learning_objectives": []
    },
    "label":
        "",
    "total_lus":
        0,
    "is_valid":
        True,
    "type":
        "subconcept",
    "alignments": {
        "skill_alignment": {
            "emsi": {
                "aligned": [{
                    "id": "124hsgxR77QKS8uS7Zgm",
                    "name": "Cyber Security",
                    "score": 1.0
                }],
                "suggested": []
            },
            "snhu": {
                "aligned": [],
                "suggested": []
            }
        },
        "role_alignment": {
            "onet": {
                "aligned": [],
                "suggested": []
            }
        },
        "organizational_alignment": "",
        "is_archived": False,
        "is_deleted": False
    }
}

TEST_LEARNING_OBJECTIVE = {
    "title": "State theorems",
    "description": "A description for State theorems",
    "parent_nodes": {
        "sub_concepts": []
    },
    "child_nodes": {
        "learning_units": []
    },
    "is_valid": True,
    "type": "learning_objective",
    "alignments": {
        "skill_alignment": {
            "emsi": {
                "aligned": [{
                    "id": "124hsgxR77QKS8uS7Zgm",
                    "name": "Cyber Security",
                    "score": 1.0
                }],
                "suggested": []
            },
            "snhu": {
                "aligned": [],
                "suggested": []
            }
        },
        "role_alignment": {
            "onet": {
                "aligned": [],
                "suggested": []
            }
        },
        "organizational_alignment": ""
    },
    "text": "",
    "is_archived": False,
    "is_deleted": False
}

TEST_LEARNING_UNIT = {
    "title":
        "Elementary Data Types",
    "text":
        "A data type is a class of data objects with a set of operations for creating and manipulating them.",
    "pdf_title":
        "",
    "parent_nodes": {
        "learning_objectives": []
    },
    "child_nodes": {},
    "topics":
        "",
    "is_valid":
        True,
    "type":
        "learning_unit",
    "alignments": {
        "skill_alignment": {
            "emsi": {
                "aligned": [{
                    "id": "124hsgxR77QKS8uS7Zgm",
                    "name": "Cyber Security",
                    "score": 1.0
                }],
                "suggested": []
            },
            "snhu": {
                "aligned": [],
                "suggested": []
            }
        },
        "role_alignment": {
            "onet": {
                "aligned": [],
                "suggested": []
            }
        },
        "organizational_alignment": ""
    },
    "coref_text":
        "",
    "is_archived":
        False,
    "is_deleted":
        False
}

TEST_KG_LEARNING_CONTENT = {
    "uuid": "1234",
    "description": "sample_description",
    "document_type": "pdf",
    "resource_path": "path/to/gcs",
    "title": "sample_title",
    "child_nodes": {
        "concepts": []
    },
    "type": "learning_resource"
}

TEST_KG_CONCEPT = {
    "uuid": "12345",
    "description": "A concept in book on OS",
    "label": "A concept in book on OS",
    "title": "A concept in book on OS",
    "type": "concept",
    "parent_nodes": {
        "learning_resource": []
    },
    "child_nodes": {
        "sub_concepts": []
    },
    "is_valid": True
}

TEST_KG_SUBCONCEPT = {
    "uuid": "1234",
    "title": "A sub-competency in book on OS",
    "description": "A sub-competency in book on OS",
    "label": "A sub-competency in book on OS",
    "total_lus": 1,
    "is_valid": True,
    "parent_nodes": {
        "concepts": []
    },
    "child_nodes": {
        "learning_objectives": []
    },
    "all_learning_resource": "the full content of the learning resource"
}

TEST_KG_LEARNING_OBJECTIVE = {
    "uuid":
        "1234",
    "description":
        "A learning objective in book on OS",
    "title":
        "A learning objective in book on OS",
    "type":
        "learning_objective",
    "is_valid":
        True,
    "parent_nodes": {
        "sub_concepts": []
    },
    "child_nodes": {
        "learning_units": []
    },
    "text":
        "An operating system is the most important software that runs on a computer. It manages the computer's memory and processes, as well as all of its software and hardware. It also allows you to communicate with the computer without knowing how to speak the computer's language. Without an operating system, a computer is useless. Your computer's operating system (OS) manages all of the software and hardware on the computer. Most of the time, there are several different computer programs running at the same time, and they all need to access your computer's central processing unit (CPU), memory, and storage. The operating system coordinates all of this to make sure each program gets what it needs."
}

TEST_KG_LEARNING_UNIT = {
    "uuid":
        "1234",
    "title":
        "A learning unit in book on OS",
    "type":
        "learning_unit",
    "pdf_title":
        "test pdf title",
    "topics":
        "test topics",
    "is_valid":
        True,
    "parent_nodes": {
        "learning_objectives": []
    },
    "child_nodes": {},
    "text":
        "An operating system is the most important software that runs on a computer. It manages the computer's memory and processes, as well as all of its software and hardware. It also allows you to communicate with the computer without knowing how to speak the computer's language. Without an operating system, a computer is useless. Your computer's operating system (OS) manages all of the software and hardware on the computer. Most of the time, there are several different computer programs running at the same time, and they all need to access your computer's central processing unit (CPU), memory, and storage. The operating system coordinates all of this to make sure each program gets what it needs."
}

TEST_DOMAIN = {
    "name":
        "Regression Analysis",
    "description":
        "Perform regression analysis to address an authentic problem",
    "keywords": ["tbn"],
    "child_nodes": {
        "sub_domains": []
    },
    "reference_id":
        "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_uri":
        "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_name":
        "Credentialengine"
}

TEST_SUB_DOMAIN = {
    "name":
        "Regression Analysis",
    "description":
        "Perform regression analysis to address an authentic problem",
    "keywords": ["tbn"],
    "parent_nodes": {
        "domains": []
    },
    "child_nodes": {
        "categories": [],
        "competencies": []
    },
    "reference_id":
        "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_uri":
        "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_name":
        "Credentialengine"
}

TEST_CATEGORY = {
    "name":
        "Regression Analysis",
    "description":
        "Perform regression analysis to address an authentic problem",
    "keywords": ["tbn"],
    "parent_nodes": {
        "sub_domains": []
    },
    "child_nodes": {
        "competencies": []
    },
    "reference_id":
        "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_uri":
        "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_name":
        "Credentialengine"
}

TEST_COMPETENCY = {
    "name":
        "Regression Analysis",
    "description":
        "Perform regression analysis to address an authentic problem",
    "keywords": ["tbn"],
    "level":
        "2",
    "subject_code":
        "MAT",
    "course_code":
        "MAT-240",
    "course_title":
        "Applied Statistics",
    "alignments": {
        "standard_alignment": {},
        "credential_alignment": {},
        "skill_alignment": {
            "aligned": "Cyber Security"
        },
        "organizational_alignment": {},
        "competency_alignment": {},
        "o_net_alignment": {}
    },
    "occupations": {
        "occupations_major_group": ["15-1212.00"],
        "occupations_minor_group": [],
        "broad_occupation": [],
        "detailed_occupation": []
    },
    "parent_nodes": {
        "sub_domains": [],
        "categories": []
    },
    "child_nodes": {
        "skills": []
    },
    "reference_id":
        "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_uri":
        "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_name":
        "Credentialengine"
}

TEST_SKILL = {
    "name":
        "Regression Analysis",
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
                "aligned": [{
                    "id": "124hsgxR77QKS8uS7Zgm",
                    "name": "Cyber Security",
                    "score": 1.0
                }],
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
    "type": {
        "id": "",
        "name": ""
    },
    "parent_nodes": {
        "competencies": []
    },
    "reference_id":
        "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_uri":
        "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_name":
        "Credentialengine"
}

TEST_V3_LEARNING_CONTENT = {
    "title": "title",
    "description": "description",
    "document_type": "",
    "concept_ids": [],
    "label": "Test label",
    "type": "learning_resource",
    "is_valid": True,
    "alignments": {
        "organizational_alignment": ""
    },
    "is_archived": False,
    "is_deleted": False
}

TEST_LEARNING_RESOURCE = {
    "uuid": "id",
    "name": "name",
    "display_name": "display_name",
    "description": "description",
    "type": "pdf",
    "resource_path": "",
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
    "metadata": {
        "design_config":{
            "theme": "blue",
            "illustration": "U1C1"
        }
    },
    "alias": "lesson",
    "order": 1,
    "duration": 15,
    "prerequisites":{"learning_resources":[],"assessments":[]}
}

LEARNER_OBJECT_TEMPLATE = {
    "uuid": "uuid",
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

GOAL_OBJECT_TEMPLATE = {
    "name": "Intellectual Skills",
    "description": "",
    "type": "Long-term",
    "aligned_skills": [],
    "aligned_workforces": [],
    "aligned_credentials": [],
    "aligned_learning_experiences": [],
    "is_archived": False
}

ACHIEVEMENT_OBJECT_TEMPLATE = {
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
    "timestamp": "",
    "is_archived": False
}

LEARNER_PROFILE_TEMPLATE = {
    "learning_goals": ["Develop Communication Skills", "Teamwork"],
    "learning_constraints": {"weekly_study_time" : 10 },
    "learning_preferences": {},
    "patterns_of_participation": {},
    "employment_status": "Unemployed",
    "potential_career_fields":  [],
    "personal_goals": "",
    "employment_history": {},
    "education_history": {},
    "account_settings": {},
    "contact_preferences": {"email":False, "phone":False},
    "enrollment_information": {},
    "attestation_object": {},
    "progress": {
      "curriculum_pathways": {},
      "learning_experiences": {},
      "learning_objects": {},
      "learning_resources": {},
      "assessments": {}
    },
    "achievements": [],
    "tagged_skills": [],
    "tagged_competencies": [],
    "mastered_skills": [],
    "mastered_competencies": [],
    "is_archived": False
}

BATCH_JOB_OBJ_TEMPLATE = {
    "name":
        "job_name",
    "type":
        "e2e_test",
    "status":
        "pending",
    "input_data":
        '{"skill_ids": ["pzAvrAzdT9JAW4pG742D", "15aor2vzGW9aVOvM2opG"]}'
}

DUMMY_BATCH_JOB_NAMES = [
    "55a1d64e-cf85-11ec-9d64-0242ac120002",
    "5b5c8d86-cf85-11ec-9d64-0242ac120002"
]

ROLE_OBJ_TEMPLATE = {
    "uuid": "12345",
    "code": "15-83-8166",
    "title": "test_title",
    "also_called": ["test_title1"],
    "description": "test_description",
    "task": ["task1", "task2", "task3"],
    "source_uri": "https://e2e/12345",
    "type": "test",
    "source_name": "e2e",
    "alignments": {}
}

TEST_ACTIVITY = {
    "name": "activity test",
    "canonical_data": {
        "name": "activity test",
        "type": "learning_experiences",
        "uuid": "oTkwe45fsrdfjhin",
        "hierarchy": {}
    },
    "authority": "authority test"
}

TEST_ACTIVITY_STATE = {
    "agent_id": "agent_id_1",
    "activity_id": "activity_id_1",
    "canonical_data": {}
}

TEST_AGENT = {
    "object_type": "agent",
    "name": "example agent",
    "mbox": "mailto:test_agent@example.org",
    "mbox_sha1sum": "SHA-123",
    "open_id": "open_id",
    "account_homepage": "homepage",
    "account_name": "test_account_name",
    "members": [],
    "user_id": "user_id_1234"
}
TEST_VERB = {
    "name": "Test Verb name",
    "url": "Test Verb URL",
    "canonical_data": {}
}

TEST_COMPLETED_VERB = {
    "name": "completed",
    "url": "Test Verb URL",
    "canonical_data": {}
}

TEST_XAPI_STATEMENT_1 = {
    "actor": {
        "uuid": "2ivy523v5y6ynefn7a",
        **TEST_AGENT
    },
    "verb": {
        "uuid": "v1bv9an0sf1n2u08na",
        **TEST_VERB
    },
    "object": {
        "uuid": "1bcv1629rbcayb8gs",
        **TEST_ACTIVITY
    },
    "object_type": "activities",
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

TEST_XAPI_STATEMENT_2 = {
    "actor": {
        "uuid": "243mhfhcayfc37rhgc",
        **TEST_AGENT
    },
    "verb": {
        "uuid": "g87to8fr2ggi7fi782",
        **TEST_VERB
    },
    "object": {
        "uuid": "4hbyjhhcv798vgufv",
        **TEST_ACTIVITY
    },
    "object_type": "activities",
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

TEST_LRS_COMPLETED_EVENT = {
    "object_type": "activities",
    "timestamp": "2022-09-30T10:25:05.864Z",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "actor": {
        "uuid": "hEGK4HYp0AAcBSAEniux",
        "object_type": "agent",
        "name": "agent Dhruv",
        "mbox": "mailto:dhruv.sharma@quantiphi.com",
        "mbox_sha1sum": "",
        "open_id": "",
        "account_homepage": "",
        "account_name": "",
        "members": [],
        "user_id": "pP4QSRThDYYSJWjUlx7RyQUsgiJ2"
    },
    "verb": {
        "uuid": "0y3v7l18KrjWclpUoZcT",
        "name": "completed",
        "url": "http://example.com/xapi/verbs#completed",
        "canonical_data": {}
    },
    "object": {
        "uuid": "i3sPymY3EdoEiVHJEklC",
        "name": "Sequencing 1",
        "authority": "Sample Authority",
        "canonical_data": {
            "name": "Sequencing 1",
            "type": "learning_resources",
            "uuid": "i3sPymY3EdoEiVHJEklC"
        }
    },
    "session_id": "ttrtyr56ggfdtyfghg"
}

TEST_USER = {
    "first_name": "steve",
    "last_name": "jobs",
    "email": "steve.jobs@example.com",
    "status": "active",
    "user_type": "learner",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "gaia_id": "F2GGRg5etyty",
    "photo_url":"//lh3.googleusercontent.com/a/default-user"
}

TEST_PLA_RECORD = {
    "title": "PLA Title",
    "user_id": "user_1234",
    "type": "catalog",
    "requested_by": "Request_user",
    "description": "",
    "status": "in progress",
    "prior_experiences": ["abscde"],
    "approved_experiences": ["mnbmnbm"],
    "is_archived": False
}
TEST_PRIOR_EXPERIENCE = {
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
                      "phone_call": "121-453-9010"},
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
        "Field to distinguish the type of assessment profile (Formative/Summative)",
    "metadata": {},
    "author":
        "A person or organization chiefly responsible for the intellectual or artistic content of this assessment item",
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

TEST_PRETEST_ASSESSMENT = {
    "name": "Pretest Assessment",
    "display_name": "Pretest Assessment",
    "type": "pretest",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {},
    "max_attempts": 1,
    "pass_threshold": 0.7,
    "achievements": [],
    "alignments": {},
    "references": {},
    "parent_nodes": {"learning_objects": [], "learning_experiences": []},
    "child_nodes": {"assessment_items": []},
    "prerequisites": {},
    "metadata": {}
}

TEST_PRACTICE_ASSESSMENT = {
    "name": "Assessment 1",
    "display_name": "Assessment 1",
    "type": "practice",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {},
    "max_attempts": 3,
    "pass_threshold": 0.7,
    "achievements": [],
    "alignments": {},
    "references": {},
    "parent_nodes": {"learning_objects": [], "learning_experiences": []},
    "child_nodes": {"rubrics": []},
    "prerequisites": {"learning_resources":[],"assessments":[]},
    "metadata": {},
    "order": 1
}

TEST_FINAL_ASSESSMENT = {
    "name": "Assessment 2",
    "display_name": "Assessment 2",
    "type": "project",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {},
    "max_attempts": 3,
    "pass_threshold": 0.7,
    "achievements": [],
    "alignments": {},
    "references": {},
    "parent_nodes": {"learning_objects": [], "learning_experiences": []},
    "child_nodes": {"assessment_items": []},
    "prerequisites": {},
    "metadata": {},
    "order": 1
}


TEST_SUBMITTED_ASSESSMENT_INPUT = {
  "assessment_id": "assessment1",
  "learner_id": "learner1",
  "learner_session_id": "learner_session_id1",
  "attempt_no": 1,
  "type": "practice",
  "is_autogradable": False
}

TEST_UPDATE_SUBMITTED_ASSESSMENT = {
    "pass_status": False
}

TEST_SESSION_DATA = {    
    "node_id": None,
    "node_type": "assessment_items",
    "learnosity_session_id": None    
}

BASIC_SESSION_DATA = {
    "user_id": "User ID",
    "parent_session_id": None,
    "session_data": { **TEST_SESSION_DATA },
    "is_expired": False
}

FULL_SESSION_DATA = {
    "session_id": "U2DDBkl3Ayg0PWudzhI",
    **BASIC_SESSION_DATA,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

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

TEST_ASSESSOR = {
    "first_name": "Random",
    "last_name": "Assessor",
    "email": "random.assessor@example.com",
    "status": "active",
    "user_type": "assessor",
    "user_type_ref": "",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "gaia_id": "F2GGRg5etyty"
}

TEST_INSTRUCTOR = {
    "first_name": "Random",
    "last_name": "Instructor",
    "email": "random.instructor@example.com",
    "status": "active",
    "user_type": "instructor",
    "user_type_ref": "",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "gaia_id": "F2GGRg5etyty"
}

TEST_COACH = {
    "first_name": "Random",
    "last_name": "Coach",
    "email": "random.coach@example.com",
    "status": "active",
    "user_type": "coach",
    "user_type_ref": "",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "gaia_id": "F2GGRg5etyty"
}

TEST_LEARNER_PROFILE={
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
        "assessments": {}
    },
    "achievements": [],
    "tagged_skills": [],
    "tagged_competencies": [],
    "mastered_skills": [],
    "mastered_competencies": []
}

TEST_CURRICULUM_PATHWAY_2 = {
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
        "design_config":{
            "theme": "blue",
            "illustration": "U1C1"
        }
    },
  "achievements": [],
  "completion_criteria": {
    "curriculum_pathways": [],
    "learning_experiences": [],
    "learning_objects": [],
    "learning_resources": [],
    "assessment_items": []
  },
  "prerequisites": {
    "curriculum_pathways": [],
    "learning_experiences": [],
    "learning_objects": [],
    "learning_resources": [],
    "assessment_items": []
  },
  "is_locked": False,
  "order": 1,
  "alias": "unit"

}

TEST_LEARNER_PROFILE_PROGRESS_UPDATE={
    "progress":{
            "curriculum_pathways":{},
            "learning_objects":{},
            "learning_resources":{},
            "learning_experiences": {},
            "assessments": {}
        }
}

TEST_PROGRESS = {
    "name": "random_name",
    "status": "completed",
    "is_locked": False,
    "progress": 100
}

TEST_SESSION = {
    "user_id": "User ID",
    "parent_session_id": None,
    "session_data": None
}

TEST_SIGN_UP ={
    "email": "e2e_testing@e2e.com",
    "password": "e2eTesting@000"
}
TEST_STARTED_VERB = {
    "name": "started",
    "url": "Test Verb URL",
    "canonical_data": {}
}

TEST_LRS_STARTED_EVENT = {
    "object_type": "activities",
    "timestamp": "2022-09-30T10:25:05.864Z",
    "result": {},
    "context": {},
    "authority": {},
    "attachments": [],
    "actor": {
        "uuid": "hEGK4HYp0AAcBSAEniux",
        "object_type": "agent",
        "name": "agent Dhruv",
        "mbox": "mailto:dhruv.sharma@quantiphi.com",
        "mbox_sha1sum": "",
        "open_id": "",
        "account_homepage": "",
        "account_name": "",
        "members": [],
        "user_id": "pP4QSRThDYYSJWjUlx7RyQUsgiJ2"
    },
    "verb": {
        "uuid": "0y3v7l18KrjWclpUoZcT",
        "name": "started",
        "url": "http://example.com/xapi/verbs#started",
        "canonical_data": {}
    },
    "object": {
        "uuid": "i3sPymY3EdoEiVHJEklC",
        "name": "Sequencing 1",
        "authority": "Sample Authority",
        "canonical_data": {
            "name": "Sequencing 1",
            "type": "learning_resources",
            "uuid": "i3sPymY3EdoEiVHJEklC"
        }
    }
}


TEST_USER_GROUP = {
    "name": "Assessor",
    "description": "Description for Assessor group",
}

TEST_ASSOCIATION_GROUP = {
    "name": "Test Association Group",
    "description": "Test Association Group Description"
}

TEST_LEARNER_ASSOCIATION_GROUP = {
  "uuid": "124hsgxR77QKS8uS7Zgm",
  "association_type": "learner",
  "users": [],
  "associations": {
    "coaches": [],
    "instructors": [],
    "curriculum_pathway_id": ""
  },
  **TEST_ASSOCIATION_GROUP,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

TEST_APPLICATION = {
    "name": "ContentManagement",
    "description": "Description for application",
    "modules": []
}

TEST_PERMISSION = {
  "name": "admin",
  "description": "Description for permission",
  "application_id": "1212122ed3d33d",
  "module_id": "wewewewedn3211",
  "action_id": "s2wss2qaqsqs",
  "user_groups": []
}

TEST_ACTION = {
  "name": "create",
  "description": "Description for action",
  "action_type": "other"
}

TEST_MODULE = {
  "name": "Assessment",
  "description": "Description for module",
  "actions": []
}

TEST_BASIC_FAQ = {
    "name": "Sample FAQ",
    "resource_path": None,
    "curriculum_pathway_id": "sample_pathway_id"
}

TEST_APPROVED_EXPERIENCE = {
  "title": "Fundamentals of Accounting",
  "description": "",
  "organization": "TPSI",
  "type": "Certificate",
  "student_type": "Graduate",
  "class_level": "Mid level",
  "credits_range": {
    "upper_limit": 20,
    "lower_limit": 5},
  "status": "Active",
  "metadata": {}
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
    "timezone": "Central (CT) - Chicago",
    "office_hours": [],
    "photo_url": "//lh3.googleusercontent.com/a/default-user",
    "calendly_url": " calendly.com/sample-url"
}

TEST_REMOVE_INSTRUCTOR = {
    "instructor": "12sdfhbejv2323231212",
    "curriculum_pathway_id": "1212erui34ut3rthvschkdsvv",
}

TEST_ADD_USERS_ASSOCIATION_GROUP = {
    "users": [],
    "status": "active"
}

TEST_ADD_INSTRUCTOR = {
    "instructors": ["12sdfhbejv2323231212"],
    "curriculum_pathway_id": "1212erui34ut3rthvschkdsvv",
    "status": "active"
}

COMPLETED_RULE_VERBS = ["completed"]

SUBMITTED_RULE_VERBS = ["submitted"]

EVALUATED_RULE_VERBS = ["evaluated"]

NON_EVALUATED_RULE_VERBS = ["non_evaluated"]

STARTED_RULE_VERBS = ["started"]

RESUMED_RULE_VERBS = ["resumed"]

EVALUATION_STARTED_RULE_VERBS = ["evaluation_started"]

SKIP_PRETEST_RULE = ["skipped"]

VALID_VERBS = STARTED_RULE_VERBS + COMPLETED_RULE_VERBS\
    + RESUMED_RULE_VERBS + SUBMITTED_RULE_VERBS + NON_EVALUATED_RULE_VERBS\
    + EVALUATION_STARTED_RULE_VERBS + SKIP_PRETEST_RULE + EVALUATED_RULE_VERBS


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
    "parent_nodes": {},
    "evaluation_criteria": {},
    "child_nodes": {
    "rubric_criteria":[
        {
        "name": "Short name or label for the rubric criterion.",
        "description": "Full text description of the rubric criterion.",
        "author": "Author name",
        "performance_indicators": [],
        "parent_nodes": {"rubrics":[]}
        }]}}],
    },
  "prerequisites": {},
  "metadata": {},
  "alias": "assessment"
}

UPDATE_HUMAN_GRADED_ASSESSMENT_EXAMPLE = {
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
  {
    "name": "New name for rubric.",
    "description": "Full text description of the rubric.",
    "author": "Author name",
    "evaluation_criteria":{},
    "parent_nodes": {},
    "child_nodes": {
    "rubric_criteria":[
    {
    "name": "New name for rubric for the rubric criterion.",
    "description": "Full text description of the rubric criterion.",
    "author": "Author name",
    "performance_indicators": [],
    "parent_nodes": {"rubrics":[]}}
    ]
    }
    },

    {
    "name": "New created rubric.",
    "description": "Full text description of the rubric.",
    "author": "Author name",
    "evaluation_criteria":{},
    "parent_nodes": {},
    "child_nodes": {
    "rubric_criteria":[
    {
    "name": "New created rubric criterion.",
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

TEST_RUBRIC = {
    "name": "Test Rubric",
    "description": "Test Rubric Description",
    "author": "",
    "evaluation_criteria": {
        "0": "Exemplary",
        "1": "Proficient",
        "2": "Needs Improvement",
        "3": "Not Evident"
    },
    "parent_nodes": {},
    "child_nodes": {}
}

TEST_RUBRIC_CRITERION = {
    "name": "Test Rubric Criterion",
    "description": "Test Rubric Criterion Description",
    "author": "Author name",
    "parent_nodes": {}
}

TEST_INAPP_NOTIFICATION = {
  "header": "simple notification",
  "content": "notification description",
  "notification_type": "nudge",
  "action_fields": None,
  "recipient_id": "44qxEpc35pVMb6AkGfd"
}

BASIC_NOTIFICATION_RULES_MODEL_EXAMPLE = {
    "name": "notification rule",
    "description": "notification rule description",
    "rule_status": "active",
    "communication_type": ["inapp-notification", "email"],
    "recipients": ["user1"],
    "allow_is_read": True,
    "trigger": [],
    "notification_settings": {},
    "email_settings": {},
    "frequency": None,
    "settings_id": None,
    "start_delivery_time": None,
    "end_delivery_time": None
}
