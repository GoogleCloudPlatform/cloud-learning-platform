"""class for handling errors"""


class ResourceNotFoundException(Exception):
  """Class for custom Exceptions"""

  def __init__(self, message="Resource not found"):
    self.message = message
    super().__init__(self.message)
