"""Example Data for testing"""
TEST_USER= {
        "uuid":"fake-user-id",
        "auth_id" : "fake-user-auth-id",
        "email" : "user@gmail.com",
        "role" : "Admin"
      }

TEST_COURSE={
            "uuid":"fake-course-id",
            "name" : "name",
            "description" : "description",
            "topic" :"topic",
            "admin" : "admin",
            "instructional_designer": "IDesiner",
            "classroom_id":"clID",
            "classroom_code":"clcode"
        }
TEST_COHORT={
            "uuid":"fake-cohort-id",
            "name": "name",
            "description": "description",
            "start_date": "2022-05-05",
            "end_date": "2022-04-04",
            "max_student": 0,
            "course_template":TEST_COURSE
        }
TEST_SECTION={
            "uuid":"fake-section-id",
            "name" : "section_name",
            "section" : "section c",
            "description": "description",
            "classroom_id" :"cl_id",
            "classroom_code" :"cl_code",
            "cohort":TEST_COHORT,
            "course_template":TEST_COURSE,
            "teachers_list":["teachera@gmail.com","teacherb@gmail.com"]
        }
