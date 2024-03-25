""" Schema examples and test objects for unit test """
# pylint: disable = line-too-long

### CATEGORY EXAMPLES ###
BASIC_CATEGORY_MODEL_EXAMPLE = {
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

FULL_CATEGORY_MODEL_EXAMPLE = {
    "uuid":
        "11rKkEkS7jTZYhzhmpPe",
    **BASIC_CATEGORY_MODEL_EXAMPLE, "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}

### COMPETENCY EXAMPLES ###
BASIC_COMPETENCY_MODEL_EXAMPLE = {
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
    "category": "",
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
    "reference_id":
        "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_uri":
        "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_name":
        "Credentialengine"
}

FULL_COMPETENCY_MODEL_EXAMPLE = {
    "uuid":
        "VLbtoEGMvf7HwNtLrT3y",
    **BASIC_COMPETENCY_MODEL_EXAMPLE, "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}

### DOMAIN EXAMPLES ###
BASIC_DOMAIN_MODEL_EXAMPLE = {
    "name":
        "Regression Analysis",
    "description":
        "Perform regression analysis to address an authentic problem",
    "keywords": ["tbn"],
    "reference_id":
        "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_uri":
        "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_name":
        "Credentialengine",
    "child_nodes": {
        "sub_domains": []
        }
}

FULL_DOMAIN_MODEL_EXAMPLE = {
    "uuid":
        "Dm7ejDD5tN5Hm6HsJMCj",
    **BASIC_DOMAIN_MODEL_EXAMPLE, "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}

### SKILL EXAMPLES ###
BASIC_SKILL_MODEL_EXAMPLE = {
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
        "id": "ST3",
        "name": "Certification"
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

FULL_SKILL_MODEL_EXAMPLE = {
    "uuid":
        "ZJYw5XczcLAEtdM081oG",
    **BASIC_SKILL_MODEL_EXAMPLE, "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}

### SUB DOMAIN EXAMPLES ###
BASIC_SUB_DOMAIN_MODEL_EXAMPLE = {
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

FULL_SUB_DOMAIN_MODEL_EXAMPLE = {
    "uuid":
        "ti4S6QMWtmB4vEUc9p4l",
    **BASIC_SUB_DOMAIN_MODEL_EXAMPLE, "created_time":
        "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time":
        "2022-03-03 09:22:49.843674+00:00"
}
