"""
    Utility methods for Dashboard course
    related operations
"""
import tornado.ioloop
from controllers.dashboard_controller import get_session_details
from services.course_ingestion_service import get_course, get_all_courses, \
  fetch_competency, fetch_subcompetency, fetch_lo, fetch_lu


async def decider_func(req_body, user_id):
  if "learning_unit_id" in req_body:
    return await get_lu(req_body)
  elif "learning_objective_id" in req_body:
    return await get_lo(req_body)
  elif "subcompetency_id" in req_body:
    return await get_subcompetency_with_session(req_body, user_id)
  elif "competency_id" in req_body:
    return await get_competency(req_body)


async def get_course_controller(course_id):
  if course_id is None:
    courses = await tornado.ioloop.IOLoop.current().run_in_executor(
      None, get_all_courses)
    return courses["data"]
  course = await tornado.ioloop.IOLoop.current().run_in_executor(
    None, get_course, course_id)
  return course["data"]


async def get_competency(req_body):
  competencies = await tornado.ioloop.IOLoop.current().run_in_executor(
    None, fetch_competency, req_body)
  if isinstance(competencies["data"], list):
    competencies["data"] = sorted(
      competencies["data"], key=lambda i: (i["title"]))
    return competencies["data"]
  return competencies["data"]


async def get_subcompetency_with_session(req_body, user_id):
  subcompetencies = await get_subcompetency(req_body)
  rq_body = {
      "completed": req_body["completed"],
      "course_id": req_body["course_id"],
      "competency_id": req_body["competency_id"]
  }
  session_details_data = await get_session_details(subcompetencies, rq_body,
                                                   user_id)
  return session_details_data


async def get_subcompetency(req_body):
  """Async function to get subcompetency"""
  subcompetencies = await tornado.ioloop.IOLoop.current().run_in_executor(
    None, fetch_subcompetency, req_body)
  if isinstance(subcompetencies["data"], list) \
    and len(subcompetencies["data"]) > 0:
    subcompetencies["data"] = sorted(
      subcompetencies["data"], key=lambda i: (i["title"]))
    return subcompetencies["data"]
  elif isinstance(subcompetencies["data"], list) \
    and not subcompetencies["data"]:
    return "No sub competencies found"


async def get_lo(req_body):
  los = await tornado.ioloop.IOLoop.current().run_in_executor(
    None, fetch_lo, req_body)
  return los["data"]


async def get_lu(req_body):
  lus = await tornado.ioloop.IOLoop.current().run_in_executor(
    None, fetch_lu, req_body)
  return lus["data"]
