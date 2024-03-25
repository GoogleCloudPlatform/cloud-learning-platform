"""
  Service for generic csv ingestion batch job
"""
import csv
from io import StringIO
from services.data_source import upsert_data_source_doc
from common.utils.gcs_adapter import get_blob_from_gcs_path
from common.models import (Skill, SkillServiceCompetency, Category, Domain,
                           SubDomain)
from common.utils.errors import ValidationError, ResourceNotFoundException
from common.utils.parent_child_nodes_handler import ParentChildNodesHandler
from common.utils.logging_handler import Logger
# pylint: disable = broad-exception-raised


def get_data_model(node_type):
  if node_type == "skill":
    data_model = Skill
  elif node_type == "competency":
    data_model = SkillServiceCompetency
  elif node_type == "category":
    data_model = Category
  elif node_type == "sub_domain":
    data_model = SubDomain
  elif node_type == "domain":
    data_model = Domain
  else:
    raise Exception(f"Invalid node type \"{node_type}\"")
  return data_model


def save_node_data(data, node_type):
  data_model = get_data_model(node_type)
  ParentChildNodesHandler.validate_parent_child_nodes_references(data)
  data_model_obj = data_model()
  data_model_obj = data_model_obj.from_dict(data)
  data_model_obj.uuid = ""
  data_model_obj.save()
  data_model_obj.uuid = data_model_obj.id
  data_model_obj.update()
  print(f"saved {node_type} with reference_id", data_model_obj.reference_id)

  doc_obj_fields = data_model_obj.get_fields(reformat_datetime=True)
  ParentChildNodesHandler.update_child_references(
      doc_obj_fields, data_model, operation="add")
  ParentChildNodesHandler.update_parent_references(
      doc_obj_fields, data_model, operation="add")

  return data_model_obj.to_dict()


def update_node_data(existing_data, new_data, node_type):
  data_model = get_data_model(node_type)
  existing_data_fields = existing_data.get_fields()

  ParentChildNodesHandler.compare_and_update_nodes_references(
      new_data, existing_data_fields, data_model)

  for key, value in new_data.items():
    existing_data_fields[key] = value
  for key, value in existing_data_fields.items():
    setattr(existing_data, key, value)

  existing_data.update()
  Logger.info(
    f"updated {node_type} with reference_id {new_data.get('reference_id')}")
  existing_data_fields = existing_data.get_fields(reformat_datetime=True)


def ingest_generic_csv(path_dict):
  """validates, transforms and saves data from csv to skill tree for skill,
  competency, sub_domain, domain nodes"""
  domain_uri = path_dict.get("domain_uri")
  sub_domain_uri = path_dict.get("sub_domain_uri")
  category_uri = path_dict.get("category_uri")
  competency_uri = path_dict.get("competency_uri")
  skill_uri = path_dict.get("skill_uri")
  source_name = path_dict.get("source_name")

  if domain_uri:
    domains_json_array = parse_csv(domain_uri)
    try:
      validate_domains_csv(domains_json_array)
    except Exception as e:
      raise Exception(str(e)) from e
    domains = domain_ingester(domains_json_array, source_name)

  if sub_domain_uri:
    sub_domains_json_array = parse_csv(sub_domain_uri)
    try:
      validate_sub_domains_csv(sub_domains_json_array)
    except Exception as e:
      raise Exception(str(e)) from e
    sub_domains = sub_domain_ingester(sub_domains_json_array, source_name)

  if category_uri:
    categories_json_array = parse_csv(category_uri)
    try:
      validate_categories_csv(categories_json_array)
    except Exception as e:
      raise Exception(str(e)) from e
    categories = category_ingester(categories_json_array, source_name)

  if competency_uri:
    competencies_json_array = parse_csv(competency_uri)
    try:
      validate_competencies_csv(competencies_json_array)
    except Exception as e:
      raise Exception(str(e)) from e
    competencies = competency_ingester(competencies_json_array, source_name)

  if skill_uri:
    skills_json_array = parse_csv(skill_uri)
    try:
      validate_skills_csv(skills_json_array)
    except Exception as e:
      raise Exception(str(e)) from e
    skills = skill_ingester(skills_json_array, source_name)

  ingestion_count = []

  if domain_uri:
    len_domain = str(domains) + " domains"
    ingestion_count.append(len_domain)

  if sub_domain_uri:
    len_sub_domain = str(sub_domains) + " sub domains"
    ingestion_count.append(len_sub_domain)

  if category_uri:
    len_category = str(categories) + " categories"
    ingestion_count.append(len_category)

  if competency_uri:
    len_competency = str(competencies) + " competencies"
    ingestion_count.append(len_competency)

  if skill_uri:
    len_skill = str(skills) + " skills"
    ingestion_count.append(len_skill)

  counts = ", ".join(ingestion_count)
  msg = f"Imported {counts}"
  response = {"success": True, "message": msg, "data": {}}
  return response


