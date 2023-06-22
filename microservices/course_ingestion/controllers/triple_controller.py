"""controller for triple level"""
#pylint: disable=redefined-builtin,broad-exception-raised
from services.triple_inference import TripleService


class TripleController():
  """controller class for triple level"""
  triple_service = TripleService()

  @staticmethod
  def create_triple_controller_method(lu_id, request_body):
    """controller method to create a triple"""
    if lu_id:
      return TripleController.triple_service.create_triple(lu_id, request_body)
    else:
      raise Exception("Learning Unit id is missing in the URL")

  @staticmethod
  def update_triple_controller_method(id, request_body):
    """controller method to update a triple"""
    if id:
      return TripleController.triple_service.update_triple(id, request_body)
    else:
      raise Exception("Triple ID is missing in the URL")

  @staticmethod
  def get_triple_controller_method(id):
    """controller method to get a triple by id"""
    if id:
      return TripleController.triple_service.get_triple(id)
    else:
      raise Exception("Triple ID is missing in the URL")

  @staticmethod
  def get_all_triple_controller_method(lu_id):
    """controller method to get all triples"""
    if lu_id:
      return TripleController.triple_service.get_all_triples(lu_id)
    else:
      raise Exception("learning unit ID is missing in the URL")

  @staticmethod
  def delete_triple_controller_method(id):
    """controller method to delete a triple"""
    if id:
      return TripleController.triple_service.delete_triple(id)
    else:
      raise Exception("Triple ID is missing in the URL")

  @staticmethod
  def create_triples_from_lu_controller_method(lu_id, req_body):
    """controller method to delete a triple"""
    if lu_id:
      top_n = req_body.get("top_n", 10)
      return TripleController.triple_service.create_triples_from_lu(lu_id,
        top_n=top_n, request_body=req_body)
    else:
      raise Exception("Learning Unit ID is missing in the URL")
