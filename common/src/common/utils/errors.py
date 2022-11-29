"""Classes for handling errors"""


class ResourceNotFoundException(Exception):
  """Error class to be raised when resource is not found"""

  def __init__(self, message="Resource not found"):
    self.message = message
    super().__init__(self.message)


class InvalidTokenError(Exception):
  """Error class to be raised when invalid/incorrect tokens are passed"""

  def __init__(self, message="Invalid token"):
    self.message = message
    super().__init__(self.message)