def parse_csv(csv_file_uri):
  blob = get_blob_from_gcs_path(csv_file_uri)
  json_array = parse_gcs_csv_file(blob)
  return json_array


def parse_gcs_csv_file(blob):
  """downloads csv from gcs and returns it as json"""
  # download file as bytes
  file_data = blob.download_as_bytes()
  byte_content = file_data
  content = byte_content.decode()
  file = StringIO(content)

  csv_reader = csv.DictReader(file, delimiter=",")
  return list(csv_reader)


def validate_skills_csv(data):
  """checks if all required columns are present in skill csv"""
  required_fields = ["id", "name", "description"]
  other_fields = [
      "aligned_competency", "aligned_domain", "aligned_sub_domain",
      "aligned_category", "keywords", "major_occupation", "minor_occupation",
      "broad_occupation", "detailed_occupation", "onet_alignment",
      "standard_alignment", "credential_alignment", "organization_alignment",
      "certifications", "author", "creator"
  ]

  # check for missing required fields
  for field in required_fields:
    if field not in data[0]:
      raise ValidationError\
        (f"Required column \"{field}\" is missing in skills csv")

  # validate if required fields are having some value
  for data_dict in data:
    for key in required_fields:
      if data_dict[key] == "":
        raise ValidationError(
            f"Some fields in required column \"{key}\" is empty in skill csv")

  # check for unknown fields
  for key, _ in data[0].items():
    if key not in required_fields and key not in other_fields:
      if not key.endswith("_skill_alignment_name") and not key.endswith(
          "_skill_alignment_id"):
        raise ValidationError(f"Unknown column \"{key}\" in skill csv")


def validate_competencies_csv(data):
  """checks if all required columns are present in competency csv"""
  required_fields = ["id", "description"]
  other_fields = [
      "subject_code", "level", "name", "course_code", "course_title",
      "aligned_domain", "aligned_sub_domain", "aligned_category",
      "major_occupation", "minor_occupation", "broad_occupation",
      "detailed_occupation", "onet_alignment", "standard_alignment",
      "credential_alignment", "aligned_competency", "organization_alignment"
  ]

  # check for missing required fields
  for field in required_fields:
    if field not in data[0]:
      raise ValidationError(
          f"Required column \"{field}\" is missing in competencies csv")

  # validate if required fields are having some value
  for data_dict in data:
    for key in required_fields:
      if data_dict[key] == "":
        raise ValidationError(
            f"Some fields in required column '{key}' is empty in competency csv"
        )

  # check for unknown fields
  for key, _ in data[0].items():
    if key not in required_fields and key not in other_fields:
      raise ValidationError(f"Unknown column \"{key}\" in competencies csv")


def validate_categories_csv(data):
  """checks if all required columns are present in category csv"""
  required_fields = ["id", "name"]
  other_fields = [
      "description", "keywords", "aligned_sub_domain", "aligned_domain"
  ]

  # check for unknown fields
  for key, _ in data[0].items():
    if key not in required_fields and key not in other_fields:
      raise ValidationError(f"Unknown column \"{key}\" in category csv")

  # check for missing required fields
  for field in required_fields:
    if field not in data[0]:
      raise ValidationError(
          f"Required column \"{field}\" is missing in categories csv")

  # validate if required fields are having some value
  for data_dict in data:
    for key in required_fields:
      if data_dict[key] == "":
        raise ValidationError(
            f"Some fields in required column \"{key}\" is empty in category csv"
        )


