"""
Filters for skill service
"""
import behave
import sys

sys.path.append("../")
from setup import post_method, get_method
from test_object_schemas import (TEST_SKILL, TEST_COMPETENCY, TEST_CATEGORY,
                    TEST_SUB_DOMAIN, TEST_DOMAIN)
from test_config import API_URL_SKILL_SERVICE, API_URL_KNOWLEDGE_SERVICE

# ------------------------------------------ scenario 1 ------------------------------------------
@behave.given("That a user has the ability to filter skill data in skill graph")
def scenario_1_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/skill"
  skill_data = TEST_SKILL

  post_skill = post_method(url, request_body=skill_data)
  assert post_skill.status_code == 200, "Status 200"


@behave.when(
    "A filter for skill is applied within the management interface with permitted filters"
)
def scenario_1_step_2(context):
  filter_params = {
      "skip": 0,
      "limit": "50",
      "creator": "https://credentialengineregistry.org/resources/ce-0f0d84f5-5c32-4526-ad39-1db0adbdbe93"
  }
  url = f"{API_URL_SKILL_SERVICE}/skills"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will retrieve the relevant filtered data for skill and serve that data back to the management interface"
)
def scenario_1_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for skill_data in context.res_data["data"]:
    assert skill_data.get(
        "creator"
    ) == "https://credentialengineregistry.org/resources/ce-0f0d84f5-5c32-4526-ad39-1db0adbdbe93", "filter not working properly"


# ------------------------------------------ scenario 2 ------------------------------------------
@behave.given(
    "That a user has the ability to filter skill data in skill graph for negative scenario"
)
def scenario_2_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/skill"
  skill_data = TEST_SKILL
  post_skill = post_method(url, request_body=skill_data)

  assert post_skill.status_code == 200, "Status 200"


@behave.when(
    "A filter for skill is applied within the management interface with invalid filters for negative scenario"
)
def scenario_2_step_2(context):
  filter_params = {
      "skip": "-1",
      "limit": "50",
      "source_name": "Credentialengine"
  }
  url = f"{API_URL_SKILL_SERVICE}/skills"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will raise error for invalid skills filter and send back to the management interface as negative scenario"
)
def scenario_2_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 3 ------------------------------------------
@behave.given(
    "That a user has the ability to filter competency data in skill graph")
def scenario_3_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/competency"
  competency_data = TEST_COMPETENCY
  post_competency = post_method(url, request_body=competency_data)

  assert post_competency.status_code == 200, "Status 200"


@behave.when(
    "A filter for competency is applied within the management interface with permitted filters"
)
def scenario_3_step_2(context):
  filter_params = {"skip": 0, "limit": "50", "subject_code": "MAT"}
  url = f"{API_URL_SKILL_SERVICE}/competencies"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will retrieve the relevant filtered data for competency and serve that data back to the management interface"
)
def scenario_3_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for competency_data in context.res_data["data"]:
    assert competency_data.get(
        "subject_code") == "MAT", "filter not working properly"


# ------------------------------------------ scenario 4 ------------------------------------------
@behave.given(
    "That a user has the ability to filter competency data in skill graph for negative scenario"
)
def scenario_4_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/competency"
  competency_data = TEST_COMPETENCY
  post_competency = post_method(url, request_body=competency_data)

  assert post_competency.status_code == 200, "Status 200"


@behave.when(
    "A filter for competency is applied within the management interface with invalid filters for negative scenario"
)
def scenario_4_step_2(context):
  filter_params = {
      "skip": "-1",
      "limit": "50",
      "source_name": "Credentialengine"
  }
  url = f"{API_URL_SKILL_SERVICE}/competencies"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will raise error for invalid competencies filter and send back to the management interface as negative scenario"
)
def scenario_4_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 5 ------------------------------------------
@behave.given(
    "That a user has the ability to filter category data in skill graph")
def scenario_5_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/category"
  category_data = TEST_CATEGORY
  post_category = post_method(url, request_body=category_data)

  assert post_category.status_code == 200, "Status 200"


