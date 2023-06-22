"""CRUD for Learning Unit"""

from common.models import LearningObjective, LearningUnit
from common.utils.errors import ResourceNotFoundException
from services.clustering.hierarchical_clustering import get_topics
from services.clustering.hierarchical_clustering import (
    create_recursive_topic_tree, get_blooms_titles,
    compress_text_for_title_generation)
from services.import_learning_content import update_clustering_collections
import ast
from services.lo_inference import LearningObjectiveService
from services.triple_inference import TripleService
from services.sc_inference import SubCompetencyService
#pylint: disable=protected-access,broad-exception-raised,redefined-builtin


class LearningUnitService():
  """Learning Unit class"""

  def __init__(self):
    self.triple_service = TripleService()
    self.sc_service = SubCompetencyService()

  def create_learning_unit(self, lo_id, learning_unit):
    """creates learning_unit"""
    lu = LearningUnit()
    if "text" in learning_unit.keys():
      text = learning_unit["text"]
      topics = []
      for i in text:
        topics.extend(get_topics(i))
      learning_unit["text"] = "<p>".join(learning_unit["text"])
      learning_unit["topics"] = str(topics)
    for key, value in learning_unit.items():
      setattr(lu, key, value)
    parent = LearningObjective.find_by_id(lo_id)
    if parent:
      setattr(lu, "parent_node", parent)
    lu.save()
    self.sc_service.update_sub_competency_lu_count(
     lu.parent_node.get().parent_node.ref.path.split("/")[1])
    self.triple_service.create_triples_from_lu(lu.id)
    return self.get_learning_unit(lu.id)

  def get_learning_unit(self, id):
    """returns learning_unit"""
    lu = LearningUnit.find_by_id(id)
    try:
      lu_item = lu.get_fields(reformat_datetime=True)
      lu_item["id"] = lu.id
      if "parent_node" in lu_item:
        lu_item["parent_node"] = lu.parent_node.ref.path
      if "text" in lu_item:
        lu_item["text"] = lu_item["text"].split("<p>")
      if lu_item["topics"]:
        lu_item["topics"] = ast.literal_eval(lu_item["topics"])
      lu_item["triples"] = self.triple_service.get_all_triples(lu.id)
      return lu_item
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch learning units") from e

  def get_all_learning_units(self, lo_id):
    """returns all learning_units"""
    lu_list = []
    lo = LearningObjective.find_by_id(lo_id)
    try:
      lo.load_children()
      for lu in lo.learning_units:
        lu_item = lu.get_fields(reformat_datetime=True)
        lu_item["id"] = lu.id
        if "parent_node" in lu_item:
          lu_item["parent_node"] = lu.parent_node.ref.path
        if "text" in lu_item:
          lu_item["text"] = lu_item["text"].split("<p>")
        if lu_item["topics"]:
          lu_item["topics"] = ast.literal_eval(lu_item["topics"])
        lu_item["triples"] = self.triple_service.get_all_triples(lu.id)
        lu_list.append(lu_item)
      return lu_list
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch learning unit") from e

  async def update_learning_unit(self, id, learning_unit):
    """updates learning_unit"""
    lu = LearningUnit.find_by_id(id)
    try:
      lu_fields = lu.get_fields()
      lu_fields["parent_node"] = lu.parent_node.ref.path
      update_lo_text = False
      for key, value in learning_unit.items():
        if key != "text":
          lu_fields[key] = value
        if key == "text":
          lu_fields["text"] = "<p>".join(value)
          lu_fields["coref_text"] = ""
          if "<p>".join(value) != lu.text:
            text_for_title = await compress_text_for_title_generation(value)
            lu_fields["title"] = get_blooms_titles(
              [text_for_title], 48, n_titles=1)[0][0]
            lu_fields["topics"] = str(
                get_topics(lu_fields["text"].replace("<p>", " ")))
            update_lo_text = True
      for key, value in lu_fields.items():
        if key == "parent_node":
          parent = lu.parent_node.get().__class__.collection.get(value)
          if parent:
            setattr(lu, key, parent)
          else:
            raise ResourceNotFoundException(
                "Learning objective with this ID does not exist")
        else:
          setattr(lu, key, value)
      lu.update()
      if update_lo_text:
        lo_service = LearningObjectiveService()
        await lo_service.update_learning_objective_text(
            lu.parent_node.ref.path.split("/")[1])
        self.triple_service.create_triples_from_lu(lu.id)
      return self.get_learning_unit(lu.id)
    except (TypeError, KeyError) as e:
      raise Exception("Failed to update leaning unit") from e

  def delete_learning_unit(self, id):
    """deletes learning_unit"""
    lu = LearningUnit.find_by_id(id)
    try:
      sc_id = lu.parent_node.get().parent_node.ref.path.split("/")[1]
      lu.delete_tree()
      self.sc_service.update_sub_competency_lu_count(sc_id)
    except Exception as e:
      raise Exception("Internal server error") from e

  def add_triples(self, topic_tree, batch_size=5):
    l = len(topic_tree)
    for i in range(0, l, batch_size):
      start = i
      end = min(i + batch_size, l)
      lu_text_list = [
          lu["text"].replace("<p>", " ") for lu in topic_tree[start:end]
      ]
      lu_wise_triples = self.triple_service.generate_triples(lu_text_list)
      for j in range(start, end):
        topic_tree[j]["triples"] = lu_wise_triples[j - start]
    return topic_tree

  async def create_lu_from_lo(self, lo_id, request_body):
    """creates all possible lus along with titles
    using clustering for a given lo"""
    lo = LearningObjective.find_by_id(lo_id)
    created_by = request_body.get("created_by", "")
    last_modified_by = request_body.get("last_modified_by", "")
    create_triples = request_body.get("create_triples",False)
    paragraphs = lo.text.split("<p>")
    topic_tree = await create_recursive_topic_tree(
        paragraphs, node_level="learning_objective")
    if create_triples:
      topic_tree = self.add_triples(topic_tree)
    response = await update_clustering_collections("learning_objective",
      lo_id, topic_tree, created_by, last_modified_by)
    return {"response": response}
