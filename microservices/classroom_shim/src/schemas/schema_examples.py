""" Schema examples and test objects for unit test """
# pylint: disable=line-too-long
import datetime

LTI_ASSIGNMENT_EXAMPLE = {
    "id": "N49q6vGt29oBvn8gt",
    "section_id": "VFh6MzA4Jfq4bYN5",
    "lti_content_item_id": "Kv57BaY2uqE23N",
    "lti_assignment_title": "Test Assignment",
    "tool_id": "Z3bV9qJ7p41uCX",
    "course_work_id": "Px5cTmh2Xvq1Cb",
    "max_points": 100,
    "start_date": datetime.datetime(year=2023, month=1, day=14),
    "end_date": datetime.datetime(year=2023, month=3, day=18),
    "due_date": datetime.datetime(year=2023, month=2, day=20)
}

INSERT_LTI_ASSIGNMENT_EXAMPLE = {
    "section_id": "VFh6MzA4Jfq4bYN5",
    "lti_content_item_id": "Kv57BaY2uqE23N",
    "lti_assignment_title": "Test Assignment",
    "tool_id": "Z3bV9qJ7p41uCX",
    "course_work_id": "Px5cTmh2Xvq1Cb",
    "max_points": 100,
    "start_date": datetime.datetime(year=2023, month=1, day=14),
    "end_date": datetime.datetime(year=2023, month=3, day=18),
    "due_date": datetime.datetime(year=2023, month=2, day=20)
}

UPDATE_LTI_ASSIGNMENT_EXAMPLE = {
    "section_id": "VFh6MzA4Jfq4bYN5",
    "lti_content_item_id": "Kv57BaY2uqE23N",
    "lti_assignment_title": "Test Assignment",
    "tool_id": "Z3bV9qJ7p41uCX",
    "course_work_id": "Px5cTmh2Xvq1Cb",
    "max_points": 100,
    "start_date": datetime.datetime(year=2023, month=1, day=14),
    "end_date": datetime.datetime(year=2023, month=3, day=18),
    "due_date": datetime.datetime(year=2023, month=2, day=20)
}

LTI_POST_GRADE_MODEL = {
    "user_id": "V2bpB62b8nPb18yn9",
    "comment": "Good work!",
    "lti_content_item_id": "2sb3C9bnVs5ybe3ne4",
    "maximum_grade": "50",
    "assigned_grade": "30",
    "draft_grade": "20",
}
