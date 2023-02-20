"""Common API services"""
from  config import USER_MANAGEMENT_BASE_URL
import requests
from common.utils.errors import  UserManagementServiceError
from common.utils.logging_handler import Logger


def call_search_user_api(headers,email):
  """ Call search by email usermanagement API to get the student data
  Args:
  email (str):  email id of user to search

  Returns:
      response object : response from search api
  """

  response = requests.get(f"\
  {USER_MANAGEMENT_BASE_URL}/user/search/email?email={email}",\
    headers=headers)
  return response

def call_create_user_api(headers,body):
  """ Call create user  API to to insert a user
  Args:
  body (dict):  Body for create user API
  Returns:
      response object : response from create user
  """

  response = requests.post(f"{USER_MANAGEMENT_BASE_URL}/user",
  json=body,headers=headers)
  return response

def create_teacher(headers,body):
  """ Call create user API if user is not present in db then
    Call create user  API to to insert a user
  Args:
  body (dict):  Body for create user API
  headers : auth headers to call user management api
  Returns:
      response object : response from create user
  """
  response = call_search_user_api(headers,body["email"])
  searched_teacher = []
  if response.status_code == 200:
    searched_teacher = response.json()["data"]
    Logger.info(f"Searched  teacher value {searched_teacher}")
    if searched_teacher == []:
      body["first_name"] = "firstname"
      body["last_name"] = "lastname"
      create_user_response = requests.post(f"{USER_MANAGEMENT_BASE_URL}/user",
      json=body,headers=headers)
      Logger.info(
        f"User created with email{body},{create_user_response.status_code}")
      if create_user_response.status_code != 200:
        raise UserManagementServiceError(response.json()["message"])
      return response.json()["data"]
  else :
    raise UserManagementServiceError(response.json()["message"])
