"""
  Script to create a new user for ui e2e
"""
import os
import json
import requests
from common.models import TempUser
DATABASE_PREFIX = os.getenv("DATABASE_PREFIX", None)
PROJECT_ID = os.getenv("PROJECT_ID", None)
CREDS = os.getenv("account", None)
creds=json.loads(CREDS)
TEST_USER = {
    "first_name": "firstname",
    "last_name": "lastname",
    "email": creds["email"],
    "status": "active",
    "user_type": "robot",
    "user_groups": [],
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "gaia_id":"test1233",
    "photo_url":"tempurl"
}

def sign_up_user():
  """Function signing up new user"""
  input_user = {**TEST_USER}
  if not TempUser.find_by_email(creds["email"]):
    user = TempUser.from_dict(input_user)
    user.user_id = ""
    user.save()
    user.user_id = user.id
    user.update()
    req = requests.post(
        "http://localhost:8889/authentication/api/v1/sign-up/credentials",
        json={"email":creds["email"],"password":creds["password"]},
        timeout=40)
    if req.status_code != 200:
      if req.status_code == 422 and req.json().get(
          "message") == "EMAIL_EXISTS":
        print("signup: user email exists")
      else:
        raise Exception("User sign-up failed")
  else:
    print("firestore: user email already exists")

def main():
  sign_up_user()


if __name__ == "__main__":
  main()
