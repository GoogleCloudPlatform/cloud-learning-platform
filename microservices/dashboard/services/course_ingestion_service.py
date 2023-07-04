"""Utility methods for database related operations."""
import requests
from config import SERVICES

# pylint: disable= consider-using-f-string,missing-timeout
def get_all_courses():
  """
          Calls endpoint of course ingestion microservice to
          get all courses
          Args:
              req_body: Dict
              token: String
          Returns:
              response: Dict
              oe Error
      """
  api_endpoint =\
      "http://{}:{}/course_ingestion/api/v1/course/?competencies=false".format(
      SERVICES["course_ingestion"]["host"],
      SERVICES["course_ingestion"]["port"])
  response = requests.get(
      url=api_endpoint, headers={
          "Content-Type": "application/json"
      }).json()
  return response


def get_course(course_id):
  """
          Calls endpoint of course ingestion microservice to
          get all courses
          Args:
              req_body: Dict
              token: String
          Returns:
              response: Dict
              oe Error
      """
  api_endpoint = "http://{}:{}/course_ingestion/api/v1/course/{}".format(
      SERVICES["course_ingestion"]["host"],
      SERVICES["course_ingestion"]["port"], course_id)
  response = requests.get(
      url=api_endpoint, headers={
          "Content-Type": "application/json"
      }).json()
  return response


def fetch_competency(req_body):
  """
          Calls endpoint of course ingestion microservice to
          get all competencies or a competency
          Args:
              req_body: Dict
              token: String
          Returns:
              response: Dict
              oe Error
      """
  api_endpoint = "http://{}:{}/course_ingestion/api/v1/course"\
      "/{}/competency/{}".format(
          SERVICES["course_ingestion"]["host"],
          SERVICES["course_ingestion"]["port"], req_body["course_id"],
          req_body["competency_id"])
  response = requests.get(
      url=api_endpoint, headers={
          "Content-Type": "application/json"
      }).json()
  return response


def fetch_subcompetency(req_body):
  """
          Calls endpoint of course ingestion microservice to
          get all subcompetencies or a subcompetency
          Args:
              req_body: Dict
              token: String
          Returns:
              response: Dict
              oe Error
      """
  api_endpoint = "http://{}:{}/course_ingestion/api/v1"\
      "/competency/{}/sub_competency/{}".format(
          SERVICES["course_ingestion"]["host"],
          SERVICES["course_ingestion"]["port"],
          req_body["competency_id"], req_body["subcompetency_id"])
  response = requests.get(
      url=api_endpoint, headers={
          "Content-Type": "application/json"
      }).json()

  # Filter all sub competencies which contains no learning unit
  if response["data"] and not req_body["subcompetency_id"]:
    response["data"] = list(filter(
      lambda x: x["total_lus"] > 0, response["data"]))

  return response


def fetch_lo(req_body):
  """
          Calls endpoint of course ingestion microservice to
          get all subcompetencies or a subcompetency
          Args:
              req_body: Dict
              token: String
          Returns:
              response: Dict
              oe Error
      """
  api_endpoint = "http://{}:{}/course_ingestion/api/v1/"\
      "competency/{}/sub_competency/{}/learning_objective/{}".format(
          SERVICES["course_ingestion"]["host"],
          SERVICES["course_ingestion"]["port"],
          req_body["competency_id"], req_body["subcompetency_id"],
          req_body["learning_objective_id"])
  response = requests.get(
      url=api_endpoint, headers={
          "Content-Type": "application/json"
      }).json()
  return response


def fetch_lu(req_body):
  """
          Calls endpoint of course ingestion microservice to
          get all subcompetencies or a subcompetency
          Args:
              req_body: Dict
              token: String
          Returns:
              response: Dict
              oe Error
      """
  api_endpoint = "http://{}:{}/course_ingestion/api/v1/competency"\
      "/{}/sub_competency/{}/learning_objective/{}/learning_unit/{}".format(
          SERVICES["course_ingestion"]["host"],
          SERVICES["course_ingestion"]["port"],
          req_body["competency_id"], req_body["subcompetency_id"],
          req_body["learning_objective_id"], req_body["learning_unit_id"])
  response = requests.get(
      url=api_endpoint, headers={
          "Content-Type": "application/json"
      }).json()
  return response
