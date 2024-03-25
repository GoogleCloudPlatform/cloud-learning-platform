"""
Read skills and concepts within skill graph and knowledge graph respectively
"""

import behave
import uuid
# sys.path.append("../")
from setup import get_method
from test_config import API_URL_SKILL_SERVICE, API_URL_KNOWLEDGE_SERVICE

# ---------------------------- Scenario 01 -------------------------------------

@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the skill")
def step_impl_1(context):
  context.url = f"{API_URL_SKILL_SERVICE}/skill/{context.skill_id}"

@behave.when("there is a request to view a particular skill node in the skill graph with correct id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested skill")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.skill_id


# ---------------------------- Scenario 02 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the skill graph")
def step_impl_1(context):
  context.url = f"{API_URL_SKILL_SERVICE}/skill/{context.skill_id}"

@behave.when("there is a request to view a particular skill node and fetch skill graph tree with correct id")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params={"fetch_tree":True})
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested skill along with tree of related nodes")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.skill_id
  assert context.res_data["data"]["parent_nodes"]["competencies"][0]["uuid"] == context.competency_id
  assert context.res_data["data"]["parent_nodes"]["competencies"][0]["name"] == "Test Random Competency"

# ---------------------------- Scenario 03 -------------------------------------
@behave.given("that a user can access Skill Service (via Competencies & Skill Management) and needs to view the skill")
def step_impl_1(context):
  context.uuid = "random_id"
  context.url = f"{API_URL_SKILL_SERVICE}/skill/{context.uuid}"

@behave.when("there is a request to view a particular skill node in the skill graph with incorrect id")
def step_impl_1(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will throw an error message for accessing invalid skill")
def step_impl_1(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None

# ---------------------------- Scenario 04 -------------------------------------

@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the competency")
def step_impl_1(context):
  context.uuid = "f5ca898a-d53b-4b10-b435-39070a7912df"
  context.url = f"{API_URL_SKILL_SERVICE}/competency/{context.uuid}"

@behave.when("there is a request to view a particular competency node in the skill graph with correct id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested competency")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.uuid


# ---------------------------- Scenario 05 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to fetch skill graph tree")
def step_impl_1(context):
  context.url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"

@behave.when("there is a request to view a particular competency node and fetch skill graph tree related to correct competency id")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params={"fetch_tree":True})
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested competency along with tree of related nodes")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.competency_id
  assert context.res_data["data"]["parent_nodes"]["categories"][0]["uuid"] == context.category_id
  assert context.res_data["data"]["parent_nodes"]["categories"][0]["name"] == "Test Random Category"
  assert context.res_data["data"]["child_nodes"]["skills"][0]["uuid"] == context.skill_id
  assert context.res_data["data"]["child_nodes"]["skills"][0]["name"] == "Test Random Skill"

# ---------------------------- Scenario 06 -------------------------------------
@behave.given("that a user can access Skill Service (via Competencies & Skill Management) and needs to view the competency")
def step_impl_1_1(context):
  context.uuid = "random_id"
  context.url = f"{API_URL_SKILL_SERVICE}/competency/{context.uuid}"

@behave.when("there is a request to view a particular competency node in the skill graph with incorrect id")
def step_impl_1_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will throw an error message for accessing invalid competency")
def step_impl_1_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ---------------------------- Scenario 07 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the category")
def step_impl_1(context):
  context.uuid = "dd5d2c0a-75d4-4eda-8bcc-d47fe0927330"
  context.url = f"{API_URL_SKILL_SERVICE}/category/{context.uuid}"

@behave.when("there is a request to view a particular category node in the skill graph with correct id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested category")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.uuid

# ---------------------------- Scenario 08 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view skill graph tree")
def step_impl_1(context):
  context.url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"

@behave.when("there is a request to view a particular category node and fetch skill graph tree related to correct category id")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params={"fetch_tree":True})
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested category along with tree of related nodes")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.category_id
  assert context.res_data["data"]["parent_nodes"]["sub_domains"][0]["uuid"] == context.sub_domain_id
  assert context.res_data["data"]["parent_nodes"]["sub_domains"][0]["name"] == "Test Random Sub-Domain"
  assert context.res_data["data"]["child_nodes"]["competencies"][0]["uuid"] == context.competency_id
  assert context.res_data["data"]["child_nodes"]["competencies"][0]["name"] == "Test Random Competency"
  assert context.res_data["data"]["child_nodes"]["competencies"][0]["child_nodes"]["skills"][0]["uuid"] == context.skill_id
  assert context.res_data["data"]["child_nodes"]["competencies"][0]["child_nodes"]["skills"][0]["name"] == "Test Random Skill"