def validate_sub_domains_csv(data):
  """checks if all required columns are present in sub domain csv"""
  required_fields = ["id", "name"]
  other_fields = ["description", "keywords", "aligned_domain"]

  # check for missing required fields
  for field in required_fields:
    if field not in data[0]:
      raise ValidationError(
          f"Required column \"{field}\" is missing in sub_domains csv")

  # validate if required fields are having some value
  for data_dict in data:
    for key in required_fields:
      if data_dict[key] == "":
        raise ValidationError(f"Some fields in required column \"{key}\""
                              f"is empty in sub domain csv")

  # check for unknown fields
  for key, _ in data[0].items():
    if key not in required_fields and key not in other_fields:
      raise ValidationError(f"Unknown column \"{key}\" in sub domain csv")


def validate_domains_csv(data):
  """checks if all required columns are present in domain csv"""
  required_fields = ["id", "name"]
  other_fields = ["description", "keywords"]

  # check for missing required fields
  for field in required_fields:
    if field not in data[0]:
      raise ValidationError\
        (f"Required column \"{field}\" is missing in domains csv")

  # validate if required fields are having some value
  for data_dict in data:
    for key in required_fields:
      if data_dict[key] == "":
        raise ValidationError(
            f"Some fields in required column \"{key}\" is empty in domain csv")

  # check for unknown fields
  for key, _ in data[0].items():
    if key not in required_fields and key not in other_fields:
      raise ValidationError(f"Unknown column \"{key}\" in domain csv")


def domain_ingester(data_json, source_name):
  final_data = []
  for data in data_json:
    data_dict = {
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "keywords": keyword_extractor(data.get("keywords", [])),
        "reference_id": data.get("id"),
        "source_uri": source_name,
        "source_name": source_name,
        "child_nodes": {"sub_domains": []}
    }
    final_data.append(data_dict)
    try:
      existing_domain_with_ref_id = Domain.find_by_reference_id(data.get("id"))
      update_node_data(existing_domain_with_ref_id, data_dict, "domain")
    except ResourceNotFoundException:
      save_node_data(data_dict, "domain")
  # Insert/Update doc in data_sources collection after ingestion:
  _ = upsert_data_source_doc("domain", source_name)
  return len(final_data)


def sub_domain_ingester(data_json, source_name):
  final_data = []
  for data in data_json:
    data_dict = {
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "keywords": keyword_extractor(data.get("keywords", [])),
        "reference_id": data.get("id"),
        "parent_nodes": {
            "domains": extract_parent_nodes_for_sub_domain(data, source_name)
        },
        "child_nodes": {
          "categories": [],
          "competencies": []
        },
        "source_uri": source_name,
        "source_name": source_name
    }
    final_data.append(data_dict)
    try:
      existing_subdomain_with_ref_id = SubDomain.find_by_reference_id(
          data.get("id"))
      update_node_data(existing_subdomain_with_ref_id, data_dict, "sub_domain")
    except ResourceNotFoundException:
      save_node_data(data_dict, "sub_domain")
  # Insert/Update doc in data_sources collection after ingestion:
  _ = upsert_data_source_doc("sub_domain", source_name)
  return len(final_data)


def category_ingester(data_json, source_name):
  final_data = []
  for data in data_json:
    data_dict = {
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "keywords": keyword_extractor(data.get("keywords", [])),
        "reference_id": data.get("id"),
        "parent_nodes": {
            "sub_domains": extract_parent_nodes_for_category(data, source_name)
        },
        "child_nodes": {"competencies": []},
        "source_uri": source_name,
        "source_name": source_name
    }
    final_data.append(data_dict)
    try:
      existing_category_with_ref_id = Category.find_by_reference_id(
          data.get("id"))
      update_node_data(existing_category_with_ref_id, data_dict, "category")
    except ResourceNotFoundException:
      save_node_data(data_dict, "category")
  # Insert/Update doc in data_sources collection after ingestion:
  _ = upsert_data_source_doc("category", source_name)
  return len(final_data)


