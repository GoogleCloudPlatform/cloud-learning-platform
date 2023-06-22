"""class and methods for error handling."""

from routes.base_handler import BaseHandler


# pylint: disable=abstract-method
class ErrorHandler(BaseHandler):
  """class def handling routes."""

  def prepare(self):
    """Method for error response."""
    return self.send_json(
        message="The resource you are looking for is not found",
        status=404,
        success=False)
