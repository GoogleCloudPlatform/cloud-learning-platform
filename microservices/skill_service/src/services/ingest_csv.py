"""
  Service for following routes:
  /import/local-csv
  /import/gcs-csv
"""
import csv
from io import StringIO
from common.utils.gcs_adapter import get_blob_from_gcs_path
from common.models import Skill, SkillServiceCompetency, Domain, SubDomain
from services.data_source import upsert_data_source_doc
# pylint: disable = broad-exception-raised


def ingest_csv(path_dict):
  """validates, transforms and saves competencies and
  skills json as skill tree"""
  competency_uri = path_dict.get("competency_uri")
  skill_uri = path_dict.get("skill_uri")

  if competency_uri:
    competencies_json_array = parse_and_validate_competency_csv(competency_uri)

    domains = import_domains(competencies_json_array)
    subdomains = import_subdomains(competencies_json_array)
    competencies = import_competencies(competencies_json_array)

  if skill_uri:
    skills_json_array = parse_and_validate_skill_csv(skill_uri)

    skills = import_skills(skills_json_array)

  msg = "Imported"
  if competency_uri:
    len_domains = str(len(domains)) + " domains"
    len_subdomains = str(len(subdomains)) + " subdomains"
    len_competencies = str(len(competencies)) + " competencies"
    msg = f"{msg} {len_domains}, {len_subdomains}, {len_competencies}"

  if skill_uri:
    msg = f"{msg} {len(skills)} skills"

  response = {"success": True, "message": msg, "data": {}}
  return response


def parse_and_validate_competency_csv(competency_uri):
  blob = get_blob_from_gcs_path(competency_uri)
  competencies_json_array = parse_gcs_csv_file(blob)
  try:
    validate_competencies_csv(competencies_json_array)
  except Exception as e:
    raise Exception(str(e)) from e
  return competencies_json_array


def parse_and_validate_skill_csv(skill_uri):
  blob = get_blob_from_gcs_path(skill_uri)
  skills_json_array = parse_gcs_csv_file(blob)
  try:
    validate_skills_csv(skills_json_array)
  except Exception as e:
    raise Exception(str(e)) from e
  return skills_json_array


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
  """checks if all required columns are present in skills csv"""
  fields = [
      "Skill", "SkillStatement", "CompetencyAlignment", "SkillCode", "Domain",
      "SubDomain", "Category", "Keyword", "OccupationsMajorGroup",
      "OccupationsMinorGroup", "BroadOccupation", "DetailedOccupation",
      "ONETJob", "StandardAlignment", "CredentialAlignment",
      "ExternalSkillAlignment", "OrganizationalAlignment"
  ]
  for field in fields:
    if field not in data[0]:
      raise Exception(f"{field} field is missing in skills csv")


def validate_competencies_csv(data):
  """checks if all required columns are present in skills csv"""
  fields = [
      "CompetencyNo.", "SubjectCode", "Level", "CompCode", "ShortTitle",
      "Statement", "CourseCode", "CourseTitle", "Domain", "SubDomain",
      "Category", "Major Occupation", "Minor Occupation", "Broad Occupation",
      "Detailed Occupation", "O*Net Alignment", "Standard Alignment",
      "Credential Alignment", "External Competency Alignment",
      "External Skill Alignment", "Organization Alignment"
  ]
  for field in fields:
    if field not in data[0]:
      raise Exception(f"{field} field is missing in competencies csv")


