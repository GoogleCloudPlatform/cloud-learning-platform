import os
import uuid
DATABASE_PREFIX = os.environ.get("DATABASE_PREFIX")
COHORT_INPUT_DATA = {
    "name": DATABASE_PREFIX+"test_cohort"+str(uuid.uuid4),
    "description": "Study Hall Test Cohort for Development purpose",
    "start_date": "2022-10-14T00:00:00",
    "end_date": "2022-12-25T00:00:00",
    "registration_start_date": "2022-10-20T00:00:00",
    "registration_end_date": "2022-11-14T00:00:00",
    "max_students": 5000
}
