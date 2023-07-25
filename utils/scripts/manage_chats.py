"""
  Script to manage user chats: batch delete, update
"""

# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common.models import UserChat
from common.utils.errors import ResourceNotFoundException

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")


def delete_all_chats(db):
  """delete all chats"""
  docs = UserChat.collection.filter().fetch()
  doc_list = list(docs)
  item_keys = [UserChat.collection_name + "/" + doc.id for doc in doc_list]
  UserChat.collection.delete_all(item_keys)

def main(argv):
  print("Started Script")
  # Use a service account.
  cred = credentials.Certificate("key.json")
  firebase_admin.initialize_app(cred)
  db = firestore.client()
  delete_all_chats(db)
  print("Completed script")

if __name__ == "__main__":
  main(sys.argv)