@behave.when(
    "A filter for category is applied within the management interface with permitted filters"
)
def scenario_5_step_2(context):
  filter_params = {"skip": 0, "limit": "50", "source_name": "Credentialengine"}
  url = f"{API_URL_SKILL_SERVICE}/categories"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will retrieve the relevant filtered data for category and serve that data back to the management interface"
)
def scenario_5_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for category_data in context.res_data["data"]:
    assert category_data.get(
        "source_name") == "Credentialengine", "filter not working properly"


# ------------------------------------------ scenario 6 ------------------------------------------
@behave.given(
    "That a user has the ability to filter category data in skill graph for negative scenario"
)
def scenario_6_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/category"
  category_data = TEST_CATEGORY
  post_category = post_method(url, request_body=category_data)

  assert post_category.status_code == 200, "Status 200"


@behave.when(
    "A filter for category is applied within the management interface with invalid filters for negative scenario"
)
def scenario_6_step_2(context):
  filter_params = {
      "skip": "-1",
      "limit": "50",
      "source_name": "Credentialengine"
  }
  url = f"{API_URL_SKILL_SERVICE}/categories"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will raise error for invalid category filter and send back to the management interface as negative scenario"
)
def scenario_6_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 7 ------------------------------------------
@behave.given(
    "That a user has the ability to filter sub domain data in skill graph")
def scenario_7_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/sub-domain"
  sub_domain_data = TEST_SUB_DOMAIN
  post_sub_domain = post_method(url, request_body=sub_domain_data)

  assert post_sub_domain.status_code == 200, "Status 200"


@behave.when(
    "A filter for sub domain is applied within the management interface with permitted filters"
)
def scenario_7_step_2(context):
  filter_params = {"skip": 0, "limit": "50", "source_name": "Credentialengine"}
  url = f"{API_URL_SKILL_SERVICE}/sub-domains"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will retrieve the relevant filtered data for sub domain and serve that data back to the management interface"
)
def scenario_7_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for sub_domain_data in context.res_data["data"]:
    assert sub_domain_data.get(
        "source_name") == "Credentialengine", "filter not working properly"


# ------------------------------------------ scenario 8 ------------------------------------------
@behave.given(
    "That a user has the ability to filter sub domain data in skill graph for negative scenario"
)
def scenario_8_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/sub-domain"
  sub_domain_data = TEST_SUB_DOMAIN
  post_sub_domain = post_method(url, request_body=sub_domain_data)

  assert post_sub_domain.status_code == 200, "Status 200"


@behave.when(
    "A filter for sub domain is applied within the management interface with invalid filters for negative scenario"
)
def scenario_8_step_2(context):
  filter_params = {
      "skip": "-1",
      "limit": "50",
      "source_name": "Credentialengine"
  }
  url = f"{API_URL_SKILL_SERVICE}/sub-domains"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will raise error for invalid sub domain filter and send back to the management interface as negative scenario"
)
def scenario_8_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 9 ------------------------------------------
@behave.given("That a user has the ability to filter domain data in skill graph"
             )
def scenario_9_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/domain"
  domain_data = TEST_DOMAIN
  post_domain = post_method(url, request_body=domain_data)

  assert post_domain.status_code == 200, "Status 200"


@behave.when(
    "A filter for domain is applied within the management interface with permitted filters"
)
def scenario_9_step_2(context):
  filter_params = {"skip": 0, "limit": "50", "source_name": "Credentialengine"}
  url = f"{API_URL_SKILL_SERVICE}/domains"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will retrieve the relevant filtered data for domain and serve that data back to the management interface"
)
def scenario_9_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for domain_data in context.res_data["data"]:
    assert domain_data.get(
        "source_name") == "Credentialengine", "filter not working properly"


# ------------------------------------------ scenario 10 ------------------------------------------
@behave.given(
    "That a user has the ability to filter domain data in skill graph for negative scenario"
)
def scenario_10_step_1(context):
  url = f"{API_URL_SKILL_SERVICE}/domain"
  domain_data = TEST_DOMAIN
  post_domain = post_method(url, request_body=domain_data)

  assert post_domain.status_code == 200, "Status 200"


