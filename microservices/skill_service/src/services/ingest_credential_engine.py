"""
  Service for credential engine data ingestion route
"""
import requests
from common.models import SkillServiceCompetency, Category
from common.utils.logging_handler import Logger
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
# pylint: disable = broad-except


def ingest_credential_engine(links):
  """fetches data from the links passed as parameters and
    transforms and saves the fetched data into competency model"""
  collected_raw_data = []
  transformed_data = []

  for link in links:
    # check for @type
    req = requests.get(link, timeout=10)
    response_data = req.json()
    resp_type = response_data.get("@type")

    if resp_type == "ceasn:CompetencyFramework":
      link = link.replace("resources", "graph")
      req = requests.get(link, timeout=10)
      response_data = req.json()
      graph_data = []
      graph_data = response_data.get("@graph", [])
      # remove first element from the graph object as it explains
      # competency framework and its childs
      graph_data.pop(0)
      collected_raw_data.extend(graph_data)

  try:
    transformed_data = parse_competency_data(collected_raw_data)
    return {
        "success": transformed_data,
        "message": "Data ingestion complete",
        "data": {}
    }
  except Exception as e:
    return {"success": False, "message": str(e), "data": {}}


def parse_competency_data(competency_array):
  """transform the passed competency_array as per
  skill model and return as json"""
  raw_categories = []
  categories = []
  competencies = []
  for competency in competency_array:
    if competency.get("@type") == "ceasn:Competency":
      final_comp = {}
      if competency.get("ceasn:competencyLabel"):
        if competency.get("ceasn:competencyLabel").get("en-us"):
          final_comp["name"] = competency.get("ceasn:competencyLabel").get(
              "en-us")
        else:
          final_comp["name"] = competency.get("ceasn:competencyLabel")
      else:
        final_comp["name"] = "no label"
      if competency.get("ceasn:competencyText"):
        if competency.get("ceasn:competencyText").get("en-us"):
          final_comp["description"] = competency.get(
              "ceasn:competencyText").get("en-us")
        else:
          final_comp["description"] = competency.get("ceasn:competencyText")
      else:
        final_comp["description"] = "no text"

      final_comp["coded_notation"] = competency.get("ceasn:codedNotation",
                                                    "no coded notation")
      final_comp["reference_id"] = competency.get("ceterms:ctid", "no ctid")
      final_comp["source_uri"] = competency.get("@id", "no id")
      final_comp["type"] = competency.get("@type", "no type")
      final_comp["source_name"] = "credential_engine"
      final_comp["parent_nodes"] = {
                                    "categories": [],
                                    "sub_domains": []
                                  }
      final_comp["child_nodes"] = {"skills": []}

      if competency.get("ceasn:competencyCategory") and competency.get(
          "ceasn:competencyCategory").get("en-us"):
        comp_category_data = competency.get("ceasn:competencyCategory").get(
            "en-us")
        final_comp["parent_nodes"] = {
              "categories": [comp_category_data.split(":", 1)[1].strip()],
              "sub_domains": []
        }

        raw_categories.append(comp_category_data)
      competencies.append(final_comp)
  raw_categories = list(set(raw_categories))

  for category in raw_categories:
    final_category = {}
    category_code, category_name = category.split(":", 1)
    final_category["category_code"] = category_code
    final_category["name"] = category_name.strip()
    final_category["description"] = ""
    final_category["parent_nodes"] = {"sub_domains": []}
    final_category["child_nodes"] = {"competencies": []}
    final_category["reference_id"] = ""
    final_category["source_uri"] = ""
    final_category["type"] = "category"
    final_category["source_name"] = "credential_engine"
    categories.append(final_category)

  Logger.info("Ingesting Categories:")
  created_category_ids = []
  for category in categories:
    new_category = Category()
    new_category = new_category.from_dict(category)
    new_category.uuid = ""
    new_category.save()
    new_category.uuid = new_category.id
    new_category.update()
    created_category_ids.append(new_category.uuid)
    Logger.info(new_category.uuid)


  Logger.info("Ingesting Competencies:")
  for competency in competencies:
    if competency["parent_nodes"]["categories"]:
      parent_category_ids = []
      for category_id in created_category_ids:
        category_obj = Category.find_by_uuid(category_id)
        if category_obj.name in competency["parent_nodes"]["categories"]:
          parent_category_ids.append(category_id)
      competency["parent_nodes"]["categories"] = parent_category_ids

    ParentChildNodesHandler.validate_parent_child_nodes_references(competency)
    new_competency = SkillServiceCompetency()
    new_competency = new_competency.from_dict(competency)
    new_competency.uuid = ""
    new_competency.save()
    new_competency.uuid = new_competency.id
    new_competency.update()
    Logger.info(new_competency.uuid)
    competency_fields = new_competency.get_fields(reformat_datetime=True)
    ParentChildNodesHandler.update_child_references(
        competency_fields, SkillServiceCompetency, operation="add")
    ParentChildNodesHandler.update_parent_references(
        competency_fields, SkillServiceCompetency, operation="add")
  return True
