"""topic tree inference"""
import os
import json
from .clustering.hierarchical_clustering import create_recursive_topic_tree
from .import_learning_content import update_clustering_collections, get_parent_node_from_id
import ast
from common.utils.errors import ResourceNotFoundException
from common.models import (LearningContentItem, Competency, SubCompetency,
                           Course, LearningObjective, LearningUnit)
from common.utils.logging_handler import Logger
from services.helper_functions import cache_topic_tree, get_tree_from_cache
from concurrent.futures import ThreadPoolExecutor
import tornado.ioloop
from tornado.gen import multi

# pylint: disable=unspecified-encoding,broad-exception-raised,consider-using-with
topic_tree_executor = ThreadPoolExecutor(max_workers=8)

async def create_hierarchy(request_body):
  """triggers recursive topic tree from the input request"""
  level = request_body.get("level", "learning_objective")
  paragraphs = request_body.get("text")
  doc_id = request_body.get("id")
  create_learning_units = request_body.get("create_learning_units", True)
  create_triples = request_body.get("create_triples", False)
  parent_node = get_parent_node_from_id(level, doc_id)
  if parent_node:
    try:
      topic_tree = await create_recursive_topic_tree(
          paragraphs, node_level=level,
          create_learning_units=create_learning_units,
          create_triples=create_triples)
      response = await update_clustering_collections(
        level, parent_node.id, topic_tree)
      return {"response" : response}
    except:
      raise Exception("Internal error while creating node level tree")  #pylint: disable=raise-missing-from
  else:
    raise Exception("{} with this id does not exist".format(level))


def save_temp_topic_tree(topic_tree,
                         level,
                         doc_id,
                         destination_folder_path="temp_topic_tree/"):
  """saving temp topic tree"""
  os.makedirs(destination_folder_path, exist_ok=True)
  file_path = destination_folder_path + level + "-" + doc_id + ".json"
  with open(file_path, "w") as fp:
    json_string = json.dumps(str(topic_tree), indent=2)
    fp.write(json_string)
  return {"temp_file": level + "-" + doc_id + ".json"}


async def write_topic_tree(request_body):
  """writes temp_topic_tree to collections and deletes the temp json"""
  file_path = request_body.get("file_path")
  try:
    json_file = "temp_topic_tree/" + file_path
    path_split = file_path.split(".")[0].split("-")
    level, parent_node_id = path_split[0], path_split[1]
    with open(json_file) as json_file:
      items = ast.literal_eval(json.load(json_file))
    response = await update_clustering_collections(level, parent_node_id, items)
    os.remove("temp_topic_tree/" + file_path)
    return {"response": response}
  except:
    raise ResourceNotFoundException("No file found with the name")  #pylint: disable=raise-missing-from


#pylint: disable=protected-access
def get_tree_data(level, doc_id):
  """loads entire topic tree for a given level and id"""
  if level == "learning_content":
    content = LearningContentItem.find_by_id(doc_id)
    items_dict = content.get_fields(reformat_datetime=True)
    items_dict["id"] = content.id
    items_dict["competencies"] = []
    for competency_id in content.competency_ids:
      items_dict["competencies"].append(
          get_tree_data("competency", competency_id))
  elif level == "course":
    course = Course.find_by_id(doc_id)
    items_dict = course.get_fields(reformat_datetime=True)
    items_dict["id"] = course.id
    items_dict["competencies"] = []
    for competency_id in course.competency_ids:
      items_dict["competencies"].append(
          get_tree_data("competency", competency_id))
  elif level == "competency":
    competency = Competency.find_by_id(doc_id)
    items_dict = competency.get_fields(reformat_datetime=True)
    items_dict["id"] = competency.id
    competency.load_children()
    items_dict["sub_competencies"] = []
    for sub_competency in competency.sub_competencies:
      items_dict["sub_competencies"].append(
          get_tree_data("sub_competency", sub_competency.id))
  elif level == "sub_competency":
    sub_competency = SubCompetency.find_by_id(doc_id)
    items_dict = sub_competency.get_fields(reformat_datetime=True)
    items_dict["id"] = sub_competency.id
    if "parent_node" in items_dict:
      items_dict["parent_node"] = sub_competency.parent_node.ref.path
    sub_competency.load_children()
    items_dict["learning_objectives"] = []
    for learning_objective in sub_competency.learning_objectives:
      items_dict["learning_objectives"].append(
          get_tree_data("learning_objective", learning_objective.id))
  elif level == "learning_objective":
    learning_objective = LearningObjective.find_by_id(doc_id)
    items_dict = learning_objective.get_fields(reformat_datetime=True)
    items_dict["id"] = learning_objective.id
    if items_dict["text"]:
      items_dict["text"] = items_dict["text"].split("<p>")
    if "parent_node" in items_dict:
      items_dict["parent_node"] = learning_objective.parent_node.ref.path
    learning_objective.load_children()
    items_dict["learning_units"] = []
    for learning_unit in learning_objective.learning_units:
      items_dict["learning_units"].append(
          get_tree_data("learning_unit", learning_unit.id))
  elif level == "learning_unit":
    learning_unit = LearningUnit.find_by_id(doc_id)
    items_dict = learning_unit.get_fields(reformat_datetime=True)
    items_dict["id"] = learning_unit.id
    items_dict["text"] = items_dict["text"].split("<p>")
    if "parent_node" in items_dict:
      items_dict["parent_node"] = learning_unit.parent_node.ref.path
  return items_dict


