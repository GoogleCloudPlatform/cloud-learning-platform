import pytest
import requests
from common.models import TempUser
from testing_objects.test_config import API_URL_AUTHENTICATION_SERVICE
from testing_objects.user import TEST_USER
from secrets_helper import get_user_email_and_password_for_e2e
USER_EMAIL_PASSWORD_DICT = get_user_email_and_password_for_e2e()

@pytest.fixture(scope="module",autouse=True)
def sign_up_user():
  input_user = {**TEST_USER}
  if not TempUser.find_by_email(input_user["email"]):
    user = TempUser.from_dict(input_user)
    user.user_id = ""
    user.save()
    user.user_id = user.id
    user.update()
    print(f"created_user {user.user_id} ")
    req = requests.post(
        f"{API_URL_AUTHENTICATION_SERVICE}/sign-up/credentials",
        json=USER_EMAIL_PASSWORD_DICT,
        timeout=40)
    if req.status_code != 200:
      if req.status_code == 422 and req.json().get(
          "message") == "EMAIL_EXISTS":
        print("signup: user email exists")
      else:
        raise Exception("User sign-up failed")
  else:
    print("firestore: user email already exists")


@pytest.fixture(scope="module")
def get_token():
  req = requests.post(f"{API_URL_AUTHENTICATION_SERVICE}/sign-in/credentials",
                      json=USER_EMAIL_PASSWORD_DICT,
                      timeout=60)
  res = req.json()
  print("Authentication response")
  print(res)
  if res is None or res["data"] is None:
    raise Exception("User sign-in failed")
  print(f"User with {USER_EMAIL_PASSWORD_DICT['email']} was logged in with "
        f"token {req.json()['data']['idToken']}")
  token = req.json()['data']['idToken']
  yield {"Authorization": f"Bearer {token}"}