# ---------------------------- Scenario 09 -------------------------------------
@behave.given("that a user can access Skill Service (via Competencies & Skill Management) and needs to view the category")
def step_impl_1_1(context):
  context.uuid = "random_id"
  context.url = f"{API_URL_SKILL_SERVICE}/category/{context.uuid}"

@behave.when("there is a request to view a particular category node in the skill graph with incorrect id")
def step_impl_1_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will throw an error message for accessing invalid category")
def step_impl_1_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ---------------------------- Scenario 10 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the sub-domain")
def step_impl_1(context):
  context.uuid = "64d8bbdb-21d2-4126-9871-1739c026e483"
  context.url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.uuid}"

@behave.when("there is a request to view a particular sub-domain node in the skill graph with correct id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested sub-domain")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.uuid


# ---------------------------- Scenario 11 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to see skill graph tree")
def step_impl_1(context):
  context.url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"

@behave.when("there is a request to view a particular sub-domain node and fetch skill graph tree related to correct sub-domain id")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params={"fetch_tree":True})
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested sub-domain along with tree of related nodes")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.sub_domain_id
  assert context.res_data["data"]["parent_nodes"]["domains"][0]["uuid"] == context.domain_id
  assert context.res_data["data"]["parent_nodes"]["domains"][0]["name"] == "Test Random Domain"
  assert context.res_data["data"]["child_nodes"]["categories"][0]["uuid"] == context.category_id
  assert context.res_data["data"]["child_nodes"]["categories"][0]["name"] == "Test Random Category"
  assert context.res_data["data"]["child_nodes"]["categories"][0]["child_nodes"]["competencies"][0]["uuid"] == context.competency_id
  assert context.res_data["data"]["child_nodes"]["categories"][0]["child_nodes"]["competencies"][0]["name"] == "Test Random Competency"
  assert context.res_data["data"]["child_nodes"]["categories"][0]["child_nodes"]["competencies"][0]["child_nodes"]["skills"][0]["uuid"] == context.skill_id
  assert context.res_data["data"]["child_nodes"]["categories"][0]["child_nodes"]["competencies"][0]["child_nodes"]["skills"][0]["name"] == "Test Random Skill"


# ---------------------------- Scenario 12 -------------------------------------
@behave.given("that a user can access Skill Service (via Competencies & Skill Management) and needs to view the sub-domain")
def step_impl_1_1(context):
  context.uuid = "random_id"
  context.url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.uuid}"

@behave.when("there is a request to view a particular sub-domain node in the skill graph with incorrect id")
def step_impl_1_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will throw an error message for accessing invalid sub-domain")
def step_impl_1_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ---------------------------- Scenario 13 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the domain")
def step_impl_1(context):
  context.uuid = "500de2f8-9ea2-4372-a624-5bf6380b440c"
  context.url = f"{API_URL_SKILL_SERVICE}/domain/{context.uuid}"

@behave.when("there is a request to view a particular domain node in the skill graph with correct id")
def step_impl_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested domain")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.uuid

# ---------------------------- Scenario 14 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs the skill graph tree")
def step_impl_1(context):
  context.url = f"{API_URL_SKILL_SERVICE}/domain/{context.domain_id}"

@behave.when("there is a request to view a particular domain node and fetch skill graph tree related to correct domain id")
def step_impl_2(context):
  context.res = get_method(url=context.url, query_params={"fetch_tree":True})
  context.res_data = context.res.json()

@behave.then("Skill Service will serve up the requested domain along with tree of related nodes")
def step_impl_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.domain_id
  assert context.res_data["data"]["child_nodes"]["sub_domains"][0]["uuid"] == context.sub_domain_id
  assert context.res_data["data"]["child_nodes"]["sub_domains"][0]["name"] == "Test Random Sub-Domain"
  assert context.res_data["data"]["child_nodes"]["sub_domains"][0]["child_nodes"]["categories"][0]["uuid"] == context.category_id
  assert context.res_data["data"]["child_nodes"]["sub_domains"][0]["child_nodes"]["categories"][0]["name"] == "Test Random Category"
  assert context.res_data["data"]["child_nodes"]["sub_domains"][0]["child_nodes"]["categories"][0]["child_nodes"]["competencies"][0]["uuid"] == context.competency_id
  assert context.res_data["data"]["child_nodes"]["sub_domains"][0]["child_nodes"]["categories"][0]["child_nodes"]["competencies"][0]["name"] == "Test Random Competency"
  assert context.res_data["data"]["child_nodes"]["sub_domains"][0]["child_nodes"]["categories"][0]["child_nodes"]["competencies"][0]["child_nodes"]["skills"][0]["uuid"] == context.skill_id
  assert context.res_data["data"]["child_nodes"]["sub_domains"][0]["child_nodes"]["categories"][0]["child_nodes"]["competencies"][0]["child_nodes"]["skills"][0]["name"] == "Test Random Skill"

