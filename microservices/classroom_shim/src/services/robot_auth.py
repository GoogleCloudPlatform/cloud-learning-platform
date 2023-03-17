"""
  Class to fetch and cache id token using robot account.
"""
import time
import requests


class Authentication:
  """
    Class to fetch and cache id token using robot account.
    params:
      email: robot email
      password: robot password
  """

  def __init__(self, email, password):
    self.email = email
    self.password = password
    self.signin_url = \
      "http://authentication/authentication/api/v1/sign-in/credentials"
    self.refresh_url = "http://authentication/authentication/api/v1/generate"
    self.token = None
    self.refresh_token = None
    self.token_expiry = None
    self.get_token()

  def get_token(self):
    """This function will hit the sign-in api"""
    payload = {"email": self.email, "password": self.password}
    response = requests.post(self.signin_url, json=payload, timeout=30)
    if response.status_code == 200:
      data = response.json().get("data")
      self.token = data.get("idToken")
      self.refresh_token = data.get("refreshToken")
      self.token_expiry = time.time() + int(data.get("expiresIn"))

  def get_id_token(self):
    """This function will fetch id_token"""
    if not self.token or time.time() > self.token_expiry:
      self.refresh_token_fetch()
    return self.token

  def refresh_token_fetch(self):
    """This function will hit the refresh token api"""
    if not self.refresh_token:
      self.get_token()
      return

    payload = {"refresh_token": self.refresh_token}
    response = requests.post(self.refresh_url, json=payload, timeout=30)
    if response.status_code == 200:
      data = response.json().get("data")
      self.token = data.get("id_token")
      self.refresh_token = data.get("refresh_token")
      self.token_expiry = int(data.get("expires_in"))
      return self.token

  def get_refresh_token(self):
    """This function will fetch refresh token"""
    if not self.refresh_token:
      self.refresh_token_fetch()
    return self.refresh_token
