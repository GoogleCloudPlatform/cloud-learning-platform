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
