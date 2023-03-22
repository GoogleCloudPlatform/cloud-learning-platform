"""Class to fetch token from robot account"""
import traceback
import time
import requests
from common.utils.logging_handler import Logger
# pylint: disable=line-too-long,broad-exception-caught


class Authentication:
  """Class to fetch token from robot account"""

  def __init__(self, email, password):
    self.email = email
    self.password = password
    self.signin_url = "http://authentication/authentication/api/v1/sign-in/credentials"
    self.refresh_url = "http://authentication/authentication/api/v1/generate"
    self.token = None
    self.refresh_token = None
    self.token_expiry = None

  def get_token(self):
    """
      This function fetches toe id token using sign-in api from auth service 
    """
    try:
      payload = {"email": self.email, "password": self.password}
      response = requests.post(self.signin_url, json=payload, timeout=30)
      if response.status_code == 200:
        data = response.json().get("data")
        self.token = data.get("idToken")
        self.refresh_token = data.get("refreshToken")
        self.token_expiry = time.time() + int(data.get("expiresIn"))
    except Exception as e:
      Logger.error(e)
      Logger.error(traceback.print_exc())
      Logger.error("Something went wrong while fetching the robot token")

  def get_id_token(self):
    """This function returns the id token"""
    if self.token is None:
      self.get_token()

    if time.time() > self.token_expiry:
      self._fetch_refresh_token()

    return self.token

  def _fetch_refresh_token(self):
    """
      This function fetches the refresh token using refresh token api from
      auth service 
    """
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
