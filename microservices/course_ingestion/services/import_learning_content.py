"""Imports a generated course competency into firestore
  using the AI Tutor Common Model."""
import json
from common.utils.logging_handler import Logger
from common.models import LearningContentItem, Competency, SubCompetency, LearningObjective
import ast
from services.triple_inference import TripleService
from services.sc_inference import SubCompetencyService
# pylint: disable=unspecified-encoding,broad-exception-raised

from services.clustering.hierarchical_clustering import (
    get_topics, get_blooms_titles, compress_text_for_title_generation)

triple_service = TripleService()
sc_service = SubCompetencyService()

def update_collections(
    parent_level, parent_node,
    items, created_by="", last_modified_by="",update_lu_count=True):
  """updates child nodes with new items for a given parent node"""
  if parent_level == "competency":
    for sub_comp_item in items:
      subcompetency = parent_node.add_sub_competency()
      subcompetency.title = sub_comp_item["title"]
      subcompetency.description = sub_comp_item["title"]
      subcompetency.all_learning_resource = ""
      subcompetency.label = sub_comp_item["title"]
      subcompetency.created_by = created_by
      subcompetency.last_modified_by = last_modified_by
      total_lus = 0
      for lo_item in sub_comp_item["learning_objectives"]:
        total_lus+=len(lo_item["learning_units"])
      subcompetency.total_lus = total_lus
      subcompetency.save()
      update_collections(
          parent_node=subcompetency,
          parent_level="sub_competency",
          items=sub_comp_item["learning_objectives"],
          update_lu_count=False)
    return "successfully updated competency child nodes"
  elif parent_level == "sub_competency":
    for lo_item in items:
      lo = parent_node.add_learning_objective()
      lo.title = lo_item["title"]
      lo.description = lo_item["title"]
      lo.text = lo_item["text"]
      lo.created_by = created_by
      lo.last_modified_by = last_modified_by
      lo.save()
      update_collections(
          parent_node=lo,
          parent_level="learning_objective",
          items=lo_item["learning_units"],update_lu_count=False)
    if update_lu_count:
      sc_service.update_sub_competency_lu_count(
        parent_node.id)
    return "successfully updated sub competency child nodes"
  elif parent_level == "learning_objective":
    for lu_item in items:
      lu = parent_node.add_learning_unit()
      lu.title = lu_item["title"]
      lu.pdf_title = ""
      topics = get_topics(lu_item["text"].replace("<p>", " "))
      lu.topics = str(topics)
      lu.text = lu_item["text"]
      lu.created_by = created_by
      lu.last_modified_by = last_modified_by
      lu.save()
      if "triples" in lu_item:
        update_collections(
          parent_node=lu,
          parent_level="learning_unit",
          items=lu_item["triples"])
    if update_lu_count:
      sc_service.update_sub_competency_lu_count(
        parent_node.parent_node.ref.path.split("/")[1])
    return "successfully updated learning objective child nodes"
  elif parent_level == "learning_unit":
    for triple_item in items:
      triple = parent_node.add_triple()
      triple.subject = triple_item["subject"]
      triple.predicate = triple_item["predicate"]
      triple.object = triple_item["object"]
      triple.confidence = triple_item["confidence"]
      triple.sentence = triple_item["sentence"]
      triple.save()
    return "successfully updated learning unit child nodes"
  else:
    raise Exception("Undefined topic tree level - {}".format(parent_level))


#pylint: disable=raise-missing-from
def get_parent_node_from_id(level, doc_id):
  """returns node given the id and collection level"""
  try:
    if level == "learning_objective":
      return LearningObjective.find_by_id(doc_id)
    elif level == "sub_competency":
      return SubCompetency.find_by_id(doc_id)
    elif level == "competency":
      return Competency.find_by_id(doc_id)
    else:
      raise Exception("Undefined topic tree level - {}".format(level))
  except:
    raise Exception("No {level} found with the given id")


