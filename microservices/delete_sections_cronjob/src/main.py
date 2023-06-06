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
"""Delete section Cronjob 

    Runs once a day to delete the sections which are failed in 
    section creation process

    https://developers.google.com/classroom/best-practices/push-notifications#overview

"""

import os
import sys
import requests
import traceback
from common.utils.token_handler import UserCredentials
from common.utils.logging_handler import Logger
from google.cloud import secretmanager
# pylint: disable=line-too-long,broad-except,missing-timeout

secrets = secretmanager.SecretManagerServiceClient()
PROJECT_ID = os.environ.get("PROJECT_ID", "")

try:
  LMS_BACKEND_ROBOT_USERNAME = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lms-backend-robot-username/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  Logger.error("Failed to fetch robot username")
  LMS_BACKEND_ROBOT_USERNAME = None

try:
  LMS_BACKEND_ROBOT_PASSWORD = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lms-backend-robot-password/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  Logger.error("Failed to fetch robot password")
  LMS_BACKEND_ROBOT_PASSWORD = None


def main():
  Logger.info("Delete section cronjob started")

  auth_client = UserCredentials(LMS_BACKEND_ROBOT_USERNAME,
                                LMS_BACKEND_ROBOT_PASSWORD)
  id_token = auth_client.get_id_token()
  api_endpoint = "http://lms/lms/api/v1/sections/cronjob/delete_failed_to_provision_section"

  res = requests.delete(
      url=api_endpoint,
      headers={
          "Content-Type": "application/json",
          "Authorization": f"Bearer {id_token}"
      })
  count = res.json()["data"]
  Logger.info(f"Response of delete api {res.status_code} deleted section count is {count}")
  if res.status_code != 200:
    Logger.error(
        f"Delete section API failed with status code {res.status_code}")
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    return False
  Logger.info("Delete FAILED TO PROVIOSION section cronjob finished")
  return True


if __name__ == "__main__":
  success = main()
  if not success:
    sys.exit(1)
