"""LTI Assignment Copy Endpoints"""
import traceback
import requests
from fastapi import APIRouter
from common.models import LTIAssignment
from common.utils.logging_handler import Logger
from common.utils.errors import ResourceNotFoundException
from common.utils.http_exceptions import (ResourceNotFound, InternalServerError)
from common.utils.secrets import get_backend_robot_id_token
from schemas.error_schema import (InternalServerErrorResponseModel,
                                  NotFoundErrorResponseModel,
                                  ValidationErrorResponseModel)
# from schemas.lti_assignment_schema import InputLTIAssignmentModel
# from routes.lti_assignment import get_lti_assignment, create_lti_assignment
# pylint: disable=line-too-long

router = APIRouter(
    tags=["LTI Assignments Copy"],
    responses={
        500: {
            "model": InternalServerErrorResponseModel
        },
        404: {
            "model": NotFoundErrorResponseModel
        },
        422: {
            "model": ValidationErrorResponseModel
        }
    })


@router.post("/lti-assignment/copy")
def copy_lti_assignment(data: dict):
  """
  Endpoint to copy LTIAssignment data model and its related child datamodel.
  data format: {
    lti_assignment_id: "123",
    context_id: "123"
  }
  """
  try:
    # fetch content_item and related line_items
    lti_assignment = LTIAssignment.find_by_id(data.get("lti_assignment_id"))
    lti_assignment_data = lti_assignment.to_dict()
    content_item_id = lti_assignment_data.get("lti_content_item_id")

    content_item_req = requests.get(
        f"http://lti/lti/api/v1/content-item/{content_item_id}",
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        timeout=60)

    if content_item_req.status_code == 200:
      content_item_data = content_item_req.json().get("data")
    else:
      Logger.error(f"Request failed with code 1300 and the status code \
            {content_item_req.status_code} and error: {content_item_req.text}")
      raise Exception(
          f"Request failed with code 1300, Please contact administrator")

    # create a copy of above content item
    content_item_data["context_id"] = data.get("context_id")
    del content_item_data["id"]
    del content_item_data["created_time"]
    del content_item_data["last_modified_time"]
    copy_content_item_req = requests.post(
        "http://lti/lti/api/v1/content-item",
        headers={"Authorization": f"Bearer {get_backend_robot_id_token()}"},
        json=content_item_data,
        timeout=60)

    if copy_content_item_req.status_code == 200:
      copy_content_item_data = copy_content_item_req.json().get("data")
    else:
      Logger.error(f"Request failed with code 1310 and the status code \
            {copy_content_item_req.status_code} and error: {copy_content_item_req.text}"
                  )
      raise Exception(
          f"Request failed with code 1310, Please contact administrator")

    prev_context_ids = lti_assignment_data["prev_context_ids"]
    prev_content_item_ids = lti_assignment_data["prev_content_item_ids"]

    if prev_context_ids:
      prev_context_ids.insert(0, data.get("context_id"))
    else:
      prev_context_ids = [data.get("context_id")]

    if prev_content_item_ids:
      prev_content_item_ids.insert(0, content_item_id)
    else:
      prev_context_ids = [content_item_id]

    new_lti_assignment_data = {
        **lti_assignment_data, "context_id": data.get("context_id"),
        "context_type": "section",
        "lti_content_item_id": copy_content_item_data.get("id"),
        "prev_content_item_ids": prev_content_item_ids,
        "prev_context_ids": prev_context_ids,
        "course_work_id": None
    }

    new_lti_assignment = LTIAssignment.from_dict(new_lti_assignment_data)
    new_lti_assignment.save()
    new_lti_assignment_item = new_lti_assignment.to_dict()

    # new_lti_assignment_item = create_lti_assignment(
    #     InputLTIAssignmentModel.parse_obj(new_lti_assignment_data))
    return new_lti_assignment_item

  except ResourceNotFoundException as e:
    Logger.error(e)
    raise ResourceNotFound(str(e)) from e
  except Exception as e:
    Logger.error(e)
    Logger.error(traceback.print_exc())
    raise InternalServerError(str(e)) from e
