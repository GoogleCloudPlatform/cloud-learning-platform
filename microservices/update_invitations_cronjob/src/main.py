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
"""Enable Notifications API Nightly CronJob

    Continuously hits the /enable_notifications API nightly to keep
    the 7 day TTL for Class Notifications running

    https://developers.google.com/classroom/best-practices/push-notifications#overview

"""

import os
import sys
import requests
import traceback
from common.utils.token_handler import UserCredentials
from common.utils.logging_handler import Logger
from common.utils.errors import CronJobException
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

def get_sections(id_token, limit, skip):
  """Get list of sections from LMS API

  Args:
      id_token : id_token to use

  Raises:
      CronJobException: If any issue hitting the internal APIs

  Returns:
      list(section): list of section API JSON output
  """
  api_endpoint = "http://lms/lms/api/v1/sections?" +\
      f"skip={skip}&limit={limit}"

  res = requests.get(url=api_endpoint,
                     headers={
                         "Content-Type": "application/json",
                         "Authorization": f"Bearer {id_token}"
                     },
                     timeout=60)
  res.raise_for_status()

  res_json = res.json()
  if res_json["success"]:
    return res_json["data"]

  raise CronJobException(
      f"Could not get sections with error: {res_json['message']}")


def main():
  Logger.info("Update Invites cronjob started")

  auth_client = UserCredentials(LMS_BACKEND_ROBOT_USERNAME,
                                LMS_BACKEND_ROBOT_PASSWORD)
  id_token = auth_client.get_id_token()
  cronjob_status = True
  skip = 0
  page_size = 20
  skip_increment = 20
  total_num_sections = 0
  update_invites_failed_sections=[]
  while True:
    sections = get_sections(id_token, limit=page_size, skip=skip)
    if not sections:
      break

    for section in sections:
      total_num_sections = total_num_sections+1
      section_id=section["id"]
      api_endpoint = f"http://lms/lms/api/v1/sections/{section_id}/update_invites"
      res = requests.patch(
      url=api_endpoint,
      headers={
          "Content-Type": "application/json",
          "Authorization": f"Bearer {id_token}"
      })

      if res.status_code == 200:
        Logger.info(f"Update invite response for section_id {section_id} {res.status_code}")
      else:
        cronjob_status=False
        update_invites_failed_sections.append(section_id)
        response = res.json()
        Logger.error(
          f"Update Invites status API failed with\
            status code for section {section_id} {res.status_code} {response}"
          )
        err = traceback.format_exc().replace("\n", " ")
        Logger.error(err)

    if len(sections) < page_size:
      break
    skip += skip_increment

  if not cronjob_status:
    Logger.error(f"Update_invites cronjob failed for sections {update_invites_failed_sections}")
  Logger.info(f"Update invites cronjob completed with status {cronjob_status}")
  Logger.info(f"Numeber of sections scanned {total_num_sections}")
  return cronjob_status

if __name__ == "__main__":
  success = main()
  if not success:
    sys.exit(1)