#pylint: disable=protected-access
async def update_clustering_collections(level, parent_node_id, items,
  created_by="", last_modified_by=""):
  """updates existing collections at different levels"""
  try:
    print("\n \n Items inside: {} \n\n".format(items))
    new_text_list = [item["text"] for item in items]
    new_text = "<p>".join(new_text_list)
    parent_node = get_parent_node_from_id(level, parent_node_id)
    parent_items = parent_node.get_fields()
    parent_items["is_valid"] = True
    if level in ["sub_competency","learning_objective"]:
      super_parent_key = parent_node.parent_node.ref.path
      parent_items["parent_node"] = parent_node.parent_node.get(
      ).__class__.collection.get(super_parent_key)
    parent_items["text"] = new_text
    text_for_title = await compress_text_for_title_generation(new_text_list)
    parent_items["title"] = get_blooms_titles(
      [text_for_title], 48, n_titles=1)[0][0]
    parent_items["label"] = parent_items["title"]
    parent_items["description"] = parent_items["title"]
    for key, value in parent_items.items():
      setattr(parent_node, key, value)
    parent_node.update()
    parent_node.delete_child_tree()
    return update_collections(
      level, parent_node, items, created_by, last_modified_by)
  except:
    raise Exception("Internal server error. Failed to update collections")


def create_clustering_learning_content_collections(title, description,
                                                   gcs_path,
                                                   start_page,
                                                   end_page,
                                                   content_type,
                                                   parsed_output_json,
                                                   last_modified_by="",
                                                   created_by="",
                                                   create_learning_units=True,
                                                   create_triples=False,
                                                   course_category=""
                                                   ):
  """creates new set of collections
  for a given learning_content using clustering"""
  learning_content_item = LearningContentItem()
  learning_content_item.title = title
  learning_content_item.description = description
  learning_content_item.gcs_path = gcs_path
  learning_content_item.document_type = content_type
  learning_content_item.last_modified_by = last_modified_by
  learning_content_item.created_by = created_by
  learning_content_item.course_category = course_category
  learning_content_item.start_page = start_page
  learning_content_item.end_page = end_page

  competency_ids = []
  with open(parsed_output_json) as json_file:
    competencies = ast.literal_eval(json.load(json_file))
    for competency_item in competencies:
      competency = Competency()
      competency.title = competency_item["title"]
      competency.description = competency_item["title"]
      competency.label = competency_item["title"]
      competency.last_modified_by = last_modified_by
      competency.created_by = created_by
      competency.save()
      competency_ids.append(competency.id)
      for sub_comp_item in competency_item["sub_competencies"]:
        subcompentency = competency.add_sub_competency()
        subcompentency.title = sub_comp_item["title"]
        subcompentency.description = sub_comp_item["title"]
        subcompentency.all_learning_resource = ""
        subcompentency.label = sub_comp_item["title"]
        subcompentency.last_modified_by = last_modified_by
        subcompentency.created_by = created_by
        total_lus = 0
        if create_learning_units:
          for lo in sub_comp_item["learning_objectives"]:
            total_lus+=len(lo["learning_units"])
        subcompentency.total_lus = total_lus
        subcompentency.save()
        for learning_objective_item in sub_comp_item["learning_objectives"]:
          learning_objective = subcompentency.add_learning_objective()
          learning_objective.title = learning_objective_item["title"]
          learning_objective.description = learning_objective_item["title"]
          learning_objective.text = learning_objective_item["text"]
          learning_objective.last_modified_by = last_modified_by
          learning_objective.created_by = created_by
          learning_objective.save()
          if create_learning_units:
            for learning_unit_item in learning_objective_item["learning_units"]:
              learning_unit = learning_objective.add_learning_unit()
              learning_unit.title = learning_unit_item["title"]
              learning_unit.text = learning_unit_item["text"]
              learning_unit.topics = str(learning_unit_item["topics"])
              learning_unit.pdf_title = ""
              learning_unit.last_modified_by = last_modified_by
              learning_unit.created_by = created_by
              learning_unit.save()
              if create_triples:
                for triple_item in learning_unit_item["triples"]:
                  triple = learning_unit.add_triple()
                  triple.subject = triple_item["subject"]
                  triple.predicate = triple_item["predicate"]
                  triple.object = triple_item["object"]
                  triple.confidence = triple_item["confidence"]
                  triple.sentence = triple_item["sentence"]
                  triple.save()
  learning_content_item.competency_ids = competency_ids
  learning_content_item.save()
  return learning_content_item.id


