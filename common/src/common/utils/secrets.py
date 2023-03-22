""" Secrets Helper Functions"""
import google_crc32c
import requests
from config import PROJECT_ID
from google.cloud import secretmanager


def get_secret(secret_id):
  """Get a generic secret payload from Google Secret Manager

  Args:
      secret_id (str): the id of the secret

  Returns:
      str: the "UTF-8" decoded secret payload
  """
  client = secretmanager.SecretManagerServiceClient()
  secret_name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"

  response = client.access_secret_version(request={"name": secret_name})
  crc32c = google_crc32c.Checksum()
  crc32c.update(response.payload.data)
  if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
    print("Data corruption detected.")
    return response
  payload = response.payload.data.decode("UTF-8")
  return payload


# TODO: this should be built into a class that can use refresh token to get
# new id_token, cache token, etc
def get_backend_robot_id_token():
  """Generate an ID Token to be used by the backend robot account for
     service to service authed API calls

  Returns:
      str: the new id_token
  """
  api_endpoint = \
  "http://authentication/authentication/api/v1/sign-in/credentials"
  res = requests.post(url=api_endpoint,
                      headers={
                          "Content-Type": "application/json",
                      },
                      json={
                          "email": get_secret("lms-backend-robot-username"),
                          "password": get_secret("lms-backend-robot-password"),
                      },
                      timeout=60)
  payload = res.json()["data"]
  return payload["idToken"]
