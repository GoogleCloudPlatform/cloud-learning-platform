import os
import uuid
from e2e.gke_api_tests.secrets_helper import get_required_emails_from_secret_manager

DATABASE_PREFIX = os.environ.get("DATABASE_PREFIX")
emails = get_required_emails_from_secret_manager()

COURSE_TEMPLATE_INPUT_DATA = {
    "name": DATABASE_PREFIX+"test_course"+str(uuid.uuid4),
    "description": "Study Hall Test Course for Development purpose",
    "topic": "e2e test",
    "admin": emails["admin"],
    "instructional_designer": emails["instructional_designer"]
}

