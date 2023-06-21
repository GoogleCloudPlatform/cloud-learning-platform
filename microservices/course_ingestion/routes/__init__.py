"""methods for creating and returning a tornado web application."""

import tornado.web

from routes.main_handler import MainHandler
from routes.error_handler import ErrorHandler
from routes.sc_handler import SubCompetencyHandler
from routes.batch_job_handler import BatchJobHandler
from routes.topic_tree_handler import TopicTreeHandler
from routes.lo_handler import LearningObjectiveHandler
from routes.course_handler import (CourseHandler, CourseContentController,
                                   UploadFile, FetchCoursePdf)
from routes.triple_handler import TripleHandler, TriplesFromLUHandler
from routes.lu_handler import (LearningUnitHandler, LearningUnitFromLOHandler,
                               FetchLearningUnit)
from routes.competency_handler import CourseCompetencyHandler, \
  LearningContentCompetencyHandler, CompetencyHandler
from routes.learning_content_handler import (LearningContentHandler,
                                             GetLearningContent)

from config import API_BASE_URL, SERVICE_NAME, IS_DEVELOPMENT
from tornado.web import Application


def make_app() -> Application:
  """
  Function for course ingestion API routes
  Return
  ------
  tornado.web.Application
  """
  settings = {"default_handler_class": ErrorHandler}
  api_path = {"service": SERVICE_NAME, "version": API_BASE_URL}

  if IS_DEVELOPMENT:
    settings["autoreload"] = True
  else:
    settings["autoreload"] = False

  return tornado.web.Application(
    [
      (r"/", MainHandler),
      ("/ping", MainHandler),
      ("/ping/", MainHandler),
      ("/{service}/{version}/course/([^/]+)?/".format(**api_path),
       CourseHandler),
      ("/{service}/{version}/course/([^/]+)?".format(**api_path),
       CourseHandler),
      ("/{service}/{version}/jobs/([^/]+)?/".format(
        **api_path), BatchJobHandler),
      ("/{service}/{version}/jobs/([^/]+)?".format(
        **api_path), BatchJobHandler),
      ("/{service}/{version}/course/([^/]+)/competency/([^/]+)?".format(
        **api_path), CourseCompetencyHandler),
      ("/{service}/{version}/course/([^/]+)/competency/([^/]+)?/".format(
        **api_path), CourseCompetencyHandler),
      ("/{service}/{version}/competency/([^/]+)/"
       "sub_competency/([^/]+)?".format(**api_path), SubCompetencyHandler),
      ("/{service}/{version}/competency/([^/]+)/"
       "sub_competency/([^/]+)?/".format(**api_path), SubCompetencyHandler),
      ("/{service}/{version}/"
       "sub_competency/([^/]+)/learning_objective/([^/]+)?".format(
        **api_path), LearningObjectiveHandler),
      ("/{service}/{version}/sub_competency"
       "/([^/]+)/learning_objective/([^/]+)?/".format(**api_path),
       LearningObjectiveHandler),
      ("/{service}/{version}/learning_objective/([^/]+)/"
       "learning_unit/tree".format(**api_path),
       LearningUnitFromLOHandler),
      ("/{service}/{version}/"
       "learning_objective/([^/]+)/learning_unit/([^/]+)?".format(
        **api_path), LearningUnitHandler),
      ("/{service}/{version}/"
       "learning_objective/([^/]+)/learning_unit/([^/]+)?/".format(
        **api_path), LearningUnitHandler),
      ("/{service}/{version}/fetch/learning_unit/".format(**api_path),
       FetchLearningUnit),
      ("/{service}/{version}/topic_tree".format(**api_path),
       TopicTreeHandler),
      ("/{service}/{version}/topic_tree/".format(**api_path),
       TopicTreeHandler),
      ("/{service}/{version}/learning_content/([^/]+)?/".format(**api_path),
       LearningContentHandler),
      ("/{service}/{version}/learning_content/([^/]+)?".format(**api_path),
       LearningContentHandler),
      ("/{service}/{version}/learning_content/"
       "([^/]+)/competency/([^/]+)?".format(**api_path),
       LearningContentCompetencyHandler),
      ("/{service}/{version}/learning_content/"
       "([^/]+)/competency/([^/]+)?/".format(**api_path),
       LearningContentCompetencyHandler),
      ("/{service}/{version}/competency/([^/]+)?/".format(**api_path),
       CompetencyHandler),
      ("/{service}/{version}/competency/([^/]+)?".format(**api_path),
       CompetencyHandler),
      ("/{service}/{version}/learning_unit/([^/]+)/"
       "triple/([^/]+)?".format(**api_path), TripleHandler),
      ("/{service}/{version}/learning_unit/([^/]+)/"
       "triple/([^/]+)?/".format(**api_path), TripleHandler),
      ("/{service}/{version}/learning_unit/([^/]+)/"
       "lu/triple/".format(**api_path), TriplesFromLUHandler),
      ("/{service}/{version}/learning_unit/([^/]+)/"
       "lu/triple".format(**api_path), TriplesFromLUHandler),
      ("/{service}/{version}/learning_contents/".format(**api_path),
       GetLearningContent),
      ("/{service}/{version}/course_resources/validate/([^/]+)".format(
        **api_path), UploadFile),
      ("/{service}/{version}/course_resources/upload/([^/]+)".format(
        **api_path), UploadFile),
      ("/{service}/{version}/course_resources/delete".format(**api_path),
       UploadFile),
      ("/{service}/{version}/course_resources".format(**api_path),
       FetchCoursePdf),
      ("/{service}/{version}/fetch/course/learning_contents/".format(
        **api_path), CourseContentController),
    ],
    **settings)
