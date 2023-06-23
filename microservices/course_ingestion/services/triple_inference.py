"""CRUD for Sub Competency"""

import json
import requests
from config import SERVICES
from common.models import Triple, LearningUnit
#pylint: disable=redefined-builtin,broad-exception-raised
#pylint: disable=protected-access


class TripleService():
  """Triple level CRUD operations class"""

  def _extract_triples_from_text(self, texts):
    try:
      prediction = json.loads(
          requests.post(
              url="http://{}:{}/triple-extraction/api/v1/predict"
              .format(
                  SERVICES["triple-extraction"]["host"],
                  SERVICES["triple-extraction"]["port"],
              ),
              json={
                  "texts": texts
              },
          ).content)["data"]
      return prediction["triples"]
    except ConnectionError as e:
      raise Exception("Failed to connect with triple \
        extraction microservice") from e
    except (TypeError, KeyError) as e:
      raise Exception("Internal server error") from e

  def generate_triples(self, lu_text_list, top_n=10):
    try:
      top_n_triples_list = []
      extracted_triples_list = self._extract_triples_from_text(lu_text_list)
      for extracted_triples in extracted_triples_list:
        triples = []
        for data in extracted_triples:
          triple_object_list = data["triples"]
          for triple_object in triple_object_list:
            triple_object["sentence"] = data["sentence"]
          triples.extend(triple_object_list)
        top_n_triples = sorted(
            triples, key=lambda x: x["confidence"], reverse=True)[:top_n]
        top_n_triples_list.append(top_n_triples)
      return top_n_triples_list
    except Exception:
      top_n_triples_list = [[]]*len(lu_text_list)
      return top_n_triples_list

  def create_triples_from_lu(self, lu_id, top_n=10, request_body = None):
    if lu_id:
      lu = LearningUnit.find_by_id(lu_id)
      lu.delete_child_tree()
      lu_text = lu.text.replace("<p>", " ")
      new_triples = self.generate_triples([lu_text], top_n=top_n)[0]
      for triple in new_triples:
        new_triple = Triple()
        for key, value in triple.items():
          setattr(new_triple, key, value)
        setattr(new_triple, "parent_node", lu)
        if request_body:
          setattr(
            new_triple, "created_by", request_body.get("created_by", ""))
          setattr(
            new_triple, "last_modified_by", request_body.get(
              "last_modified_by", ""))
        new_triple.save()
        triple["id"] = new_triple.id
        triple["parent_node"] = new_triple.parent_node.ref.path
      return new_triples
    else:
      raise Exception("Learning unit ID is missing from request body")

  def create_triple(self, lu_id, triple_item):
    """creates triples"""
    lu = LearningUnit.find_by_id(lu_id)
    new_triple = Triple()
    for key, value in triple_item.items():
      setattr(new_triple, key, value)
    setattr(new_triple, "parent_node", lu)
    new_triple.save()
    triple_item["id"] = new_triple.id
    triple_item["parent_node"] = new_triple.parent_node.ref.path
    return triple_item

  def get_triple(self, id):
    """gets a single triple"""
    triple = Triple.find_by_id(id)
    try:
      triple_item = triple.get_fields(reformat_datetime=True)
      triple_item["id"] = triple.id
      if "parent_node" in triple_item:
        triple_item["parent_node"] = triple.parent_node.ref.path
      return triple_item
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch the triple") from e

  def get_all_triples(self, lu_id):
    """returns all triples"""
    lu = LearningUnit.find_by_id(lu_id)
    try:
      lu.load_children()
      triples_list = []
      for triple in lu.triples:
        triple_item = triple.get_fields(reformat_datetime=True)
        triple_item["id"] = triple.id
        if "parent_node" in triple_item:
          triple_item["parent_node"] = triple.parent_node.ref.path
        triples_list.append(triple_item)
      return triples_list
    except (TypeError, KeyError) as e:
      raise Exception("Failed to fetch all triples") from e

  def update_triple(self, id, triple_item):
    """upadates a triple"""
    triple = Triple.find_by_id(id)
    try:
      triple_fields = triple.get_fields()
      triple_fields["parent_node"] = triple.parent_node.ref.path
      for key, value in triple_item.items():
        triple_fields[key] = value
      for key, value in triple_fields.items():
        if key == "parent_node":
          parent = LearningUnit.collection.get(value)
          if parent:
            value = parent
          else:
            raise Exception(
                "Invalid parent node. Learning unit does not exist")
        setattr(triple, key, value)
      triple.update()
      return self.get_triple(triple.id)
    except (KeyError, TypeError) as e:
      raise Exception("Failed to update triple") from e

  def delete_triple(self, id):
    """deletes triple"""
    triple = Triple.find_by_id(id)
    triple.delete_by_id(id)
