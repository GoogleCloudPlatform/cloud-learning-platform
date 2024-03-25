"""
  Service for emsi data ingestion route
"""
import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from common.models import Skill
from services.data_source import upsert_data_source_doc
from config import CLIENT_ID, CLIENT_SECRET, EMSI_AUTH_URL, EMSI_URL
# pylint: disable = broad-except


class AnyncSkillInserts:
  """Class to insert skills_list in async fashion with insert_data() function"""

  def __init__(self):
    self.inserted_skills = []
    pass

  def insert(self, skill):
    obj = Skill()
    skill = dict(skill)

    if skill.get("tags"):
      skill_description = skill.get("tags")[0].get("value")
    else:
      skill_description = ""
    skill_dict = {
        "uuid": "",
        "name": skill.get("name"),
        "description": skill_description,
        "keywords": [],
        "author": "",
        "creator": "",
        "alignments": {
            "standard_alignment": {},
           "credential_alignment": {},
            "skill_alignment": {},
            "knowledge_alignment": {},
            "role_alignment": {},
            "organizational_alignment": {},
        },
        "organizations": [],
        "certifications": [],
        "occupations": {
            "occupations_major_group": [],
            "occupations_minor_group": [],
            "broad_occupation": [],
            "detailed_occupation": [],
        },
        "onet_job": "",
        "type": skill.get("type"),
        "parent_nodes": {"competencies": []},
        "reference_id": skill.get("id"),
        "source_uri": skill.get("infoUrl"),
        "source_name": "emsi"
    }
    obj = obj.from_dict(skill_dict)
    obj.save()
    obj.uuid = obj.id
    obj.update()
    self.inserted_skills.append(skill)

  async def start_insert_process(self, skills_list):
    with ThreadPoolExecutor(max_workers=30) as executor:
      loop = asyncio.get_event_loop()
      tasks = []
      for skill in skills_list:
        runner = loop.run_in_executor(executor, self.insert, skill)
        tasks.append(runner)

      for _ in await asyncio.gather(*tasks):
        pass

  def insert_data(self, skills_list):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(self.start_insert_process(skills_list))
    loop.run_until_complete(future)

  def get_inserted_skills_count(self):
    return len(self.inserted_skills)


def auth_emsi():
  """ Get access token required to fetch emsi skills

  Returns:
      str: access token
  """
  payload = (f"client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type="
             "client_credentials&scope=emsi_open")
  headers = {"Content-Type": "application/x-www-form-urlencoded"}

  response = requests.post(EMSI_AUTH_URL, data=payload, headers=headers,
                           timeout=10)
  return response.json().get("access_token")


def fetch_emsi_skills(token, size):
  """fetch data from emsi using emsi api's"""
  emsi_url = EMSI_URL
  if size:
    emsi_url = f"{emsi_url}&limit={size}"

  headers = {"Authorization": f"Bearer {token}"}
  response = requests.get(emsi_url, headers=headers, timeout=10)
  emsi_skills = response.json().get("data")
  return emsi_skills


def ingest_emsi(size):
  """ingest data from emsi using emsi api's"""
  token = auth_emsi()
  emsi_skills = fetch_emsi_skills(token, size)

  async_inserts = AnyncSkillInserts()
  async_inserts.insert_data(emsi_skills)
  inserted_skills_length = async_inserts.get_inserted_skills_count()

  # Insert/Update doc in data_sources collection after ingestion:
  _ = upsert_data_source_doc("skill", "emsi")

  msg = f"Imported {inserted_skills_length} skills"
  response = {"success": True, "message": msg, "data": {}}
  return response
