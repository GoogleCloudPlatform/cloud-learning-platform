'''
Test script to generate 429s against Google Classroom API and test `num_retries` for backoff
'''
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

CLASSROOM_ADMIN_EMAIL = os.environ["CLASSROOM_ADMIN_EMAIL"]
COURSE_ID = os.environ["COURSE_ID"]


def list_courses(creds):
  service = build('classroom', 'v1', credentials=creds)

  start = time.time()
  for i in range(100):
    print(i)
    try:
      results = service.courses().get(id=COURSE_ID).execute(num_retries=15)

      print(results)
    except Exception as e:
      print(json.loads(e.content)['error']['code'])

    print(time.time() - start)
    start = time.time()


def get_sa_creds():
  with open("sa_key.json", "r") as f:
    classroom_key = json.load(f)
  creds = service_account.Credentials.from_service_account_info(classroom_key,
                                                                scopes=SCOPES)
  creds = creds.with_subject(CLASSROOM_ADMIN_EMAIL)
  return creds


def main():
  creds = get_sa_creds()

  threads = 100
  pool = ThreadPoolExecutor(max_workers=threads)

  for i in range(threads):
    pool.submit(list_courses, creds)


if __name__ == "__main__":
  main()
