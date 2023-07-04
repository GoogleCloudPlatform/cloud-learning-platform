"""
    Class and methods for dashboardItems route.
"""
import json
from routes.base_handler import BaseHandler
from middleware.authentication import verify_authentication
from middleware.validation import validate_request
from controllers.dashboard_controller import get_dashboard_items
from utils.exception_handler import InvalidContextError, \
    InternalServerError, Error


class DashboardHandler(BaseHandler):
  """Class def handling routes."""

  @verify_authentication
  @validate_request
  async def post(self):
    """Method for post request"""
    try:
      return self.send_json(
          status=200,
          message="",
          success=True,
          response=await
          get_dashboard_items(json.loads(self.request.body), self.user_id))
    except (InvalidContextError, InternalServerError, Error) as err:
      return self.send_json(status=500, message=str(err), success=False)
