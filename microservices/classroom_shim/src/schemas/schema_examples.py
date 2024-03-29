""" Schema examples and test objects for unit test """
# pylint: disable=line-too-long
import datetime

BASE_LTI_ASSIGNMENT_EXAMPLE = {
    "context_id": "VFh6MzA4Jfq4bYN5",
    "lti_content_item_id": "Kv57BaY2uqE23N",
    "lti_assignment_title": "Test Assignment",
    "tool_id": "Z3bV9qJ7p41uCX",
    "max_points": 100,
    "start_date": datetime.datetime(year=2023, month=1, day=14),
    "end_date": datetime.datetime(year=2023, month=3, day=18),
    "due_date": datetime.datetime(year=2043, month=2, day=20)
}

INSERT_LTI_ASSIGNMENT_EXAMPLE = {
    "context_type": "section",
    "course_work_type": "course_work",
    **BASE_LTI_ASSIGNMENT_EXAMPLE
}

LTI_ASSIGNMENT_EXAMPLE = {
    "id": "N49q6vGt29oBvn8gt",
    "course_work_id": "Px5cTmh2Xvq1Cb",
    **INSERT_LTI_ASSIGNMENT_EXAMPLE
}

UPDATE_LTI_ASSIGNMENT_EXAMPLE = {
    "course_work_id": "Px5cTmh2Xvq1Cb",
    **BASE_LTI_ASSIGNMENT_EXAMPLE
}

COPY_LTI_ASSIGNMENT_EXAMPLE = {
    "lti_assignment_id": "bV2EH89JdS76t7q34",
    "context_id": "n0q082N1CN8Wb34y3",
    "source_context_id": "N4gq3n07w9vbHsAqc",
    "course_work_id": "Bre15nb2n03Vm8PsY",
    "start_date": datetime.datetime(year=2023, month=1, day=14),
    "end_date": datetime.datetime(year=2023, month=3, day=14),
    "due_date": datetime.datetime(year=2023, month=2, day=14)
}

LTI_POST_GRADE_MODEL = {
    "user_id": "V2bpB62b8nPb18yn9",
    "comment": "Good work!",
    "lti_content_item_id": "2sb3C9bnVs5ybe3ne4",
    "maximum_grade": "50",
    "assigned_grade": "30",
    "draft_grade": "20",
    "line_item_title": "Test Assignment 1",
    "validate_title": False
}

CONTEXT_EXAMPLE = {
    "id": "BOqh34378v3qGir",
    "name": "Context name",
    "description": "Context description",
    "context_type": "section"
}

CONTEXT_MEMBERS_EXAMPLE = {
    "user_id": "Ka1OyrOb9YuQ34",
    "email": "test@email.com",
    "user_type": "learner",
    "first_name": "Test",
    "last_name": "User1",
    "photo_url": "https://lh3.googleusercontent.com/a/test",
    "status": "active",
    "enrollment_status": "active"
}
