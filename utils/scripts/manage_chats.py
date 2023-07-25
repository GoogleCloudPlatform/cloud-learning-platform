"""
  Script to manage user chats: batch delete, update
"""

import os
import sys
import firebase_admin
from firebase_admin import credentials
from common.models import UserChat

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")


def delete_all_chats():
  """delete all chats"""
  docs = UserChat.collection.filter().fetch()
  doc_list = list(docs)
  item_keys = [UserChat.collection_name + "/" + doc.id for doc in doc_list]
  UserChat.collection.delete_all(item_keys)

def main(argv):
  del argv # unused
  print("Started Script")
  # Use a service account.
  cred = credentials.Certificate("key.json")
  firebase_admin.initialize_app(cred)
  delete_all_chats()
  print("Completed script")

if __name__ == "__main__":
  main(sys.argv)
