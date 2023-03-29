"""
Bigquery dataset cleanup related functions
"""
import os
from google.cloud import bigquery

# disabling for linting to pass
# pylint: disable = broad-exception-raised

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")

GCP_PROJECT = os.getenv("PROJECT_ID", None)

BQ_REGION= os.getenv("BQ_REGION", "US")

BQ_DATASET = DATABASE_PREFIX + os.getenv("BQ_DATASET", "lms_analytics")
# Print statements are being used in this file to debug in the Github actions

bq_client = bigquery.Client(location=BQ_REGION)

def delete_bigquery_dataset(dataset):
  dataset_id = f"{GCP_PROJECT}.{dataset}"
  print("Deleting BQ dataset: " + dataset_id)
  bq_client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)


if __name__ == "__main__":
  # To run locally comment out the if condition
  # appropriate BQ permissions should be there and
  # be logged in to the respective GCP project using google sdk

  # Set the environment variables BQ_LRS_DATASET, GCP_PROJECT
  # Run the following commands
  # cd utils
  # PYTHONPATH=../common/src python3 bq_cleanup.py

  if not GCP_PROJECT:
    raise Exception("Please set 'GCP_PROJECT' environment variable")

  if not DATABASE_PREFIX:
    raise Exception(
        "DATABASE_PREFIX is not defined. Database cleanup skipped.")

  delete_bigquery_dataset(BQ_DATASET)
