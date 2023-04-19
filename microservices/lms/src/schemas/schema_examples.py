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
    "admin": "admin@gmail.com",
    "instructional_designer": "idesiner@gmail.com",
    "classroom_id": "clID",
    "classroom_code": "clcode",
    "classroom_url": "https://classroom.google.com"
}
UPDATE_COURSE_TEMPLATE_EXAMPLE = {
    "name": "name",
    "description": "description",
    "instructional_designer": "idesiner@gmail.com"
}

INSERT_COURSE_TEMPLATE_EXAMPLE = {
    "name": "name",
    "description": "description",
    "instructional_designer": "idesiner@gmail.com"
}

COHORT_EXAMPLE = {
    "id": "fake-cohort-id",
    "name": "name",
    "description": "description",
    "start_date": datetime.datetime(year=2022, month=10, day=14),
    "end_date": datetime.datetime(year=2022, month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022, month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022, month=11, day=14),
    "max_students": 200,
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
    "max_students": 200,
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
    "max_students": 200,
    "course_template_id": "fake-id"
}

SECTION_EXAMPLE = {
    "id": "id",
    "name": "science 101",
    "section": "create_section_test C",
    "description": "This is updated create section test",
    "classroom_id": "123456789100",
    "classroom_code": "abcdef",
    "classroom_url": "https://classroom.google.com",
    "teachers": ["test_user_1@gmail.com"],
    "course_template": "course_templates/7d2zTApD-id",
    "cohort": "cohorts/1j-id",
    "enrolled_students_count":2
}
INSERT_SECTION_EXAMPLE = {
    "name": "section c",
    "description": "This is updated create section test",
    "course_template": "course_template-id",
    "cohort": "cohort-id",
    "teachers": ["test_user@gmail.com"]
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
TEMP_USER = {
  "user_id":"kh5FoIBOx5qDsfh4ZRuv",
  "first_name": "",
  "last_name": "",
  "email":"clplmstestuser1@gmail.com",
  "user_type": "learner",
  "user_type_ref": "",
  "user_groups": [],
  "status": "active",
  "is_registered": True,
  "failed_login_attempts_count": 0,
  "access_api_docs": False,
  "gaia_id":"1234577657333",
  "photo_url":"https://lh3.googleusercontent.com/a/AEd"
  }
GET_STUDENT_EXAMPLE = TEMP_USER
GET_STUDENT_EXAMPLE["course_enrollment_id"]="2xBnBjqm2X3eRgVxE6Bv"
GET_STUDENT_EXAMPLE["invitation_id"]="2xBnBjqm2X3eRgVxE6Bv"
GET_STUDENT_EXAMPLE["student_email"]="test_user@gmail"
GET_STUDENT_EXAMPLE["section_id"]="fake-section-id"
GET_STUDENT_EXAMPLE["cohort_id"]="fake-cohort-id"
GET_STUDENT_EXAMPLE["classroom_id"]="123453333"
GET_STUDENT_EXAMPLE["enrollment_status"]="active"
GET_STUDENT_EXAMPLE["classroom_url"]="https://classroom.google.com/c/NTYzMhjhjr"

UPDATE_SECTION = {
    "id": "string",
    "course_id": "string",
    "section_name": "string",
    "description": "string",
    "teachers": ["test_user_1@gmail.com"]
}

ASSIGNMENT_MODEL = {
    "id": "1234567888",
    "classroom_id": "1237777333",
    "title": "Assignment name",
    "description": "description",
    "link": "https://link.com",
    "state": "PUBLISHED",
    "creation_time": "2023-02-16T10:32:25.059Z",
    "update_time": "2023-02-16T11:01:09.375Z",
    "due_date": "20xx-0x-1x",
    "due_time": "hh:mm:ss",
    "max_grade": 100,
    "work_type": "ASSIGNMENT",
    "assignee_mode": "ALL_STUDENTS"
}

SHORT_COURSEWORK_MODEL = {
    "courseId": "555555555",
    "id": "5789246",
    "title": "test assignment",
    "state": "PUBLISHED",
    "creationTime": "2023-02-16T10:45:49.833Z",
    "materials":[]
}

STUDENT = {
      "first_name": "steve4",
      "last_name": "jobs",
      "email": "clplmstestuser1@gmail.com",
      "user_type": "other",
      "user_groups": [],
      "status": "active",
      "is_registered":True,
      "failed_login_attempts_count": 0,
      "access_api_docs": False,
      "gaia_id": "F2GGRg5etyty",
      "user_id": "vtETClM9JdWBSUBB4ZEr",
      "created_time": "2023-01-24 17:38:32.689496+00:00",
      "last_modified_time": "2023-01-24 17:38:32.823430+00:00",
      "user_type_ref": "cnkybYRTLPobwyo52JBR",
      "invitation_id":"NTk2NTY1NzYyMjE5KjU5NzAwNTkxMjgzNFpa",
      "is_invitation_accepted":False}

INVITE_STUDENT = {"course_enrollment_id":"2xBnBjqm2X3eRgVxE6Bv",
            "student_email":"test_user@gmail",
            "section_id":"fake-section-id",
            "cohort_id":"fake-cohort-id",
            "classroom_id":"123453333",
            "classroom_url":"https://classroom.google.com/c/NTYzMhjhjrx",
            "invitation_id":"NTk2NTY1NzYyMjE5KjU5NzAwNTkwODM2NVpa",
            "user_id":"En4SSjm3ttfTT8Cq4nog"}
