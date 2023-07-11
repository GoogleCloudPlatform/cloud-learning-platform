"""controller for course level"""

from common.models import Course
from services.course_inference import CourseService


# pylint: disable=redefined-builtin,broad-exception-raised


class CourseController:
  """controller class for course level"""

  course = CourseService()

  @staticmethod
  def create_course_controller_method(request_body):
    """controller method to create a course"""
    course = Course.collection.filter("title", "==",
                                      request_body["title"]).get()
    if course:
      raise Exception("Course for the given title exists, Please try with a "
                      "different name")
    return CourseController.course.create_course(request_body)

  @staticmethod
  def update_course_controller_method(id, request_body):
    """controller method to update a course"""
    if id:
      override = request_body.pop("override_existing_competencies", False)
      if override:
        return CourseController.course.update_course(id, request_body)
      else:
        return CourseController.course.add_competencies(id, request_body)
    else:
      raise Exception("Course ID is missing in the URL")

  @staticmethod
  def get_course_controller_method(id):
    """controller method to get a course"""
    if id:
      return CourseController.course.get_course(id)
    else:
      raise Exception("Course ID is missing in the URL")

  @staticmethod
  def get_all_courses_controller_method(skip: int, limit: int, sort_by: str,
                                        order_by: str, competencies: bool,
                                        search_query: str):
    """controller method to get all courses in firestore"""
    return CourseController.course.get_all_courses(skip=skip, limit=limit,
                                                   sort_by=sort_by,
                                                   order_by=order_by,
                                                   competencies=competencies,
                                                   search_query=search_query)

  @staticmethod
  def delete_course_controller_method(id):
    """controller method to delete a course"""
    if id:
      return CourseController.course.delete_course(id)
    else:
      raise Exception("Course ID is missing in the URL")

  @staticmethod
  def fetch_course_lc(course_id: str):
    """
    Controller for fetch linked course contents
    :param course_id: str
    :return: list
    """

    res = CourseController.course.fetch_course_linked_contents(
      course_id=course_id)
    return res

  @staticmethod
  def validate_upload_course_pdf(user_id: str, course_pdf: object) -> str:
    """
    Controller to validate upload the course PDF to GCS bucket
    :param course_pdf: file object
    :param user_id: string
    :return: string
    """
    return CourseController.course.validate_upload_course_pdf_service(
      course_pdf=course_pdf, user_id=user_id)

  @staticmethod
  def upload_course_pdf(user_id: str) -> str:
    """
    Function to upload Validated PDF to GCS bucket
    :param user_id: str
    :return: string/gcs path
    """
    return CourseController.course.upload_course_pdf_service(user_id=user_id)

  @staticmethod
  def fetch_course_pdf(search_query: str) -> str:
    """
    Function to fetch all the course PDF
    :return: string
    """

    return CourseController.course.fetch_all_course_pdf_service(
      search_query=search_query)

  @staticmethod
  def delete_blob_gcs_controller(gs_path: str) -> dict:
    """
    Function to delete blob from the GCS Bucket
    :param gs_path: str
    :return: dict
    """

    return CourseController.course.delete_the_blob_from_bucket(gs_path=gs_path)
