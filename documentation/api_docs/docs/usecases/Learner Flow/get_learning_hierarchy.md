---
sidebar_label: Fetching Progress for Learner in Learning Hierarchy
sidebar_position: 1
---

# Fetching Progress for Learner in Learning Hierarchy

The following steps are to fetch progress of a learner on various Learning Hierarchy nodes.

:::note

Assumptions:
- Learner has logged in and has a valid `user_id`, `learner_id` and `session_id`
- Learner is interacting with a `learning_pathway` Program node and has the `node_id` for that node

:::


To fetch learner progress for any learning hierarchy level, A **GET** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/<learner_id>`** with **`node_type`** and **`node_id`** params where **`node_type`** is the hierarchy level of the node for which learner progress is to be fetched that accepts one of the following values **`curriculum_pathways`**, **`learning_experiences`**, **`learning_objects`** and **`learning_resources`** and **`node_id`** is the id of that node

### Fetching Progress on Levels and Units
When a learner reaches the pathway homepage, the learner will be presented with the following details
1. Level Information
  1. Learner progress for all levels
  2. Total number of units for each level
  3. Total number of completed units for each level

2. Learner Progress for all units within each level
  1. Total number of learning objects (hereafter referred as modules) for each unit
  2. Total number of completed modules units for each unit
  3. Up Next Module (most recent module) for each unit
  4. Units to be sorted based on the order of recent activity, unlocked, not attempted and completed

To fetch these details, **GET** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/<learner_id>`** with **`node_type`** set to  **`curriculum_pathways`** and **`node_id`** set to the node_id of program curriculum pathway (root pathway). The response object contains progress information as shown below

