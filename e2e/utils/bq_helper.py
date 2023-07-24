"""_summary_
"""
import os
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
# disabling for linting to pass
# pylint: disable = broad-exception-raised

GCP_PROJECT = os.getenv("PROJECT_ID", None)

BQ_REGION = os.getenv("BQ_REGION", "US")

bq_client = bigquery.Client(location=BQ_REGION)
# Print statements are being used in this file to debug in the Github actions


DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
BQ_DATASET = DATABASE_PREFIX +  "lms_analytics"
BQ_TABLE_DICT = {
    "BQ_COLL_SECTION_TABLE": "section",
    "BQ_COLL_COHORT_TABLE": "cohort",
    "BQ_COLL_COURSETEMPLATE_TABLE": "courseTemplate",
    "BQ_ANALYTICS_VIEW":"gradeBookEnrichedView",
    "BQ_ENROLLMENT_RECORD" : "sectionEnrollmentRecord",
    "EXISTS_IN_CLASSROOM_NOT_IN_DB_VIEW":"roastersExitsInClassroomNotInDB",
    "EXISTS_IN_DB_NOT_IN_CLASSROOM_VIEW":"roastersExitsInDBNotInClassroom"
}

def create_bigquery_dataset():
  """Create a dataset in the bigquery"""
  dataset_id = f"{GCP_PROJECT}.{BQ_DATASET}"
  print("Dataset_id", dataset_id)
  dataset = bigquery.Dataset(dataset_id)
  try:
    bq_client.create_dataset(dataset, timeout=30)
    print(f"{dataset} dataset created")
  except Exception as e:  # pylint: disable = broad-except
    print("Error raised", e)


def create_table_using_sql(query,table_name):
  """Create a table using the query from the given file in the BQ dataset"""
  dataset_id = f"{GCP_PROJECT}.{BQ_DATASET}"
  job_config = bigquery.QueryJobConfig(default_dataset=dataset_id)
  query_job = bq_client.query(query,
                              project=GCP_PROJECT,
                              job_config=job_config)
  error = ""
  try:
    query_job.result()
    print("Completed for the table: ", table_name)
  except BadRequest as e:
    for e in query_job.errors:
      error = f"ERROR: {e['message']}"
      raise Exception(error) from e
