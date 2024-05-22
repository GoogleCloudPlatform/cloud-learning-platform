"""
  Script to insert enrollment records in BQ
"""

# disabling for linting to pass
# pylint: disable = broad-exception-raised, broad-except
import datetime
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from common.models import CourseEnrollmentMapping, Section
from common.utils.bq_helper import insert_rows_to_bq

DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", "")
BQ_DATASET = DATABASE_PREFIX + "lms_analytics"

cred = credentials.Certificate("service_creds.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()


def main():
  print("script started")
  enrollment_ref = db.collection(CourseEnrollmentMapping.collection_name)
  docs = enrollment_ref.stream()
  for doc in docs:
    try:
      doc_dict = doc.to_dict()
      section = Section.find_by_id(doc_dict["section"].id)
      enrollment_record = CourseEnrollmentMapping.find_by_id(doc.id)
      rows = [{
          "enrollment_id": enrollment_record.id,
          "email": enrollment_record.user.email,
          "user_id": enrollment_record.user.user_id,
          "role": enrollment_record.role,
          "status": enrollment_record.status,
          "invitation_id": enrollment_record.invitation_id,
          "section_id": section.id,
          "cohort_id": section.cohort.id,
          "course_id": section.classroom_id,
          "timestamp": datetime.datetime.utcnow(),
      }]
      if insert_rows_to_bq(
          rows=rows, dataset=BQ_DATASET, table_name="sectionEnrollmentRecord"):
        print("Successfully Enrollment record " +
              f"inserted in bq by id: {enrollment_record.id}")
      else:
        print("Failed Enrollment record inserted" +
              f" in bq by id: {enrollment_record.id}")
    except Exception as e:
      print(f"failed insertion due to:{e}")


if __name__ == "__main__":
  main()
