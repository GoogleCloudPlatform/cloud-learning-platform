""" Schema examples and test objects for unit test """
import datetime

USER_EXAMPLE = {
    "id": "fake-user-id",
    "auth_id": "fake-user-id",
    "email": "user@gmail.com",
    "role": "Admin"
}

COURSE_TEMPLATE_EXAMPLE = {
    "id": "id",
    "name": "name",
    "description": "description",
    "admin": "admin",
    "instructional_designer": "IDesiner",
    "classroom_id": "clID",
    "classroom_code": "clcode",
    "classroom_url": "https://classroom.google.com"
}
UPDATE_COURSE_TEMPLATE_EXAMPLE = {
    "name": "name",
    "description": "description",
    "admin": "admin",
    "instructional_designer": "IDesiner",
    "classroom_id": "clID",
    "classroom_code": "clcode",
    "classroom_url": "https://classroom.google.com"
}

INSERT_COURSE_TEMPLATE_EXAMPLE = {
    "name": "name",
    "description": "description",
    "admin": "admin@gmail.com",
    "instructional_designer": "IDesiner@gmail.com"
}

COHORT_EXAMPLE = {
    "id": "fake-cohort-id",
    "name": "name",
    "description": "description",
    "start_date": datetime.datetime(year=2022, month=10, day=14),
    "end_date": datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022, month=11, day=14),
    "max_students": 0,
    "enrolled_students_count": 0,
    "course_template": "course_template/fake-id"
}
UPDATE_COHORT_EXAMPLE = {
    "name": "name",
    "description": "description",
    "start_date": datetime.datetime(year=2022, month=10, day=14),
    "end_date": datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022, month=11, day=14),
    "max_students": 0,
    "enrolled_students_count": 0,
    "course_template": "course_template/fake-id"
}
INSERT_COHORT_EXAMPLE = {
    "name": "name",
    "description": "description",
    "start_date": datetime.datetime(year=2022, month=10, day=14),
    "end_date": datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022, month=11, day=14),
    "max_students": 0,
    "course_template": "fake-id"
}

SECTION_EXAMPLE = {
    "id": "DLx0TNnYpCCwtCAJHUir",
    "name": "science 101",
    "section": "create_section_test C",
    "description": "This is updated create section test",
    "classroom_id": "123456789100",
    "classroom_code": "abcdef",
    "classroom_url": "https://classroom.google.com",
    "teachers_list": ["test_user_1@gmail.com"],
    "course_template": "course_templates/7d2zTApDFE6yEvUn8JFu",
    "cohort": "cohorts/1j4YsDuylLWtzHVszcAf"
}

CREDENTIAL_JSON = {
    "token": "fake-token",
    "refresh_token": "refresh-token",
    "token_uri": "fake_token_uri",
    "client_id": "client_fake_id",
    "client_secret": "client_fake_secrets",
    "scopes": ["Scopes"],
    "expiry": "2022-11-23T12:01:17Z"
}
