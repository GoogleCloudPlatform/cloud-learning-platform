""" Schema examples and test objects for unit test """
import datetime

USER_EXAMPLE = {
    "uuid": "fake-user-id",
    "auth_id": "fake-user-id",
    "email": "user@gmail.com",
    "role": "Admin"
}

COURSE_TEMPLATE_EXAMPLE = {
    "uuid": "id",
    "name": "name",
    "description": "description",
    "admin": "admin",
    "instructional_designer": "IDesiner",
    "classroom_id": "clID",
    "classroom_code": "clcode"
}

INSERT_COURSE_TEMPLATE_EXAMPLE = {
    "name": "name",
    "description": "description",
    "admin": "admin@gmail.com",
    "instructional_designer": "IDesiner@gmail.com"
}

COHORT_EXAMPLE = {
    "uuid": "fake-cohort-id",
    "name": "name",
    "description": "description",
    "start_date": datetime.datetime(year=2022,
                                    month=10, day=14),
    "end_date": datetime.datetime(year=2022,
                                  month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022,
                                                 month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022,
                                               month=11, day=14),
    "max_students": 0,
    "enrolled_students_count": 0,
    "course_template": "course_template/fake-uuid"
}
INSERT_COHORT_EXAMPLE = {
    "name": "name",
    "description": "description",
    "start_date": datetime.datetime(year=2022,
                                    month=10, day=14),
    "end_date": datetime.datetime(year=2022,
                                  month=12, day=25),
    "registration_start_date": datetime.datetime(year=2022,
                                                 month=10, day=20),
    "registration_end_date": datetime.datetime(year=2022,
                                               month=11, day=14),
    "max_students": 0,
    "course_template": "fake-uuid"
}
