"""Line item service"""
from common.models import LineItem


def create_new_line_item(input_line_item_dict):
  """Creates a new line item"""
  new_line_item = LineItem()
  new_line_item = new_line_item.from_dict(input_line_item_dict)
  new_line_item.uuid = ""
  new_line_item.save()
  new_line_item.uuid = new_line_item.id
  new_line_item.update()

  return new_line_item
