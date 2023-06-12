"""Example Data for testing"""
import datetime
from common.models.cohort import Cohort
from common.models.section import Section
from common.models.course_template import CourseTemplate

TEST_USER = {
    "user_id": "kh5FoIBOx5qDsfh4ZRuv",
    "first_name": "first",
    "last_name": "last",
    "email": "xyz@gmail.com",
    "user_type": "learner",
    "status": "active",
    "gaia_id": "1234577657333",
    "photo_url": "https://lh3.googleusercontent.com/a/AEd"
}

TEST_COURSE_TEMPLATE = {
    "name": "name",
    "description": "description",
    "admin": "admin@gmail.com",
    "classroom_id": "clID",
    "classroom_code": "clcode",
    "classroom_url": "https://classroom.google.com"
}

TEST_COHORT = {
    "name": "name",
    "description": "description",
    "start_date": datetime.datetime(year=2022, month=10, day=14),
    "end_date": datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022, month=11, day=14),
    "max_students": 100,
    "enrolled_students_count": 0
}

TEST_SECTION = {
    "name": "section_name",
    "section": "section c",
    "description": "description",
    "classroom_id": "cl_id",
    "classroom_code": "cl_code",
    "classroom_url": "https://classroom.google.com",
    "enrolled_students_count": 0,
    "max_students":25
}

TEST_COURSE_TEMPLATE2 = {
    "name": "test-name",
    "description": "test-description",
    "admin": "test-admin@gmail.com",
    "instructional_designer": "IDesiner@gmail.com",
    "classroom_id": "fake_classroom_id",
    "classroom_code": "fake-classroom_code",
    "classroom_url": "https://classroom.google.com"
}

TEST_COHORT2 = {
    "name": "name",
    "description": "description",
    "course_template": "fake_template_id",
    "start_date": datetime.datetime(year=2022, month=10, day=14),
    "end_date": datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022, month=11, day=14),
    "max_students": 100,
    "enrolled_students_count": 0
}

TEST_SECTION2 = {
    "name": "section_name",
    "section": "section c",
    "description": "description",
    "classroom_id": "cl_id",
    "classroom_code": "cl_code",
    "classroom_url": "https://classroom.google.com",
    "course_template": "fake_template_id",
    "cohort": "fake_cohort_id",
    "enrolled_students_count": 0,
    "max_students":25

}


def create_fake_data(test_course_template, test_cohort, test_section,
                     classroom_id):
  """Function to create temprory data"""

  test_course_template["classroom_id"] = classroom_id
  course_template = CourseTemplate.from_dict(test_course_template)
  course_template.save()
  test_cohort["course_template"] = course_template
  cohort = Cohort.from_dict(test_cohort)
  cohort.save()
  test_section["cohort"] = cohort
  test_section["course_template"] = course_template
  section = Section.from_dict(test_section)
  section.save()
  return course_template, cohort, section

TEST_COURSE = {
    "title": "test course",
    "label": "test label for course"
}

TEST_COMPETENCY = {
    "title": "test competency",
    "description": "test description for competency",
    "label": "test label for competency"
}

TEST_SUB_COMPETENCY = {
    "title": "test sub_competency",
    "description": "test description for sub_competency",
    "all_learning_resource": "the full content of the learning resource",
    "label": "test label for competency",
    "total_lus": 10
}

TEST_LEARNING_OBJECTIVE = {
    "title": "test learning_objective",
    "description": "test description for learning_objective"
}

TEST_LEARNING_UNIT = {
    "title": "test learning_unit",
    "text": "test text for learning_unit"
}

PARENT_LEARNING_OBJECT = {
    "uuid": "GW3bquwvTYbfnwBbyL",
    "name": "Online presentation",
    "description": "",
    "author": "",
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

CHILD_LEARNING_OBJECTS = [{
    "uuid": "2sdGDkf5IV7fa1nA",
    "name": "Online presentation 2",
    "description": "",
    "author": "",
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
}, {
    "uuid": "UY7kvV88IVvyiv7d",
    "name": "Online presentation 3",
    "description": "",
    "author": "",
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
}]

PARENT_CURRICULUM_PATHWAY_OBJECT = {
    "uuid": "asd98798as7dhjgkjsdfh",
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

CHILD_CURRICULUM_PATHWAY_OBJECTS = [{
    "uuid": "h3d98798asjgkjsdfh7d6",
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
}]