```json
{
    "success": true,
    "message": "Successfully fetched the curriculum_pathways progress for the given learner",
    "data": {
        "uuid": "Hf2kUwhf8fwI0W3H4A0y",
        "name": "Level Up Program",
        "display_name": "Level Up Program",
        "alias": "program",
        "order": null,
        "description": "Level Up Program Pathway",
        "author": null,
        "alignments": null,
        "references": {},
        "child_nodes": {
            "curriculum_pathways": [
                {
                    "uuid": "pfR8FXM4DtmcJDeVa6gk",
                    "name": "Humanity",
                    "display_name": "Humanity",
                    "alias": "discipline",
                    "order": 1,
                    "description": "",
                    "author": null,
                    "alignments": null,
                    "references": {},
                    "child_nodes": {
                        "curriculum_pathways": [
                            {
                                "uuid": "VzwvtsFo5f9vVw5tAfMB",
                                "name": "Level 1",
                                "display_name": "Level 1",
                                "alias": "level",
                                "order": 1,
                                "description": "HUM102PT,HUM13507,HUM13508,HUM23509",
                                "author": null,
                                "alignments": null,
                                "references": {},
                                "child_nodes": {
                                    "curriculum_pathways": [
                                        {
                                            "uuid": "HMAEeDh4Bvavq760r9y6",
                                            "name": "HUM13507",
                                            "display_name": "HUM13507",
                                            "alias": "unit",
                                            "order": 1,
                                            "description": "Unit 1:HUM13507",
                                            "author": null,
                                            "alignments": null,
                                            "references": {},
                                            "child_nodes": {
                                                "learning_experiences": [
                                                    {
                                                        "uuid": "uf4H3JFA2lembNcOEemr",
                                                        "name": "Humanities, Self & Society",
                                                        "display_name": "Humanities, Self & Society",
                                                        "description": "",
                                                        "author": null,
                                                        "alignments": {},
                                                        "references": {},
                                                        "parent_nodes": {
                                                            "curriculum_pathways": [
                                                                "HMAEeDh4Bvavq760r9y6"
                                                            ]
                                                        },
                                                        "version": 1,
                                                        "parent_version_uuid": "",
                                                        "root_version_uuid": "",
                                                        "is_archived": false,
                                                        "is_deleted": false,
                                                        "metadata": {},
                                                        "achievements": [],
                                                        "completion_criteria": {},
                                                        "prerequisites": {},
                                                        "is_locked": false,
                                                        "equivalent_credits": 0,
                                                        "duration": null,
                                                        "alias": "learning experience",
                                                        "order": 1,
                                                        "created_time": "2023-02-08 10:01:49.316645+00:00",
                                                        "last_modified_time": "2023-02-08 10:02:01.250341+00:00",
                                                        "created_by": "",
                                                        "last_modified_by": "",
                                                        "progress": 0,
                                                        "status": "not_attempted",
                                                        "last_attempted": "",
                                                        "child_count": 7,
                                                        "completed_child_count": 0,
                                                        "recent_child_node": {}
                                                    }
                                                ]
                                            },
                                            "parent_nodes": {
                                                "curriculum_pathways": [
                                                    "VzwvtsFo5f9vVw5tAfMB"
                                                ]
                                            },
                                            "version": 1,
                                            "parent_version_uuid": "",
                                            "root_version_uuid": "",
                                            "is_archived": false,
                                            "is_deleted": false,
                                            "metadata": {},
                                            "achievements": [
                                                "keCVXLcG1rlP7ZqvRzye"
                                            ],
                                            "completion_criteria": {},
                                            "prerequisites": {},
                                            "is_locked": false,
                                            "equivalent_credits": 0,
                                            "duration": null,
                                            "created_time": "2023-02-08 10:01:48.926857+00:00",
                                            "last_modified_time": "2023-02-08 10:01:49.624377+00:00",
                                            "created_by": "",
                                            "last_modified_by": "",
                                            "progress": 0,
                                            "status": "not_attempted",
                                            "last_attempted": "",
                                            "child_count": 1,
                                            "completed_child_count": 0,
                                            "earned_achievements": []
                                        }
                                    ]
                                },
                                "parent_nodes": {
                                    "curriculum_pathways": [
                                        "pfR8FXM4DtmcJDeVa6gk"
                                    ]
                                },
                                "version": 1,
                                "parent_version_uuid": "",
                                "root_version_uuid": "",
                                "is_archived": false,
                                "is_deleted": false,
                                "metadata": {},
                                "achievements": [
                                    "08KuLOgv1w5jxXTvM7e8"
                                ],
                                "completion_criteria": {},
                                "prerequisites": {},
                                "is_locked": false,
                                "equivalent_credits": 0,
                                "duration": null,
                                "created_time": "2023-02-08 10:01:48.160055+00:00",
                                "last_modified_time": "2023-02-08 10:01:49.202978+00:00",
                                "created_by": "",
                                "last_modified_by": "",
                                "progress": 0,
                                "status": "not_attempted",
                                "last_attempted": "",
                                "child_count": 1,
                                "completed_child_count": 0,
                                "earned_achievements": []
                            }
                        ]
                    },
                    "parent_nodes": {
                        "curriculum_pathways": [
                            "Hf2kUwhf8fwI0W3H4A0y"
                        ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": false,
                    "equivalent_credits": 0,
                    "duration": null,
                    "created_time": "2023-02-08 10:01:47.356417+00:00",
                    "last_modified_time": "2023-02-08 10:01:48.491302+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 1,
                    "completed_child_count": 0,
                    "earned_achievements": []
                },
                {
                    "uuid": "cjcCkqvAEvk8PUW2Hd1m",
                    "name": "English",
                    "display_name": "English",
                    "alias": "discipline",
                    "order": 1,
                    "description": "",
                    "author": null,
                    "alignments": null,
                    "references": {},
                    "child_nodes": {
                        "curriculum_pathways": [
                            {
                                "uuid": "PbJO32n2HfGou14LU9eV",
                                "name": "Level 1",
                                "display_name": "Level 1",
                                "alias": "level",
                                "order": 1,
                                "description": "ENG130.0, ENG130.1, ENG130.2, ENG130.3",
                                "author": null,
                                "alignments": null,
                                "references": {},
                                "child_nodes": {
                                    "curriculum_pathways": [
                                        {
                                            "uuid": "b48lR58Hu7IubopDxVSD",
                                            "name": "Unit 1",
                                            "display_name": "Unit 1",
                                            "alias": "unit",
                                            "order": 1,
                                            "description": "Unit 1:HUM13507",
                                            "author": null,
                                            "alignments": null,
                                            "references": {},
                                            "child_nodes": {
                                                "learning_experiences": [
                                                    {
                                                        "uuid": "8V40LOD7SpyzNb2UCIJt",
                                                        "name": "Analyze Written Works",
                                                        "display_name": "Analyze Written Works",
                                                        "description": "",
                                                        "author": null,
                                                        "alignments": {},
                                                        "references": {},
                                                        "parent_nodes": {
                                                            "curriculum_pathways": [
                                                                "b48lR58Hu7IubopDxVSD"
                                                            ]
                                                        },
                                                        "version": 1,
                                                        "parent_version_uuid": "",
                                                        "root_version_uuid": "",
                                                        "is_archived": false,
                                                        "is_deleted": false,
                                                        "metadata": {},
                                                        "achievements": [],
                                                        "completion_criteria": {},
                                                        "prerequisites": {},
                                                        "is_locked": false,
                                                        "equivalent_credits": 0,
                                                        "duration": null,
                                                        "alias": "learning experience",
                                                        "order": 1,
                                                        "created_time": "2023-02-08 10:02:02.405807+00:00",
                                                        "last_modified_time": "2023-02-08 10:02:04.715389+00:00",
                                                        "created_by": "",
                                                        "last_modified_by": "",
                                                        "progress": 0,
                                                        "status": "not_attempted",
                                                        "last_attempted": "",
                                                        "child_count": 8,
                                                        "completed_child_count": 0,
                                                        "recent_child_node": {}
                                                    }
                                                ]
                                            },
                                            "parent_nodes": {
                                                "curriculum_pathways": [
                                                    "PbJO32n2HfGou14LU9eV"
                                                ]
                                            },
                                            "version": 1,
                                            "parent_version_uuid": "",
                                            "root_version_uuid": "",
                                            "is_archived": false,
                                            "is_deleted": false,
                                            "metadata": {},
                                            "achievements": [
                                                "geAzkTlOQ1hYZyTtZrfC"
                                            ],
                                            "completion_criteria": {},
                                            "prerequisites": {},
                                            "is_locked": false,
                                            "equivalent_credits": 0,
                                            "duration": null,
                                            "created_time": "2023-02-08 10:02:02.077801+00:00",
                                            "last_modified_time": "2023-02-08 10:02:02.579592+00:00",
                                            "created_by": "",
                                            "last_modified_by": "",
                                            "progress": 0,
                                            "status": "not_attempted",
                                            "last_attempted": "",
                                            "child_count": 1,
                                            "completed_child_count": 0,
                                            "earned_achievements": []
                                        }
                                    ]
                                },
                                "parent_nodes": {
                                    "curriculum_pathways": [
                                        "cjcCkqvAEvk8PUW2Hd1m"
                                    ]
                                },
                                "version": 1,
                                "parent_version_uuid": "",
                                "root_version_uuid": "",
                                "is_archived": false,
                                "is_deleted": false,
                                "metadata": {},
                                "achievements": [
                                    "Dk8OSMMqQraiTziRQmGZ"
                                ],
                                "completion_criteria": {},
                                "prerequisites": {},
                                "is_locked": false,
                                "equivalent_credits": 0,
                                "duration": null,
                                "created_time": "2023-02-08 10:02:01.724520+00:00",
                                "last_modified_time": "2023-02-08 10:02:02.297659+00:00",
                                "created_by": "",
                                "last_modified_by": "",
                                "progress": 0,
                                "status": "not_attempted",
                                "last_attempted": "",
                                "child_count": 1,
                                "completed_child_count": 0,
                                "earned_achievements": []
                            }
                        ]
                    },
                    "parent_nodes": {
                        "curriculum_pathways": [
                            "Hf2kUwhf8fwI0W3H4A0y"
                        ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": false,
                    "equivalent_credits": 0,
                    "duration": null,
                    "created_time": "2023-02-08 10:02:01.352331+00:00",
                    "last_modified_time": "2023-02-08 10:02:01.857653+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 1,
                    "completed_child_count": 0,
                    "earned_achievements": []
                }
            ]
        },
        "parent_nodes": {},
        "version": 1,
        "parent_version_uuid": "",
        "root_version_uuid": "",
        "is_archived": false,
        "is_deleted": false,
        "metadata": {},
        "achievements": [],
        "completion_criteria": {},
        "prerequisites": {},
        "is_locked": false,
        "equivalent_credits": 0,
        "duration": null,
        "created_time": "2023-02-08 10:01:47.104199+00:00",
        "last_modified_time": "2023-02-08 10:02:01.485922+00:00",
        "created_by": "",
        "last_modified_by": "",
        "progress": 0,
        "status": "not_attempted",
        "last_attempted": "",
        "child_count": 2,
        "completed_child_count": 0,
        "earned_achievements": []
    }
}
```
### Fetching Progress on Learning Experiences
On expanding a Learning Experience, the learner will be presented with the following details
1. Learner's progress and status for the Learning Experience
2. Total number of modules and completed modules for learning experience
3. Learner's progress and status for all the modules of the learning experience