@behave.when(
    "A filter for domain is applied within the management interface with invalid filters for negative scenario"
)
def scenario_10_step_2(context):
  filter_params = {
      "skip": "-1",
      "limit": "50",
      "source_name": "Credentialengine"
  }
  url = f"{API_URL_SKILL_SERVICE}/domains"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Skill Service will raise error for invalid domain filter and send back to the management interface as negative scenario"
)
def scenario_10_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 11 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter concept data in knowledge graph"
)
def scenario_11_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)
  saved_lr_id = post_learning_resource.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{saved_lr_id}/concept"
  concept_data = {
      "title": "Idealism",
      "description": "The belief that a perfect life, situation, etc. can be achieved, even when this != very likely",
      "label": "",
      "parent_nodes":  {"learning_resource": []},
      "child_nodes": {"sub_concepts": []},
      "is_valid": "false",
      "type": "concept",
      "alignments": {}
  }
  post_concept = post_method(url, request_body=concept_data)
  assert post_concept.status_code == 200, "Status 200"


@behave.when(
    "A filter for concept is applied within the management interface with permitted filters"
)
def scenario_11_step_2(context):
  filter_params = {"skip": 0, "limit": "50", "is_valid": "false"}
  url = f"{API_URL_KNOWLEDGE_SERVICE}/concepts"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will retrieve the relevant filtered data for concept and serve that data back to the management interface"
)
def scenario_11_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for concept_data in context.res_data["data"]:
    assert concept_data.get("is_valid") is False, "filter not working properly"


# ------------------------------------------ scenario 12 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter concept data in knowledge graph for negative scenario"
)
def scenario_12_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)
  saved_lr_id = post_learning_resource.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{saved_lr_id}/concept"
  concept_data = {
      "title": "Idealism",
      "description": "The belief that a perfect life, situation, etc. can be achieved, even when this != very likely",
      "label": "",
      "parent_nodes":  {"learning_resource": []},
      "child_nodes": {"sub_concepts": []},
      "is_valid": "false",
      "type": "concept",
      "alignments": {}
  }
  post_concept = post_method(url, request_body=concept_data)
  assert post_concept.status_code == 200, "Status 200"


@behave.when(
    "A filter for concept is applied within the management interface with invalid filters for negative scenario"
)
def scenario_12_step_2(context):
  filter_params = {"skip": "-1", "limit": "50", "is_valid": "false"}
  url = f"{API_URL_KNOWLEDGE_SERVICE}/concepts"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will raise error for invalid concepts filter and send back to the management interface as negative scenario"
)
def scenario_12_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 13 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter subconcept data in knowledge graph"
)
def scenario_13_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)
  saved_lr_id = post_learning_resource.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{saved_lr_id}/concept"
  concept_data = {
      "title": "Idealism",
      "description": "The belief that a perfect life, situation, etc. can be achieved, even when this != very likely",
      "label": "",
      "parent_nodes":  {"learning_resource": []},
      "child_nodes": {"sub_concepts": []},
      "is_valid": "false",
      "type": "concept",
      "alignments": {}
  }
  post_concept = post_method(url, request_body=concept_data)
  saved_concept_id = post_concept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{saved_concept_id}/subconcept"
  subconcept_data = {
      "title": "Essentialism",
      "description": "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods",
      "all_learning_resource": "",
      "parent_nodes":  {"concepts": []},
      "child_nodes": {"learning_objectives": []},
      "label": "",
      "total_lus": 0,
      "is_valid": "false",
      "type": "subconcept",
      "alignments": {}
  }

  post_subconcept = post_method(url, request_body=subconcept_data)
  assert post_subconcept.status_code == 200, "Status 200"


@behave.when(
    "A filter for subconcept is applied within the management interface with permitted filters"
)
def scenario_13_step_2(context):
  filter_params = {"skip": 0, "limit": "50", "is_valid": "false"}
  url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcepts"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will retrieve the relevant filtered data for subconcept and serve that data back to the management interface"
)
def scenario_13_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for subconcept_data in context.res_data["data"]:
    assert subconcept_data.get(
        "is_valid") is False, "filter not working properly"


