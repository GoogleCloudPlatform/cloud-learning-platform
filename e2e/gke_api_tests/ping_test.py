# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
from e2e.gke_api_tests.endpoint_proxy import get_baseurl
from common.utils.errors import ResourceNotFoundException

def test_api_ping():
  base_url = get_baseurl("lms")
  if not base_url:
    raise ResourceNotFoundException("Unable to locate the service URL for lms")
  res = requests.get(base_url + "/ping")
  assert res.status_code == 200


def test_hello_world():
  base_url = get_baseurl("lms")
  if not base_url:
    raise ResourceNotFoundException("Unable to locate the service URL for lms")
  res = requests.get(base_url + "/")
  assert res.text == "\"Hello World.\""
