""" Config used for testing in unit tests """
from Crypto.PublicKey import RSA

API_URL = "http://localhost/lti/api/v1"

DEL_KEYS = [
    "id",
    "created_time",
    "last_modified_time",
    "archived_at_timestamp",
    "archived_by",
    "created_by",
    "deleted_at_timestamp",
    "deleted_by",
    "last_modified_by",
]


def generate_test_rsa_private_key():
  key = RSA.generate(2048)
  private_key = key.exportKey("PEM").decode()
  return private_key
