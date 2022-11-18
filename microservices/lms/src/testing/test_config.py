import datetime
BASE_URL = "http://localhost/lms/api/v1"

# TEST DATA
COURSE_TEMPLATE_LIST_TEST_DATA = [
    {
        "uuid": "",
        "name": "test-name_1",
        "description": "test-description_1",
        "admin": "test-admin_1@gmail.com",
        "instructional_designer": "IDesiner_1@gmail.com",
        "classroom_id": "fake-classroom_id_1",
        "classroom_code": "fake-classroom_code_1"
    },
    {
        "uuid": "",
        "name": "test-name_2",
        "description": "test-description_2",
        "admin": "test-admin_2@gmail.com",
        "instructional_designer": "IDesiner_2@gmail.com",
        "classroom_id": "fake-classroom_id_2",
        "classroom_code": "fake-classroom_code_2"
    },
    {
        "uuid": "",
        "name": "test-name_3",
        "description": "test-description_3",
        "admin": "test-admin@gmail.com_3",
        "instructional_designer": "IDesiner_3@gmail.com",
        "classroom_id": "fake-classroom_id_3",
        "classroom_code": "fake-classroom_code_3"
    }
]

COHORT_LIST_TEST_DATA = [
    {
        "name": "name-1",
        "description": "description-1",
        "start_date": datetime.datetime(year=2022,
                                        month=10, day=14),
        "end_date": datetime.datetime(year=2022,
                                      month=12, day=25),
        "registration_start_date": datetime.datetime(year=2022,
                                                     month=10, day=20),
        "registration_end_date": datetime.datetime(year=2022,
                                                   month=11, day=14),
        "max_student": 0,
        "enrolled_student_count": 0
    },
    {
        "name": "name-2",
        "description": "description-2",
        "start_date": datetime.datetime(year=2022,
                                        month=10, day=14),
        "end_date": datetime.datetime(year=2022,
                                      month=12, day=25),
        "registration_start_date": datetime.datetime(year=2022,
                                                     month=10, day=20),
        "registration_end_date": datetime.datetime(year=2022,
                                                   month=11, day=14),
        "max_student": 0,
        "enrolled_student_count": 0
    },
    {
        "uuid": "fake-cohort-id-3",
        "name": "name-3",
        "description": "description-3",
        "start_date": datetime.datetime(year=2022,
                                        month=10, day=14),
        "end_date": datetime.datetime(year=2022,
                                      month=12, day=25),
        "registration_start_date": datetime.datetime(year=2022,
                                                     month=10, day=20),
        "registration_end_date": datetime.datetime(year=2022,
                                                   month=11, day=14),
        "max_student": 0,
        "enrolled_student_count": 0
    }
]

INPUT_COHORT_TEST_DATA = {
    "name": "name",
    "description": "description",
    "start_date": "2022-10-14T00:00:00",
    "end_date": "2022-12-25T00:00:00",
    "registration_start_date": "2022-10-20T00:00:00",
    "registration_end_date": "2022-11-14T00:00:00",
    "max_student": 0
}
