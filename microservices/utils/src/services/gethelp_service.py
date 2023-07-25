"""Utility methods to handle get_help data"""
from services.firestore_service import get_paginated_documents,\
    get_paginated_topic_documents


def get_help_faqs(collection_path, topic, page_no):
  """Method to handle fetched help faqs"""
  try:
    docs = get_paginated_topic_documents(collection_path, topic, page_no)
    return_list = []
    for doc in docs:
      data = doc.to_dict()
      return_list.append(data)
    return {"items": return_list}
  except Exception as err:  # pylint: disable=broad-except
    print(err)
    return err


def gettopics(collection_path, page_no):
  """Method to handle fetched topics"""
  try:
    docs = get_paginated_documents(collection_path, page_no)
    return_list = []
    for doc in docs:
      data = doc.to_dict()
      return_list.append(data)
    return {"items": return_list}
  except Exception as err:  # pylint: disable=broad-except
    print(err)
    return err
