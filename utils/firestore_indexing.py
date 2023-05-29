"""
  Script to create indexing in firestore for dev environment
"""

import os
import json
from google.cloud import firestore_admin_v1

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
PROJECT_ID = os.getenv("PROJECT_ID", None)

client = firestore_admin_v1.FirestoreAdminClient()
# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except

def create_index(index_data):
  """Create index in the firestore"""
  collection_group = DATABASE_PREFIX + index_data.get("collection_group")
  project = (f"projects/{PROJECT_ID}/databases/"
             +f"(default)/collectionGroups/{collection_group}")
  del index_data["collection_group"]
  request = firestore_admin_v1.CreateIndexRequest(parent=project,
                                                  index=index_data)

  try:
    client.create_index(request=request)
    print(f"created index for {collection_group}")
  except Exception as e:
    print(f"Exception while creating index for {collection_group}", e)


if __name__ == "__main__":
  if PROJECT_ID is None:
    raise Exception("PROJECT_ID is not defined. Indexing skipped.")

  indexes = []

  with open("indexe_rules.json", encoding="utf-8") as indexs_file:
    indexes.extend(json.load(indexs_file))

  with open("v3_filter_api_indexes.json", encoding="utf-8") as indexs_file:
    indexes.extend(json.load(indexs_file))

  for index in indexes:
    create_index(index)
