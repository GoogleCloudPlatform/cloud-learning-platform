"""
  Script to create indexing in firestore for dev environment
"""

import os
import json
import sys
from google.cloud import firestore_admin_v1

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.getenv("PROJECT_ID", None)

client = firestore_admin_v1.FirestoreAdminClient()
# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except

def create_index(index_data):
  """Create index in the firestore"""
  collection_group = DATABASE_PREFIX + index_data.get("collection_group")
  project = (f"projects/{PROJECT_ID}/databases/(default)/"
      f"collectionGroups/{collection_group}")
  del index_data["collection_group"]
  request = firestore_admin_v1.CreateIndexRequest(
      parent=project, index=index_data)

  try:
    client.create_index(request=request)
    print(f"created index for {collection_group}")
  except Exception as e:
    print(f"Exception while creating index for {collection_group}", e)
    if type(e).__name__ != "AlreadyExists":
      sys.exit(1)

def process_indexes_file(index_file_name):
  indexes = []

  with open(index_file_name, encoding="utf-8") as indexes_file:
    service_index_mapping = json.load(indexes_file)
    for _, index_list in service_index_mapping.items():
      indexes.extend(index_list)

  for index in indexes:
    create_index(index)

if __name__ == "__main__":
  if PROJECT_ID is None:
    raise Exception("PROJECT_ID is not defined. Indexing skipped.")

  index_files = [
        "index_rules.json", "v3_filter_api_indexes.json"
  ]
  for file_name in index_files:
    process_indexes_file(file_name)
