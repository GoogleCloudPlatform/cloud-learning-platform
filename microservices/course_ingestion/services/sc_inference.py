"""CRUD for Sub Competency"""

from common.models import Competency, SubCompetency

#pylint: disable=redefined-builtin,broad-exception-raised,protected-access


class SubCompetencyService():
  """Sub Competency creation class"""

  def create_sub_competency(self, competency_id, sub_competency):
    """creates sub_competency"""
    sc = SubCompetency()
    for key, value in sub_competency.items():
      setattr(sc, key, value)
    parent = Competency.find_by_id(competency_id)
    if parent:
      setattr(sc, "parent_node", parent)
    sc.save()
    return self.get_sub_competency(sc.id)

  def get_sub_competency(self, id,is_text_required=False):
    """returns sub_competency"""
    sc = SubCompetency.find_by_id(id)
    try:
      subcompetency_item = sc.get_fields(reformat_datetime=True)
      subcompetency_item["id"] = sc.id
      if "parent_node" in subcompetency_item:
        subcompetency_item["parent_node"] = sc.parent_node.ref.path
      if is_text_required:
        sc.load_children()
        subcompetency_text = []
        for learning_objective in sc.learning_objectives:
          subcompetency_text.extend(learning_objective.text.split("<p>"))
        subcompetency_item["text"] = subcompetency_text
      return subcompetency_item
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch sub Competency") from e

  def get_all_sub_competencies(self, sc_id):
    """returns all sub_competencies"""
    sc_list = []
    competency = Competency.find_by_id(sc_id)
    try:
      competency.load_children()
      for sc in competency.sub_competencies:
        subcompetency_item = sc.get_fields(reformat_datetime=True)
        subcompetency_item["id"] = sc.id
        if "parent_node" in subcompetency_item:
          subcompetency_item["parent_node"] = sc.parent_node.ref.path
        sc_list.append(subcompetency_item)
      return sc_list
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch all sub competencies") from e

  def update_sub_competency(self, id, sub_competency):
    """upadtes sub_competency"""
    sc = SubCompetency.find_by_id(id)
    try:
      sc_fields = sc.get_fields()
      sc_fields["parent_node"] = sc.parent_node.ref.path
      for key, value in sub_competency.items():
        sc_fields[key] = value
      for key, value in sc_fields.items():
        if key == "parent_node":
          parent = sc.parent_node.get().__class__.collection.get(value)
          setattr(sc, key, parent)
        else:
          setattr(sc, key, value)
      sc.update()
      return self.get_sub_competency(sc.id)
    except (KeyError, TypeError) as e:
      raise Exception("Failed to update sub competency") from e

  def delete_sub_competency(self, id):
    """deletes sub competency"""
    sc = SubCompetency.find_by_id(id)
    sc.delete_tree()

  def update_sub_competency_lu_count(self,id):
    """Updates total learning units count for the given sub competency"""
    sc = SubCompetency.find_by_id(id)
    sc.load_tree()
    total_lus = 0
    for lo in sc.children_nodes:
      total_lus+=len(lo.children_nodes)
    sc.parent_node = sc.parent_node.get()
    sc.total_lus = total_lus
    sc.update()