# ------------------------------------------ scenario 14 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter subconcept data in knowledge graph for negative scenario"
)
def scenario42_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)
  saved_lr_id = post_learning_resource.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{saved_lr_id}/concept"
  concept_data = {
      "title": "Idealism",
      "description": "The belief that a perfect life, situation, etc. can be achieved, even when this != very likely",
      "label": "",
      "parent_nodes":  {"learning_resource": []},
      "child_nodes": {"sub_concepts": []},
      "is_valid": "false",
      "type": "concept",
      "alignments": {}
  }
  post_concept = post_method(url, request_body=concept_data)
  saved_concept_id = post_concept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{saved_concept_id}/subconcept"
  subconcept_data = {
      "title": "Essentialism",
      "description": "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods",
      "all_learning_resource": "",
      "parent_nodes":  {"concepts": []},
      "child_nodes": {"learning_objectives": []},
      "label": "",
      "total_lus": 0,
      "is_valid": "false",
      "type": "subconcept",
      "alignments": {}
  }
  post_subconcept = post_method(url, request_body=subconcept_data)
  context.saved_subconcept_id = post_subconcept.json().get("data").get("uuid")
  assert post_subconcept.status_code == 200, "Status 200"


@behave.when(
    "A filter for subconcept is applied within the management interface with invalid filters for negative scenario"
)
def scenario_14_step_2(context):
  filter_params = {"skip": "-1", "limit": "50", "is_valid": "false"}
  url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcepts"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will raise error for invalid subconcepts filter and send back to the management interface as negative scenario"
)
def scenario_14_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 15 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter learning objective data in knowledge graph"
)
def scenario_15_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)
  saved_lr_id = post_learning_resource.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{saved_lr_id}/concept"
  concept_data = {
      "title": "Idealism",
      "description": "The belief that a perfect life, situation, etc. can be achieved, even when this != very likely",
      "label": "",
      "parent_nodes":  {"learning_resource": []},
      "child_nodes": {"sub_concepts": []},
      "is_valid": "false",
      "type": "concept",
      "alignments": {}
  }
  post_concept = post_method(url, request_body=concept_data)
  saved_concept_id = post_concept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{saved_concept_id}/subconcept"
  subconcept_data = {
      "title": "Essentialism",
      "description": "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods",
      "all_learning_resource": "",
      "parent_nodes":  {"concepts": []},
      "child_nodes": {"learning_objectives": []},
      "label": "",
      "total_lus": 0,
      "is_valid": "false",
      "type": "subconcept",
      "alignments": {}
  }

  post_subconcept = post_method(url, request_body=subconcept_data)
  saved_subconcept_id = post_subconcept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/sub-concept/{saved_subconcept_id}/learning-objective"
  learning_objective_data = {
      "title": "State theorems",
      "description": "A description for State theorems",
      "parent_nodes": {"sub_concepts": []},
      "child_nodes": {"learning_units": []},
      "is_valid": "false",
      "type": "learning_objective",
      "alignments": {},
      "text": [""]
  }
  post_learning_objective = post_method(
      url, request_body=learning_objective_data)
  assert post_learning_objective.status_code == 200, "Status 200"


@behave.when(
    "A filter for learning objective is applied within the management interface with permitted filters"
)
def scenario_15_step_2(context):
  filter_params = {"skip": 0, "limit": "50", "is_valid": "false"}
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objectives"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will retrieve the relevant filtered data for learning objective and serve that data back to the management interface"
)
def scenario_15_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for learning_objective_data in context.res_data["data"]:
    assert learning_objective_data.get(
        "is_valid") is False, "filter not working properly"


# ------------------------------------------ scenario 16 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter learning objective data in knowledge graph for negative scenario"
)
def scenario_16_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)
  saved_lr_id = post_learning_resource.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{saved_lr_id}/concept"
  concept_data = {
      "title": "Idealism",
      "description": "The belief that a perfect life, situation, etc. can be achieved, even when this != very likely",
      "label": "",
      "parent_nodes":  {"learning_resource": []},
      "child_nodes": {"sub_concepts": []},
      "is_valid": "false",
      "type": "concept",
      "alignments": {}
  }
  post_concept = post_method(url, request_body=concept_data)
  saved_concept_id = post_concept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{saved_concept_id}/subconcept"
  subconcept_data = {
      "title": "Essentialism",
      "description": "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods",
      "all_learning_resource": "",
      "parent_nodes":  {"concepts": []},
      "child_nodes": {"learning_objectives": []},
      "label": "",
      "total_lus": 0,
      "is_valid": "false",
      "type": "subconcept",
      "alignments": {}
  }

  post_subconcept = post_method(url, request_body=subconcept_data)
  saved_subconcept_id = post_subconcept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/sub-concept/{saved_subconcept_id}/learning-objective"
  learning_objective_data = {
      "title": "State theorems",
      "description": "A description for State theorems",
      "parent_nodes": {"sub_concepts": []},
      "child_nodes": {"learning_units": []},
      "is_valid": "false",
      "type": "learning_objective",
      "alignments": {},
      "text": [""]
  }
  post_learning_objective = post_method(
      url, request_body=learning_objective_data)
  assert post_learning_objective.status_code == 200, "Status 200"


