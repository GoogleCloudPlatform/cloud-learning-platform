"""
    Class and methods for course context route.
"""
import json
from routes.base_handler import BaseHandler
from middleware.authentication import verify_authentication
from controllers.dashboard_course_controller import get_course_controller,\
  decider_func
from utils.exception_handler import InternalServerError, Error


class DashboardCourseHandler(BaseHandler):
  """Class def handling routes."""

  @verify_authentication
  async def get(self):
    """Method for get request"""
    try:
      course = self.get_argument("course", None)
      return self.send_json(
          status=200,
          message="Successfully fetched course related contexts",
          success=True,
          response=await get_course_controller(course))
    except (InternalServerError, Error) as err:
      return self.send_json(status=500, message=str(err), success=False)

  @verify_authentication
  async def post(self):
    """Method for post request"""
    try:
      course_obj = json.loads(self.request.body)
      return self.send_json(
          status=200,
          message="Successfully fetched course related contexts",
          success=True,
          response=await decider_func(course_obj, self.user_id))
    except (InternalServerError, Error) as err:
      return self.send_json(status=500, message=str(err), success=False)
