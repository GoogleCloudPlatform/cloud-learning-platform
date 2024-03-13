"""
  Script to create indexing in firestore for e2e environment
"""

import os
import json
import sys
from google.cloud import firestore_admin_v1

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.getenv("PROJECT_ID", "gcp-classroom-dev")

client = firestore_admin_v1.FirestoreAdminClient()
# pylint: disable=broad-exception-caught

def create_index(index_data):
  """Create all the indexes"""
  collection_group = DATABASE_PREFIX + index_data.get("collection_group")
  project = (f"projects/{PROJECT_ID}/databases/(default)/"
      f"collectionGroups/{collection_group}")
  del index_data["collection_group"]
  request = firestore_admin_v1.CreateIndexRequest(
      parent=project, index=index_data)

  try:
    client.create_index(request=request)
    print(f"created index for {collection_group}")
    return 1
  except Exception as e:
    print(f"Exception while creating index for {collection_group}", e)
    if type(e).__name__ != "AlreadyExists":
      sys.exit(1)

if __name__ == "__main__":
  if not DATABASE_PREFIX:
    # raise Exception("DATABASE_PREFIX is not defined. Indexing skipped.")
    DATABASE_PREFIX = ""

  indexes = []
  with open("index_rules.json", encoding="utf-8") as index_file:
    service_index_mapping = json.load(index_file)
    for service_name, index_list in service_index_mapping.items():
      indexes.extend(index_list)

  total = 0
  for index in indexes:
    total += create_index(index)

  print(f"Created a total of {total} indexes")
