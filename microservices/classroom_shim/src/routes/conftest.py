""" conftest.py: Consist of fixtures"""
import pytest
from common.models import LTIAssignment


@pytest.fixture(name="create_lti_assignment")
def create_lti_assignment(request):
  lti_assignment = LTIAssignment.from_dict(request.param)
  lti_assignment.save()
  return lti_assignment
