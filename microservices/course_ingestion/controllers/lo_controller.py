"""controller for course level"""
#pylint: disable=redefined-builtin,broad-exception-raised
from services.lo_inference import LearningObjectiveService


class LearningObjectiveController():
  """controller class for learning objective level"""
  learning_objective = LearningObjectiveService()

  @staticmethod
  def create_lo_controller_method(parent_id, request_body):
    """controller method to create a learning objective"""
    if parent_id:
      return LearningObjectiveController.learning_objective.\
        create_learning_objective(
          parent_id, request_body)
    else:
      raise Exception("sub competency ID is missing in the URL")

  @staticmethod
  async def update_lo_controller_method(id, request_body):
    """controller method to update a learning objective"""
    if id:
      return await LearningObjectiveController.learning_objective.\
        update_learning_objective(
          id, request_body)
    else:
      raise Exception("learning objective ID is missing in the URL")

  @staticmethod
  def get_lo_controller_method(id):
    """controller method to get a learning objective by id"""
    if id:
      return LearningObjectiveController.learning_objective.\
        get_learning_objective(
          id)
    else:
      raise Exception("learning objective ID is missing in the URL")

  @staticmethod
  def get_all_lo_controller_method(parent_id):
    """controller method to get all learning objectives"""
    if parent_id:
      return LearningObjectiveController.learning_objective.\
        get_all_learning_objectives(
          parent_id)
    else:
      raise Exception("sub competency ID is missing in the URL")

  @staticmethod
  def delete_lo_controller_method(id):
    """controller method to delete a learning objective"""
    if id:
      return LearningObjectiveController.learning_objective.\
        delete_learning_objective(id)
    else:
      raise Exception("learning objective ID is missing in the URL")
