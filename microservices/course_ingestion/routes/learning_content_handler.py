"""class and methods for routes handling."""
import json
import traceback
from routes.base_handler import BaseHandler
from controllers.learning_content_controller import LearningContentController
from common.utils.logging_handler import Logger
from middleware.validation import (validate_create_learning_content,
                                   validate_update_learning_content)
from utils.exception_handlers import LearningContentIDMissing, \
  LearningContentNotFound


# pylint: disable=unused-argument
# pylint: disable=abstract-method
# pylint: disable=redefined-builtin
# pylint: disable=Catching too general exception Exception (broad-except)

class LearningContentHandler(BaseHandler):
  """class def handling routes."""

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      if args[-1]:
        id = args[-1]
        response = LearningContentController. \
          get_learning_content_controller_method(id)
      else:
        response = LearningContentController. \
          get_all_learning_content_items_controller_method()
      return self.send_json(
        status=200,
        success=True,
        message="Successfully fetched the learning content item(s)",
        response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_learning_content
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      request_body = json.loads(self.request.body)
      res = LearningContentController. \
        create_learning_content_controller_method(request_body)

      return self.send_json(
        status=200,
        success=True,
        message="A job with name {} has been started".format(res["job_name"]),
        response=res)

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
        status=500, success=False, message=str(err), response=None)

  @validate_update_learning_content
  def put(self, *args, **kwargs):
    """Method for put request."""
    try:
      id = args[-1]
      request_body = json.loads(self.request.body)
      return self.send_json(
        status=200,
        success=True,
        message="Successfully updated the learning content",
        response=LearningContentController
        .update_learning_content_controller_method(id, request_body),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
        status=500, success=False, message=str(err), response=None)

  def delete(self, *args) -> json:
    """
    Endpoint to delete LC and unlink competency from that LC
    Parameters
    ----------
    args: LC ID (str)
    Return
    ------
    JSON Response
    """
    try:
      content_id = args[-1]
      LearningContentController. \
        delete_learning_content_controller_method(content_id=content_id)
      return self.send_json(status=200, success=True,
                            message="Successfully deleted the learning content")
    except LearningContentIDMissing as err:
      return self.send_json(status=400, success=False, message=str(err),
                            response=None)
    except LearningContentNotFound as err:
      return self.send_json(status=404, success=False, message=str(err),
                            response=None)
    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(status=500, success=False,
                            message="Internal Server Error",
                            response=None)


class GetLearningContent(BaseHandler):
  """
  API functionality for get learning contents and competencies
  """

  def get(self):
    """
    Get request method for learning content
    """
    search_query = self.get_argument("search_query", None, True)
    skip = self.get_argument("skip", 0, True)
    limit = self.get_argument("limit", 0, True)
    sort_by = self.get_argument("sort_by", "descending", True)
    order_by = self.get_argument("order_by", "created_time", True)
    try:
      res = LearningContentController. \
        get_all_contents(skip=int(skip), limit=int(limit), sort_by=sort_by,
                         order_by=order_by, search_query=search_query)
      if not res:
        return self.send_json(
          status=400,
          success=False,
          message="Failed to fetch learning contents")
      else:
        return self.send_json(
          status=200,
          success=True,
          message="Successfully fetched learning content",
          response=res)
    except Exception as e:
      Logger.error(traceback.format_exc())
      return self.send_json(
        status=500, success=False, message=str(e), response=None)