def competency_ingester(data_json, source_name):
  final_data = []
  for data in data_json:
    data_dict = {
        "subject_code": data.get("subject_code", ""),
        "level": data.get("level", ""),
        "reference_id": data.get("id"),
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "course_code": data.get("course_code", ""),
        "course_title": data.get("course_title", ""),
        "keywords": keyword_extractor(data.get("keywords", "")),
        "occupations": extract_occupations_data(data),
        "alignments": extract_alignments_for_competency_node(data),
        "parent_nodes": extract_parent_nodes_for_competency(data, source_name),
        "child_nodes": {"skills": []},
        "source_uri": source_name,
        "source_name": source_name
    }
    final_data.append(data_dict)
    try:
      existing_comp_with_ref_id = SkillServiceCompetency.find_by_reference_id(
          data.get("id"))
      update_node_data(existing_comp_with_ref_id, data_dict, "competency")
    except ResourceNotFoundException:
      save_node_data(data_dict, "competency")
  # Insert/Update doc in data_sources collection after ingestion:
  _ = upsert_data_source_doc("competency", source_name)
  return len(final_data)


def skill_ingester(data_json, source_name):
  final_data = []
  for data in data_json:
    data_dict = {
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "keywords": keyword_extractor(data.get("keywords", [])),
        "author": data.get("author", ""),
        "creator": data.get("creator", ""),
        "alignments": extract_alignments_for_skill_node(data),
        "occupations": extract_occupations_data(data),
        "organizations": [],
        "certifications": extract_certification(data.get("certifications",)),
        "onet_job": data.get("onet_alignment", ""),
        "type": {},
        "parent_nodes": {
            "competencies": extract_parent_nodes_for_skill(data, source_name)
        },
        "reference_id": data.get("id"),
        "source_uri": source_name,
        "source_name": source_name
    }
    final_data.append(data_dict)
    try:
      existing_skill_with_ref_id = Skill.find_by_reference_id(data.get("id"))
      update_node_data(existing_skill_with_ref_id, data_dict, "skill")
    except ResourceNotFoundException:
      save_node_data(data_dict, "skill")
  # Insert/Update doc in data_sources collection after ingestion:
  _ = upsert_data_source_doc("skill", source_name)
  return len(final_data)


def keyword_extractor(keywords_string: str):
  keywords = keywords_string.split(",")
  if len(keywords) == 1 and keywords[0] == "":
    keywords = []
  keywords = [i.strip() for i in keywords]
  return keywords


def extract_certification(certifications_string: str):
  certifications = certifications_string.split(",")
  if len(certifications) == 1 and certifications[0] == "":
    certifications = []
  certifications = [i.strip() for i in certifications]
  return certifications


def extract_alignments_for_competency_node(skill_data):
  standard_alignment = {}
  if skill_data.get("standard_alignment"):
    standard_alignment = {"aligned": skill_data.get("standard_alignment", "")}

  credential_alignment = {}
  if skill_data.get("credential_alignment"):
    credential_alignment = {
        "aligned": skill_data.get("credential_alignment", "")
    }

  organizational_alignment = {}
  if skill_data.get("organization_alignment"):
    organizational_alignment = {
        "aligned": skill_data.get("organization_alignment", "")
    }

  o_net_alignment = {}
  if skill_data.get("onet_alignment"):
    o_net_alignment = {"aligned": skill_data.get("onet_alignment", "")}

  data = {
      "standard_alignment": standard_alignment,
      "credential_alignment": credential_alignment,
      "organizational_alignment": organizational_alignment,
      "o_net_alignment": o_net_alignment,
  }

  return data


def extract_alignments_for_skill_node(skill_data):
  standard_alignment = {}
  if skill_data.get("standard_alignment"):
    standard_alignment = {"aligned": skill_data.get("standard_alignment", "")}

  credential_alignment = {}
  if skill_data.get("credential_alignment"):
    credential_alignment = {
        "aligned": skill_data.get("credential_alignment", "")
    }

  organizational_alignment = {}
  if skill_data.get("organization_alignment"):
    organizational_alignment = {
        "aligned": skill_data.get("organization_alignment", "")
    }

  data = {
      "standard_alignment": standard_alignment,
      "credential_alignment": credential_alignment,
      "organizational_alignment": organizational_alignment,
      "skill_alignment": extract_data_for_skill_alignment(skill_data),
      "knowledge_alignment": {},
      "role_alignment": {}
  }

  return data


