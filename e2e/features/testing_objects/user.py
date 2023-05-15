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

from e2e.gke_api_tests.secrets_helper import get_user_email_and_password_for_e2e

email = get_user_email_and_password_for_e2e()["email"]
user_name = email.split("@")[0]

TEST_USER = {
    "first_name": user_name,
    "last_name": "lastname",
    "email": email,
    "status": "active",
    "user_type": "admin",
    "user_type_ref": "",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "gaia_id":"test1233",
    "photo_url":"tempurl"
}
