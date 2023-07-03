""""contains data models related functions"""
from common.models import Course
#pylint: disable=unnecessary-comprehension
def get_learning_units(course_id):
  """returns all learning units for a given course"""
  course = Course.find_by_id(course_id)
  course.load_tree()
  learning_unit_list = []
  for competency in course.children_nodes:
    for sub_competency in competency.children_nodes:
      for learning_objective in sub_competency.children_nodes:
        learning_unit_list.extend(learning_objective.children_nodes)
  lu_id_list = [lu.id for lu in learning_unit_list]
  return lu_id_list

def get_all_courses():
  courses = Course.collection.fetch()
  courses = [i for i in courses]
  return courses

def filter_events_with_empty_feedback(user_event):
  """Internal function to clean user_events with incorrect schema"""
  if "second_attempt" in user_event["feedback"]:
    if "evaluation_flag" in user_event["feedback"]["second_attempt"]:
      return True
  elif "first_attempt" in user_event["feedback"]:
    if "evaluation_flag" in user_event["feedback"]["first_attempt"]:
      return True
  return False
