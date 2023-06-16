"""References for the Collection"""

from common.models import (
    LearningObject, AssessmentItem, LearningExperience, LearningResource,
    CurriculumPathway, KnowledgeServiceLearningContent, Concept, SubConcept,
    KnowledgeServiceLearningObjective, KnowledgeServiceLearningUnit, Skill,
    SkillServiceCompetency, Category, Domain, SubDomain, Achievement,
    Assessment, SubmittedAssessment, User, UserGroup, Action, Permission,
    Module, Application, Activity, Agent, Rubric,RubricCriterion)

collection_references = {
    # Assessment Service
    "assessment_items": AssessmentItem,
    "assessments": Assessment,
    "submitted_assessments": SubmittedAssessment,
    "rubric_criteria": RubricCriterion,
    "rubrics": Rubric,
    # Learning Object Service
    "learning_resources": LearningResource,
    "learning_objects": LearningObject,
    "learning_experiences": LearningExperience,
    "curriculum_pathways": CurriculumPathway,
    "achievements": Achievement,
    # Knowledge Service
    "learning_resource": KnowledgeServiceLearningContent,
    "concepts": Concept,
    "sub_concepts": SubConcept,
    "learning_objectives": KnowledgeServiceLearningObjective,
    "learning_units": KnowledgeServiceLearningUnit,
    # Skill Service
    "skills": Skill,
    "competencies": SkillServiceCompetency,
    "categories": Category,
    "domains": Domain,
    "sub_domains": SubDomain,
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
