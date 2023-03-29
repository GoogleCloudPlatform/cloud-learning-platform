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

"""
Bigquery helper Service
"""

from google.cloud.exceptions import NotFound
from common.utils.logging_handler import Logger
from common.utils.bq_helper import get_client
from config import BQ_TABLE_DICT,PROJECT_ID,BQ_DATASET


def check_bq_tables():
  try:
    for table in BQ_TABLE_DICT.values():
      get_client().get_table(f"{PROJECT_ID}.{BQ_DATASET}.{table}")
    return True
  except NotFound as ne:
    Logger.info(str(ne))
    Logger.info(f"BQ Table {PROJECT_ID}.{BQ_DATASET}.{table} not found")
    return False
