"""
  Script to create indexing in firestore for e2e environment
"""

import os
import json
import sys
from google.cloud import firestore_admin_v1

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
project_id = os.getenv("PROJECT_ID", "core-learning-services-dev")

client = firestore_admin_v1.FirestoreAdminClient()
# pylint: disable=broad-exception-caught

def create_index(index_data):
  """Create all the indexes"""
  collection_group = DATABASE_PREFIX + index_data.get("collection_group")
  project = (
      f"projects/{project_id}/databases/(default)/"
      f"collectionGroups/{collection_group}"
  )

  del index_data["collection_group"]
  request = firestore_admin_v1.CreateIndexRequest(
      parent=project, index=index_data)

  try:
    client.create_index(request=request)
    print(f"created index for {collection_group}")
  except Exception as e:
    print(f"Exception while creating index for {collection_group}", e)
    sys.exit(1)


if __name__ == "__main__":
  if not DATABASE_PREFIX:
    # raise Exception("DATABASE_PREFIX is not defined. Indexing skipped.")
    DATABASE_PREFIX = ""

  with open("index_rules.json", encoding="utf-8") as index_file:
    indexes = json.load(index_file)

  for index in indexes:
    create_index(index)
