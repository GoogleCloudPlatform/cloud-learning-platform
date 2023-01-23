""" conftest.py: Consist of fixtures"""
import pytest
from uuid import uuid4
from common.models import Tool, Platform, LTIContentItem, LineItem


@pytest.fixture(name="create_tool")
def create_tool(request):
  tool = Tool.from_dict(request.param)
  tool.client_id = str(uuid4())
  tool.deployment_id = str(uuid4())
  tool.save()
  return tool


@pytest.fixture(name="create_platform")
def create_platform(request):
  platform = Platform.from_dict(request.param)
  platform.uuid = ""
  platform.save()
  platform.uuid = platform.id
  platform.update()
  return platform


@pytest.fixture(name="create_content_item")
def create_content_item(request):
  content_item = LTIContentItem.from_dict(request.param)
  content_item.uuid = ""
  content_item.client_id = str(uuid4())
  content_item.deployment_id = str(uuid4())
  content_item.save()
  content_item.uuid = content_item.id
  content_item.update()
  return content_item


@pytest.fixture(name="create_line_item")
def create_line_item(request):
  line_item = LineItem.from_dict(request.param)
  line_item.uuid = ""
  line_item.client_id = str(uuid4())
  line_item.deployment_id = str(uuid4())
  line_item.save()
  line_item.uuid = line_item.id
  line_item.update()
  return line_item
