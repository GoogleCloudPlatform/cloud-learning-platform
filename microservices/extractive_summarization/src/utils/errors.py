"""class for handling errors"""


class ResourceNotFoundException(Exception):
  """Class for custom Exceptions"""

  def __init__(self, message="Resource not found"):
    self.message = message
    super().__init__(self.message)


class NoItemGeneratedError(Exception):
  """Class for custom Exceptions"""

  def __init__(self, message="No items were generated."):
    self.message = message
    super().__init__(self.message)


class InvalidFileType(Exception):
  """Error class to be raised when file with wrong/invalid ext is sent"""

  def __init__(self, message="Invalid file type"):
    self.message = message
    super().__init__(self.message)


class ValidationError(Exception):
  """Error class to be raised when there is a validation failed"""

  def __init__(self, message="Validation Failed", data=None):
    self.message = message
    self.data = data
    super().__init__(self.message)


class ConflictError(Exception):
  """Error class to be raised when there is a conflict"""

  def __init__(self, message="Validation Failed"):
    self.message = message
    super().__init__(self.message)