To fetch these details, **GET** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/<learner_id>`** with **`node_type`** set to  **`learning_experiences`** and **`node_id`** set to the node_id of the learning experience node. The response object contains progress information as shown below

``` json
{
    "success": true,
    "message": "Successfully fetched the learning_experiences progress for the given learner",
    "data": {
        "uuid": "uf4H3JFA2lembNcOEemr",
        "name": "Humanities, Self & Society",
        "display_name": "Humanities, Self & Society",
        "description": "",
        "author": null,
        "alignments": {},
        "references": {
            "skills": null,
            "competencies": null
        },
        "child_nodes": {
            "assessments": [
                {
                    "uuid": "JxlYoS0IxQghaACKXRWI",
                    "name": "Summative Assessment",
                    "type": "final",
                    "author_id": null,
                    "order": 6,
                    "assessment_reference": null,
                    "instructor_id": null,
                    "assessor_id": null,
                    "parent_nodes": {
                        "learning_experiences": [
                            "uf4H3JFA2lembNcOEemr"
                        ]
                    },
                    "child_nodes": null,
                    "pass_threshold": null,
                    "max_attempts": null,
                    "alignments": null,
                    "references": {
                        "skills": [
                            "fCKY3Tny7vOr4spvVG7D",
                            "5HoJVaNnpxea5CGlgGN3",
                            "bPzBthnORxzztLIupHyx",
                            "0nN8n3stW5gmO9wxe07B",
                            "GKOvbD1qoyhWjWBehNIL"
                        ],
                        "competencies": [
                            "GbLVqkRia88bQp4CiLRt"
                        ]
                    },
                    "achievements": [],
                    "prerequisites": {
                        "learning_objects": [
                            "CMqTApalNvFLonHBafwB"
                        ]
                    },
                    "is_locked": true,
                    "is_deleted": false,
                    "metadata": null,
                    "tags": null,
                    "resource_paths": null,
                    "instructions": null,
                    "created_time": "2023-02-08 10:02:00.940111+00:00",
                    "last_modified_time": "2023-02-08 10:02:01.048873+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                }
            ],
            "learning_resources": [],
            "learning_objects": [
                {
                    "uuid": "bDN6F6Yyb6Hy6p8K3QGg",
                    "name": "HUM102.1 Pre-test",
                    "display_name": "HUM102.1 Pre-test",
                    "description": "pre-test module",
                    "author": null,
                    "alignments": {},
                    "references": {
                        "skills": [
                            "fCKY3Tny7vOr4spvVG7D",
                            "5HoJVaNnpxea5CGlgGN3"
                        ]
                    },
                    "child_nodes": {
                        "assessments": [
                            "IxyXMKKMcEe9ZIxv6fhS"
                        ]
                    },
                    "parent_nodes": {
                        "learning_experiences": [
                            "uf4H3JFA2lembNcOEemr"
                        ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": false,
                    "equivalent_credits": 0,
                    "duration": null,
                    "alias": "module",
                    "order": 0,
                    "created_time": "2023-02-08 10:01:50.331380+00:00",
                    "last_modified_time": "2023-02-08 10:01:51.034658+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 1,
                    "completed_child_count": 0
                },
                {
                    "uuid": "5yx48E3OCcbx1CptaAsV",
                    "name": "Unit Overview",
                    "display_name": "Unit Overview",
                    "description": "Module 1",
                    "author": null,
                    "alignments": {},
                    "references": {},
                    "child_nodes": {
                        "learning_resources": [
                            "kRyYs49OgrntJXcKZ4ot"
                        ]
                    },
                    "parent_nodes": {
                        "learning_experiences": [
                            "uf4H3JFA2lembNcOEemr"
                        ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": false,
                    "equivalent_credits": 0,
                    "duration": null,
                    "alias": "module",
                    "order": 1,
                    "created_time": "2023-02-08 10:01:51.138197+00:00",
                    "last_modified_time": "2023-02-08 10:01:51.940983+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 1,
                    "completed_child_count": 0
                },
                {
                    "uuid": "UAhOn02kycBAH9GWKv03",
                    "name": "What Are the Humanities?",
                    "display_name": "What Are the Humanities?",
                    "description": null,
                    "author": null,
                    "alignments": {},
                    "references": {
                        "skills": [
                            "fCKY3Tny7vOr4spvVG7D"
                        ]
                    },
                    "child_nodes": {
                        "learning_resources": [
                            "XTIXn4T2dHE6u5GnUAbU",
                            "MruMiR9Vc9nDrDk1Eypo",
                            "dcI6MFBHwxuUtKf1BCt2",
                            "85jFDdPUI9DzRTAGJ1tZ"
                        ],
                        "assessments": [
                            "oOWt81s3Rb6nsQ6vEGkC"
                        ]
                    },
                    "parent_nodes": {
                        "learning_experiences": [
                            "uf4H3JFA2lembNcOEemr"
                        ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {
                        "learning_objects": [
                            "5yx48E3OCcbx1CptaAsV"
                        ]
                    },
                    "is_locked": true,
                    "equivalent_credits": 0,
                    "duration": null,
                    "alias": null,
                    "order": 2,
                    "created_time": "2023-02-08 10:01:52.090798+00:00",
                    "last_modified_time": "2023-02-08 10:01:54.166199+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 5,
                    "completed_child_count": 0
                },
                {
                    "uuid": "cNVYIG9phpsSiftrgKpe",
                    "name": "Humanities in everyday life",
                    "display_name": "Humanities in everyday life",
                    "description": "Module 3",
                    "author": null,
                    "alignments": {},
                    "references": {
                        "skills": [
                            "5HoJVaNnpxea5CGlgGN3"
                        ]
                    },
                    "child_nodes": {
                        "assessments": [
                            "kPtQDBJ2ototTq3drC2a"
                        ],
                        "learning_resources": [
                            "T0F1lyY4bZ4UGM17NeXM",
                            "fc4tyGo1hxsx4UaEWXLq",
                            "j1xeqMnYXXboFzdEKwOB",
                            "3IQtXndmt7DPraGjpLUY",
                            "qYK3EarSwEeMDU5lCvIM"
                        ]
                    },
                    "parent_nodes": {
                        "learning_experiences": [
                            "uf4H3JFA2lembNcOEemr"
                        ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {
                        "learning_objects": [
                            "UAhOn02kycBAH9GWKv03"
                        ]
                    },
                    "is_locked": true,
                    "equivalent_credits": 0,
                    "duration": null,
                    "alias": null,
                    "order": 3,
                    "created_time": "2023-02-08 10:01:54.298950+00:00",
                    "last_modified_time": "2023-02-08 10:01:56.411852+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 6,
                    "completed_child_count": 0
                },
                {
                    "uuid": "E9Pbx1899KXn0TXr8qit",
                    "name": "Understanding sources in the humanities",
                    "display_name": "Understanding sources in the humanities",
                    "description": "Module 4",
                    "author": null,
                    "alignments": {},
                    "references": {
                        "skills": [
                            "bPzBthnORxzztLIupHyx",
                            "0nN8n3stW5gmO9wxe07B"
                        ]
                    },
                    "child_nodes": {
                        "learning_resources": [
                            "U5Mtf5wUGYtVTto6gxC5",
                            "8gHMbH9cXfZMqjzySyes",
                            "xF79qQ7HpfdnQiuJBqZS",
                            "Bb6AYZF88r90iudCHltF",
                            "bcALzSpYNfndpyneADwX"
                        ],
                        "assessments": [
                            "lyFv4CYs0nGb6acmsetn"
                        ]
                    },
                    "parent_nodes": {
                        "learning_experiences": [
                            "uf4H3JFA2lembNcOEemr"
                        ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {
                        "learning_objects": [
                            "cNVYIG9phpsSiftrgKpe"
                        ]
                    },
                    "is_locked": true,
                    "equivalent_credits": 0,
                    "duration": null,
                    "alias": "module",
                    "order": 4,
                    "created_time": "2023-02-08 10:01:56.972342+00:00",
                    "last_modified_time": "2023-02-08 10:01:58.788955+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 6,
                    "completed_child_count": 0
                },
                {
                    "uuid": "CMqTApalNvFLonHBafwB",
                    "name": "Interpreting the humanities",
                    "display_name": "Interpreting the humanities",
                    "description": null,
                    "author": null,
                    "alignments": {},
                    "references": {
                        "skills": [
                            "bPzBthnORxzztLIupHyx",
                            "GKOvbD1qoyhWjWBehNIL"
                        ]
                    },
                    "child_nodes": {
                        "learning_resources": [
                            "8BEEffq6V5Lg4f9wagui",
                            "EpkM3PCkMd9C4if9jk8I",
                            "KuCBXapyDpP1FKj7Shzu"
                        ],
                        "assessments": [
                            "uNbjO0ggFFAgPvataQcI"
                        ]
                    },
                    "parent_nodes": {
                        "learning_experiences": [
                            "uf4H3JFA2lembNcOEemr"
                        ]
                    },
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {
                        "learning_objects": [
                            "E9Pbx1899KXn0TXr8qit"
                        ]
                    },
                    "is_locked": true,
                    "equivalent_credits": 0,
                    "duration": null,
                    "alias": null,
                    "order": 5,
                    "created_time": "2023-02-08 10:01:59.035329+00:00",
                    "last_modified_time": "2023-02-08 10:02:00.270758+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "status": "not_attempted",
                    "last_attempted": "",
                    "child_count": 4,
                    "completed_child_count": 0
                }
            ]
        },
        "parent_nodes": {
            "learning_experiences": null,
            "learning_objects": null
        },
        "version": 1,
        "parent_version_uuid": "",
        "root_version_uuid": "",
        "is_archived": false,
        "is_deleted": false,
        "metadata": {},
        "achievements": [],
        "completion_criteria": {},
        "prerequisites": {},
        "is_locked": false,
        "equivalent_credits": 0,
        "duration": null,
        "created_time": "2023-02-08 10:01:49.316645+00:00",
        "last_modified_time": "2023-02-08 10:02:01.250341+00:00",
        "created_by": "",
        "last_modified_by": "",
        "progress": 0,
        "status": "not_attempted",
        "last_attempted": "",
        "child_count": 7,
        "completed_child_count": 0,
        "alias": "learning experience",
        "order": 1
    }
}
```
### Fetching Progress on Modules
On expanding a Module, the learner will be presented with the following details
1. Learner's progress and status for the chosen module
2. Total number of resources and completed resources for chosen module
3. Learner's progress and status for all the learning resources of the chosen module


To fetch these details, **GET** request has to be made to the API endpoint - **`<APP_URL>/learner-profile-service/api/v1/learner/<learner_id>`** with **`node_type`** set to  **`learning_objects`** and **`node_id`** set to the node_id of the module node. The response object contains progress information as shown below

``` json
{
    "success": true,
    "message": "Successfully fetched the learning_objects progress for the given learner",
    "data": {
        "uuid": "5yx48E3OCcbx1CptaAsV",
        "name": "Unit Overview",
        "display_name": "Unit Overview",
        "description": "Module 1",
        "author": null,
        "alignments": {},
        "references": {
            "skills": null,
            "competencies": null
        },
        "child_nodes": {
            "assessments": [],
            "learning_resources": [
                {
                    "uuid": "kRyYs49OgrntJXcKZ4ot",
                    "name": "Unit Overview",
                    "display_name": "Unit Overview",
                    "description": null,
                    "author": null,
                    "type": "html",
                    "resource_path": null,
                    "lti_content_item_id": null,
                    "course_category": [],
                    "alignments": {},
                    "references": {},
                    "parent_nodes": {
                        "learning_objects": [
                            "5yx48E3OCcbx1CptaAsV"
                        ]
                    },
                    "child_nodes": {},
                    "version": 1,
                    "parent_version_uuid": "",
                    "root_version_uuid": "",
                    "is_archived": false,
                    "is_deleted": false,
                    "metadata": {},
                    "achievements": [],
                    "completion_criteria": {},
                    "prerequisites": {},
                    "is_locked": false,
                    "status": "not_attempted",
                    "current_content_version": null,
                    "content_history": {},
                    "publish_history": {},
                    "alias": null,
                    "order": 1,
                    "created_time": "2023-02-08 10:01:51.527117+00:00",
                    "last_modified_time": "2023-02-08 10:01:51.787829+00:00",
                    "created_by": "",
                    "last_modified_by": "",
                    "progress": 0,
                    "last_attempted": "",
                    "child_count": 0,
                    "completed_child_count": 0
                }
            ],
            "learning_objects": []
        },
        "parent_nodes": {
            "learning_experiences": [
                "uf4H3JFA2lembNcOEemr"
            ],
            "learning_objects": null
        },
        "version": 1,
        "parent_version_uuid": "",
        "root_version_uuid": "",
        "is_archived": false,
        "is_deleted": false,
        "metadata": {},
        "achievements": [],
        "completion_criteria": {},
        "prerequisites": {},
        "is_locked": false,
        "equivalent_credits": 0,
        "duration": null,
        "created_time": "2023-02-08 10:01:51.138197+00:00",
        "last_modified_time": "2023-02-08 10:01:51.940983+00:00",
        "created_by": "",
        "last_modified_by": "",
        "progress": 0,
        "status": "not_attempted",
        "last_attempted": "",
        "child_count": 1,
        "completed_child_count": 0,
        "alias": "module",
        "order": 1
    }
}
```