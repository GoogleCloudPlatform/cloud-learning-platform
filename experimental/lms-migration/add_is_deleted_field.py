
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate("service_credsjson")

app = firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection(u'users')
docs = users_ref.stream()
count =0

for doc1 in docs:
  doc_ref =  db.collection("users").document(doc1.id)
  doc_ref.update({u'is_deleted': False})
  count = count +1
  print(f'{doc1.id} => {doc1.to_dict()}')
print("is_deleted count updation",count)