@behave.when(
    "A filter for learning objective is applied within the management interface with invalid filters for negative scenario"
)
def scenario_16_step_2(context):
  filter_params = {"skip": "-1", "limit": "50", "is_valid": "false"}
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objectives"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will raise error for invalid learning objective filter and send back to the management interface as negative scenario"
)
def scenario_16_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 17 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter learning unit data in knowledge graph"
)
def scenario_17_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)
  saved_lr_id = post_learning_resource.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{saved_lr_id}/concept"
  concept_data = {
      "title": "Idealism",
      "description": "The belief that a perfect life, situation, etc. can be achieved, even when this != very likely",
      "label": "",
      "parent_nodes":  {"learning_resource": []},
      "child_nodes": {"sub_concepts": []},
      "is_valid": "false",
      "type": "concept",
      "alignments": {}
  }
  post_concept = post_method(url, request_body=concept_data)
  saved_concept_id = post_concept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{saved_concept_id}/subconcept"
  subconcept_data = {
      "title": "Essentialism",
      "description": "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods",
      "all_learning_resource": "",
      "parent_nodes":  {"concepts": []},
      "child_nodes": {"learning_objectives": []},
      "label": "",
      "total_lus": 0,
      "is_valid": "false",
      "type": "subconcept",
      "alignments": {}
  }

  post_subconcept = post_method(url, request_body=subconcept_data)
  saved_subconcept_id = post_subconcept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/sub-concept/{saved_subconcept_id}/learning-objective"
  learning_objective_data = {
      "title": "State theorems",
      "description": "A description for State theorems",
      "parent_nodes": {"sub_concepts": []},
      "child_nodes": {"learning_units": []},
      "is_valid": "false",
      "type": "learning_objective",
      "alignments": {},
      "text": [""]
  }
  post_learning_objective = post_method(
      url, request_body=learning_objective_data)
  saved_lo_id = post_learning_objective.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{saved_lo_id}/learning-unit"
  learning_unit_data = {
      "title": "Elementary Data Types",
      "text": [
          "A data type is a class of data objects with a set of operations for creating and manipulating them."
      ],
      "pdf_title": "",
      "parent_nodes": {"learning_objectives": []},
      "child_nodes": {},
      "topics": "",
      "is_valid": "false",
      "type": "learning_resource",
      "alignments": {},
      "coref_text": "",
  }
  post_learning_unit = post_method(url, request_body=learning_unit_data)

  assert post_learning_unit.status_code == 200, "Status 200"


@behave.when(
    "A filter for learning unit is applied within the management interface with permitted filters"
)
def scenario_17_step_2(context):
  filter_params = {"skip": 0, "limit": "50", "is_valid": "false"}
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-units"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will retrieve the relevant filtered data for learning unit and serve that data back to the management interface"
)
def scenario_17_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for learning_unit_data in context.res_data["data"]:
    assert learning_unit_data.get(
        "is_valid") is False, "filter not working properly"


