"""class and methods for routes handling."""

import json
from tornado import web


# pylint: disable=abstract-method
class BaseHandler(web.RequestHandler):
  """class def handling routes."""

  user_email = None

  def set_default_headers(self):
    """Set headers."""
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "*")
    self.set_header("Access-Control-Max-Age", 1000)
    self.set_header(
        "Content-type", "application/json, text/plain")
    self.set_header(
        "Access-Control-Allow-Methods",
        "POST, PUT, GET, DELETE, OPTIONS")
    self.set_header(
        "Access-Control-Allow-Headers",
        "Content-Type, Access-Control-Allow-Origin,\
                         Access-Control-Allow-Headers, X-Requested-By,\
                         X-Requested-With, Access-Control-Allow-Methods")

  def options(self):
    """no body"""
    self.set_status(204)
    self.finish()

  def send_json(self, message="", success=True, response=None, status=200):
    """Return dictionary as response.

        Args:
            dictionary containing:
                "success" - True or False
                "message" - "All good" or error message
                "data" - dictionary containing containing response
                         from inference
    """
    self.set_status(status)
    return self.write(
        json.dumps({
            "success": success,
            "message": message,
            "data": response
        }))
