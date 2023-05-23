""" Helper Functions"""
from fastapi import Depends
from common.utils.auth_service import validate_user_type_and_token, auth_scheme


def validate_user(token: auth_scheme = Depends()):
  return validate_user_type_and_token(["other", "faculty", "admin", "robot"],
                                      token)
