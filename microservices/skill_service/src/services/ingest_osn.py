"""
  Service for following routes:
  /import/local-csv
  /import/gcs-csv
"""
import csv
import asyncio
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
from services.data_source import upsert_data_source_doc
from common.models import Skill, Category
from common.utils.gcs_adapter import get_blob_from_gcs_path
from common.utils.errors import ValidationError
# pylint: disable = broad-exception-raised


class AsyncInserts:
  """Class to insert data in async fashion with insert_data() function"""

  def __init__(self):
    self.inserted_skills = []
    self.inserted_categories = []
    pass

  def insert_skill(self, skill):
    obj = Skill()
    obj = obj.from_dict(skill)
    obj.uuid = ""
    obj.save()
    obj.uuid = obj.id
    obj.update()
    self.inserted_skills.append(skill)

  def insert_category(self, category):
    obj = Category()
    obj = obj.from_dict(category)
    obj.uuid = ""
    obj.save()
    obj.uuid = obj.id
    obj.update()
    self.inserted_categories.append(category)

  async def start_insert_process(self, data, obj_type):
    with ThreadPoolExecutor(max_workers=30) as executor:
      loop = asyncio.get_event_loop()
      tasks = []
      for data_obj in data:
        if obj_type == "skill":
          runner = loop.run_in_executor(executor, self.insert_skill, data_obj)
        elif obj_type == "category":
          runner = loop.run_in_executor(executor, self.insert_category,
                                        data_obj)
        tasks.append(runner)

      for _ in await asyncio.gather(*tasks):
        pass

  def insert_data(self, data, data_type):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(self.start_insert_process(data, data_type))
    loop.run_until_complete(future)

  def get_inserted_skills_count(self):
    return len(self.inserted_skills)

  def get_inserted_categories_count(self):
    return len(self.inserted_categories)


def ingest_osn_csv(path_dict):
  """validates, transforms and saves competencies and
  skills and category json as skill tree"""
  osn_uri = path_dict.get("osn_uri")

  osn_json_array = parse_and_validate_osn_csv(osn_uri)

  skills_count = import_skills(osn_json_array)
  _ = upsert_data_source_doc("skill", "osn")

  msg = f"Imported {skills_count} skills"

  response = {"success": True, "message": msg, "data": {}}
  return response


def parse_and_validate_osn_csv(osn_uri):
  blob = get_blob_from_gcs_path(osn_uri)
  osn_json_array = parse_gcs_csv_file(blob)
  try:
    validate_osn_csv(osn_json_array)
  except Exception as e:
    raise Exception(str(e)) from e
  return osn_json_array


def parse_gcs_csv_file(blob):
  """downloads csv from gcs and returns it as json"""
  # download file as bytes
  file_data = blob.download_as_bytes()
  byte_content = file_data
  content = byte_content.decode()
  file = StringIO(content)

  csv_reader = csv.DictReader(file, delimiter=",")
  return list(csv_reader)


def validate_osn_csv(data):
  """checks if all required columns are present in osn csv"""
  fields = [
      "Canonical URL", "RSD Name", "Author", "Skill Statement", "Category",
      "Keywords", "Certifications", "Occupation Major Groups",
      "Occupation Minor Groups", "Broad Occupations", "Detailed Occupations",
      "O*Net Job Codes", "Alignment Name", "Alignment URL"
  ]
  missing_fields = []
  for field in fields:
    if field not in data[0]:
      missing_fields.append(field)

  if len(missing_fields) > 0:
    fields = ", ".join(missing_fields)
    raise ValidationError\
      (f"Following fields are missing in provided csv: '{fields}'")


def import_skills(osn_json_array):
  """extracts and saves the skills as per skill fireo model"""
  inserted_skills = []
  for osn_skill in osn_json_array:
    skill_id = osn_skill.get("Canonical URL", "").split("/")[-1]
    aligned_id = osn_skill.get("Alignment URL", "").split("/")[-1]

    occ_major_group = osn_skill.get("Occupation Major Groups").split(";")
    if len(occ_major_group) == 1 and occ_major_group[0] == "":
      occ_major_group = []
    occ_major_group = [i.strip() for i in occ_major_group]

    occ_minor_group = osn_skill.get("Occupation Minor Groups").split(";")
    if len(occ_minor_group) == 1 and occ_minor_group[0] == "":
      occ_minor_group = []
    occ_minor_group = [i.strip() for i in occ_minor_group]

    broad_occupation = osn_skill.get("Broad Occupations").split(";")
    if len(broad_occupation) == 1 and broad_occupation[0] == "":
      broad_occupation = []
    broad_occupation = [i.strip() for i in broad_occupation]

    detailed_occupation = osn_skill.get("Detailed Occupations").split(";")
    if len(detailed_occupation) == 1 and detailed_occupation[0] == "":
      detailed_occupation = []
    detailed_occupation = [i.strip() for i in detailed_occupation]

    keywords = osn_skill.get("Keywords").split(";")
    if len(keywords) == 1 and keywords[0] == "":
      keywords = []
    keywords = [i.strip() for i in keywords]

    certifications = osn_skill.get("Certifications").split(";")
    if len(certifications) == 1 and certifications[0] == "":
      certifications = []
    certifications = [i.strip() for i in certifications]

    skill = {
        "name": osn_skill.get("RSD Name"),
        "description": osn_skill.get("Skill Statement"),
        "parent_nodes": {"competencies": []},
        "reference_id": skill_id,
        "keywords": keywords,
        "occupations": {
            "occupations_major_group": occ_major_group,
            "occupations_minor_group": occ_minor_group,
            "broad_occupation": broad_occupation,
            "detailed_occupation": detailed_occupation
        },
        "onet_job": osn_skill.get("O*Net Job Codes"),
        "alignments": {
            "standard_alignment": {},
           "credential_alignment": {},
            "skill_alignment": {
                "emsi": {
                    "aligned": [{
                        "id": aligned_id,
                        "name": osn_skill.get("Alignment Name"),
                        "score": 1.0
                    }],
                    "suggested": []
                }
            },
            "knowledge_alignment": {},
            "role_alignment": {},
            "organizational_alignment": {}
        },
        "author": osn_skill.get("Author"),
        "creator": "",
        "organizations": [],
        "certifications": certifications,
        "type": {
            "id": "",
            "name": ""
        },
        "source_uri": osn_skill.get("Canonical URL"),
        "source_name": "osn"
    }
    inserted_skills.append(skill)
  async_inserts = AsyncInserts()
  async_inserts.insert_data(inserted_skills, "skill")
  inserted_skills_length = async_inserts.get_inserted_skills_count()
  return inserted_skills_length
