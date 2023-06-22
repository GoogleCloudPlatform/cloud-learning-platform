"""class and methods for routes handling."""
# pylint: disable=redefined-builtin
import json
import traceback
from routes.base_handler import BaseHandler
from controllers.sc_controller import SubCompetencyController
from common.utils.logging_handler import Logger
from common.models import Course
from common.utils.cache_service import delete_key
from middleware.validation import (validate_create_sub_competency,
                                   validate_update_sub_competency)
import time
import tornado.ioloop

# pylint: disable=abstract-method
# pylint: disable=unused-argument
#pylint: disable=broad-exception-raised
class SubCompetencyHandler(BaseHandler):
  """class def handling routes."""

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      if args[-1]:
        id = args[-1]
        is_text_required = self.get_query_argument("is_text_required","false")
        if is_text_required not in ["true", "false", ""]:
          raise Exception("Query param is_text_required should either"
                          "be 'true' or 'false'")
        is_text_required = bool(is_text_required.lower()=="true")
        response = SubCompetencyController.get_sc_controller_method(id,
        is_text_required)
      else:
        parent_id = args[-2]
        response = SubCompetencyController.get_all_sc_controller_method(
            parent_id)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully fetched the sub competency(s)",
          response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_sub_competency
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      parent_id = args[-2]
      request_body = json.loads(self.request.body)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully created the sub competency",
          response=SubCompetencyController.create_sc_controller_method(
              parent_id, request_body),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  @validate_update_sub_competency
  def put(self, *args, **kwargs):
    """Method for put request."""
    try:
      id = args[-1]
      request_body = json.loads(self.request.body)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully updated the sub competency",
          response=SubCompetencyController.update_sc_controller_method(
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
          message="Successfully deleted the sub competency",
          response=SubCompetencyController.delete_sc_controller_method(id),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  def on_finish(self):
    """Method to be called on finish"""
    tornado.ioloop.IOLoop.current().add_callback(self.on_finish_async)

  async def on_finish_async(self):
    """Method for on finish tasks"""
    start = time.time()
    status_code = self.get_status()
    method = self.request.method
    if (status_code == 200 and (method in ("PUT", "DELETE", "POST"))):
      Logger.info("INVALIDATING THE CACHE")
      competency_id = self.path_args[-2]
      courses = list(Course.collection.filter(
        "competency_ids", "array_contains", competency_id).fetch())
      courses = [course.id for course in courses]
      Logger.info("FOUND COURSES: ----------------------->")
      Logger.info(courses)
      for course_id in courses:
        delete_key(course_id)
    end = time.time()
    Logger.info("Time taken")
    Logger.info(end-start)
