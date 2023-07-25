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

""" build script for query engines """

#pylint: disable=wrong-import-position

import logging
import sys
sys.path.append("microservices/llm_service/src")
sys.path.append("common/src")
from services.query_service import query_engine_build

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

if __name__ == "__main__":
  args = sys.argv[1:]

  doc_url = args[0]
  query_engine = args[1]
  user_id = args[2]

  print(f"*** building query index for {doc_url}," \
        " query_engine {query_engine}, for user id {user_id}")

  params = {}
  query_engine_build(doc_url, query_engine, user_id)
  