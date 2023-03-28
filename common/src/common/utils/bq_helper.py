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

from google.cloud import bigquery
from common.utils.logging_handler import Logger
from common.config import PROJECT_ID,BQ_REGION

bq_client = bigquery.Client(location=BQ_REGION)

def insert_rows_to_bq(rows,dataset,table_name):
  """Insert rows to BQ

  Args:
    rows (list): _description_

  Returns:
    Bool: _description_
  """
  table = bq_client.get_table(f"{PROJECT_ID}.{dataset}.{table_name}")
  errors = bq_client.insert_rows(
    table=table, rows=rows)
  if not errors:
    Logger.info(f"New data pushed data {rows[0]} in {table_name}")
    return True
  Logger.info(f"Encountered errors while inserting rows: {errors}")
  return False


def run_query(query):
  """Function to run queries on BQ

  Args:
    query (string): _description_

  Returns:
    _type_: _description_
    """
  query_job = bq_client.query(query)
  results = query_job.result()
  return results

def get_client():
  """Function to return configured bq_client

  Returns:
    Client: bigquery client object
  """
  return bq_client
