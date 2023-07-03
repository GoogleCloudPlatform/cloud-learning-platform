""" Fucntions fo RubricCriterion """
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.common_api_handler import CommonAPIHandler
from common.models import RubricCriterion
from common.utils.http_exceptions import InternalServerError
from schemas.rubric_criterion_schema import RubricCriterionModel,UpdateRubricCriterionModel

def create_rubric_criterion(input_rubric_criterion: RubricCriterionModel):
  """The create rubric criterion endpoint will add the rubric criterion to the
  firestore if it does not exist.If the rubric criterion exist then it will
  update the rubric criterion

  Args:
      input_rubric_criterion (RubricCriterionModel): input rubric criterion to
      be inserted

  Raises:
      ResourceNotFoundException: If the rubric criterion does not exist
      Exception: 500 Internal Server Error if something went wrong

  Returns:
      str: UUID(Unique identifier for rubric criterion)
  """
  try:

    new_rubric_criterion = RubricCriterion()
    input_rubric_criterion_dict = {**input_rubric_criterion.dict()}
    ParentChildNodesHandler.validate_parent_child_nodes_references(
        input_rubric_criterion_dict)

    new_rubric_criterion = new_rubric_criterion.from_dict(
        input_rubric_criterion_dict)
    new_rubric_criterion.uuid = ""

    new_rubric_criterion.save()
    new_rubric_criterion.uuid = new_rubric_criterion.id
    new_rubric_criterion.update()
    rubric_criterion_fields = new_rubric_criterion.get_fields(
        reformat_datetime=True)

    ParentChildNodesHandler.update_child_references(
        rubric_criterion_fields, RubricCriterion, operation="add")
    ParentChildNodesHandler.update_parent_references(
        rubric_criterion_fields, RubricCriterion, operation="add")

    return {
        "success": True,
        "message": "Successfully created the rubric criterion",
        "data": rubric_criterion_fields
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e

def update_rubric_criterion(uuid: str,
                            input_rubric_criterion: UpdateRubricCriterionModel):
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
    input_rubric_criterion_dict = {**input_rubric_criterion.dict()}
    rubric_criterion_fields = CommonAPIHandler.update_document(
        RubricCriterion, uuid, input_rubric_criterion_dict)

    return {
        "success": True,
        "message": "Successfully updated the rubric",
        "data": rubric_criterion_fields
    }
  except Exception as e:
    raise InternalServerError(str(e)) from e