# ---------------------------- Scenario 15 -------------------------------------
@behave.given("that a user can access Skill Service (via Competencies & Skill Management) and needs to view the domain")
def step_impl_1_1(context):
  context.uuid = "random_id"
  context.url = f"{API_URL_SKILL_SERVICE}/domain/{context.uuid}"

@behave.when("there is a request to view a particular domain node in the skill graph with incorrect id")
def step_impl_1_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()

@behave.then("Skill Service will throw an error message for accessing invalid domain")
def step_impl_1_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ---------------------------- Scenario 16 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the concept")
def step_1_1(context):
  context.req_id = "dd70920c-f0af-4636-8711-3a9aa9751e53"
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{context.req_id}"


@behave.when("there is a request to view a particular concept node in the knowledge graph with correct concept id")
def step_1_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will serve up the requested concept")
def step_1_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.req_id


# ---------------------------- Scenario 17 -------------------------------------
@behave.given("that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the concept")
def step_2_1(context):
  _id = uuid.uuid4()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{_id}"


@behave.when("there is a request to view a particular concept node in the knowledge graph with incorrect concept id")
def step_2_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an error message for accessing invalid concept")
def step_2_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ---------------------------- Scenario 18 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the sub-concept")
def step_3_1(context):
  context.req_id = "d814e1b6-591b-4920-aea9-e434c6332dc7"
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/{context.req_id}"


@behave.when("there is a request to view a particular sub-concept node in the knowledge graph with correct sub-concept id")
def step_3_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will serve up the requested sub-concept")
def step_3_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.req_id


# ---------------------------- Scenario 19 -------------------------------------
@behave.given("that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the sub-concept")
def step_4_1(context):
  _id = uuid.uuid4()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/{_id}"


@behave.when("there is a request to view a particular sub-concept node in the knowledge graph with incorrect sub-concept id")
def step_4_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an error message for accessing invalid sub-concept")
def step_4_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ---------------------------- Scenario 20 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the learning-objective")
def step_5_1(context):
  context.req_id = "8d8d5005-3cad-42fe-8c33-fda079dd70b8"
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{context.req_id}"


@behave.when("there is a request to view a particular learning-objective node in the knowledge graph with correct learning-objective id")
def step_5_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will serve up the requested learning-objective")
def step_5_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.req_id


# ---------------------------- Scenario 21 -------------------------------------
@behave.given("that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the learning-objective")
def step_6_1(context):
  _id = uuid.uuid4()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{_id}"


@behave.when("there is a request to view a particular learning-objective node in the knowledge graph with incorrect learning-objective id")
def step_6_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an error message for accessing invalid learning-objective")
def step_6_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ---------------------------- Scenario 22 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the learning-unit")
def step_7_1(context):
  context.req_id = "be73e5f6-43e7-410b-9e81-c0b50ed180a6"
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{context.req_id}"


@behave.when("there is a request to view a particular learning-unit node in the knowledge graph with correct learning-unit id")
def step_7_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will serve up the requested learning-unit")
def step_7_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.req_id


# ---------------------------- Scenario 23 -------------------------------------
@behave.given("that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the learning-unit")
def step_8_1(context):
  _id = uuid.uuid4()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{_id}"


@behave.when("there is a request to view a particular learning-unit node in the knowledge graph with incorrect learning-unit id")
def step_8_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an error message for accessing invalid learning-unit")
def step_8_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None


# ---------------------------- Scenario 24 -------------------------------------
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to view the learning-resource")
def step_9_1(context):
  context.req_id = "45b76f86-3031-4ac5-a251-057b0ad8c371"
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{context.req_id}"


@behave.when("there is a request to view a particular learning-resource node in the knowledge graph with correct learning-resource id")
def step_9_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will serve up the requested learning-resource")
def step_9_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert context.res_data["data"]["uuid"] == context.req_id


# ---------------------------- Scenario 25 -------------------------------------
@behave.given("that a user can access to Skill Service (via Competencies & Skill Management) and needs to view the learning-resource")
def step_10_1(context):
  _id = uuid.uuid4()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{_id}"


@behave.when("there is a request to view a particular learning-resource node in the knowledge graph with incorrect learning-resource id")
def step_10_2(context):
  context.res = get_method(url=context.url)
  context.res_data = context.res.json()


@behave.then("Skill Service will throw an error message for accessing invalid learning-resource")
def step_10_3(context):
  assert context.res.status_code == 404
  assert context.res_data["success"] is False
  assert context.res_data["data"] is None
