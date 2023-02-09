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

    Continusouly hits the /enable_notifications API nightly to keep
    the 7 day TTL for Class Notifications running

    https://developers.google.com/classroom/best-practices/push-notifications#overview

"""

import requests
from common.utils.secrets import get_backend_robot_id_token

from common.utils.logging_handler import Logger as logger
from common.utils.errors import CronJobException


def enable_notifications(section, id_token):
  """Enable notifications for a given section

  Args:
      section : LMS Section API response object
      id_token : id_token to use

  Raises:
      CronJobException: If any issue hitting the internal APIs
  """
  api_endpoint = "http://lms/lms/api/v1/sections/enable_notifications"

  for feed_type in ["COURSE_WORK_CHANGES", "COURSE_ROSTER_CHANGES"]:
    res = requests.post(url=api_endpoint,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {id_token}"
                        },
                        json={
                            "feed_type": feed_type,
                            "section_id": section["id"]
                        },
                        timeout=60)
    res.raise_for_status()

    res_json = res.json()
    if res_json["success"]:
      logger.info(res_json)
      continue

    raise CronJobException("Could not enable Classroom notifications" +
                           f"with error: {res_json['message']}")


def get_sections(id_token):
  """Get list of sections from LMS API

  Args:
      id_token : id_token to use

  Raises:
      CronJobException: If any issue hitting the internal APIs

  Returns:
      list(section): list of section API JSON output
  """
  api_endpoint = "http://lms/lms/api/v1/sections"

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
  logger.info(
      "Classroom Pubsub Registration / Notifications API Cronjob STARTING")

  id_token = get_backend_robot_id_token()

  sections = get_sections(id_token)
  for section in sections:
    enable_notifications(section, id_token)

  logger.info(
      "Classroom Pubsub Registration / Notifications API Cronjob FINISHED")


if __name__ == "__main__":
  main()
