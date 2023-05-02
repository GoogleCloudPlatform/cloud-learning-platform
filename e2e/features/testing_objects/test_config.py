from e2e.gke_api_tests.endpoint_proxy import get_baseurl
from common.utils.errors import ResourceNotFoundException
base_url = get_baseurl("lms")
auth_url = get_baseurl("authentication")

if not base_url:
  raise ResourceNotFoundException("Unable to locate the service URL for lms")
else:
  API_URL = f"{base_url}/lms/api/v1"
if not auth_url:
  raise ResourceNotFoundException(
      "Unable to locate the service URL for authentication")
else:
  API_URL_AUTHENTICATION_SERVICE = f"{auth_url}/authentication/api/v1"

e2e_google_form_id = "1oZrH6Wc1TSMSQDwO17Y_TCf38Xdpw55PYRRVMMS0fBM"
e2e_drive_folder_id = "1JZuikDnHvta7jJwnHSjWw5IcS7EK0QTG"