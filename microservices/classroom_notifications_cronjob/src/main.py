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

ID_TOKEN = "<INSERT_ID_TOKEN>"


def enable_notifications(section):
  api_endpoint = "https://core-learning-services-dev.cloudpssolutions.com/lms/api/v1/sections/enable_notifications"

  for feed_type in ["COURSE_WORK_CHANGES", "COURSE_ROSTER_CHANGES"]:
    res = requests.post(url=api_endpoint,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {ID_TOKEN}"
                        },
                        json={
                            "feed_type": feed_type,
                            "section_id": section["id"]
                        },
                        timeout=60)
    print(res.text)


def get_sections():
  print("cronjob starting")
  api_endpoint = "https://core-learning-services-dev.cloudpssolutions.com/lms/api/v1/sections"
  res = requests.get(url=api_endpoint,
                     headers={
                         "Content-Type": "application/json",
                         "Authorization": f"Bearer {ID_TOKEN}"
                     },
                     timeout=60)
  res = res.json()

  if res["success"]:
    return res["data"]

  return False


def main():
  sections = get_sections()
  for section in sections:
    enable_notifications(section)


if __name__ == "__main__":
  main()
