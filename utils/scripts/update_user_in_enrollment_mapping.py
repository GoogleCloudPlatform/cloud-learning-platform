"""
  Script to update user in course enrollment mapping 
"""

# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common.models import User, CourseEnrollmentMapping, Section

# Use a service account.
cred = credentials.Certificate("service_creds.json")

app = firebase_admin.initialize_app(cred)

db = firestore.client()
enrollment_ref = db.collection(CourseEnrollmentMapping.collection_name)
docs = enrollment_ref.stream()
count = 0

for doc in docs:
  doc_ref = db.collection(CourseEnrollmentMapping.collection_name).document(
      doc.id)
  d = doc.to_dict()
  if isinstance(d["user"], str):
    user_ref = db.collection(User.collection_name).document(d["user"])
    user = user_ref.get().to_dict()
    if user:
      doc_ref.update({"user": user_ref})
      count = count + 1
      print(f"{doc.id} => {doc_ref.get().to_dict()}")
    else:
      try:
        print(Section.find_by_id(d["section"].id).to_dict())
      except Exception as e:
        print(e)
      print(f"User not found by this user_id {d['user']}." +
            f" Section {d['section'].id} status {d['status']}")
print("updation count", count)
