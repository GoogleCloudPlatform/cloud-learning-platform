import os
from e2e.gke_api_tests.endpoint_proxy import get_baseurl
from common.utils.errors import ResourceNotFoundException
base_url=get_baseurl("lms")
base_url = get_baseurl("lms")
if not base_url:
    raise ResourceNotFoundException(
        "Unable to locate the service URL for lms")
else:
    API_URL = f"{base_url}/lms/api/v1"

