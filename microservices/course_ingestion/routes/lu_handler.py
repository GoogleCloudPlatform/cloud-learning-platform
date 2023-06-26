"""class and methods for routes handling."""
# pylint: disable=redefined-builtin
import json
import traceback
import tornado.ioloop
from routes.base_handler import BaseHandler
from controllers.lu_controller import LearningUnitController
from common.utils.logging_handler import Logger
from common.utils.cache_service import delete_key
from common.models import Course, LearningObjective
from middleware.validation import (validate_create_lu,
                                   validate_update_lu,
                                   validate_create_lu_from_lo)
import time


# pylint: disable=abstract-method
# pylint: disable=unused-argument
class LearningUnitHandler(BaseHandler):
  """class def handling routes."""

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      if args[-1]:
        id = args[-1]
        response = LearningUnitController.get_lu_controller_method(id)
      else:
        parent_id = args[-2]
        response = LearningUnitController.get_all_lu_controller_method(
          parent_id)
      return self.send_json(
        status=200,
        success=True,
        message="Successfully fetched the learning unit(s)",
        response=response)
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_lu
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      parent_id = args[-2]
      request_body = json.loads(self.request.body)
      return self.send_json(
        status=200,
        success=True,
        message="Successfully created the learning unit",
        response=LearningUnitController.create_lu_controller_method(
          parent_id, request_body))

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
        status=500, success=False, message=str(err), response=None)

  @validate_update_lu
  async def put(self, *args, **kwargs):
    """Method for put request."""
    try:
      id = args[-1]
      request_body = json.loads(self.request.body)
      return self.send_json(
        status=200,
        success=True,
        message="Successfully updated the learning unit",
        response=await
        LearningUnitController.update_lu_controller_method(id, request_body))

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
        message="Successfully deleted the learning unit",
        response=LearningUnitController.delete_lu_controller_method(id))

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
    if status_code == 200 and (method in ("PUT", "DELETE", "POST")):
      Logger.info("INVALIDATING THE C`ACHE")
      lo_obj = LearningObjective.find_by_id(self.path_args[-2])
      sc_obj = lo_obj.parent_node.get()
      competency_id = sc_obj.parent_node.ref.path.split("/")[1]
      courses = list(Course.collection.filter(
        "competency_ids", "array_contains", competency_id).fetch())
      courses = [course.id for course in courses]
      Logger.info("FOUND COURSES: ----------------------->")
      Logger.info(courses)
      for course_id in courses:
        delete_key(course_id)
    end = time.time()
    Logger.info("Time taken")
    Logger.info(end - start)


class LearningUnitFromLOHandler(BaseHandler):
  """class def handling routes."""

  @validate_create_lu_from_lo
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      lo_id = args[-1]
      request_body = json.loads(self.request.body)
      response = LearningUnitController.create_lu_from_lo_controller_method(
          lo_id, request_body)
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

  def on_finish(self):
    """Method to be called on finish"""
    tornado.ioloop.IOLoop.current().add_callback(self.on_finish_async)

  async def on_finish_async(self):
    """Method for on finish tasks"""
    start = time.time()
    status_code = self.get_status()
    method = self.request.method
    if (status_code == 200 and (method in ("POST",))):
      Logger.info("INVALIDATING THE CACHE")
      lo_obj = LearningObjective.find_by_id(self.path_args[-1])
      sc_obj = lo_obj.parent_node.get()
      competency_id = sc_obj.parent_node.ref.path.split("/")[1]
      courses = list(Course.collection.filter(
        "competency_ids", "array_contains", competency_id).fetch())
      courses = [course.id for course in courses]
      Logger.info("FOUND COURSES: ----------------------->")
      Logger.info(courses)
      for course_id in courses:
        delete_key(course_id)
    end = time.time()
    Logger.info("Time taken")
    Logger.info(end - start)


class FetchLearningUnit(BaseHandler):
  """
  Route for Fetching learning unit
  """

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      lu_id = self.get_argument("lu_id", None, True)
      response = LearningUnitController.get_lu_controller_method(lu_id)
      return self.send_json(
        status=200,
        success=True,
        message="Successfully fetched the learning unit(s)",
        response=response)
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)
