""" Functions for rubrics """
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.common_api_handler import CommonAPIHandler
from common.utils.http_exceptions import InternalServerError
from common.models import Rubric
from schemas.rubric_schema import RubricModel,UpdateRubricModel

# pylint: disable = broad-except

def create_rubric(input_rubric: RubricModel):
  """The create rubric function will add the rubric to the firestore if it
  does not exist.If the rubric exist then it will update the rubric

  Args:
      input_rubric (RubricModel): input rubric to be
      inserted

  Raises:
      ResourceNotFoundException: If the rubric does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      str: UUID(Unique identifier for rubric)
  """
  try:
    new_rubric = Rubric()
    input_rubric_dict = {**input_rubric.dict()}
    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_rubric_dict)
    new_rubric = new_rubric.from_dict(input_rubric_dict)
    new_rubric.uuid = ""
    new_rubric.save()
    new_rubric.uuid = new_rubric.id
    new_rubric.update()
    rubric_fields = new_rubric.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        rubric_fields, Rubric, operation="add")
    ParentChildNodesHandler.update_parent_references(
        rubric_fields, Rubric, operation="add")

    return {
        "success": True,
        "message": "Successfully created the rubric",
        "data": rubric_fields
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e

def update_rubric(uuid: str, input_rubric: UpdateRubricModel):
  """The create rubric function will add the rubric to the firestore if it
  does not exist.If the rubric exist then it will update the rubric

  Args:
      input_rubric (RubricModel): input rubric to be
      inserted

  Raises:
      ResourceNotFoundException: If the rubric does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      str: UUID(Unique identifier for rubric)
  """
  try:
    input_rubric_dict = {**input_rubric.dict()}
    rubric_fields = CommonAPIHandler.update_document(
        Rubric, uuid, input_rubric_dict)

    return {
        "success": True,
        "message": "Successfully updated the rubric",
        "data": rubric_fields
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e
