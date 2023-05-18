"""
  Script to update teacher course enrollment mapping 
"""

# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
# Use a service account.
cred = credentials.Certificate("service_creds.json")

app = firebase_admin.initialize_app(cred)

db = firestore.client()
collection_name=DATABASE_PREFIX + "course_enrollment_mapping"
enrollment_ref = db.collection(collection_name)
docs = enrollment_ref.stream()
count =0

for doc in docs:
  doc_ref =  db.collection(collection_name).document(doc.id)
  d=doc.to_dict()
  if isinstance(d["user"],str):
    user_ref=db.collection(DATABASE_PREFIX+"users").document(d["user"])
    user=user_ref.get().to_dict()
    if user:
      doc_ref.update({"user":user_ref})
      count = count +1
      print(f"{doc.id} => {doc_ref.get().to_dict()}")
    else:
      print(f"User not found by this user_id {d['user']}."
            + f" Section {d['section'].id}")
print("updation count",count)
      