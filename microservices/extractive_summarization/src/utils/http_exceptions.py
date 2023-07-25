"""Classes for handling HTTP Exceptions"""

from typing import Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request

# pylint: disable=unused-argument

class CustomHTTPException(Exception):
  """Exception raised for any API errors.
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, status_code: int, success: bool, message: str, data: Any):
    self.status_code = status_code
    self.message = message
    self.success = success
    self.data = data
    super().__init__(message)

# Exception handlers
def add_exception_handlers(_app: FastAPI):
  @_app.exception_handler(CustomHTTPException)
  async def generic_exception_handler(req: Request, exc: CustomHTTPException):
    return JSONResponse(status_code=exc.status_code,
    content= {"success": False, "message": exc.message, "data": exc.data})

  @_app.exception_handler(RequestValidationError)
  async def pydantic_exception_handler(req: Request,
    exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "Validation Failed",
        "data": exc.errors()})

class BadRequest(CustomHTTPException):
  """Exception raised for errors in the input request.
  This can contain following scenarios:
  Invalid Argument: The argument is not as expected by the server.
  Precondition Failed: The request cannot be completed in
    the current system state.
  Out of range: For fetching records where range is required
    and is invalid.
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, message: str = "Bad Request", data=None):
    super().__init__(status_code=422, message=message, \
      success=False, data=data)

class Unauthenticated(CustomHTTPException):
  """Exception raised when permission is denied.
  Request is not authenticated due to missing,
  invalid or expired OAuth token.
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, message: Any = "Unauthenticated"):
    super().__init__(status_code=401, message=message, \
      success=False, data=None)

class PermissionDenied(CustomHTTPException):
  """Exception raised when permission is denied.
  Client does not have sufficient permission
  or privilege to make a particular request.
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, message: Any = "Permission Denied"):
    super().__init__(status_code=403, message=message, \
      success=False, data=None)

class ResourceNotFound(CustomHTTPException):
  """Exception raised if a Resource is not found.
  A specific resource is not found.
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, message: str = "Resource Not Found"):
    super().__init__(status_code=404, message=message, \
      success=False, data=None)

class Conflict(CustomHTTPException):
  """Exception raised for conflicts.
  Conflict of the request with current system state.
  This can include the following:
    Aborted: Concurrency conflict. Read-modify-write conflict.
    Already exists:The resource that a client tried to create already exists.
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, message: Any = "Bad Request"):
    super().__init__(status_code=409, message=message, \
      success=False, data=None)

class ResourceExhausted(CustomHTTPException):
  """Exception raised for errors in the input request.
  Either the server has reached the resource quota (resource limiting)
  or client has created too many requests (rate limiting)
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, message: Any = "Internal Server Error"):
    super().__init__(status_code=429, message=message, \
      success=False, data=None)

class InternalServerError(CustomHTTPException):
  """Exception raised for errors caused by the server.
  Errors caused at the server end which may require manual intervention.
  This includes the following:
    Data Loss: In case there is an unrecoverable data loss because of request.
    Unknown: An error occurred because of unknown reasons.
    Internal: An error occurred because of a server bug.
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, message: Any = "Internal Server Error"):
    super().__init__(status_code=500, message=message, \
      success=False, data=None)

class APINotImplemented(CustomHTTPException):
  """Exception raised for not implemented methods.
  API method not implemented on the server.
  Attributes:
    message -- explanation of the error
  """

  def __init__(self, message: Any = "Internal Server Error"):
    super().__init__(status_code=501, message=message, \
      success=False, data=None)
