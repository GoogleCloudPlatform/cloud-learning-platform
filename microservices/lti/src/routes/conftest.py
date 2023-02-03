""" conftest.py: Consist of fixtures"""
import pytest
from uuid import uuid4
from common.models import Tool, Platform, LTIContentItem, LineItem


@pytest.fixture(name="create_tool")
def create_tool(request):
  tool = Tool.from_dict(request.param)
  tool.client_id = str(uuid4())
  tool.id = str(uuid4())
  tool.deployment_id = str(uuid4())
  tool.save()
  return tool


@pytest.fixture(name="create_platform")
def create_platform(request):
  platform = Platform.from_dict(request.param)
  platform.id = str(uuid4())
  platform.save()
  return platform


@pytest.fixture(name="create_content_item")
def create_content_item(request):
  content_item = LTIContentItem.from_dict(request.param)
  content_item.client_id = str(uuid4())
  content_item.deployment_id = str(uuid4())
  content_item.save()
  return content_item


@pytest.fixture(name="create_line_item")
def create_line_item(request):
  line_item = LineItem.from_dict(request.param)
  line_item.client_id = str(uuid4())
  line_item.deployment_id = str(uuid4())
  line_item.save()
  return line_item
