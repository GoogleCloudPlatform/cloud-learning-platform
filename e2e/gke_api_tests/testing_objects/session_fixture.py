import httpx
import pytest
import requests
from testing_objects.test_config import API_URL_AUTHENTICATION_SERVICE
from secrets_helper import get_user_email_and_password_for_e2e


def user_login():
  """
  Function to do firebase login
  """
  user_email_password = get_user_email_and_password_for_e2e()
  req = requests.post(f"{API_URL_AUTHENTICATION_SERVICE}/sign-in/credentials",
                      json=user_email_password,
                      timeout=60)
  res = req.json()
  if res is None or res["data"] is None:
    raise Exception("User sign-in failed")
  print(f"User with {user_email_password['email']} was logged in with "
        f"token {req.json()['data']['idToken']}")
  return req.json()['data']['idToken']

@pytest.fixture(scope="module")
def get_session():
  token = user_login()
  session=httpx.Client(headers={"Authorization": f"Bearer {token}"})
  # session = requests.Session()
  # session.headers.update({"Authorization": f"Bearer {token}"})
  yield session
