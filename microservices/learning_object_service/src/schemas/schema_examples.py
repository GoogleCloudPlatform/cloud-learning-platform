""" Schema examples and test objects for unit test """

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
    "duration": 15,
    "is_optional": False,
    "is_hidden": False,
    "is_active": False,
    "equivalent_credits": 0,
    "order": 1,
    "alias": "unit",
    "type": "pathway"
}

UPDATE_CURRICULUM_PATHWAY_EXAMPLE = {
    **BASIC_CURRICULUM_PATHWAY_EXAMPLE, "is_archived": False
}

FULL_CURRICULUM_PATHWAY_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_CURRICULUM_PATHWAY_EXAMPLE, "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "",
    "is_archived": False,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

CURRICULUM_PATHWAY_BY_ALIAS_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Kubernetes",
    "alias": "discipline"
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
    "references": {
        "skills": [],
        "competencies": []
    },
    "child_nodes": {
        "learning_objects": [],
        "assessments": []
    },
    "parent_nodes": {
        "learning_opportunities": [],
        "curriculum_pathways": []
    },
    "is_optional": False,
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
    "alias": "learning_experience",
    "order": 1,
    "type": "learning_experience",
    "resource_path": "",
    "srl_resource_path": ""
}

UPDATE_LEARNING_EXPERIENCE_EXAMPLE = {
    **BASIC_LEARNING_EXPERIENCE_EXAMPLE, "is_archived": False
}

FULL_LEARNING_EXPERIENCE_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_LEARNING_EXPERIENCE_EXAMPLE, "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "",
    "is_archived": False,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
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

UPDATE_LEARNING_OBJECT_EXAMPLE = {
    **BASIC_LEARNING_OBJECT_EXAMPLE, "is_archived": False
}

FULL_LEARNING_OBJECT_EXAMPLE = {
    "uuid": "asd98798as7dhjgkjsdfh",
    **BASIC_LEARNING_OBJECT_EXAMPLE, "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "",
    "is_archived": False,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

### LEARNING RESOURCE EXAMPLES ###
BASIC_LEARNING_RESOURCE_EXAMPLE = {
    "name": "Text Books",
    "display_name": "Text Books",
    "description": "Testing description",
    "is_optional": False,
    "type": "video",
    "resource_path": "",
    "lti_content_item_id": "",
    "course_category": ["Testing category"],
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
    "alias": "lesson",
    "order": 1,
    "duration": 15

}

UPDATE_LEARNING_RESOURCE_EXAMPLE = {
    **BASIC_LEARNING_RESOURCE_EXAMPLE, "is_archived": False
}

FULL_LEARNING_RESOURCE_EXAMPLE = {
    "uuid":
        "U2DDBkl3Ayg0PWudzhI",
    "root_version_uuid":
        "U2DDBkl3Ayg0PWudzhI",
    "parent_version_uuid":
        "",
    "version":
        1,
    "is_archived":
        False,
    **BASIC_LEARNING_RESOURCE_EXAMPLE, "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}

BASIC_FAQ_CONTENT_EXAMPLE = {
    "resource_path": None,
    "name": "Sample FAQ",
    "curriculum_pathway_id": "Sample_pathway_id"
}

FULL_FAQ_CONTENT_EXAMPLE = {
    **BASIC_FAQ_CONTENT_EXAMPLE,
    "uuid":
        "U2DDBkl3Ayg0PWudzhI",
    "is_archived":
        False,
    "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}