def import_skills(skills_json_array):
  """extracts and saves the skills as per skill fireo model"""
  skill_competency_mapping = {}
  inserted_skills = []
  for skill in skills_json_array:
    comp_code = skill.get("CompetencyAlignment")
    skill_code = skill.get("SkillCode")

    if skill_competency_mapping.get(skill_code):
      if comp_code not in skill_competency_mapping.get(skill_code).get(
          "parent_nodes")["competencies"]:
        skill_competency_mapping[skill_code]["parent_nodes"][
          "competencies"].append(comp_code)
    else:
      if skill.get("Keyword"):
        keywords = skill.get("Keyword").split(",")
        for i, item in enumerate(keywords):
          item = item.lstrip()
          keywords[i] = item.rstrip()
      else:
        keywords = []
      # adding id and score to the sme aligned skill
      # TODO: Istead of hardcoding skill_source("emsi")
      #       somehow get it from the csv
      aligned_skill = skill.get("ExternalSkillAlignment")
      skill_alignment = {"emsi": {"aligned": [], "suggested": []}}
      if aligned_skill:
        skill_alignment["emsi"]["aligned"].append({
            "id": "",
            "name": aligned_skill,
            "score": 1.0  # since human aligned this skill
        })
        aligned_skill_doc = Skill.collection.filter("name", "==",
                                                    aligned_skill).get()
        if aligned_skill_doc:
          skill_alignment["emsi"]["aligned"][0]["id"] = aligned_skill_doc.id

      occupations_major_group = []
      if skill.get("OccupationsMajorGroup"):
        occupations_major_group.append(skill.get("OccupationsMajorGroup"))

      occupations_minor_group = []
      if skill.get("OccupationsMinorGroup"):
        occupations_minor_group.append(skill.get("OccupationsMinorGroup"))

      broad_occupation = []
      if skill.get("BroadOccupation"):
        broad_occupation.append(skill.get("BroadOccupation"))

      detailed_occupation = []
      if skill.get("DetailedOccupation"):
        detailed_occupation.append(skill.get("DetailedOccupation"))

      skill_competency_mapping[skill_code] = {
          "name": skill.get("Skill"),
          "description": skill.get("SkillStatement"),
          "parent_nodes": {"competencies": [comp_code]},
          "reference_id": skill.get("SkillCode"),
          "keywords": keywords,
          "occupations": {
              "occupations_major_group": occupations_major_group,
              "occupations_minor_group": occupations_minor_group,
              "broad_occupation": broad_occupation,
              "detailed_occupation": detailed_occupation
          },
          "onet_job": skill.get("ONETJob"),
          "alignments": {
              "standard_alignment": skill.get("StandardAlignment"),
              "credential_alignment": skill.get("CredentialAlignment"),
              "skill_alignment": {
                  "emsi": {
                      "aligned": [{
                          "id": "",
                          "name": skill_alignment,
                          "score": 1.0
                      }],
                      "suggested": []
                  }
              },
              "knowledge_alignment": {},
              "role_alignment": {},
              "organizational_alignment": skill.get("OrganizationalAlignment"),
          },
          "author": "",
          "creator": "",
          "organizations": [],
          "certifications": [],
          "type": {
              "id": "",
              "name": ""
          },
          "source_uri": "snhu",
          "source_name": "snhu",
      }

  for skill in skill_competency_mapping.values():
    skill_obj = Skill()
    skill_obj = skill_obj.from_dict(skill)
    skill_obj.uuid = ""
    skill_obj.save()
    skill_obj.uuid = skill_obj.id
    skill_obj.update()
    inserted_skills.append(skill_obj.to_dict())

  # Insert/Update doc in data_sources collection after ingestion:
  _ = upsert_data_source_doc("skill", "snhu")

  return inserted_skills