def create_learning_content_collections(title, gcs_path, content_type,
                                        start_page, end_page,
                                        parsed_output_json,last_modified_by="",
                                        created_by="", course_category=""):
  """creates new set of end
  to end documents (in collections)
  using parser alone for a new course"""
  json_filename = parsed_output_json

  try:
    last_competency = None
    last_subcompetency = None
    with open(json_filename) as json_file:
      competencies = json.load(json_file)
    if competencies:
      learning_content_item = LearningContentItem()
      learning_content_item.title = title
      learning_content_item.description = title
      learning_content_item.gcs_path = gcs_path
      learning_content_item.document_type = content_type
      learning_content_item.last_modified_by = last_modified_by
      learning_content_item.created_by = created_by
      learning_content_item.course_category = course_category
      learning_content_item.start_page = start_page
      learning_content_item.end_page = end_page

      competency_ids = []
      for competency_item in competencies:

        if last_competency != competency_item["competency"]:
          last_competency = competency_item["competency"]

          competency = Competency()
          competency.title = competency_item["competency"]
          competency.description = competency_item["competency"]
          competency.label = competency_item["competency"]
          competency.last_modified_by = last_modified_by
          competency.created_by = created_by
          competency.save()
          competency_ids.append(competency.id)
        sub_comp_item = competency_item["sub_competency"]

        if last_subcompetency != sub_comp_item["title"]:
          last_subcompetency = sub_comp_item["title"]
          subcompentency = competency.add_sub_competency()
          subcompentency.title = sub_comp_item["title"]
          subcompentency.description = sub_comp_item["title"]
          subcompentency.all_learning_resource = ""
          subcompentency.label = sub_comp_item["title"]
          subcompentency.total_lus = len(
              sub_comp_item["learning_objectives"]["learning_units"])
          subcompentency.last_modified_by = last_modified_by
          subcompentency.created_by = created_by
          subcompentency.save()

        learning_objective_items = sub_comp_item["learning_objectives"]

        learning_objective = subcompentency.add_learning_objective()
        learning_objective.title = learning_objective_items["title"]
        learning_objective.description = learning_objective_items["title"]
        learning_objective.text = " ".join(
          [lu["text"] for lu in learning_objective_items["learning_units"]])
        learning_objective.last_modified_by = last_modified_by
        learning_objective.created_by = created_by
        learning_objective.save()
        for learning_unit_item in learning_objective_items["learning_units"]:
          learning_unit = learning_objective.add_learning_unit()
          learning_unit.title = learning_unit_item["title"]
          learning_unit.text = learning_unit_item["text"]
          learning_unit.topics = "{}"
          learning_unit.pdf_title = ""
          learning_unit.last_modified_by = last_modified_by
          learning_unit.created_by = created_by
          learning_unit.save()
      learning_content_item.competency_ids = competency_ids
      learning_content_item.save()
      return learning_content_item.id
    else:
      Logger.debug("No competency found")
      raise Exception("Failed in parsing the given document")
  except FileNotFoundError:
    raise Exception(
        "No file found with the name - {}".format(parsed_output_json))
#pylint: disable=superfluous-parens
  except Exception as e: #pylint: disable=broad-except
    if (e.args):
      raise Exception(e)
    else:
      raise Exception("Internal server error. Failed to create Learning \
      content")
