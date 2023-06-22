"""class and methods for routes handling."""
# pylint: disable=redefined-builtin
import json
import traceback
from routes.base_handler import BaseHandler
from controllers.triple_controller import TripleController
from common.utils.logging_handler import Logger
from middleware.validation import (validate_create_triple, validate_update_triple,
                                      validate_create_triple_from_lu)


# pylint: disable=abstract-method
# pylint: disable=unused-argument
class TripleHandler(BaseHandler):
  """class def handling routes."""

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      if args[-1]:
        id = args[-1]
        response = TripleController.get_triple_controller_method(id)
      else:
        parent_id = args[-2]
        response = TripleController.get_all_triple_controller_method(parent_id)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully fetched the triple(s)",
          response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_triple
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      parent_id = args[-2]
      request_body = json.loads(self.request.body)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully created the triple",
          response=TripleController.create_triple_controller_method(
              parent_id, request_body),
      )
    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  @validate_update_triple
  def put(self, *args, **kwargs):
    """Method for put request."""
    try:
      id = args[-1]
      request_body = json.loads(self.request.body)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully updated the triple",
          response=TripleController.update_triple_controller_method(
              id, request_body),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  def delete(self, *args, **kwargs):
    """Method for delete request."""
    try:
      id = args[-1]
      return self.send_json(
          status=200,
          success=True,
          message="Successfully deleted the triple",
          response=TripleController.delete_triple_controller_method(id))
    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

class TriplesFromLUHandler(BaseHandler):
  """class def handling routes."""

  @validate_create_triple_from_lu
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      lu_id = args[-1]
      request_body = json.loads(self.request.body)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully created new triples for "
          "given learning unit",
          response=TripleController.create_triples_from_lu_controller_method(
            lu_id, request_body),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)