def import_competencies(competencies_json_array):
  """extracts and saves the competencies as per v3_competencies fireo model"""
  competency_subdomain_mapping = {}
  inserted_competencies = []
  for competency in competencies_json_array:
    comp_code = competency.get("CompCode")
    subdomain = competency.get("SubDomain")

    occupations_major_group = []
    if competency.get("OccupationsMajorGroup"):
      occupations_major_group.append(competency.get("OccupationsMajorGroup"))

    occupations_minor_group = []
    if competency.get("OccupationsMinorGroup"):
      occupations_minor_group.append(competency.get("OccupationsMinorGroup"))

    broad_occupation = []
    if competency.get("BroadOccupation"):
      broad_occupation.append(competency.get("BroadOccupation"))

    detailed_occupation = []
    if competency.get("DetailedOccupation"):
      detailed_occupation.append(competency.get("DetailedOccupation"))

    if competency_subdomain_mapping.get(comp_code):
      if subdomain not in competency_subdomain_mapping.get(comp_code).get(
          "parent_nodes")["sub_domains"]:
        competency_subdomain_mapping[comp_code]["parent_nodes"][
            "sub_domains"].append(subdomain)
    else:
      competency_subdomain_mapping[comp_code] = {
          "subject_code": competency.get("SubjectCode"),
          "level": competency.get("Level"),
          "reference_id": competency.get("CompCode"),
          "name": competency.get("ShortTitle"),
          "description": competency.get("Statement"),
          "course_code": competency.get("CourseCode"),
          "course_title": competency.get("CourseTitle"),
          "category": competency.get("Category"),
          "keywords": [],
          "parent_nodes": {"sub_domains": [subdomain],
                           "categories": [competency.get("Category")]},
          "source_uri": "snhu",
          "source_name": "snhu",
          "occupations": {
              "occupations_major_group": occupations_major_group,
              "occupations_minor_group": occupations_minor_group,
              "broad_occupation": broad_occupation,
              "detailed_occupation": detailed_occupation
          },
          "alignments": {
              "o_net_alignment": {
                  "aligned": competency.get("O*Net Alignment")
              },
              "standard_alignment": {
                  "aligned": competency.get("Standard Alignment")
              },
              "credential_alignment": {
                  "aligned": competency.get("Credential Alignment")
              },
              "competency_alignment": {
                  "aligned": competency.get("External Competency Alignment")
              },
              "skill_alignment": {
                  "aligned": competency.get("External Skill Alignment")
              },
              "organizational_alignment": {
                  "aligned": competency.get("Organization Alignment")
              },
          }
      }

  for competency in competency_subdomain_mapping.values():
    competency_obj = SkillServiceCompetency()
    competency_obj = competency_obj.from_dict(competency)
    competency_obj.uuid = ""
    competency_obj.save()
    competency_obj.uuid = competency_obj.id
    competency_obj.update()
    inserted_competencies.append(competency_obj.to_dict())

  return inserted_competencies


def import_subdomains(competencies_json_array):
  """extracts and saves the subdomains as per subdomains fireo model"""
  subdomain_domain_mapping = {}
  inserted_subdomains = []
  for competency in competencies_json_array:
    subdomain = competency.get("SubDomain")
    domain = competency.get("Domain")
    if subdomain_domain_mapping.get(subdomain):
      if domain not in subdomain_domain_mapping.get(subdomain):
        subdomain_domain_mapping[subdomain].append(domain)
    else:
      subdomain_domain_mapping[subdomain] = [domain]

  for key, values in subdomain_domain_mapping.items():
    # key is name of subdomain
    # value is list of domains connected to the subdomain(key)
    data = {
        "name": key,
        "description": "",
        "keywords": [],
        "parent_nodes": {"domains": values},
        "child_nodes": {"categories": [], "competencies": []},
        "reference_id": key,
        "source_uri": "snhu",
        "source_name": "snhu",
    }
    subdomain_obj = SubDomain()
    subdomain_obj = subdomain_obj.from_dict(data)
    subdomain_obj.uuid = ""
    subdomain_obj.save()
    subdomain_obj.uuid = subdomain_obj.id
    subdomain_obj.update()
    inserted_subdomains.append(subdomain_obj.to_dict())
  return inserted_subdomains


def import_domains(competencies_json_array):
  """extracts and saves the subdomains as per domains fireo model"""

  domain_list = []
  inserted_domains = []
  for competency in competencies_json_array:
    domain_list.append(competency.get("Domain"))

  # remove duplicates
  domain_list = list(set(domain_list))
  # save domains
  for domain in domain_list:
    domain_obj = Domain()
    data = {
        "name": domain,
        "reference_id": domain,
        "description": "",
        "keywords": [],
        "source_uri": "snhu",
        "source_name": "snhu",
        "child_nodes": {"sub_domains": []}
    }
    domain_obj = domain_obj.from_dict(data)
    domain_obj.uuid = ""
    domain_obj.save()
    domain_obj.uuid = domain_obj.id
    domain_obj.update()
    inserted_domains.append(domain_obj.to_dict())
  return inserted_domains
