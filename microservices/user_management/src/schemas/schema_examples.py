"""Schema Examples for User APIs"""
import json


BASIC_USER_MODEL_EXAMPLE = {
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
  "photo_url" :"//lh3.googleusercontent.com/a/default-user",
  "inspace_user": {
    "is_inspace_user": False,
    "inspace_user_id": ""
  },
  "is_deleted": False
}

UPDATE_USER_MODEL_EXAMPLE = {
  "first_name": "steve",
  "last_name": "jobs",
  "user_groups": ["44qxEpc35pVMb6AkZGbi"],
  "access_api_docs": False,
  "email": "updateemailtest@gamil.com"
}

FULL_USER_MODEL_EXAMPLE = {
  "user_id": "124hsgxR77QKS8uS7Zgm",
  **BASIC_USER_MODEL_EXAMPLE, "user_type_ref": "U2DDBkl3Ayg0PWudzhI"
}

BASIC_ACTION_MODEL_EXAMPLE = {
    "name": "edit",
    "description": "edit includes view and create permissions",
    "action_type": "other"
}

FULL_ACTION_MODEL_EXAMPLE = {
  "uuid": "124hsgxR77QKS8uS7Zgm",
  **BASIC_ACTION_MODEL_EXAMPLE
}

BASIC_MODULE_MODEL_EXAMPLE = {
    "name": "learning resource",
    "description": "learning resource module",
    "actions": ["44qxEpc35pVMb6AkZGbi"]
}

FULL_MODULE_MODEL_EXAMPLE = {
  "uuid": "124hsgxR77QKS8uS7Zgm",
  **BASIC_MODULE_MODEL_EXAMPLE
}

BASIC_GROUP_MODEL_EXAMPLE = {
    "name": "assessors",
    "description": "group of assessors",
    "users": ["44qxEpc35pVMb6AkZGbi"],
    "permissions": ["U2DDBkl3Ayg0PWudzhI"],
    "applications": ["dfeSo7867vDSDDFC89HJ"]
}

POST_USERGROUP_MODEL_EXAMPLE = {
  "name": "assessors",
  "description": "group of assessors"
}

UPDATE_GROUP_MODEL_EXAMPLE = {
    "name": "assessors",
    "description": "group of assessors"
}

BASIC_GROUP_USERS_EDIT_EXAMPLE = {"user_ids": ["44qxEpc35pVMb6AkZGbi"]}

FULL_GROUP_MODEL_EXAMPLE = {
  "uuid": "124hsgxR77QKS8uS7Zgm",
  **BASIC_GROUP_MODEL_EXAMPLE
}



POST_PERMISSION_MODEL_EXAMPLE = {
  "name": "assessment_authoring.summative_assessment.edit",
  "description": "edit permission",
  "application_id": "Dfchd56otyghfgfjioiK",
  "module_id": "55txEec45pVMf6Akvcew",
  "action_id": "44qxEpc35pVMb6AkZGbi",
}

BASIC_PERMISSION_MODEL_EXAMPLE = {
    **POST_PERMISSION_MODEL_EXAMPLE,
    "user_groups": ["U2DDBkl3Ayg0PWudzhI"]
}

FULL_PERMISSION_MODEL_EXAMPLE = {
  "uuid": "124hsgxR77QKS8uS7Zgm",
  **BASIC_PERMISSION_MODEL_EXAMPLE
}

PERMISSION_FILTER_UNIQUE_EXAMPLE = {
  "applications": [
    {"uuid": "124hsgxR77QKS8uS7Zgm", "name": "content management"}
  ],
  "modules": [
    {"uuid": "124hsgxR77QKS8uioZgm", "name": "learning resource"}
  ],
  "actions": [
    {"uuid": "1579jkR77QKS8uS7Zgm", "name": "edit"}
  ],
  "user_groups": [
    {"uuid": "147dvlgxR77QKS8uS76", "name": "assessors"}
  ]
}

BASIC_APPLICATION_MODEL_EXAMPLE = {
    "name": "content management",
    "description": "application for content creation",
    "modules": ["44qxEpc35pVMb6AkZGbi"]
}

FULL_APPLICATION_MODEL_EXAMPLE = {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    **BASIC_APPLICATION_MODEL_EXAMPLE
}

## SESSION EXAMPLES ###

POST_SESSION_EXAMPLE = {
  "user_id": "User ID",
  "parent_session_id": None,
  "session_data": None
}

UPDATE_SESSION_EXAMPLE = {
  "session_data": {
    "node_id": "U2DDBkl3Ayg0PWudzhI",
    "node_type": "assessment_items",
    "learnosity_session_id": "U2DDBkl3Ayg0PWudzhI"
  }
}

