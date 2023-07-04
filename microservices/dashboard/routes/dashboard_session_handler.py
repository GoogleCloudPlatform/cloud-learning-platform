"""
    Class and methods for session route.
"""
import json
from routes.base_handler import BaseHandler
from middleware.authentication import verify_authentication
from middleware.validation import validate_request
from controllers.dashboard_session_controller import manage_session, \
    manage_session_retrieval, manage_session_update
from utils.exception_handler import InvalidContextError, \
    InvalidSessionIdError, InternalServerError, Error
from common.utils.logging_handler import Logger


class DashboardSessionHandler(BaseHandler):
  """Class def handling routes."""

  @verify_authentication
  @validate_request
  async def get(self):
    """Method for get request"""
    try:
      Logger.info(self.request.arguments["id"])
      return self.send_json(
          status=200,
          message="Session Details fetched successfully",
          success=True,
          response=await manage_session_retrieval(self.request.arguments["id"],
                                                  self.user_id))
    except (InvalidSessionIdError, InternalServerError, Error) as err:
      return self.send_json(status=500, message=str(err), success=False)

  @verify_authentication
  @validate_request
  async def post(self):
    """Method for post request"""
    try:
      return self.send_json(
          status=200,
          message="Session Created Successfully",
          success=True,
          response=manage_session(json.loads(self.request.body), self.user_id))
    except (InvalidContextError, InternalServerError, Error) as err:
      return self.send_json(status=500, message=str(err), success=False)

  @verify_authentication
  @validate_request
  async def put(self):
    """Method for put request"""
    try:
      return self.send_json(
          status=200,
          message="Session updated successfully",
          success=True,
          response=manage_session_update(json.loads(self.request.body),
            self.user_id))
    except (InternalServerError, Error) as err:
      return self.send_json(status=500, message=str(err), success=False)
