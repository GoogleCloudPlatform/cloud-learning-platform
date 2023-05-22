"""References for the Collection"""

from common.models import (
    LearningObject, LearningExperience, LearningResource,
    CurriculumPathway, Achievement, User, UserGroup, Action, Permission,
    Module, Application, Activity, Agent)

collection_references = {
    # Learning Object Service
    "learning_resources": LearningResource,
    "learning_objects": LearningObject,
    "learning_experiences": LearningExperience,
    "curriculum_pathways": CurriculumPathway,
    "achievements": Achievement,
    # User Management
    "user_groups": UserGroup,
    "users": User,
    "actions": Action,
    "action_id": Action,
    "modules": Module,
    "module_id": Module,
    "permissions": Permission,
    "applications": Application,
    "application_id": Application,
    "activities": Activity,
    "agents": Agent
}

LOS_COLLECTIONS = [
    "curriculum_pathways", "learning_experiences", "learning_objects",
    "learning_resources", "assessments"
]
