"""class and methods for routes handling."""

import json
import traceback
from routes.base_handler import BaseHandler
from controllers.topic_tree_controller import TopicTreeController
from common.utils.logging_handler import Logger
from middleware.validation import validate_create_topic_tree


# pylint: disable=abstract-method
# pylint: disable=unused-argument
class TopicTreeHandler(BaseHandler):
  """class def handling routes."""

  async def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      level = self.get_query_argument("level", "course")
      node_id = self.get_query_argument("id", None)
      if not node_id:
        return self.send_json(
            message="Query param id is required", success=False, status=500)
      response = await TopicTreeController.get_complete_tree({
          "level": level,
          "id": node_id
      })
      return self.send_json(
          status=200,
          success=True,
          message="Successfully fetched the Tree",
          response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_topic_tree
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      request_body = json.loads(self.request.body)
      response = TopicTreeController.topic_tree_controller_method(request_body)
      return self.send_json(
          status=200,
          success=True,
          message="A job with name {} has been started".format(
            response["job_name"]),
          response=response
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)
