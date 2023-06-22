"""class and methods for routes handling."""
# pylint: disable=redefined-builtin
import json
import traceback
from routes.base_handler import BaseHandler
from controllers.competency_controller import CompetencyController
from common.utils.logging_handler import Logger
from common.utils.cache_service import delete_key
from common.models import Course
from middleware.validation import (validate_update_competency,
                                   validate_create_competency)
import time
import tornado.ioloop

# pylint: disable=abstract-method
# pylint: disable=unused-argument
# pylint: disable=broad-exception-raised
class CourseCompetencyHandler(BaseHandler):
  """class def handling routes."""

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      if args[-1]:
        id = args[-1]
        parent_id = args[-2]
        response = CompetencyController.get_course_competency_controller_method(
            id, parent_id)
      else:
        parent_id = args[-2]
        response = CompetencyController.\
          get_course_all_competency_controller_method(
            parent_id)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully fetched the  Competency(s)",
          response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_competency
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      parent_id = args[-2]
      request_body = json.loads(self.request.body)
      response = CompetencyController.\
        create_course_competency_controller_method(
          parent_id, request_body)

      return self.send_json(
          status=200,
          success=True,
          message="Successfully created the Competency",
          response=response,
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  def delete(self, *args, **kwargs):
    """Method for delete request."""
    try:
      id = args[-1]
      parent_id = args[-2]
      return self.send_json(
          status=200,
          success=True,
          message="Successfully deleted the Competency",
          response=CompetencyController
          .delete_course_competency_controller_method(id, parent_id),
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
    if (status_code == 200 and (method in ("DELETE", "POST"))):
      Logger.info("INVALIDATING THE CACHE")
      courses = [self.path_args[-2]]
      Logger.info("FOUND COURSES: ----------------------->")
      Logger.info(courses)
      for course_id in courses:
        delete_key(course_id)
    end = time.time()
    Logger.info("Time taken")
    Logger.info(end-start)


class LearningContentCompetencyHandler(BaseHandler):
  """class def handling routes."""

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      if args[-1]:
        id = args[-1]
        parent_id = args[-2]
        response = CompetencyController.get_lc_competency_controller_method(
            id, parent_id)
      else:
        parent_id = args[-2]
        response = CompetencyController.get_all_lc_competency_controller_method(
            parent_id)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully fetched the  Competency(s)",
          response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_competency
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      parent_id = args[-2]
      request_body = json.loads(self.request.body)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully created the Competency",
          response=CompetencyController.create_lc_competency_controller_method(
              parent_id, request_body),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  def delete(self, *args, **kwargs):
    """Method for delete request."""
    try:
      id = args[-1]
      parent_id = args[-2]
      return self.send_json(
          status=200,
          success=True,
          message="Successfully deleted the Competency",
          response=CompetencyController.delete_lc_competency_controller_method(
              id, parent_id),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)


class CompetencyHandler(BaseHandler):
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
        response = CompetencyController.get_competency_controller_method(id,
        is_text_required)
      else:
        response = CompetencyController.get_all_competency_controller_method()
      return self.send_json(
          status=200,
          success=True,
          message="Successfully fetched the  Competency(s)",
          response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_competency
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      request_body = json.loads(self.request.body)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully created the Competency",
          response=CompetencyController.create_competency_controller_method(
              request_body),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  @validate_update_competency
  def put(self, *args, **kwargs):
    """Method for put request."""
    try:
      id = args[-1]
      request_body = json.loads(self.request.body)
      return self.send_json(
          status=200,
          success=True,
          message="Successfully updated the Competency",
          response=CompetencyController.update_competency_controller_method(
              id, request_body),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
          status=500, success=False, message=str(err), response=None)

  def delete(self, *args, **kwargs):
    """Method for Delete request."""
    try:
      id = args[-1]
      return self.send_json(
          status=200,
          success=True,
          message="Successfully deleted the Competency",
          response=CompetencyController.delete_competency_controller_method(id),
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
    if (status_code == 200 and (method in ("PUT", ))):
      Logger.info("INVALIDATING THE CACHE")
      competency_id = self.path_args[-1]
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
