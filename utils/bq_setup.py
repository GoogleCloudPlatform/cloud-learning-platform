"""
Bigquery setup related functions
"""
import os
import argparse
from os import listdir
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

GCP_PROJECT = os.getenv("PROJECT_ID", None)

BQ_DATASET = DATABASE_PREFIX + os.getenv("BQ_DATASET", "cns")

bq_client = bigquery.Client()
# Print statements are being used in this file to debug in the Github actions


def create_bigquery_dataset(dataset):
  """Delete a dataset from the bigquery"""
  dataset_id = f"{GCP_PROJECT}.{dataset}"
  print("Dataset_id", dataset_id)
  dataset = bigquery.Dataset(dataset_id)
  try:
    bq_client.create_dataset(dataset, timeout=30)
    print(f"{dataset} dataset created")
  except Exception as e:  # pylint: disable = broad-except
    print("Error raised", e)


def create_table_using_sql_file(dataset, file_name):
  """Create a table using the query from the given file in the BQ dataset"""
  dataset_id = f"{GCP_PROJECT}.{dataset}"
  print("Dataset_id", dataset_id)
  job_config = bigquery.QueryJobConfig(default_dataset=dataset_id)
  with open(file_name, "r", encoding="utf-8") as file:
    query = file.read()
  query_job = bq_client.query(
      query, project=GCP_PROJECT, job_config=job_config)
  error = ""
  try:
    query_job.result()
    print("Completed for the file: ", file_name)
  except BadRequest as e:
    for e in query_job.errors:
      error = f"ERROR: {e['message']}"
      raise Exception(error) from e


def create_tables(dataset):
  """Create tables in the bigquery"""
  print("dataset", dataset)
  sql_file_list = []

  file_path = "sql/"
  sql_files = listdir(file_path)
  sql_file_list = [file_path + i for i in sql_files]

  for each_file in sql_file_list:
    print(f"Running ddl_file: {each_file}")
    create_table_using_sql_file(dataset, each_file)


def parse_arguments():
  """Parse the given arguments"""
  parser = argparse.ArgumentParser()

  parser.add_argument(
      "--create-dataset",
      dest="create_dataset",
      type=str,
      default="false",
      choices=["true", "false"],
      help="Create dataset for cns? true or false")

  parser.add_argument(
      "--create-tables",
      dest="create_tables",
      type=str,
      default="false",
      choices=["true", "false"],
      help="Create table for logs in cns dataset? true or false")
  return parser.parse_args()


if __name__ == "__main__":
  # To run locally, appropriate BQ permissions should be there and
  # be logged in to the respective GCP project using google sdk

  # Set the following environment variables
  # BQ_DATASET -<dataset-name> (default -> cns), GCP_PROJECT -<project_id>
  # Run the following command with the required arguments to trigger the script
  # cd utils
  # PYTHONPATH=../common/src python3 bq_setup.py

  args = parse_arguments()

  if not GCP_PROJECT:
    raise Exception("Please set 'GCP_PROJECT' environment variable")

  if args.create_dataset == "true":
    create_bigquery_dataset(BQ_DATASET)
  if args.create_tables == "true":
    create_tables(BQ_DATASET)