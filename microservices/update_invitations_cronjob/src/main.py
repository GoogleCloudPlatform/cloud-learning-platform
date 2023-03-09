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
import sys
import traceback
from common.utils.secrets import get_backend_robot_id_token
from common.utils.logging_handler import Logger


def main():
  Logger.info(
      "Update Invites cronjob started")

  id_token = get_backend_robot_id_token()
  api_endpoint = "http://lms/lms/api/v1/sections/update_invites"

  res = requests.patch(url=api_endpoint,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {id_token}"
                        })
  Logger.info(f"Response of patch api {res.status_code}")
  if res.status_code!=200:
    Logger.error(f"Update Invites status API failed with status code {res.status_code}")
    err = traceback.format_exc().replace("\n", " ")
    Logger.error(err)
    return False
  Logger.info(
      "Update invites cronjob finished")
  return True



if __name__ == "__main__":
  success = main()
  if not success:
    sys.exit(1)