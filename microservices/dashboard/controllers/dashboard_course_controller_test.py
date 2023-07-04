"""
  utility methods to execute unit tests
  for module dashboard_cource_controller.py
"""
# pylint: disable=wrong-import-position
import pytest
import mock
import sys

sys.path.append("../../common/src")
from controllers.dashboard_course_controller import (get_course_controller,
            decider_func, get_competency, get_subcompetency, get_lo, get_lu)


@pytest.mark.asyncio
@pytest.mark.parametrize("course_id", [{"course_id": None}])
@mock.patch("controllers.dashboard_course_controller.get_all_courses")
async def test_get_all_course_controller(mock_get_all_courses, course_id):
  mock_get_all_courses.return_value = {"data": {"course_name": "Socialogy"}}
  course_details = await get_course_controller(course_id["course_id"])
  assert course_details is not None


@pytest.mark.asyncio
@pytest.mark.parametrize("course_id", [{"course_id": "12345"}])
@mock.patch("controllers.dashboard_course_controller.get_course")
async def test_get_course_controller(mock_get_course, course_id):
  mock_get_course.return_value = {"data": {"course_name": "Socialogy"}}
  course_details = await get_course_controller(course_id["course_id"])
  assert course_details is not None


@pytest.mark.asyncio
@mock.patch("controllers.dashboard_course_controller.get_competency")
async def test_decider_func(mock_get_competency):
  mock_get_competency.return_value = {"data": {"course_name": "Socialogy"}}
  res = await decider_func({"competency_id": "12345678"}, user_id="12345")
  assert res is not None


@pytest.mark.asyncio
@mock.patch("controllers.dashboard_course_controller.get_lu")
async def test_decider_func_lu(mock_get_lu):
  mock_get_lu.return_value = {"data": {"course_name": "Socialogy"}}
  res = await decider_func({"learning_unit_id": "12345678"}, user_id="12345")
  assert res is not None


@pytest.mark.asyncio
@mock.patch("controllers.dashboard_course_controller.get_lo")
async def test_decider_func_lo(mock_get_lo):
  mock_get_lo.return_value = {"data": {"course_name": "Socialogy"}}
  res = await decider_func({"learning_objective_id": "12345678"},
                           user_id="12345")
  assert res is not None


@pytest.mark.asyncio
@mock.patch(
  "controllers.dashboard_course_controller.get_subcompetency_with_session")
async def test_decider_func_sub_compentency(
  mock_get_subcompetency_with_session):
  mock_get_subcompetency_with_session.return_value = {
    "data": {
      "course_name": "Socialogy"
    }
  }
  res = await decider_func({"subcompetency_id": "12345678"}, user_id="12345")
  assert res is not None


@pytest.mark.asyncio
@mock.patch("controllers.dashboard_course_controller.fetch_competency")
async def test_get_competency(mock_fetch_competency):
  mock_fetch_competency.return_value = {"data": {"course_name": "Socialogy"}}
  res = await get_competency({"subcompetency_id": "12345678"})
  assert res is not None


@pytest.mark.asyncio
@mock.patch("controllers.dashboard_course_controller.fetch_subcompetency")
async def test_get_subcompetency(mock_fetch_subcompetency):
  mock_fetch_subcompetency.return_value = {"data": {"course_name": "Socialogy"}}
  res = await get_subcompetency({"subcompetency_id": "12345678"})
  assert res is None


@pytest.mark.asyncio
@mock.patch("controllers.dashboard_course_controller.fetch_lo")
async def test_get_lo(mock_fetch_lo):
  mock_fetch_lo.return_value = {"data": {"course_name": "Socialogy"}}
  res = await get_lo({"course_name": "Socialogy"})
  assert res is not None


@pytest.mark.asyncio
@mock.patch("controllers.dashboard_course_controller.fetch_lu")
async def test_get_lu(mock_fetch_lu):
  mock_fetch_lu.return_value = {"data": {"course_name": "Socialogy"}}
  res = await get_lu({"course_name": "Socialogy"})
  assert res is not None
