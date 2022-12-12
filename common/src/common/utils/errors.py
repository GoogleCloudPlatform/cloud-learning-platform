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


class ValidationError(Exception):
  """Error class to be raised when there is a validation failed"""

  def __init__(self, message="Validation Failed", data=None):
    self.message = message
    self.data = data
    super().__init__(self.message)

class TokenNotFoundError(Exception):
  """Error class to be raised when auth token is not found"""

  def __init__(self, message="Token not found"):
    self.message = message
    super().__init__(self.message)


class UnauthorizedUserError(Exception):
  """Error class to be raised when unknown user tries to sign_up/sign_in"""

  def __init__(self, message="Unauthorized"):
    self.message = message
    super().__init__(self.message)
