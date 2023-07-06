"""Utility methods to handle firestore data"""
from uuid import uuid4
import google.auth
from google.cloud import firestore


def get_doc_id():
  """
    This method returns a randomly generated unique id
    """
  return str(uuid4())


def get_firestore_instance():
  """
    This method creates a firestore instance and returns it to calling method
    """
  cred, project = google.auth.default()
  db = firestore.Client(project=project, credentials=cred)
  return db


def get_documents(collection_name):
  """
    This method will return all documents with that collection
    """
  db = get_firestore_instance()
  docs = db.collection(collection_name).get()
  print(docs)
  return docs


def get_paginated_topic_documents(collection_name, topic, page_no):
  """
    This method returns doc_limit no. of documents
    at a time  from given collection
    and page no
    """
  db = get_firestore_instance()
  doc_ref = db.collection(collection_name)
  if topic is not None:
    doc_ref = doc_ref.where("topic", "==", topic)
  doc_limit = 10
  query = doc_ref.limit(doc_limit).offset((page_no - 1) * doc_limit)
  docs = query.get()
  return docs


def get_paginated_documents(collection_name, page_no):
  """
    This method returns doc_limit no. of documents
    at a time  from given collection
    and page no
    """
  db = get_firestore_instance()
  doc_ref = db.collection(collection_name)
  doc_limit = 10
  query = doc_ref.limit(doc_limit).offset((page_no - 1) * doc_limit)
  docs = query.get()
  return docs


def save_feedback_doc(collection_name, subcollection_name, data, user_id):
  """
    This method inserts document in firestore collection
    and returns document id
    """
  db = get_firestore_instance()
  doc_id = get_doc_id()
  db.collection(collection_name).document(user_id).collection(
    subcollection_name).document(doc_id).set(data)
  return doc_id


def save_inline_feedback_doc(collection_name, subcollection_name, data,
                             user_id):
  """
    This method inserts document in firestore collection
    and returns document id
    """
  db = get_firestore_instance()
  doc_id = get_doc_id()
  db.collection(collection_name).document(user_id).collection(
    subcollection_name).document(doc_id).set(data)
  return doc_id


# pylint: disable=inconsistent-return-statements
def update_feedback(collection_name, subcollection, doc_id, data, user_id):
  """Method to call firestore to update feedback"""
  db = get_firestore_instance()
  doc_ref = db.collection(collection_name).document(user_id).collection(
    subcollection).document(doc_id)
  if doc_ref.get().to_dict() is not None:
    doc_ref.update(data)
    return doc_ref.id


def check_user_feedback(collection_name, subcollection, user_id):
  """Method to call firestore to check user feedback"""
  db = get_firestore_instance()
  doc_ref = db.collection(collection_name).document(user_id).collection(
    subcollection)
  return doc_ref.get()
