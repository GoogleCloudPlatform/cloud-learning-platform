"""
  Script to deleting indexing in firestore for e2e environment
"""
import json
import os
from google.cloud import firestore_admin_v1

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
PROJECT_ID = os.getenv("PROJECT_ID", None)
# pylint: disable = broad-exception-raised, broad-except

def delete_index(client, index_id, tokens):
  try:
    request = firestore_admin_v1.DeleteIndexRequest(name=index_id)
    client.delete_index(request=request)
    index_name = "/".join(tokens[5:8])
    print(f"Deleting {index_name}")
  except Exception as e:
    print("Exception", e)

def fetch_and_remove_indexes(col_group):
  """Fetch and remove indexes"""
  parent = (f"projects/{PROJECT_ID}/databases/(default)/"
            f"collectionGroups/{col_group}")

  client = firestore_admin_v1.FirestoreAdminClient()
  request = firestore_admin_v1.ListIndexesRequest(parent=parent)

  response = client.list_indexes(request=request)
  num_indexes = 0
  for res in response:
    tokens = res.name.split("/")
    if col_group == tokens[5]:
      num_indexes += 1
      delete_index(client, res.name, tokens)
  return num_indexes

if __name__ == "__main__":
  print("PROJECT_ID = ", PROJECT_ID)
  if not PROJECT_ID:
    raise Exception("PROJECT_ID is not defined. Deleting indexes skipped.")

  print("DATABASE_PREFIX = ", DATABASE_PREFIX)
  if not DATABASE_PREFIX:
    raise Exception(
        "DATABASE_PREFIX is not defined. Deleting indexes skipped.")

  indexes = []
  # collection_groups whose indexes needs to be deleted
  with open("index_rules.json", encoding="utf-8") as indexes_file:
    service_index_mapping = json.load(indexes_file)
    for _, index_list in service_index_mapping.items():
      indexes.extend(index_list)

  collection_groups = {DATABASE_PREFIX + i["collection_group"] for i in indexes}

  total = 0
  for collection_group in collection_groups:
    print(f"CollectionGroup = {collection_group}")
    total += fetch_and_remove_indexes(collection_group)
  print(f"Deleted a total of {total} indexes")
