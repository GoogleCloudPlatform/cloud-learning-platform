"""Method to communicate with session microservice"""
# import json
import requests
from config import SERVICES


def get_session_response(session_id, token):
  """Method to get session response"""
  api_endpoint = "http://{}:{}/dashboard/api/v1/session".format(
      SERVICES["dashboard"]["host"], SERVICES["dashboard"]["port"])
  response = requests.get(
      url=api_endpoint,
      headers={
          "Content-Type": "application/json",
          "Authorization": token
      },
      params={
          "id": session_id
      }).json()
  return response
