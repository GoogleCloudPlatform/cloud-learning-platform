""" Config used for testing in unit tests """
from Crypto.PublicKey import RSA

API_URL = "http://localhost/lti-service/api/v1"

DEL_KEYS = [
    "is_archived",
    "uuid",
    "created_time",
    "last_modified_time",
]


def generate_test_rsa_private_key():
  key = RSA.generate(2048)
  private_key = key.exportKey("PEM").decode()
  return private_key
