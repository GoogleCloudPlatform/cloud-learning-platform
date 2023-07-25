"""
This file has the Bigquery setup related functions
"""
from config import PROJECT_ID, BQ_LRS_DATASET
from google.api_core.exceptions import (NotFound as GCP_Resource_NotFound,
                                        BadRequest as GCP_BadRequest)
from common.utils.bq_client import bq_client


def insert_data_to_bq(table_name, rows_to_insert):
  """Function to insert data into BigQuery Table"""
  try:
    table_id = f"{PROJECT_ID}.{BQ_LRS_DATASET}.{table_name}"
    client = bq_client()
    output_res = client.insert_rows_json(table_id, rows_to_insert)

    if output_res and isinstance(output_res, list):
      error_msgs = ", ".join("For row " + str(i.get("index")) + " -> " +
                             k.get("message")
                             for i in output_res
                             for k in i.get("errors"))
      message = f"Errors while inserting the data - {error_msgs}"
      raise ValueError(message)

  except (GCP_BadRequest, GCP_Resource_NotFound) as e:
    if isinstance(e.errors, list):
      error_msgs = ", ".join(i.get("message") for i in e.errors)
      message = f"Errors while inserting the data - {error_msgs}"
    else:
      message = e.errors
    raise ValueError(message) from e
  except Exception as e:
    raise e


def fetch_all_data_from_bq(table_name,
                           selected_fields=None,
                           skip=None,
                           limit=None):
  """Function to fetch all data from BigQuery Table"""
  try:
    table_id = f"{PROJECT_ID}.{BQ_LRS_DATASET}.{table_name}"
    client = bq_client()
    row_iterator = client.list_rows(
        table=table_id,
        selected_fields=selected_fields,
        start_index=skip,
        max_results=limit)
    results = [dict(row) for row in row_iterator]

    return results

  except (GCP_BadRequest, GCP_Resource_NotFound) as e:
    if isinstance(e.errors, list):
      error_msgs = ", ".join(i.get("message") for i in e.errors)
      message = f"Errors while getting the data: {error_msgs}"
    else:
      message = e.errors
    raise ValueError(message) from e

  except Exception as e:
    raise e


def fetch_data_using_query_from_bq(query_string):
  """Function to fetch data for given query from BigQuery Table"""
  try:
    client = bq_client()
    query_job = client.query(query_string)
    records = [dict(row) for row in query_job]

    return records

  except (GCP_BadRequest, GCP_Resource_NotFound) as e:
    if isinstance(e.errors, list):
      error_msgs = ", ".join(i.get("message") for i in e.errors)
      message = f"Errors while getting the data: {error_msgs}"
    else:
      message = e.errors
    raise ValueError(message) from e

  except Exception as e:
    raise e