def extract_data_for_skill_alignment(skill_data: dict):
  valid_external_alignments = ["osn", "snhu", "emsi"]
  skill_alignment_data = {}
  temp_data = {}
  for key, value in skill_data.items():
    if key.endswith("_skill_alignment_name"):
      registry = key.split("_")[0]
      if not temp_data.get(registry):
        temp_data[registry] = {}
      temp_data[registry]["name"] = value

    if key.endswith("_skill_alignment_id"):
      registry = key.split("_")[0]
      if not temp_data.get(registry):
        temp_data[registry] = {}
      temp_data[registry]["id"] = value

  for key, value in temp_data.items():
    if value.get("id") or value.get("name"):
      pass
    else:
      continue
    if key in valid_external_alignments:
      skill_alignment_data[key] = {
          "aligned": [{
              "id": value.get("id", ""),
              "name": value.get("name", ""),
              "score": 1.0  # since human aligned this skill
          }],
          "suggested": []
      }

  return skill_alignment_data


def extract_occupations_data(skill_data):
  occupations_major_group = skill_data.get("major_occupation", "").split(",")
  if len(occupations_major_group) == 1 and occupations_major_group[0] == "":
    occupations_major_group = []
  occupations_major_group = [i.strip() for i in occupations_major_group]

  occupations_minor_group = skill_data.get("minor_occupation", "").split(",")
  if len(occupations_minor_group) == 1 and occupations_minor_group[0] == "":
    occupations_minor_group = []
  occupations_minor_group = [i.strip() for i in occupations_minor_group]

  broad_occupation = skill_data.get("broad_occupation", "").split(",")
  if len(broad_occupation) == 1 and broad_occupation[0] == "":
    broad_occupation = []
  broad_occupation = [i.strip() for i in broad_occupation]

  detailed_occupation = skill_data.get("detailed_occupation", "").split(",")
  if len(detailed_occupation) == 1 and detailed_occupation[0] == "":
    detailed_occupation = []
  detailed_occupation = [i.strip() for i in detailed_occupation]

  occupations = {
      "occupations_major_group": occupations_major_group,
      "occupations_minor_group": occupations_minor_group,
      "broad_occupation": broad_occupation,
      "detailed_occupation": detailed_occupation
  }
  return occupations


def extract_parent_nodes_for_skill(data, source_name):
  parent_nodes = []

  if data.get("aligned_competency"):
    temp_parent_nodes = data.get("aligned_competency").split(",")
    if len(temp_parent_nodes) == 1 and temp_parent_nodes[0] == "":
      temp_parent_nodes = []
    temp_parent_nodes = [i.strip() for i in temp_parent_nodes]

    for pn in temp_parent_nodes:
      existing_comp_with_name = SkillServiceCompetency.find_by_name(pn)
      if not existing_comp_with_name:
        try:
          existing_comp_with_ref_id = SkillServiceCompetency\
                                        .find_by_reference_id(pn)
          parent_nodes.append(existing_comp_with_ref_id.to_dict().get("uuid"))
        except ResourceNotFoundException:
          comp = {
              "name": pn,
              "description": pn,
              "keywords": [],
              "level": "",
              "subject_code": "",
              "course_code": "",
              "course_title": "",
              "category": "",
              "alignments": {},
              "occupations": {},
              "parent_nodes": {
                  "categories": [],
                  "sub_domains": []
              },
              "reference_id": pn,
              "source_uri": source_name,
              "source_name": source_name
          }
          saved_comp = save_node_data(comp, "competency")
          parent_nodes.append(saved_comp.get("uuid"))
      else:
        for existing_comp_name in existing_comp_with_name:
          parent_nodes.append(
              existing_comp_name.get_fields(reformat_datetime=True).get("uuid"))
  return parent_nodes


def parent_name_to_data_model_mapping(parent_name):
  data_model_mapping = {
      "aligned_category": Category,
      "aligned_sub_domain": SubDomain,
      "aligned_domain": Domain
  }
  return data_model_mapping[parent_name]