BASIC_SESSION_EXAMPLE = {
  "user_id": "User ID",
  "parent_session_id": None,
  "session_data": None,
  "is_expired": False
}

FULL_SESSION_EXAMPLE = {
  "session_id": "U2DDBkl3Ayg0PWudzhI",
  **BASIC_SESSION_EXAMPLE, "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

BASIC_ASSOCIATION_GROUP_EXAMPLE = {
    "name": "Association Group Name",
    "description": "Description for Association Group"
}

FULL_LEARNER_ASSOCIATION_GROUP_EXAMPLE = {
  "uuid": "124hsgxR77QKS8uS7Zgm",
  "association_type": "learner",
  "users": [],
  "associations": {
    "coaches": [],
    "instructors": [],
    "curriculum_pathway_id": ""
  },
  **BASIC_ASSOCIATION_GROUP_EXAMPLE,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

FULL_DISCIPLINE_ASSOCIATION_GROUP_EXAMPLE = {
  "uuid": "hsgxR77QKS8uS7Zg",
  "association_type": "discipline",
  "users": [],
  "associations": {
    "curriculum_pathways": []
  },
  **BASIC_ASSOCIATION_GROUP_EXAMPLE,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

ASSOCIATION_GROUP_EXAMPLE = {
  "uuid": "hsgxR77QKS8uS7Zg",
  "association_type": "discipline",
  "users": [],
  "associations": {},
  **BASIC_ASSOCIATION_GROUP_EXAMPLE,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

UPDATE_LEARNER_ASSOCIATION_STATUS_EXAMPLE = {
  "user": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "status": "inactive"
    },
  "coach": {
    "coach_id": "hsgxR77QKS8uS7Zg",
    "status": "inactive"
    },
  "instructor": {
    "instructor_id": "sgxR77QKS8uS7Zgm",
    "curriculum_pathway_id": "24hsgxR77aer",
    "status": "inactive"
    }
}

UPDATE_DISCIPLINE_ASSOCIATION_STATUS_EXAMPLE = {
  "user": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "status": "inactive"
    },
  "curriculum_pathway": {
    "curriculum_pathway_id": "U2DDBkl3Ayg0PWudzhI",
    "status": "inactive"
    }
}

BASIC_STAFF_EXAMPLE = {
  "first_name": "Ted",
  "last_name": "Turner",
  "preferred_name": "staff",
  "bio": "",
  "pronoun": "he/him/his",
  "email": "ted.turner@email.com",
  "phone_number": "0000000000",
  "shared_inboxes": "",
  "timezone": "Eastern (ET) - Washington, DC",
  "office_hours": [],
  "photo_url" :"//lh3.googleusercontent.com/a/default-user"
}

FULL_STAFF_EXAMPLE = {
  "uuid": "hsgxR77QKS8uS7Zg",
  **BASIC_STAFF_EXAMPLE,
  "created_time": "2022-03-03 09:22:49.843674+00:00",
  "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
}

ADD_USER_EXAMPLE = {
    "users": ["hsgxR77QKS8uS7Zg", "124hsgxR77QKS8uS7Zgm"],
    "status": "active"
}

REMOVE_USER_EXAMPLE = {"user": "hsgxR77QKS8uS7Zg"}

ADD_COACH_EXAMPLE = {
    "coaches": ["hsgxR77QKS8uS7Zg"],
    "status": "active"
}

REMOVE_COACH_EXAMPLE = {"coach": "hsgxR77QKS8uS7Zg"}

GET_APPLICATIONS_OF_USER = {
  "applications": [{
      "application_name": "content management",
      "application_id": "RT34swyyiutdhjiiou"
  }]
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

BASIC_CURRICULUM_PATHWAY_EXAMPLE = {
  "name": "Test Curriculum Pathway",
  "alias": "discipline",
  "display_name": "Test CP",
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
}

ADD_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE = {
  "instructors": ["evz38z0IVuj719DrdUXg"],
  "curriculum_pathway_id": "t0U9eJzsxCtB7Z3LLwdK",
  "status": "active"
}

REMOVE_INSTRUCTOR_LEARNER_ASSOCIATION_GROUP_EXAMPLE = {
  "instructor": "evz38z0IVuj719DrdUXg",
  "curriculum_pathway_id": "t0U9eJzsxCtB7Z3LLwdK",
}

with open("./data/profile_fields.json", "r", encoding="utf-8") as f:
  fields = json.load(f)

PROFILE_FIELDS = fields