# ------------------------------------------ scenario 18 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter learning unit data in knowledge graph for negative scenario"
)
def scenario_18_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)
  saved_lr_id = post_learning_resource.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{saved_lr_id}/concept"
  concept_data = {
      "title": "Idealism",
      "description": "The belief that a perfect life, situation, etc. can be achieved, even when this != very likely",
      "label": "",
      "parent_nodes":  {"learning_resource": []},
      "child_nodes": {"sub_concepts": []},
      "is_valid": "false",
      "type": "concept",
      "alignments": {}
  }
  post_concept = post_method(url, request_body=concept_data)
  saved_concept_id = post_concept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{saved_concept_id}/subconcept"
  subconcept_data = {
      "title": "Essentialism",
      "description": "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods",
      "all_learning_resource": "",
      "parent_nodes":  {"concepts": []},
      "child_nodes": {"learning_objectives": []},
      "label": "",
      "total_lus": 0,
      "is_valid": "false",
      "type": "subconcept",
      "alignments": {}
  }

  post_subconcept = post_method(url, request_body=subconcept_data)
  saved_subconcept_id = post_subconcept.json().get("data").get("uuid")

  url = f"{API_URL_KNOWLEDGE_SERVICE}/sub-concept/{saved_subconcept_id}/learning-objective"
  learning_objective_data = {
      "title": "State theorems",
      "description": "A description for State theorems",
      "parent_nodes": {"sub_concepts": []},
      "child_nodes": {"learning_units": []},
      "is_valid": "false",
      "type": "learning_objective",
      "alignments": {},
      "text": [""]
  }
  post_learning_objective = post_method(
      url, request_body=learning_objective_data)
  saved_lo_id = post_learning_objective.json().get("data").get("uuid")
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{saved_lo_id}/learning-unit"
  learning_unit_data = {
      "title": "Elementary Data Types",
      "text": [
          "A data type is a class of data objects with a set of operations for creating and manipulating them."
      ],
      "pdf_title": "",
      "parent_nodes": {"learning_objectives": []},
      "child_nodes": {},
      "topics": "",
      "is_valid": "false",
      "type": "learning_resource",
      "alignments": {},
      "coref_text": "",
  }
  post_learning_unit = post_method(url, request_body=learning_unit_data)

  assert post_learning_unit.status_code == 200, "Status 200"


@behave.when(
    "A filter for learning unit is applied within the management interface with invalid filters for negative scenario"
)
def scenario_18_step_2(context):
  filter_params = {"skip": "-1", "limit": "50", "is_valid": "false"}
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-units"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will raise error for invalid learning unit filter and send back to the management interface as negative scenario"
)
def scenario_18_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"


# ------------------------------------------ scenario 19 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter learning resource data in knowledge graph"
)
def scenario_19_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)

  assert post_learning_resource.status_code == 200, "Status 200"


@behave.when(
    "A filter for learning resource is applied within the management interface with permitted filters"
)
def scenario_19_step_2(context):
  filter_params = {
      "skip": 0,
      "limit": "50",
      "document_type": "pdf",
      "course_category": "biology"
  }
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resources"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will retrieve the relevant filtered data for learning resource and serve that data back to the management interface"
)
def scenario_19_step_3(context):
  assert context.res.status_code == 200
  assert context.res_data["success"] is True
  assert len(context.res_data["data"]) != 0
  for learning_resource_data in context.res_data["data"]:
    assert learning_resource_data.get(
        "document_type") == "pdf", "filter not working properly"
    assert learning_resource_data.get(
        "course_category") == "biology", "filter not working properly"


# ------------------------------------------ scenario 20 -------------------------------------------------------------
@behave.given(
    "Given that a user has the ability to filter learning resource data in knowledge graph for negative scenario"
)
def scenario_20_step_1(context):
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"
  learning_resource_data = {
      "title": "Text Books",
      "description": "",
      "document_type": "pdf",
      "child_nodes": {"concepts": []},
      "resource_path": "",
      "type": "learning_resource",
      "alignments": {},
      "course_category": "biology"
  }
  post_learning_resource = post_method(url, request_body=learning_resource_data)

  assert post_learning_resource.status_code == 200, "Status 200"


@behave.when(
    "A filter for learning resource is applied within the management interface with invalid filters for negative scenario"
)
def scenario_20_step_2(context):
  filter_params = {
      "skip": "-1",
      "limit": "50",
      "document_type": "pdf",
      "course_category": "biology"
  }
  url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resources"
  context.res = get_method(url=url, query_params=filter_params)
  context.res_data = context.res.json()


@behave.then(
    "Knowledge Service will raise error for invalid learning resource filter and send back to the management interface as negative scenario"
)
def scenario_20_step_3(context):
  assert context.res.status_code == 422
  assert context.res_data.get(
      "message"
  ) == "Invalid value passed to \"skip\" query parameter", "unknown response received"
