"""Utility methods for handling activites"""
from services.firestore_service import get_documents

COLLECTION_NAME = "activities"


def get_activity_list():
  """Method to fetch activities"""
  doc_list = list(get_documents(COLLECTION_NAME))
  if len(doc_list) > 0:
    activity_list = list(map(lambda x: x.to_dict(), doc_list))
    return activity_list
  raise Exception("No data found")
