"""Line item service"""
from common.models import LineItem, LTIContentItem, Result
from common.utils.errors import ResourceNotFoundException
from config import LTI_ISSUER_DOMAIN
# pylint: disable=line-too-long


def create_new_line_item(input_line_item_dict):
  """Creates a new line item"""
  new_line_item = LineItem()
  new_line_item = new_line_item.from_dict(input_line_item_dict)
  new_line_item.save()
  return new_line_item


def create_new_content_item(input_content_item_dict, context_id=None):
  """Creates a new content item"""
  new_content_item = LTIContentItem()
  new_content_item = new_content_item.from_dict(input_content_item_dict)
  new_content_item.save()
  content_item_fields = new_content_item.get_fields(reformat_datetime=True)

  content_item_info = input_content_item_dict.get("content_item_info")

  if "lineItem" in content_item_info.keys():
    line_item_data = content_item_info.get("lineItem")

    start_date_time = ""
    end_date_time = ""

    if content_item_info.get("available", ""):
      start_date_time = content_item_info.get("available",
                                              "").get("startDateTime", "")
      end_date_time = content_item_info.get("available",
                                            "").get("endDateTime", "")

    input_line_item = {
        "startDateTime": start_date_time,
        "endDateTime": end_date_time,
        "scoreMaximum": line_item_data.get("scoreMaximum"),
        "label": line_item_data.get("label"),
        "tag": line_item_data.get("tag", ""),
        "resourceId": line_item_data.get("resourceId", ""),
        "resourceLinkId": new_content_item.id,
        "contextId": context_id
    }
    create_new_line_item(input_line_item)

  content_item_fields["id"] = new_content_item.id
  return content_item_fields


def get_line_item_results(context_id,
                          line_item_id=None,
                          user_id=None,
                          is_grade_sync_completed=None,
                          skip=0,
                          limit=10):
  """Get the results of a given line item for a specific context id"""
  result_fields = []

  result_collection_manager = Result.collection

  if user_id:
    result_collection_manager = result_collection_manager.filter(
        "userId", "==", user_id)

  if line_item_id:
    result_collection_manager = result_collection_manager.filter(
        "lineItemId", "==", line_item_id)

  if is_grade_sync_completed is not None:
    result_collection_manager = result_collection_manager.filter(
        "isGradeSyncCompleted", "==", is_grade_sync_completed)

  result = result_collection_manager.offset(skip).fetch(limit)

  for i in result:
    result_data = i.get_fields(reformat_datetime=True)
    result_data[
        "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}/results/{i.id}"
    result_data[
        "scoreOf"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}"
    result_fields.append(result_data)

  return result_fields


def get_result_of_line_item(context_id, line_item_id, result_id):
  """Get the result details of a given line item"""
  line_item = LineItem.find_by_id(line_item_id)

  if line_item.contextId != context_id:
    raise ResourceNotFoundException(
        f"Line item with id {line_item_id} in {context_id} not found")

  result = Result.find_by_id(result_id)
  if result.lineItemId != line_item_id:
    raise ResourceNotFoundException(
        "Incorrect result id provided for the given line item")

  result_fields = result.get_fields(reformat_datetime=True)
  result_fields[
      "id"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}/results/{result.id}"

  result_fields[
      "scoreOf"] = f"{LTI_ISSUER_DOMAIN}/lti/api/v1/{context_id}/line_items/{line_item_id}"

  return result_fields
