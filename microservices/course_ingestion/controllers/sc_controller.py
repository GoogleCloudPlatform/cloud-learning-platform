"""controller for course level"""
#pylint: disable=redefined-builtin,broad-exception-raised
from services.sc_inference import SubCompetencyService


class SubCompetencyController():
  """controller class for sub competency level"""
  sub_competency_service = SubCompetencyService()

  @staticmethod
  def create_sc_controller_method(parent_id, request_body):
    """controller method to create a sub comptency"""
    if parent_id:
      return SubCompetencyController.sub_competency_service.\
        create_sub_competency(
          parent_id, request_body)
    else:
      raise Exception("competency ID is missing in the URL")

  @staticmethod
  def update_sc_controller_method(id, request_body):
    """controller method to update a sub comptency"""
    if id:
      return SubCompetencyController.sub_competency_service.\
        update_sub_competency(
          id, request_body)
    else:
      raise Exception("sub competency ID is missing in the URL")

  @staticmethod
  def get_sc_controller_method(id,is_text_required=False):
    """controller method to get a sub comptency by id"""
    if id:
      return SubCompetencyController.sub_competency_service.get_sub_competency(
          id,is_text_required)
    else:
      raise Exception("sub competency ID is missing in the URL")

  @staticmethod
  def get_all_sc_controller_method(parent_id):
    """controller method to get all sub comptencies"""
    if parent_id:
      return SubCompetencyController.sub_competency_service.\
        get_all_sub_competencies(
          parent_id)
    else:
      raise Exception("competency ID is missing in the URL")

  @staticmethod
  def delete_sc_controller_method(id):
    """controller method to delete a sub comptency"""
    if id:
      return SubCompetencyController.sub_competency_service.\
        delete_sub_competency(
          id)
    else:
      raise Exception("sub competency ID is missing in the URL")
