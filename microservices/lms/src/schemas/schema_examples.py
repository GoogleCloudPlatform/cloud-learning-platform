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
    "classroom_id": "clID",
    "classroom_code": "clcode",
    "classroom_url": "https://classroom.google.com"
}
UPDATE_COURSE_TEMPLATE_EXAMPLE = {
    "name": "name",
    "description": "description"
}

INSERT_COURSE_TEMPLATE_EXAMPLE = {
    "name": "name",
    "description": "description",
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
    "enrolled_students_count": 2
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
    "user_id": "kh5FoIBOx5qDsfh4ZRuv",
    "first_name": "first",
    "last_name": "last",
    "email": "clplmstestuser1@gmail.com",
    "user_type": "learner",
    "status": "active",
    "gaia_id": "1234577657333",
    "photo_url": "https://lh3.googleusercontent.com/a/AEd"
}
GET_STUDENT_EXAMPLE = TEMP_USER
GET_STUDENT_EXAMPLE["course_enrollment_id"] = "2xBnBjqm2X3eRgVxE6Bv"
GET_STUDENT_EXAMPLE["invitation_id"] = "2xBnBjqm2X3eRgVxE6Bv"
GET_STUDENT_EXAMPLE["student_email"] = "test_user@gmail"
GET_STUDENT_EXAMPLE["section_id"] = "fake-section-id"
GET_STUDENT_EXAMPLE["cohort_id"] = "fake-cohort-id"
GET_STUDENT_EXAMPLE["classroom_id"] = "123453333"
GET_STUDENT_EXAMPLE["enrollment_status"] = "active"
GET_STUDENT_EXAMPLE[
    "classroom_url"] = "https://classroom.google.com/c/NTYzMhjhjr"

COURSE_ENROLLMENT_USER_EXAMPLE = {
    "user_id": "kh5FoIBOx5qDsfh4ZRuv",
    "first_name": "",
    "last_name": "",
    "email": "clplmstestuser1@gmail.com",
    "user_type": "learner",
    "status": "active",
    "gaia_id": "1234577657333",
    "photo_url": "https://lh3.googleusercontent.com/a/AEd",
    "course_enrollment_id": "2xBnBjqm2X3eRgVxE6Bv",
    "invitation_id": "2xBnBjqm2X3eRgVxE6Bv",
    "section_id": "fake-section-id",
    "cohort_id": "fake-cohort-id",
    "classroom_id": "123453333",
    "enrollment_status": "active",
    "classroom_url": "https://classroom.google.com/c/NTYzMhjhjr"
}

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
    "materials": []
}

STUDENT = {
    "user_id": "12345678",
    "first_name": "steve4",
    "last_name": "jobs",
    "email": "clplmstestuser1@gmail.com",
    "user_type": "other",
    "status": "active",
    "gaia_id": "F2GGRg5etyty",
    "created_time": "2023-01-24 17:38:32.689496+00:00",
    "last_modified_time": "2023-01-24 17:38:32.823430+00:00",
    "invitation_id": "NTk2NTY1NzYyMjE5KjU5NzAwNTkxMjgzNFpa"
}

INVITE_STUDENT = {
    "course_enrollment_id": "2xBnBjqm2X3eRgVxE6Bv",
    "email": "test_user@gmail",
    "section_id": "fake-section-id",
    "cohort_id": "fake-cohort-id",
    "classroom_id": "123453333",
    "classroom_url": "https://classroom.google.com/c/NTYzMhjhjrx",
    "invitation_id": "NTk2NTY1NzYyMjE5KjU5NzAwNTkwODM2NVpa",
    "user_id": "En4SSjm3ttfTT8Cq4nog"
}

ANALYTICS_USER_EXAMPLE = {
    "user_gaia_id": "12345678",
    "user_name": {
        "givenName": "first_name",
        "familyName": "last_name",
        "fullName": "first_name last_name"
    },
    "user_email_address": "xyz@gmail.com",
    "user_photo_url": "//lh3.googleusercontent.com/a/default-user",
    "user_permissions": [{
        "permission": "CREATE_COURSE"
    }],
    "user_verified_teacher": True
}

