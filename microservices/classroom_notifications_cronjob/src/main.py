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
from common.utils.token_handler import UserCredentials
from common.utils.logging_handler import Logger as logger
from common.utils.errors import CronJobException
from google.cloud import secretmanager
# pylint: disable=line-too-long,broad-except

secrets = secretmanager.SecretManagerServiceClient()
PROJECT_ID = os.environ.get("PROJECT_ID", "")

try:
  LMS_BACKEND_ROBOT_USERNAME = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lms-backend-robot-username/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  logger.error("Failed to fetch robot username")
  LMS_BACKEND_ROBOT_USERNAME = None

try:
  LMS_BACKEND_ROBOT_PASSWORD = secrets.access_secret_version(
      request={
          "name":
              f"projects/{PROJECT_ID}/secrets/lms-backend-robot-password/versions/latest"
      }).payload.data.decode("utf-8")
except Exception as e:
  logger.error("Failed to fetch robot password")
  LMS_BACKEND_ROBOT_PASSWORD = None


def enable_notifications(section_id, id_token):
  """Enable notifications for a given section

  Args:
      section : LMS Section API response object
      id_token : id_token to use

  Raises:
      CronJobException: If any issue hitting the internal APIs
  """
  api_endpoint = "http://lms/lms/api/v1/sections"+\
    f"/{section_id}/enable_notifications"

  res = requests.post(
      url=api_endpoint,
      headers={
          "Content-Type": "application/json",
          "Authorization": f"Bearer {id_token}"
      },
      timeout=60)
  res.raise_for_status()

  res_json = res.json()
  if res_json["success"]:
    logger.info(res_json)
  else:
    raise CronJobException("Could not enable Classroom notifications" +
                           f"with error: {res_json['message']}")


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

  res = requests.get(
      url=api_endpoint,
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
  logger.info(
      "Classroom Pubsub Registration / Notifications API Cronjob STARTING")

  auth_client = UserCredentials(LMS_BACKEND_ROBOT_USERNAME,
                                LMS_BACKEND_ROBOT_PASSWORD)
  id_token = auth_client.get_id_token()
  skip = 0
  page_size = 20
  num_enabled = 0
  num_sections = 0
  skip_increment = 20
  while True:
    # get list of sections according to skip & limit value
    sections = get_sections(id_token, limit=page_size, skip=skip)
    if not sections:
      break

    num_sections += len(sections)
    # enable notification for each section
    for section in sections:
      # added try except so that if any section enable notification
      # get failed it will get continue
      try:
        enable_notifications(section["id"], id_token)
        num_enabled += 1
      except requests.HTTPError as rte:
        logger.info(str(rte))
    if len(sections) < page_size:
      break
    skip += skip_increment
  if num_enabled < num_sections:
    logger.error(f"Cron Job failed only {num_enabled}" +
                 " these number of sections get enabled out of " +
                 f"{num_sections} sections")
    sys.exit(1)

  logger.info("Cron Job Successfully enabled notifications for " +
              f"{num_enabled} out of {num_sections} number of sections")
  logger.info(
      "Classroom Pubsub Registration / Notifications API Cronjob FINISHED")


if __name__ == "__main__":
  main()
