"""class and methods for routes handling."""
from routes.base_handler import BaseHandler


# pylint: disable=abstract-method
class MainHandler(BaseHandler):
  """class def handling routes."""

  def get(self):
    """Method for connection check."""
    return self.send_json(
        message="You have Successfully reached Deeplit API for Course Ingestion"
    )
