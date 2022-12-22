""" Creating public key, private key and jwks url """
import requests
import hashlib
from Crypto.PublicKey import RSA
from base64 import urlsafe_b64encode
from config import (LTI_SERVICE_PLATFORM_PRIVATE_KEY,
                    LTI_SERVICE_TOOL_PRIVATE_KEY)
#pylint: disable=broad-except


def base64urlUInt_encode(val):
  """ Encoding the base64 url and decoding as string """
  val_bytes = val.to_bytes((val.bit_length() + 7) // 8, byteorder="big")
  return urlsafe_b64encode(val_bytes).decode()


def create_public_keyset(private_key):
  try:
    key = RSA.importKey(private_key)
    key_hash = hashlib.sha256()
    key_hash.update(key.exportKey("PEM"))
    key_id = key_hash.hexdigest()
    public_keyset = {
        "keys": [{
            "kty": "RSA",
            "alg": "RS256",
            "kid": key_id,
            "use": "sig",
            "e": base64urlUInt_encode(key.publickey().e),
            "n": base64urlUInt_encode(key.publickey().n)
        }]
    }
    web_key = {
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "kid": key_id,
        "e": base64urlUInt_encode(key.e),
        "d": base64urlUInt_encode(key.d),
        "n": base64urlUInt_encode(key.n)
    }

    return {
        "key": key,
        "key_id": key_id,
        "public_keyset": public_keyset,
        "web_key": web_key
    }
  except Exception as e:
    raise Exception(str(e)) from e


def get_platform_public_keyset() -> dict:
  """ Returns the Platform Public keyset """
  key = get_platform_private_key()
  return create_public_keyset(key)


def get_platform_private_key():
  """ Returns the Platform Private key from config """
  return LTI_SERVICE_PLATFORM_PRIVATE_KEY


def get_tool_public_keyset() -> dict:
  """ Returns the Tool Public keyset """
  key = get_tool_private_key()
  return create_public_keyset(key)


def get_tool_private_key():
  """ Returns the Tool Private key from config """
  return LTI_SERVICE_TOOL_PRIVATE_KEY


def get_remote_keyset(jwks_uri: str) -> dict:
  """ Returns the remote keyset and specifying the algorithm as RS256 is not
  present """
  keyset = requests.get(jwks_uri).json()
  for k in keyset["keys"]:
    if not "alg" in k:
      k["alg"] = "RS256"
  return keyset
