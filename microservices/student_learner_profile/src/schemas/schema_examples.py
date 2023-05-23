"""
Schema examples and test objects for unit test
"""
### ACHIEVEMENT EXAMPLES ###
POST_ACHIEVEMENT_EXAMPLE = {
  "type": "course equate",
  "name": "ML Professional",
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
  "tags": ["ML"],
  "credits_available": 0,
  "field_of_study": "",
  "metadata": {
    "design_config" : {
      "shape" : "",
      "theme": "",
      "illustration": ""
    }
  },
  "image": "",
  "result_descriptions": [],
  "timestamp": ""
}

BASIC_ACHIEVEMENT_EXAMPLE = {**POST_ACHIEVEMENT_EXAMPLE}

UPDATE_ACHIEVEMENT_EXAMPLE = {
  **POST_ACHIEVEMENT_EXAMPLE,
  "is_archived": False
}

FULL_ACHIEVEMENT_EXAMPLE = {
  "uuid": "U2DDBkl3Ayg0PWudzhI",
  **BASIC_ACHIEVEMENT_EXAMPLE,
  "is_archived": False,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

### GOAL EXAMPLES ###
BASIC_GOAL_EXAMPLE = {
  "name": "Intellectual Skills",
  "description": "",
  "type": "Long-term",
  "aligned_skills": [],
  "aligned_workforces": [],
  "aligned_credentials": [],
  "aligned_learning_experiences": [],
}

UPDATE_GOAL_EXAMPLE = {
  **BASIC_GOAL_EXAMPLE,
  "is_archived": False
}

FULL_GOAL_EXAMPLE = {
  "uuid": "44qxEpc35pVMb6AkZGbi",
  **BASIC_GOAL_EXAMPLE,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

### LEARNER PROFILE EXAMPLES ###
UPDATE_LEARNER_PROFILE_EXAMPLE = {
  "learning_goals": ["Develop Communication Skills", "Teamwork"],
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
  "is_archived": False,
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

POST_LEARNER_PROFILE_EXAMPLE = {
  "learning_goals": ["Develop Communication Skills", "Teamwork"],
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

BASIC_LEARNER_PROFILE_EXAMPLE = {
  "learner_id": "Learner ID",
  **POST_LEARNER_PROFILE_EXAMPLE
}

FULL_LEARNER_PROFILE_EXAMPLE = {
  "uuid": "44qxEpc35pVMb6AkZGbi",
  "is_archived": False,
  **BASIC_LEARNER_PROFILE_EXAMPLE,
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

UPDATE_LEARNER_EXAMPLE = {
  "preferred_name": "",
  "preferred_first_name": "",
  "preferred_middle_name": "",
  "preferred_last_name": "",
  "preferred_name_type": "PreferredName",
  "preferred_pronoun": "",
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
  "gender": "NotSelected",
  "country_of_birth_code": "",
  "ethnicity": "",
  "employer_id": "test_employer_id",
  "employer": "",
  "employer_email": "testid@employer.com",
  "organisation_email_id": "jon.doe@foobar.com",
  "affiliation": "",
  "is_archived": False,
}

FULL_LEARNER_EXAMPLE = {
  "uuid": "U2DDBkl3Ayg0PWudzhI",
  **BASIC_LEARNER_EXAMPLE,
  "is_archived": False,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

BASIC_CURRICULUM_PATHWAY_EXAMPLE = {
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
  "metadata": {},
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
  "is_locked": False
}

FULL_CURRICULUM_PATHWAY_EXAMPLE = {
  "uuid": "asd98798as7dhjgkjsdfh",
  **BASIC_CURRICULUM_PATHWAY_EXAMPLE,
  "version": 1,
  "parent_version_uuid": "",
  "root_version_uuid": "",
  "is_archived": False,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

BASIC_LEARNER_HIERARCHY = {
  "label": "Program",
  "type": "curriculum_pathways",
  "data": {
    "name": "Program",
    "display_name": "Program",
    "description": "Next Step Pathway",
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {
      "learning_experiences": [],
      "curriculum_pathways": [
        "2VuPBz7Z1mHhcJ2Qvarb"
      ]
    },
    "achievements": [],
    "earned_achievements": [],
    "prerequisites": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": []
    },
    "is_locked": False,
    "uuid": "a1O2bogMGBToc8SpyTOb",
    "version": 1,
    "is_archived": False,
    "parent_version_uuid": "",
    "root_version_uuid": "",
    "created_time": "2022-11-17 12:56:25.713996+00:00",
    "last_modified_time": "2022-11-17 12:56:25.748592+00:00"
  },
  "children": [
    {
      "type": "curriculum_pathways",
      "data": {
        "uuid": "2VuPBz7Z1mHhcJ2Qvarb",
        "name": "HUM102",
        "display_name": "HUM102",
        "description": "Cluster A1 Pathway",
        "references": {},
        "parent_nodes": {
          "curriculum_pathways": [
            "a1O2bogMGBToc8SpyTOb"
          ]
        },
        "version": 1,
        "parent_version_uuid": "",
        "root_version_uuid": "",
        "is_archived": False,
        "is_deleted": False,
        "achievements": [],
        "prerequisites": {},
        "is_locked": False,
        "created_time": "2022-11-17 12:56:25.733674+00:00",
        "last_modified_time": "2022-11-17 12:56:25.770688+00:00",
        "created_by": "",
        "last_modified_by": "",
        "child_nodes": {
          "curriculum_pathways": [
            "6bM4QBvgdzMrFlx7Wj24"
          ]
        }
      },
      "label": "HUM102",
      "children": []
    }
  ]
}

LEARNING_RESOURCE_PROGRESS_RESPONSE = {
  "uuid": "zq3Yvjzs1l8HDWzQV3E7",
  "name": "Sources: Credible or not?",
  "display_name": "",
  "description": "Sources: Credible or not?",
  "author": "",
  "type": "html",
  "resource_path": "",
  "lti_content_item_id": "",
  "course_category": [],
  "alignments": {},
  "references": {},
  "parent_nodes": {
    "learning_objects": [
      "o5wWrgef1k2ei1aRhWfD"
    ]
  },
  "child_nodes": {},
  "version": 1,
  "parent_version_uuid": "",
  "root_version_uuid": "",
  "is_archived": False,
  "is_deleted": False,
  "metadata": {},
  "achievements": [],
  "completion_criteria": {},
  "prerequisites": {},
  "is_locked": False,
  "status": "not_attempted",
  "current_content_version": "",
  "content_history": {},
  "publish_history": {},
  "created_time": "2023-01-23 11:06:05.407870+00:00",
  "last_modified_time": "2023-01-23 11:06:05.554904+00:00",
  "created_by": "",
  "last_modified_by": "",
  "progress": 0,
  "last_attempted": "",
  "child_count": 0,
  "completed_child_count": 0
}

LEARNING_OBJECT_PROGRESS_RESPONSE = {
  "uuid": "o5wWrgef1k2ei1aRhWfD",
  "name": "Learning Object Topic 3",
  "display_name": "The humanities and the self",
  "description": "The humanities and the self",
  "author": "",
  "alignments": {},
  "references": {
    "skills": [
      "A2cdEGGlz3Fd3dwSHBt3"
    ]
  },
  "child_nodes": {
    "assessments": [{
      "uuid": "3WNiAl95GB3GPyxXgRyH",
      "name": "Formative assessment",
      "type": "practice",
      "author_id": "",
      "assessment_reference": "",
      "instructor_id": "",
      "assessor_id": "",
      "parent_nodes": {
        "learning_objects": [
          "o5wWrgef1k2ei1aRhWfD"
        ]
      },
      "child_nodes": "",
      "pass_threshold": "",
      "max_attempts": "",
      "alignments": "",
      "references": "",
      "achievements": [],
      "prerequisites": {
        "learning_resources": [
          "JO0sO8bxqBuh81P7vmhw"
        ]
      },
      "is_locked": True,
      "is_deleted": False,
      "metadata": "",
      "created_time": "2023-01-23 11:06:07.479463+00:00",
      "last_modified_time": "2023-01-23 11:06:07.608617+00:00",
      "created_by": "",
      "last_modified_by": "",
      "progress": 0,
      "status": "not_attempted",
      "last_attempted": "",
      "child_count": 0,
      "completed_child_count": 0
    }],
    "learning_resources": [{
      "uuid": "JO0sO8bxqBuh81P7vmhw",
      "name": "Understanding and Unlocking Your Source",
      "display_name": "",
      "description": "Understanding and Unlocking Your Source",
      "author": "",
      "type": "html",
      "resource_path": "",
      "lti_content_item_id": "",
      "course_category": [],
      "alignments": {},
      "references": {},
      "parent_nodes": {
        "learning_objects": [
          "o5wWrgef1k2ei1aRhWfD"
        ]
      },
      "child_nodes": {},
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "",
      "is_archived": False,
      "is_deleted": False,
      "metadata": {},
      "achievements": [],
      "completion_criteria": {},
      "prerequisites": {},
      "is_locked": False,
      "status": "in_progress",
      "current_content_version": "",
      "content_history": {},
      "publish_history": {},
      "created_time": "2023-01-23 11:06:07.003125+00:00",
      "last_modified_time": "2023-01-23 11:06:07.155958+00:00",
      "created_by": "",
      "last_modified_by": "",
      "progress": 0,
      "last_attempted": "2023-01-28 09:48:35.915681",
      "child_count": 0,
      "completed_child_count": 0
    }]
  },
  "parent_nodes": {
    "learning_experiences": [
      "QKhL7d795RLZ7Fd5UaMl"
    ]
  },
  "version": 1,
  "parent_version_uuid": "",
  "root_version_uuid": "",
  "is_archived": False,
  "is_deleted": False,
  "metadata": {},
  "achievements": [],
  "completion_criteria": {},
  "prerequisites": {},
  "is_locked": False,
  "equivalent_credits": 0,
  "duration": "",
  "created_time": "2023-01-23 11:06:04.912892+00:00",
  "last_modified_time": "2023-01-23 11:06:07.784580+00:00",
  "created_by": "",
  "last_modified_by": "",
  "progress": 0,
  "status": "in_progress",
  "last_attempted": "2023-01-28 09:48:35.915681",
  "child_count": 2,
  "completed_child_count": 0
}

LEARNING_EXPERIENCE_PROGRESS_RESPONSE = {
  "uuid": "QKhL7d795RLZ7Fd5UaMl",
  "name": "Topic 3",
  "display_name": "The humanities and the self",
  "description": "The humanities and the self",
  "author": "",
  "alignments": {},
  "references": {},
  "child_nodes": {
    "learning_objects": [
      {
        "uuid": "o5wWrgef1k2ei1aRhWfD",
        "name": "Learning Object Topic 3",
        "display_name": "The humanities and the self",
        "description": "The humanities and the self",
        "author": "",
        "alignments": {},
        "references": {
          "skills": [
            "A2cdEGGlz3Fd3dwSHBt3"
          ]
        },
        "child_nodes": {
          "learning_resources": [
            "zq3Yvjzs1l8HDWzQV3E7",
            "uBc8ph2Blk5KZKsBobAB",
            "oCfw2hiUFaKtp4SzI1HU",
            "XbIczFSRZbcmgncNaGN6",
            "JO0sO8bxqBuh81P7vmhw"
          ],
          "assessments": [
            "3WNiAl95GB3GPyxXgRyH"
          ]
        },
        "parent_nodes": {
          "learning_experiences": [
            "QKhL7d795RLZ7Fd5UaMl"
          ]
        },
        "version": 1,
        "parent_version_uuid": "",
        "root_version_uuid": "",
        "is_archived": False,
        "is_deleted": False,
        "metadata": {},
        "achievements": [],
        "completion_criteria": {},
        "prerequisites": {},
        "is_locked": False,
        "equivalent_credits": 0,
        "duration": "",
        "created_time": "2023-01-23 11:06:04.912892+00:00",
        "last_modified_time": "2023-01-23 11:06:07.784580+00:00",
        "created_by": "",
        "last_modified_by": "",
        "progress": 0,
        "status": "in_progress",
        "last_attempted": "2023-01-28 09:48:35.915681",
        "child_count": 6,
        "completed_child_count": 0
      }
    ]
  },
  "parent_nodes": {
    "curriculum_pathways": [
      "qw4vrxpYanLCSuL8Y45J"
    ]
  },
  "version": 1,
  "parent_version_uuid": "",
  "root_version_uuid": "",
  "is_archived": False,
  "is_deleted": False,
  "metadata": {},
  "achievements": [],
  "completion_criteria": {},
  "prerequisites": {},
  "is_locked": False,
  "equivalent_credits": 3,
  "duration": 60,
  "created_time": "2023-01-23 11:06:04.320224+00:00",
  "last_modified_time": "2023-01-23 11:06:05.258037+00:00",
  "created_by": "",
  "last_modified_by": "",
  "progress": 0,
  "status": "in_progress",
  "last_attempted": "2023-01-28 09:48:35.915681",
  "child_count": 1,
  "completed_child_count": 0
}

CURRICULUM_PATHWAY_PROGRESS_RESPONSE = {
  "uuid": "3kVJyWibMIUXjKnd3leY",
  "name": "Program",
  "display_name": "Program",
  "description": "Next Step Pathway",
  "author": "",
  "alignments": "",
  "references": {},
  "child_nodes": {
    "curriculum_pathways": [
      {
        "uuid": "CfjJG9Zd8qv6OeH1DAwS",
        "name": "HUM102",
        "display_name": "HUM102",
        "description": "Cluster A1 Pathway",
        "author": "",
        "alignments": "",
        "references": {},
        "child_nodes": {
          "curriculum_pathways": [
            {
              "uuid": "qw4vrxpYanLCSuL8Y45J",
              "name": "Examine how the humanities "
                      "influence understanding of "
                      "one's self-identity",
              "display_name": "Examine how the humanities "
                              "influence understanding of "
                              "one's self-identity",
              "description": "Competency 2 Pathway",
              "author": "",
              "alignments": "",
              "references": {},
              "child_nodes": {
                "learning_experiences": [
                  {
                    "uuid": "QKhL7d795RLZ7Fd5UaMl",
                    "name": "Topic 3",
                    "display_name": "The humanities and the self",
                    "description": "The humanities and the self",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "qw4vrxpYanLCSuL8Y45J"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 3,
                    "duration": 60,
                    "created_time": "2023-01-23 11:06:04.320224+00:00",
                    "last_modified_time": "2023-01-23 11:06:05.258037+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "in_progress",
                    "last_attempted": "2023-01-28 09:48:35.915681",
                    "child_count": 1,
                    "completed_child_count": 0,
                    "recent_child_node": {
                      "uuid": "o5wWrgef1k2ei1aRhWfD",
                      "name": "Learning Object Topic 3",
                      "display_name": "The humanities and the self",
                      "description": "The humanities and the self",
                      "author": "",
                      "alignments": {},
                      "references": {
                        "skills": [
                          "A2cdEGGlz3Fd3dwSHBt3"
                        ]
                      },
                      "child_nodes": {
                        "assessments": [
                          "3WNiAl95GB3GPyxXgRyH"
                        ],
                        "learning_resources": [
                          "zq3Yvjzs1l8HDWzQV3E7",
                          "uBc8ph2Blk5KZKsBobAB",
                          "oCfw2hiUFaKtp4SzI1HU",
                          "XbIczFSRZbcmgncNaGN6",
                          "JO0sO8bxqBuh81P7vmhw"
                        ]
                      },
                      "parent_nodes": {
                        "learning_experiences": [
                          "QKhL7d795RLZ7Fd5UaMl"
                        ]
                      },
                      "version": 1,
                      "parent_version_uuid": "",
                      "root_version_uuid": "",
                      "is_archived": False,
                      "is_deleted": False,
                      "metadata": {},
                      "achievements": [],
                      "completion_criteria": {},
                      "prerequisites": {},
                      "is_locked": False,
                      "equivalent_credits": 0,
                      "duration": "",
                      "created_time": "2023-01-23 11:06:04.912892+00:00",
                      "last_modified_time": "2023-01-23 11:06:07.784580+00:00",
                      "created_by": "",
                      "last_modified_by": "",
                      "progress": 0,
                      "status": "in_progress",
                      "last_attempted": "2023-01-28 09:48:35.915681",
                      "child_count": 6,
                      "completed_child_count": 0
                    }
                  },
                  {
                    "uuid": "G8KfmRiJyJ9IwxinvWea",
                    "name": "Topic 1",
                    "display_name": "What is self-identity?",
                    "description": "What is self-identity?",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "qw4vrxpYanLCSuL8Y45J"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 3,
                    "duration": 60,
                    "created_time": "2023-01-23 11:05:57.371709+00:00",
                    "last_modified_time": "2023-01-23 11:05:58.271737+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                  },
                  {
                    "uuid": "XeMfC3Q7HvbCsI7CtDhD",
                    "name": "Topic 2",
                    "display_name": "How identity is formed",
                    "description": "How identity is formed",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "qw4vrxpYanLCSuL8Y45J"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 3,
                    "duration": 60,
                    "created_time": "2023-01-23 11:06:01.068513+00:00",
                    "last_modified_time": "2023-01-23 11:06:02.048503+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                  },
                  {
                    "uuid": "rdTDi1qEdLHKnCvjkg1d",
                    "name": "Competency A2 Exam",
                    "display_name": "HUM102 Competency 2 Exam",
                    "description": "HUM102 Competency 2 Exam",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "qw4vrxpYanLCSuL8Y45J"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 3,
                    "duration": 60,
                    "created_time": "2023-01-23 11:06:07.924281+00:00",
                    "last_modified_time": "2023-01-23 11:06:09.525962+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                  }
                ]
              },
              "parent_nodes": {
                "curriculum_pathways": [
                  "CfjJG9Zd8qv6OeH1DAwS"
                ]
              },
              "version": 1,
              "parent_version_uuid": "",
              "root_version_uuid": "",
              "is_archived": False,
              "is_deleted": False,
              "metadata": {},
              "achievements": [],
              "completion_criteria": {},
              "prerequisites": {},
              "is_locked": False,
              "equivalent_credits": 0,
              "duration": "",
              "created_time": "2023-01-23 11:05:56.886484+00:00",
              "last_modified_time": "2023-01-23 11:06:08.201046+00:00",
              "created_by": "",
              "last_modified_by": "",
              "progress": 0,
              "status": "in_progress",
              "last_attempted": "2023-01-28 09:48:35.915681",
              "child_count": 4,
              "completed_child_count": 0,
              "earned_achievements": []
            },
            {
              "uuid": "nm9GNH0hvfnWFOC90qKD",
              "name": "Differentiate the various "
                      "perspectives of the humanities "
                      "in relation to a topic",
              "display_name": "Differentiate the various "
                              "perspectives of the humanities in "
                              "relation to a topic",
              "description": "Competency 1 Pathway",
              "author": "",
              "alignments": "",
              "references": {},
              "child_nodes": {
                "learning_experiences": [
                  {
                    "uuid": "mRnK0JqsNggf84NVKuN5",
                    "name": "Topic 1",
                    "display_name": "What are the humanities?",
                    "description": "What are the humanities?",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "nm9GNH0hvfnWFOC90qKD"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 3,
                    "duration": 60,
                    "created_time": "2023-01-23 11:05:34.904624+00:00",
                    "last_modified_time": "2023-01-23 11:05:37.587399+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                  },
                  {
                    "uuid": "EY6KNbNyiFlrhdqcPjLR",
                    "name": "Topic 2",
                    "display_name": "Humanities in everyday life",
                    "description": "Humanities in everyday life",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "nm9GNH0hvfnWFOC90qKD"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 4,
                    "duration": 60,
                    "created_time": "2023-01-23 11:05:41.241201+00:00",
                    "last_modified_time": "2023-01-23 11:05:42.849213+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                  },
                  {
                    "uuid": "N8NDmuoieO2qN5rY2glU",
                    "name": "Topic 3",
                    "display_name": "Understanding sources in the humanities",
                    "description": "Understanding sources in the humanities",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "nm9GNH0hvfnWFOC90qKD"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 3,
                    "duration": 40,
                    "created_time": "2023-01-23 11:05:46.207985+00:00",
                    "last_modified_time": "2023-01-23 11:05:47.811321+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                  },
                  {
                    "uuid": "IhfS19xp06W3UlD4vgce",
                    "name": "Topic 4",
                    "display_name": "Interpreting the humanities",
                    "description": "Interpreting the humanities",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "nm9GNH0hvfnWFOC90qKD"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 3,
                    "duration": 60,
                    "created_time": "2023-01-23 11:05:51.147173+00:00",
                    "last_modified_time": "2023-01-23 11:05:52.324925+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                  },
                  {
                    "uuid": "EiEukGmLf57vJ2NNLJVB",
                    "name": "Competency A1 Exam",
                    "display_name": "HUM102 Competency 1 Exam",
                    "description": "HUM102 Competency 1 Exam",
                    "author": "",
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                      "curriculum_pathways": [
                        "nm9GNH0hvfnWFOC90qKD"
                      ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": False,
                    "is_deleted": False,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": False,
                    "equivalent_credits": 3,
                    "duration": 60,
                    "created_time": "2023-01-23 11:05:54.298628+00:00",
                    "last_modified_time": "2023-01-23 11:05:56.752678+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                  }
                ]
              },
              "parent_nodes": {
                "curriculum_pathways": [
                  "CfjJG9Zd8qv6OeH1DAwS"
                ]
              },
              "version": 1,
              "parent_version_uuid": "",
              "root_version_uuid": "",
              "is_archived": False,
              "is_deleted": False,
              "metadata": {},
              "achievements": [
                "7zFdI9AJZ0RcbtyYwYMV"
              ],
              "completion_criteria": {},
              "prerequisites": {},
              "is_locked": False,
              "equivalent_credits": 0,
              "duration": "",
              "created_time": "2023-01-23 11:05:34.107785+00:00",
              "last_modified_time": "2023-01-23 11:05:54.627598+00:00",
              "created_by": "",
              "last_modified_by": "",
              "progress": 0,
              "status": "not_attempted",
              "last_attempted": "",
              "child_count": 0,
              "completed_child_count": 0,
              "earned_achievements": []
            }
          ]
        },
        "parent_nodes": {
          "curriculum_pathways": [
            "3kVJyWibMIUXjKnd3leY"
          ]
        },
        "version": 1,
        "parent_version_uuid": "",
        "root_version_uuid": "",
        "is_archived": False,
        "is_deleted": False,
        "metadata": {},
        "achievements": [
          "Dmmu7RHVRxO3GWXB4QB2",
          "FGfoMM2e4H2aKtPtzcIU"
        ],
        "completion_criteria": {},
        "prerequisites": {},
        "is_locked": False,
        "equivalent_credits": 0,
        "duration": "",
        "created_time": "2023-01-23 11:05:32.842625+00:00",
        "last_modified_time": "2023-01-23 11:05:57.269885+00:00",
        "created_by": "",
        "last_modified_by": "",
        "progress": 0,
        "status": "in_progress",
        "last_attempted": "2023-01-28 09:48:35.915681",
        "child_count": 2,
        "completed_child_count": 0,
        "earned_achievements": []
      }
    ]
  },
  "parent_nodes": {},
  "version": 1,
  "parent_version_uuid": "",
  "root_version_uuid": "",
  "is_archived": False,
  "is_deleted": False,
  "metadata": {},
  "achievements": [
    "DXb8TfeuN8W5FnnV6pby",
    "xp4EwXLm4qyFepvTe18N",
    "t0kVd7xrfM28zvcruy5N"
  ],
  "completion_criteria": {},
  "prerequisites": {},
  "is_locked": False,
  "equivalent_credits": 0,
  "duration": "",
  "created_time": "2023-01-23 11:05:31.430458+00:00",
  "last_modified_time": "2023-01-23 11:05:33.504965+00:00",
  "created_by": "",
  "last_modified_by": "",
  "progress": 0,
  "status": "in_progress",
  "last_attempted": "2023-01-28 09:48:35.915681",
  "child_count": 1,
  "completed_child_count": 0,
  "earned_achievements": []
}

BASIC_LEARNING_RESOURCE_EXAMPLE = {
  "name": "Text Books",
  "display_name": "Text Books",
  "description": "Testing description",
  "type": "video",
  "resource_path": "",
  "lti_content_item_id": "",
  "course_category": [
    "Testing category"
  ],
  "alignments": {
    "competency_alignments": [],
    "skill_alignments": []
  },
  "references": {
    "skills": [],
    "competencies": []
  },
  "parent_nodes": {
    "learning_objects": []
  },
  "child_nodes": {
    "concepts": []
  },
  "metadata": {},
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
  "is_locked": False
}

EDUCATION_TAB_DROPDOWN_VALUES = {
  "education_goals": [
    "To be able to do what I love",
    "To start a new career",
    "To make more money",
    "To provide a better life for my family",
    "To feel proud of what I've done",
    "To advance my existing career",
    "To make my family proud of me",
    "To make the world a better place"
  ],
  "employment_status": [
    "Full-time",
    "Part-time",
    "Seeking work",
    "Unemployed"
  ],
  "potential_career_fields": [
    {
      "field_name": "Architecture, engineering",
      "examples": "e.g., architect, drafter, electrical engineer"
    },
    {
      "field_name": "Arts, design, entertainment, sports, media",
      "examples": "e.g., fashion designer, video editor, author"
    },
    {
      "field_name": "Business, financial operations",
      "examples": "e.g., project manager, accountant, "
                  "human resources specialist, "
                  "marketing specialist"
    },
    {
      "field_name": "Community, social services",
      "examples": "e.g., social worker, clergy, community health worker"
    },
    {
      "field_name": "Computers, mathematics",
      "examples": "e.g., video game designer, actuary"
    },
    {
      "field_name": "Construction, extraction",
      "examples": "e.g., general contractor, carpenter, electrician"
    },
    {
      "field_name": "Educational instruction, library sciences",
      "examples": "e.g., teacher, professor, librarian"
    },
    {
      "field_name": "Farming, fishing, forestry",
      "examples": "e.g., forest ranger, animal breeder, agricultural inspector"
    },
    {
      "field_name": "Food preparation, service",
      "examples": "e.g., chef, bartender"
    },
    {
      "field_name": "Healthcare",
      "examples": "e.g., medical transcriptionist, "
                  "pharmacist, registered nurse, "
                  "medical assistant"
    },
    {
      "field_name": "Installation, maintenance, repair",
      "examples": "e.g., HVAC technician, auto mechanic, locksmith"
    },
    {
      "field_name": "Legal",
      "examples": "e.g., lawyer, paralegal"
    },
    {
      "field_name": "Personal care, service",
      "examples": "e.g., animal trainer, funeral attendant, cosmetologist"
    },
    {
      "field_name": "Protective service",
      "examples": "e.g., police officer, firefighter"
    },
    {
      "field_name": "Sales",
      "examples": "e.g., insurance agent, sales representative, "
                  "real estate broker"
    },
    {
      "field_name": "Sciences (life, physical, social)",
      "examples": "e.g., chemist, clinical psychologist, forensic scientist"
    },
    {
      "field_name": "Support (office, administrative)",
      "examples": "e.g., executive secretary, proofreader, data entry clerk"
    },
    {
      "field_name": "Something else not listed here",
      "examples": ""
    }
  ]
}

LEARNER_ACHIEVEMENTS = [
  {
    "uuid": "eMipP0l2DIDXNg4jYdBl",
    "name": "HUM102 Badge (course)",
    "type": "course equate",
    "alignments": "",
    "associations": "",
    "credits_available": "",
    "field_of_study": "",
    "metadata": {
      "design_config": {
        "shape": "",
        "theme": "",
        "illustration": ""
      }
    },
    "image": "",
    "result_descriptions": "",
    "tags": "",
    "description": "HUM102 Badge (course)",
    "timestamp": "",
    "is_archived": False,
    "is_deleted": False,
    "created_time": "2023-02-07 11:22:14.855202+00:00",
    "last_modified_time": "2023-02-07 11:22:15.016737+00:00",
    "created_by": "",
    "last_modified_by": "",
    "parent_node": {
      "uuid": "EjJ8xbDDIxWF9D5mWwDs",
      "name": "Level 1",
      "display_name": "Level 1",
      "alias": "level",
      "order": 1,
      "description": "HUM102PT,HUM13507,HUM13508,HUM23509",
      "author": "",
      "alignments": "",
      "references": {},
      "child_nodes": {
        "curriculum_pathways": [
          "gUj99wqBuY3hy0EEw3Jm"
        ]
      },
      "parent_nodes": {
        "curriculum_pathways": [
          "lL0BblkTWA7vF7uZO8ld"
        ]
      },
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "",
      "is_archived": False,
      "is_deleted": False,
      "metadata": {},
      "achievements": [
        "eMipP0l2DIDXNg4jYdBl"
      ],
      "completion_criteria": {},
      "prerequisites": {},
      "is_locked": False,
      "is_optional": "",
      "equivalent_credits": 0,
      "duration": "",
      "created_time": "2023-02-07 11:22:15.183627+00:00",
      "last_modified_time": "2023-02-07 11:22:16.918014+00:00",
      "created_by": "",
      "last_modified_by": ""
    },
    "status": "not_attempted",
    "child_achievements": [
      {
        "uuid": "Xf7vn1wrq02NvrtH69hX",
        "name": "competency",
        "type": "competency",
        "alignments": "",
        "associations": "",
        "credits_available": "",
        "field_of_study": "",
        "metadata": {
          "design_config": {
            "shape": "",
            "theme": "",
            "illustration": ""
          }
        },
        "image": "",
        "result_descriptions": "",
        "tags": "",
        "description": "competency",
        "timestamp": "",
        "is_archived": False,
        "is_deleted": False,
        "created_time": "2023-02-07 11:22:15.862169+00:00",
        "last_modified_time": "2023-02-07 11:22:16.026127+00:00",
        "created_by": "",
        "last_modified_by": "",
        "parent_node": {
          "uuid": "gUj99wqBuY3hy0EEw3Jm",
          "name": "HUM13507",
          "display_name": "HUM13507",
          "alias": "unit",
          "order": 1,
          "description": "Unit 1:HUM13507",
          "author": "",
          "alignments": "",
          "references": {},
          "child_nodes": {
            "learning_experiences": [
              "YkEc1j7qHnR96B1CfE6k"
            ]
          },
          "parent_nodes": {
            "curriculum_pathways": [
              "EjJ8xbDDIxWF9D5mWwDs"
            ]
          },
          "version": 1,
          "parent_version_uuid": "",
          "root_version_uuid": "",
          "is_archived": False,
          "is_deleted": False,
          "metadata": {},
          "achievements": [
            "Xf7vn1wrq02NvrtH69hX"
          ],
          "completion_criteria": {},
          "prerequisites": {},
          "is_locked": False,
          "is_optional": "",
          "equivalent_credits": 0,
          "duration": "",
          "created_time": "2023-02-07 11:22:16.187410+00:00",
          "last_modified_time": "2023-02-07 11:22:17.938154+00:00",
          "created_by": "",
          "last_modified_by": ""
        },
        "status": "not_attempted",
        "child_achievements": []
      }
    ]
  },
  {
    "uuid": "r0RymaDzuVtKwx8zcwM3",
    "name": "ENG130 Badge (course)",
    "type": "course equate",
    "alignments": "",
    "associations": "",
    "credits_available": "",
    "field_of_study": "",
    "metadata": {
      "design_config": {
        "shape": "",
        "theme": "",
        "illustration": ""
      }
    },
    "image": "",
    "result_descriptions": "",
    "tags": "",
    "description": "ENG130 Badge (course)Competency",
    "timestamp": "",
    "is_archived": False,
    "is_deleted": False,
    "created_time": "2023-02-07 11:22:35.056123+00:00",
    "last_modified_time": "2023-02-07 11:22:35.153295+00:00",
    "created_by": "",
    "last_modified_by": "",
    "parent_node": {
      "uuid": "7dHhauq60SyxqbVdOGAB",
      "name": "Level 1",
      "display_name": "Level 1",
      "alias": "level",
      "order": 1,
      "description": "ENG130.0, ENG130.1, ENG130.2, ENG130.3",
      "author": "",
      "alignments": "",
      "references": {},
      "child_nodes": {
        "curriculum_pathways": [
          "PyV6nIYJC0OnggzEew1N"
        ]
      },
      "parent_nodes": {
        "curriculum_pathways": [
          "9ASlLgzkZ6HesnVw0KY9"
        ]
      },
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "",
      "is_archived": False,
      "is_deleted": False,
      "metadata": {},
      "achievements": [
        "r0RymaDzuVtKwx8zcwM3"
      ],
      "completion_criteria": {},
      "prerequisites": {},
      "is_locked": False,
      "is_optional": "",
      "equivalent_credits": 0,
      "duration": "",
      "created_time": "2023-02-07 11:22:35.281370+00:00",
      "last_modified_time": "2023-02-07 11:22:36.080539+00:00",
      "created_by": "",
      "last_modified_by": ""
    },
    "status": "not_attempted",
    "child_achievements": [
      {
        "uuid": "0ldsjdcCGeHjMbOzUizW",
        "name": "competency",
        "type": "competency",
        "alignments": "",
        "associations": "",
        "credits_available": "",
        "field_of_study": "",
        "metadata": {
          "design_config": {
            "shape": "",
            "theme": "",
            "illustration": ""
          }
        },
        "image": "",
        "result_descriptions": "",
        "tags": "",
        "description": "competency",
        "timestamp": "",
        "is_archived": False,
        "is_deleted": False,
        "created_time": "2023-02-07 11:22:35.616831+00:00",
        "last_modified_time": "2023-02-07 11:22:35.737277+00:00",
        "created_by": "",
        "last_modified_by": "",
        "parent_node": {
          "uuid": "PyV6nIYJC0OnggzEew1N",
          "name": "Unit 1",
          "display_name": "Unit 1",
          "alias": "unit",
          "order": 1,
          "description": "Unit 1:HUM13507",
          "author": "",
          "alignments": "",
          "references": {},
          "child_nodes": {
            "learning_experiences": [
              "nzxm5SRDf8TbQUuGmxHp"
            ]
          },
          "parent_nodes": {
            "curriculum_pathways": [
              "7dHhauq60SyxqbVdOGAB"
            ]
          },
          "version": 1,
          "parent_version_uuid": "",
          "root_version_uuid": "",
          "is_archived": False,
          "is_deleted": False,
          "metadata": {},
          "achievements": [
            "0ldsjdcCGeHjMbOzUizW"
          ],
          "completion_criteria": {},
          "prerequisites": {},
          "is_locked": False,
          "is_optional": "",
          "equivalent_credits": 0,
          "duration": "",
          "created_time": "2023-02-07 11:22:35.828606+00:00",
          "last_modified_time": "2023-02-07 11:22:36.495865+00:00",
          "created_by": "",
          "last_modified_by": ""
        },
        "status": "not_attempted",
        "child_achievements": []
      }
    ]
  }
]
