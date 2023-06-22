"""class and methods for logs handling."""
# Imports the Cloud Logging client library
import google.cloud.logging
import logging
from config import IS_CLOUD_LOGGING_ENABLED

if IS_CLOUD_LOGGING_ENABLED:
  # Instantiates a client
  client = google.cloud.logging.Client()

  # Retrieves a Cloud Logging handler based on the environment
  # you're running in and integrates the handler with the
  # Python logging module. By default this captures all logs
  # at INFO level and higher
  client.setup_logging()

  logging.basicConfig(
      format="%(asctime)s:%(levelname)s:%(message)s", level=logging.DEBUG)

class Logger():
  """class def handling logs."""

  @staticmethod
  def info(message):
    """Display info logs."""
    logging.info(message)

  @staticmethod
  def warning(message):
    """Display warning logs."""
    logging.warning(message)

  @staticmethod
  def debug(message):
    """Display debug logs."""
    logging.debug(message)

  @staticmethod
  def error(message):
    """Display error logs."""
    logging.error(message)
