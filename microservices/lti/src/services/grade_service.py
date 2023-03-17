"""Grade service"""
import requests
from common.utils.logging_handler import Logger
from config import auth_client
# pylint: disable=line-too-long, broad-except


def grade_pass_back(input_grade: dict, user_id: str, line_item_id: str):
  """Grade passback to the required LMS service"""
  try:
    post_grade_url = "http://classroom-shim/classroom-shim/api/v1/grade"

    grade_res = requests.post(
        url=post_grade_url,
        headers={"Authorization": f"Bearer {auth_client.get_id_token()}"},
        json=input_grade,
        timeout=60)

    if grade_res.status_code == 200:
      Logger.info(
          f"Success: Grade pass back for user id - {user_id} for line item {line_item_id}"
      )
      return True

    else:
      Logger.error(
          f"Failed: Grade pass back for user id - {user_id} for line item {line_item_id}"
      )
      return False
  except Exception as e:
    Logger.error(e)
    return False