ANALYTICS_COURSE_WORK_EXAMPLE = {
    "course_work_id":
    "596333555555",
    "course_work_title":
    "assignment 2",
    "course_work_description":
    "Created from ID account",
    "course_work_materials": [{
        "driveFile": {
            "object": "SharedDriveFile"
        },
        "youtubeVideo": {
            "object": "YouTubeVideo"
        },
        "link": {
            "object": "Link"
        },
        "form": {
            "object": "Form"
        }
    }],
    "course_work_state":
    "PUBLISHED",
    "course_work_alternate_link":
    "https://classroom.google.com/c/xyz/a/gh/details",
    "course_work_creation_time":
    "2023-03-02T17:50:24.127000+00:00",
    "course_work_update_time":
    "2023-03-02T17:50:23.406000+00:00",
    "course_work_due_date":
    "2023-03-15",
    "course_work_due_time":
    "18:29:00",
    "course_work_schedule_time":
    "2023-03-02T17:50:23.406000+00:00",
    "course_work_max_points":
    100,
    "course_work_work_type":
    "ASSIGNMENT",
    "course_work_associated_with_developer":
    True,
    "course_work_assignee_mode":
    "ALL_STUDENTS",
    "course_work_individual_students_options": {
        "studentIds": ["string"]
    },
    "course_work_submission_modification_mode":
    "MODIFIABLE_UNTIL_TURNED_IN",
    "course_work_creator_user_id":
    "12309876543",
    "course_work_topic_id":
    "09876544445678",
    "course_work_grade_category": {
        "id": "string",
        "name": "string",
        "weight": "integer",
        "defaultGradeDenominator": "integer"
    },
    "course_work_assignment": {
        "studentWorkFolder": {
            "id": "ctct3789021123bhh",
            "title": "string",
            "alternateLink": "string"
        }
    },
    "course_work_multiple_choice_question": {
        "choices": ["string"]
    },
    "submission_id":
    "Cg4Int098765xdfy5678",
    "submission_assigned_grade":
    10,
    "submission_creation_time":
    "2023-03-23T13:27:50.745000+00:00",
    "submission_update_time":
    "2023-03-23T13:27:50.657000+00:00",
    "submission_late":
    False
}

ANALYTICS_COURSE_EXAMPLE = {
    "course_id": "12345678",
    "course_name": "course_name",
    "course_section": "section a",
    "course_description": "section desc",
    "course_url": "https://classroom.google.com",
    "section_id": "1235678",
    "section_name": "section name",
    "cohort_id": "qwe1234dfg",
    "cohort_name": "cohort name",
    "cohort_description": "cohort desc",
    "cohort_registration_start_date": "2023-02-19T18:30:00+00:00",
    "cohort_registration_end_date": "2023-05-19T18:30:00+00:00",
    "cohort_start_date": "2023-02-19T18:30:00+00:00",
    "cohort_end_date": "2023-05-19T18:30:00+00:00",
    "cohort_max_students": 0,
    "course_work_list": [ANALYTICS_COURSE_WORK_EXAMPLE]
}

COURSE_EXAMPLE={
  "id": "456789",
  "name": "course_name",
  "section": "section",
  "description": "desc",
  "description_heading": "desc_heading",
  "room": "room",
  "owner_id": "1234567888887654",
  "creation_time": "2023-04-20T10:44:05.896Z",
  "update_time": "2023-04-20T10:44:05.896Z",
  "enrollment_code": "ry7ui2z",
  "course_state": "ACTIVE",
  "alternate_link": "https://classroom.google.com/c/xcvbn",
  "teacher_group_email": "course_name_section_teachers_678fg@google.com",
  "course_group_email": "course_name_section_hj678@google.com",
  "teacher_folder": {
    "id": "234567xdcfgyhu345678",
    "title": "course name section",
    "alternate_link":
      "https://drive.google.com/drive/folders/234567xdcfgyhu345678"
  },
  "course_material_sets":[{"drive_file":"ewrty"}],
  "guardians_enabled": False,
  "calendar_id": "dfghj56789@group.calendar.google.com",
  "gradebook_settings": {
    "calculation_type": "TOTAL_POINTS",
    "display_setting": "HIDE_OVERALL_GRADE"
  }
}
