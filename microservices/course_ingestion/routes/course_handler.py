"""
class and methods for routes handling.
"""
import json
import traceback

from routes.base_handler import BaseHandler
from controllers.course_controller import CourseController
from common.utils.logging_handler import Logger
from common.utils.cache_service import delete_key
from common.utils.errors import PayloadTooLargeError
from middleware.validation import (validate_create_course,
                                   validate_update_course)
import time
import tornado.ioloop


# pylint: disable=redefined-builtin
# pylint: disable=broad-except,broad-exception-raised


# pylint: disable=abstract-method
# pylint: disable=unused-argument
# pylint: disable=simplifiable-if-statement
class CourseHandler(BaseHandler):
  """class def handling routes."""

  def get(self, *args, **kwargs):
    """Method for get request."""
    try:
      if args[-1]:
        id = args[-1]
        response = CourseController.get_course_controller_method(id)
      else:
        competencies = self.get_argument("competencies", "true", True)
        search_query = self.get_argument("search_query", None, True)
        skip = self.get_argument("skip", 0, True)
        limit = self.get_argument("limit", 0, True)
        sort_by = self.get_argument("sort_by", "descending", True)
        order_by = self.get_argument("order_by", "created_time", True)
        if competencies not in ["true", "false", ""]:
          raise Exception("Query param competencies should either"
                          "be 'true' or 'false'")
        if competencies in ("true", ""):
          competencies = True
        else:
          competencies = False
        response = CourseController. \
          get_all_courses_controller_method(skip=int(skip), limit=int(limit),
                                            sort_by=sort_by, order_by=order_by,
                                            competencies=competencies,
                                            search_query=search_query)
      return self.send_json(
        status=200,
        success=True,
        message="Successfully fetched the course(s)",
        response=response,
      )
    except Exception as e:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(message=str(e), success=False, status=500)

  @validate_create_course
  def post(self, *args, **kwargs):
    """Method for post request."""
    try:
      request_body = json.loads(self.request.body)
      return self.send_json(
        status=200,
        success=True,
        message="Successfully created the course",
        response=CourseController.create_course_controller_method(
          request_body),
      )

    except Exception as err:  # pylint: disable=broad-except
      Logger.error(traceback.format_exc())
      return self.send_json(
        status=500, success=False, message=str(err), response=None)

  @validate_update_course
  def put(self, *args, **kwargs):
    """Method for put request."""
    try:
      id = args[-1]
      request_body = json.loads(self.request.body)
      return self.send_json(
        status=200,
        success=True,
        message="Successfully updated the course",
        response=CourseController.update_course_controller_method(
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
      CourseController.delete_course_controller_method(id)
      return self.send_json(
        status=200, success=True, message="successfully deleted the course")

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
    Logger.info("ON FINISH TRIGGRED")
    if (status_code == 200 and (method in ("PUT", "DELETE"))):
      Logger.info("INVALIDATING THE CACHE IN UPDATE/DELETE")
      course_id = self.path_args[-1]
      delete_key(course_id)
    end = time.time()
    Logger.info("Time taken")
    Logger.info(end - start)


class UploadFile(BaseHandler):
  """
  API End point to upload course
  """

  def get(self, *args, **kwargs):
    uid = args[-1]
    try:
      res = CourseController.upload_course_pdf(user_id=uid)
      return self.send_json(
        status=200, success=True,
        message="successfully uploaded the course PDF", response=res)
    except Exception as e:
      Logger.error(f"Failed to upload course PDF {e}")
      return self.send_json(status=500, success=False,
                            message="Failed to upload course PDF")

  def post(self, *args, **kwargs):
    course_pdf = [{"filename": "sample.pdf", "body": "Hello World"}]
    # This test data, using for testing purpose only
    uid = args[-1]
    try:
      pdf_file = self.request.files.get("course_pdf", course_pdf)
      res = CourseController.validate_upload_course_pdf(user_id=uid,
                                                        course_pdf=pdf_file)
      if res:
        return self.send_json(
          status=200, success=True,
          message="successfully validated the course PDF", response=res)

    except PayloadTooLargeError as e:
      Logger.error(f"Course PDF size too large {e}")
      return self.send_json(status=413, success=False, message=e)
    except Exception as e:
      Logger.error(f"Failed to validate course PDF {e}")
      return self.send_json(status=500, success=False,
                            message="Failed to validate course PDF")

  def delete(self, *args, **kwargs):
    """
    API End Point to delete blob from the GCS bucket
    :return: JSON Response
    """

    try:
      gs_path = self.get_argument("gs_path", None, True)
      res = CourseController.delete_blob_gcs_controller(gs_path=gs_path)
      return self.send_json(
        status=200, success=True, message=res)
    except Exception as e:
      Logger.error(f"Failed to delete course PDF {e}")
      return self.send_json(status=500, success=False,
                            message="Failed to delete course PDF")


class FetchCoursePdf(BaseHandler):
  """
  API END Point to fetch all the objects from the GCS
  """

  def get(self, *args, **kwargs):
    """
    API Endpoint to fetch all the course gs path and file name
    :return: JSON Response
    """
    search_query = self.get_argument("search", None, True)
    try:
      res = CourseController.fetch_course_pdf(search_query=search_query)
      return self.send_json(
        status=200, success=True,
        message="successfully fetched all the course PDF", response=res)
    except Exception as e:
      Logger.error(f"Failed to fetch course PDF {e}")
      return self.send_json(status=500, success=False,
                            message="Failed to fetch course PDF")


class CourseContentController(BaseHandler):
  """
  API Controller for learning contents linked with course
  """

  def get(self, *args, **kwargs):
    """
    API End Point for fetch learning contents linked with course
    return: JSON Response
    """
    course_id = self.get_argument("course_id", "true", True)
    try:
      res = CourseController.fetch_course_lc(course_id=course_id)
      return self.send_json(
        status=200, success=True, message="successfully fetched the course "
                                          "linked learning contents",
        response=res)
    except Exception as e:
      Logger.error(e)
      return self.send_json(
        status=500, success=False, message=f"failed to fetch the course "
                                           f"linked learning contents {e}")
