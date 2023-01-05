"""
  Script to deleting indexing in firestore for e2e environment
"""
import json
import os
from google.cloud import firestore_admin_v1

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
PROJECT_ID = os.getenv("PROJECT_ID", None)


def delete_index(index_id):
  client = firestore_admin_v1.FirestoreAdminClient()
  request = firestore_admin_v1.DeleteIndexRequest(name=index_id)

  try:
    client.delete_index(request=request)
    print(f"deleted index {index_id}")
  except Exception as e:
    print("Exception", e)


def fetch_and_remove_indexes(collection):
  parent = "projects/{}/databases/(default)/collectionGroups/{}".format(
      PROJECT_ID, collection)

  client = firestore_admin_v1.FirestoreAdminClient()
  request = firestore_admin_v1.ListIndexesRequest(parent=parent)

  response = client.list_indexes(request=request)
  for res in response:
    for col_id in collection_groups:
      if col_id == res.name.split("/")[5]:
        print("res.name", res.name)
        delete_index(res.name)


if __name__ == "__main__":
  if not DATABASE_PREFIX:
    raise Exception(
        "DATABASE_PREFIX is not defined. Deleting indexes skipped.")

  print("DATABASE_PREFIX:", DATABASE_PREFIX)

  # collection_groups whose indexes needs to be deleted
  with open("indexe_rules.json", encoding="utf-8") as indexes_file:
    indexes = json.load(indexes_file)

  collection_groups = list(set([i["collection_group"] for i in indexes]))

  collection_groups = [DATABASE_PREFIX + i for i in collection_groups]

  for collection_group in collection_groups:
    fetch_and_remove_indexes(collection_group)
