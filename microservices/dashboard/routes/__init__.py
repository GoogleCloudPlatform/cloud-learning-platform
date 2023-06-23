"""Methods for creating and returning a tornado web application."""
import tornado.web
from config import SERVICE_NAME, API_BASE_URL, IS_DEVELOPMENT
from routes.error_handler import ErrorHandler
from routes.main_handler import MainHandler
from routes.dashboard_session_handler import DashboardSessionHandler
from routes.dashboard_handler import DashboardHandler
from routes.dashboard_course_handler import DashboardCourseHandler


def make_app():
  """
        Create a tornado web application.
        Args:
            None
        Returns:
            tornado web application
    """
  settings = {"default_handler_class": ErrorHandler}
  if IS_DEVELOPMENT:
    settings["autoreload"] = True
  else:
    settings["autoreload"] = False
  api_path = {"service": SERVICE_NAME, "version": API_BASE_URL}
  return tornado.web.Application(
      [("/ping", MainHandler), ("/ping/", MainHandler),
       ("/{service}/{version}/session".format(**api_path),
        DashboardSessionHandler),
       ("/{service}/{version}/session/".format(**api_path),
        DashboardSessionHandler),
       ("/{service}/{version}/dashboardItems".format(**api_path),
        DashboardHandler),
       ("/{service}/{version}/dashboardItems/".format(**api_path),
        DashboardHandler),
       ("/{service}/{version}/courseContexts".format(**api_path),
        DashboardCourseHandler),
       ("/{service}/{version}/courseContexts/".format(**api_path),
        DashboardCourseHandler)], **settings)
