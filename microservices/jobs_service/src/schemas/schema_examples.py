# Copyright 2023 Google LLC
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

""" Schema examples and test objects for unit tests """
# pylint: disable = line-too-long


USER_EXAMPLE = {
    "id": "fake-user-id",
    "first_name": "Test",
    "last_name": "Tester",
    "user_id": "fake-user-id",
    "auth_id": "fake-user-id",
    "email": "user@gmail.com",
    "role": "Admin",
    "user_type": "learner",
    "status": "active"
}

BATCHJOB_EXAMPLE = {
    "id": "fake-job-id",
    "type": "query_engine_build",
    "name": "fake-job-id",
    "input_data": "{\"fake-key\":\"fake-value\"}",
    "status": "active",
    "message": "test message",
    "generated_item_id": "asdf1234",
    "output_gcs_path": "gs://test-path",
    "errors": {},
    "job_logs": {},
    "metadata": {},
    "result_data": {
      "docs_processed": ["a", "b", "c"],
      "docs_not_processed": ["a", "b", "c"]
    },
    "uuid": "fake-job-id"
}