def extract_and_create_parent_nodes(data, source_name, parent_name):
  parent_nodes = []
  if data.get(parent_name):
    temp_parent_nodes = data.get(parent_name).split(",")
    if len(temp_parent_nodes) == 1 and temp_parent_nodes[0] == "":
      temp_parent_nodes = []
    temp_parent_nodes = [i.strip() for i in temp_parent_nodes]

    for pn in temp_parent_nodes:
      parent_class = parent_name_to_data_model_mapping(parent_name)
      existing_parent_with_name = parent_class.find_by_name(pn)
      if not existing_parent_with_name:
        try:
          existing_parent_with_ref_id = parent_class.find_by_reference_id(pn)
          parent_nodes.append(existing_parent_with_ref_id.to_dict().get("uuid"))
        except ResourceNotFoundException:
          parent_dict = {
              "name": pn,
              "description": pn,
              "keywords": [],
              "reference_id": pn,
              "source_uri": source_name,
              "source_name": source_name
          }
          if parent_name == "aligned_sub_domain":
            parent_dict.update({
                "parent_nodes": {
                    "domains": []
                },
                "child_nodes": {
                    "categories": [],
                    "competencies": []
                }
            })
          elif parent_name == "aligned_domain":
            parent_dict.update({"child_nodes": {"sub_domains": []}})
          elif parent_name == "aligned_category":
            parent_dict.update({
                "parent_nodes": {
                    "sub_domains": []
                },
                "child_nodes": {
                    "competencies": []
                }
            })
          saved_parent = save_node_data(
              parent_dict,
              parent_name.replace("aligned_", "").replace("_", ""))
          parent_nodes.append(saved_parent.get("uuid"))
      else:
        for existing_parent in existing_parent_with_name:
          parent_nodes.append(
              existing_parent.get_fields(reformat_datetime=True).get("uuid"))
  return parent_nodes


def extract_parent_nodes_for_competency(data, source_name):
  parent_categories = extract_and_create_parent_nodes(data, source_name,
                                                      "aligned_category")
  parent_sub_domain = extract_and_create_parent_nodes(data, source_name,
                                                      "aligned_sub_domain")
  _ = extract_and_create_parent_nodes(data, source_name, "aligned_domain")
  return {"categories": parent_categories, "sub_domains": parent_sub_domain}


def extract_parent_nodes_for_category(data, source_name):
  parent_nodes = []

  if data.get("aligned_sub_domain"):
    temp_parent_nodes = data.get("aligned_sub_domain").split(",")
    if len(temp_parent_nodes) == 1 and temp_parent_nodes[0] == "":
      temp_parent_nodes = []
    temp_parent_nodes = [i.strip() for i in temp_parent_nodes]

    for pn in temp_parent_nodes:
      existing_subdomain_with_name = SubDomain.find_by_name(pn)
      if not existing_subdomain_with_name:
        try:
          existing_domain_with_ref_id = SubDomain.find_by_reference_id(pn)
          parent_nodes.append(existing_domain_with_ref_id.to_dict().get("uuid"))
        except ResourceNotFoundException:
          sub_domain = {
              "name": pn,
              "description": pn,
              "keywords": [],
              "parent_nodes": {
                  "domains": []
              },
              "reference_id": pn,
              "source_uri": source_name,
              "source_name": source_name
          }
          saved_sub_domain = save_node_data(sub_domain, "sub_domain")
          parent_nodes.append(saved_sub_domain.get("uuid"))
      else:
        for existing_subdomain_name in existing_subdomain_with_name:
          parent_nodes.append(
              existing_subdomain_name.get_fields(
                  reformat_datetime=True).get("uuid"))
  return parent_nodes


def extract_parent_nodes_for_sub_domain(data, source_name):
  parent_nodes = []

  if data.get("aligned_domain"):
    temp_parent_nodes = data.get("aligned_domain").split(",")
    if len(temp_parent_nodes) == 1 and temp_parent_nodes[0] == "":
      temp_parent_nodes = []
    temp_parent_nodes = [i.strip() for i in temp_parent_nodes]

    for pn in temp_parent_nodes:
      existing_domain_with_name = Domain.find_by_name(pn)
      if not existing_domain_with_name:
        try:
          existing_domain_with_ref_id = Domain.find_by_reference_id(pn)
          parent_nodes.append(existing_domain_with_ref_id.to_dict().get("uuid"))
        except ResourceNotFoundException:
          domain = {
              "name": pn,
              "description": pn,
              "keywords": [],
              "reference_id": pn,
              "source_uri": source_name,
              "source_name": source_name
          }
          saved_domain = save_node_data(domain, "domain")
          parent_nodes.append(saved_domain.get("uuid"))
      else:
        for existing_domain_name in existing_domain_with_name:
          parent_nodes.append(
              existing_domain_name.get_fields(
                  reformat_datetime=True).get("uuid"))
  return parent_nodes
