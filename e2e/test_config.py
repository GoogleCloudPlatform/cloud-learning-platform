from e2e.gke_api_tests.endpoint_proxy import get_baseurl
from common.utils.errors import ResourceNotFoundException
base_url = get_baseurl("lms")
auth_url = get_baseurl("authentication")
user_management_url = get_baseurl("user-management")
lrs_url = get_baseurl("learning-record-service")
los_url = get_baseurl("learning-object-service")
slp_url = get_baseurl("student-learner-profile")

if not base_url:
  raise ResourceNotFoundException("Unable to locate the service URL for lms")
else:
  API_URL = f"{base_url}/lms/api/v1"

if not auth_url:
  raise ResourceNotFoundException(
      "Unable to locate the service URL for authentication")
else:
  API_URL_AUTHENTICATION_SERVICE = f"{auth_url}/authentication/api/v1"

if not user_management_url:
  raise ResourceNotFoundException(
      "Unable to locate the service URL for user management")
else:
  API_URL_USER_MANAGEMENT = f"{user_management_url}/user-management/api/v1"

if not lrs_url:
  raise ResourceNotFoundException(
      "Unable to locate the service URL for user management")
else:
  API_URL_LEARNING_RECORD_SERVICE = f"{lrs_url}/learning-record-service/api/v1"


if not los_url:
  raise ResourceNotFoundException(
      "Unable to locate the service URL for user management")
else:
  API_URL_LEARNING_OBJECT_SERVICE = f"{los_url}/learning-object-service/api/v1"

if not slp_url:
  raise ResourceNotFoundException(
      "Unable to locate the service URL for user management")
else:
  API_URL_LEARNER_PROFILE_SERVICE = f"{slp_url}/learner-profile-service/api/v1"


e2e_google_form_id = "1oZrH6Wc1TSMSQDwO17Y_TCf38Xdpw55PYRRVMMS0fBM"
e2e_drive_folder_id = "1JZuikDnHvta7jJwnHSjWw5IcS7EK0QTG"


DEL_KEYS = [
  "is_archived", "is_deleted", "version", "uuid", "parent_version_uuid",
  "root_version_uuid", "progress", "status", "created_time",
  "last_modified_time", "earned_achievements", "child_nodes_count",
  "completed_child_nodes_count", "created_by", "last_modified_by",
  "archived_by", "deleted_by", "archived_at_timestamp", "deleted_at_timestamp"
]
