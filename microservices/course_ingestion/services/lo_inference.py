"""CRUD for learning objective"""

from common.models import LearningObjective, SubCompetency
from common.utils.errors import ResourceNotFoundException
from services.clustering.hierarchical_clustering import (
    get_blooms_titles, compress_text_for_title_generation)
from services.sc_inference import SubCompetencyService
#pylint: disable=redefined-builtin,broad-exception-raised,protected-access


class LearningObjectiveService():
  """LO creation class"""

  def create_learning_objective(self, sc_id, learning_objective):
    """creates learning_objective"""
    lo = LearningObjective()
    for key, value in learning_objective.items():
      if key == "text":
        setattr(lo,key,"<p>".join(value))
      else:
        setattr(lo, key, value)
    parent = SubCompetency.find_by_id(sc_id)
    if parent:
      setattr(lo, "parent_node", parent)
    lo.save()
    return self.get_learning_objective(lo.id)

  def get_learning_objective(self, id):
    """returns learning_objective"""
    lo = LearningObjective.find_by_id(id)
    try:
      lo_item = lo.get_fields(reformat_datetime=True)
      lo_item["id"] = lo.id
      if lo_item["text"]:
        lo_item["text"] = lo_item["text"].split("<p>")
      if "parent_node" in lo_item:
        lo_item["parent_node"] = lo.parent_node.ref.path
      return lo_item
    except (KeyError, TypeError) as e:
      raise Exception("Failed to fetch learning objective") from e

  def get_all_learning_objectives(self, sc_id):
    """returns all_learning_objectives"""
    lo_list = []
    sc = SubCompetency.find_by_id(sc_id)
    try:
      sc.load_children()
      for lo in sc.learning_objectives:
        lo_item = lo.get_fields(reformat_datetime=True)
        lo_item["id"] = lo.id
        if "parent_node" in lo_item:
          lo_item["parent_node"] = lo.parent_node.ref.path
        if lo_item["text"]:
          lo_item["text"] = lo_item["text"].split("<p>")
        lo_list.append(lo_item)
      return lo_list
    except (KeyError, TypeError) as e:
      raise Exception("Failed to fetch all learning objectives") from e

  def get_learning_objective_text(self, lo):
    """returns learning_objective_text"""
    try:
      lo_text = []
      lo.load_children()
      for lu in lo.learning_units:
        lo_text.extend(lu.text.split("<p>"))
      return lo_text
    except Exception as e:
      raise Exception("Internal server error") from e

  async def update_learning_objective_text(self, id):
    """updates LO text when LU text gets updated"""
    lo = LearningObjective.find_by_id(id)
    try:
      lo_fields = lo.get_fields()
      lo_fields["parent_node"] = lo.parent_node.ref.path
      lo.load_children()
      lo_text = []
      for i in lo.children_nodes:
        lo_text.extend(i.text.split("<p>"))
      lo_fields["text"] = lo_text
      await self.update_learning_objective(
          id, lo_fields, delete_child_tree=False)
    except (TypeError, KeyError) as e:
      raise Exception("Failed to update Learning objective") from e

  async def update_learning_objective(self,
                                      id,
                                      learning_objective,
                                      delete_child_tree=True):
    """updates learning_objective"""
    lo = LearningObjective.find_by_id(id)
    try:
      lo_fields = lo.get_fields()
      lo_fields["parent_node"] = lo.parent_node.ref.path
      invalidate = False
      for key, value in learning_objective.items():
        if key != "text":
          lo_fields[key] = value
        if key == "text" and "<p>".join(value) != lo.text:
          lo_fields["text"] = "<p>".join(value)
          if "title" not in learning_objective:
            text_for_title = await compress_text_for_title_generation(value)
            lo_fields["title"] = get_blooms_titles(
              [text_for_title], 48, n_titles=1)[0][0]
          if delete_child_tree:
            lo.delete_child_tree()
            invalidate = True
      for key, value in lo_fields.items():
        if key == "parent_node":
          parent = lo.parent_node.get().__class__.collection.get(value)
          if parent:
            setattr(lo, key, parent)
          else:
            raise ResourceNotFoundException(
                "Sub competency with this ID does not exist")
        else:
          setattr(lo, key, value)
      if invalidate:
        setattr(lo, "is_valid", False)
      lo.update()
      return self.get_learning_objective(lo.id)
    except (TypeError, KeyError) as e:
      raise Exception("Failed to update Learning objective") from e

  def delete_learning_objective(self, id):
    """deletes learning_objective"""
    lo = LearningObjective.find_by_id(id)
    sc_service = SubCompetencyService()
    sc_id = lo.parent_node.ref.path.split("/")[1]
    lo.delete_tree()
    sc_service.update_sub_competency_lu_count(sc_id)