def get_complete_tree(request_body):
  """triggers topic tree retrival from the input request"""
  level = request_body.get("level", "learning_objective")
  doc_id = request_body.get("id")
  output = get_tree_from_cache(level, doc_id)
  if output is None:
    output = get_tree_data(level, doc_id)
    if level == "course":
      cache_topic_tree(output, doc_id)
  return output

async def get_complete_tree_async(request_body):
  """triggers topic tree retrival from the input request using async"""
  level = request_body.get("level", "learning_objective")
  doc_id = request_body.get("id")
  output = get_tree_from_cache(level, doc_id)
  if output is None:
    Logger.info("CACHE MISSED")
    output = await get_tree_data_async(level, doc_id)
    if level == "course":
      cache_topic_tree(output, doc_id)
  return output

async def get_tree_data_async(level,doc_id):
  """alternative method to get topic tree data using parallel processing"""
  if level == "learning_content":
    content = LearningContentItem.find_by_id(doc_id)
    items_dict = content.get_fields(reformat_datetime=True)
    items_dict["id"] = content.id
    items_dict["competencies"] = []
    items_dict["competencies"] = await multi([
          tornado.ioloop.IOLoop.current().run_in_executor(
              topic_tree_executor, get_tree_data,"competency", comp_id)
          for comp_id in content.competency_ids
      ])
    return items_dict
  elif level == "course":
    course = Course.find_by_id(doc_id)
    items_dict = course.get_fields(reformat_datetime=True)
    items_dict["id"] = course.id
    items_dict["competencies"] = []
    items_dict["competencies"] = await multi([
          tornado.ioloop.IOLoop.current().run_in_executor(
              topic_tree_executor, get_tree_data,"competency", comp_id)
          for comp_id in course.competency_ids
      ])
  elif level == "competency":
    competency = Competency.find_by_id(doc_id)
    items_dict = competency.get_fields(reformat_datetime=True)
    items_dict["id"] = competency.id
    competency.load_children()
    items_dict["sub_competencies"] = []
    for sub_competency in competency.sub_competencies:
      items_dict["sub_competencies"].append(
          get_tree_data("sub_competency", sub_competency.id))
  elif level == "sub_competency":
    sub_competency = SubCompetency.find_by_id(doc_id)
    items_dict = sub_competency.get_fields(reformat_datetime=True)
    items_dict["id"] = sub_competency.id
    if "parent_node" in items_dict:
      items_dict["parent_node"] = sub_competency.parent_node.ref.path
    sub_competency.load_children()
    items_dict["learning_objectives"] = []
    for learning_objective in sub_competency.learning_objectives:
      items_dict["learning_objectives"].append(
          get_tree_data("learning_objective", learning_objective.id))
  elif level == "learning_objective":
    learning_objective = LearningObjective.find_by_id(doc_id)
    items_dict = learning_objective.get_fields(reformat_datetime=True)
    items_dict["id"] = learning_objective.id
    if items_dict["text"]:
      items_dict["text"] = items_dict["text"].split("<p>")
    if "parent_node" in items_dict:
      items_dict["parent_node"] = learning_objective.parent_node.ref.path
    learning_objective.load_children()
    items_dict["learning_units"] = []
    for learning_unit in learning_objective.learning_units:
      items_dict["learning_units"].append(
          get_tree_data("learning_unit", learning_unit.id))
  elif level == "learning_unit":
    learning_unit = LearningUnit.find_by_id(doc_id)
    items_dict = learning_unit.get_fields(reformat_datetime=True)
    items_dict["id"] = learning_unit.id
    items_dict["text"] = items_dict["text"].split("<p>")
    if "parent_node" in items_dict:
      items_dict["parent_node"] = learning_unit.parent_node.ref.path
  return items_dict
