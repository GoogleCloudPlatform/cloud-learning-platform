"""controller for course level"""
#pylint: disable=redefined-builtin,broad-exception-raised
from services import competency_inference


class CompetencyController():
  """controller class for competency level"""
  competency = competency_inference.CompetencyService()

  @staticmethod
  def create_course_competency_controller_method(parent_id, request_body):
    """controller method to create a comptency"""
    if parent_id:
      return CompetencyController.competency.create_course_competency(
          parent_id, request_body)
    else:
      raise Exception("Course id is missing in the URL")

  @staticmethod
  def update_course_competency_controller_method(id, request_body, parent_id):
    """controller method to update a competency"""
    if not id:
      raise Exception("Competency ID is missing in the URL")
    elif not parent_id:
      raise Exception("Course ID is missing in the URL")
    elif id and parent_id:
      return CompetencyController.competency.update_course_competency(
          id, request_body, parent_id)
    else:
      raise Exception("Internal Server Error")

  @staticmethod
  def get_course_competency_controller_method(id, parent_id):
    """controller method to get a competency by id"""
    if not id:
      raise Exception("Competency ID is missing in the URL")
    elif not parent_id:
      raise Exception("Course ID is missing in the URL")
    elif id and parent_id:
      return CompetencyController.competency.get_course_competency(
          id, parent_id)
    else:
      raise Exception("Internal Server Error")

  @staticmethod
  def get_course_all_competency_controller_method(parent_id):
    """controller method to get all competencies"""
    if parent_id:
      return CompetencyController.competency.get_course_all_competencies(
          parent_id)
    else:
      raise Exception("Course ID is missing in the URL")

  @staticmethod
  def delete_course_competency_controller_method(id, parent_id):
    """controller method to delete a comptency"""
    if not id:
      raise Exception("Competency ID is missing in the URL")
    elif not parent_id:
      raise Exception("Course ID is missing in the URL")
    elif id and parent_id:
      return CompetencyController.competency.delete_course_competency(
          id, parent_id)
    else:
      raise Exception("Internal Server Error")

  @staticmethod
  def create_lc_competency_controller_method(parent_id, request_body):
    """controller method to create a comptency"""
    if parent_id:
      return CompetencyController.competency.create_learning_content_competency(
          parent_id, request_body)
    else:
      raise Exception("LearningContent ID is missing in the URL")

  @staticmethod
  def update_lc_competency_controller_method(id, request_body, parent_id):
    """controller method to update a competency"""
    if not id:
      raise Exception("Competency ID is missing in the URL")
    elif not parent_id:
      raise Exception("Course ID is missing in the URL")
    elif id and parent_id:
      return CompetencyController.competency.update_learning_content_competency(
          id, request_body, parent_id)
    else:
      raise Exception("Internal Server Error")

  @staticmethod
  def get_lc_competency_controller_method(id, parent_id):
    """controller method to get a competency by id"""
    if not id:
      raise Exception("Competency ID is missing in the URL")
    elif not parent_id:
      raise Exception("Course ID is missing in the URL")
    elif id and parent_id:
      return CompetencyController.competency.get_learning_content_competency(
          id, parent_id)
    else:
      raise Exception("Internal Server Error")

  @staticmethod
  def get_all_lc_competency_controller_method(parent_id):
    """controller method to get all competencies"""
    if parent_id:
      return CompetencyController.competency\
        .get_all_learning_content_competencies(parent_id)
    else:
      raise Exception("LearningContent ID is missing in the URL")

  @staticmethod
  def delete_lc_competency_controller_method(id, parent_id):
    """controller method to delete a comptency"""
    if not id:
      raise Exception("Competency ID is missing in the URL")
    elif not parent_id:
      raise Exception("Course ID is missing in the URL")
    elif id and parent_id:
      return CompetencyController.competency.delete_learning_content_competency(
          id, parent_id)
    else:
      raise Exception("Internal Server Error")

  @staticmethod
  def create_competency_controller_method(request_body):
    """controller method to create a comptency"""
    return CompetencyController.competency.create_competency(request_body)

  @staticmethod
  def update_competency_controller_method(id, request_body):
    """controller method to update a competency"""
    if id:
      return CompetencyController.competency.update_competency(id, request_body)
    else:
      raise Exception("Competency ID is missing in the URL")

  @staticmethod
  def get_competency_controller_method(id,is_text_required=False):
    """controller method to get a competency by id"""
    if id:
      return CompetencyController.competency.get_competency(id,is_text_required)
    else:
      raise Exception("Competency ID is missing in the URL")

  @staticmethod
  def get_all_competency_controller_method():
    """controller method to get all competencies"""
    return CompetencyController.competency.get_all_competencies()

  @staticmethod
  def delete_competency_controller_method(id):
    """controller method to delete a comptency"""
    if id:
      return CompetencyController.competency.delete_competency(id)
    else:
      raise Exception("competency ID is missing in the URL")
