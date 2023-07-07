"""Method to communicate with session microservice"""
# import json
import requests
from config import SERVICES


def get_session_response(session_id, token):
  """Method to get session response"""
  api_endpoint = f"http://{SERVICES['dashboard']['host']}:" \
                 f"{SERVICES['dashboard']['port']}/dashboard/api/v1/session"
  response = requests.get(
      url=api_endpoint,
      headers={
          "Content-Type": "application/json",
          "Authorization": token
      },
      params={
          "id": session_id
      }, timeout=60).json()
  return response
