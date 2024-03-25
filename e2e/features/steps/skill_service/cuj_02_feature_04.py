"""
Feature 04 - Delete skills or concepts from skill graph or knowledge graph respectively
"""

import behave
import json
import sys
from copy import deepcopy
sys.path.append("../")
from setup import get_method, post_method, delete_method
from common.models import (Skill, SkillServiceCompetency, Category, Domain, SubDomain,
                          Concept, SubConcept, KnowledgeServiceLearningObjective,
                          KnowledgeServiceLearningUnit, KnowledgeServiceLearningContent)
from test_object_schemas import TEST_SKILL
from test_config import API_URL_SKILL_SERVICE, API_URL_KNOWLEDGE_SERVICE

SKILL =  {
            "uuid": "skill_123",
            "name": "Test skill",
            "description": "Test description"
          }

COMPETENCY = {
            "uuid": "competency_123",
            "name": "Test competency",
            "description": "Test description"
          }

CATEGORY = {
            "uuid": "category_123",
            "name": "Test category",
            "description": "Test description"
          }

DOMAIN = {
            "uuid": "domain_123",
            "name": "Test domain",
            "description": "Test description"
          }

SUB_DOMAIN = {
            "uuid": "subdomain_123",
            "name": "Test subdomain",
            "description": "Test description"
          }

CONCEPT = {
            "uuid": "concept_123",
            "title": "Test concept",
            "label": "Test label",
            "is_valid": True,
            "parent_nodes":  {"learning_resource": []},
            "child_nodes": {"sub_concepts": []},
            "is_archived": False,
            "is_deleted": False
          }

SUB_CONCEPT = {
            "uuid": "subconcept_123",
            "title": "Test subconcept",
            "label": "Test label",
            "all_learning_resource": "Test",
            "total_lus": 0,
            "is_valid": True,
            "parent_nodes":  {"concepts": []},
            "child_nodes": {"learning_objectives": []},
            "is_archived": False,
            "is_deleted": False
          }

LEARNING_UNIT = {
            "uuid": "LU_123",
            "title": "Test LU",
            "text": "Test text",
            "is_valid": True,
            "parent_nodes": {"learning_objectives": []},
            "child_nodes": {},
            "is_archived": False,
            "is_deleted": False
            }

LEARNING_OBJECTIVE = {
            "uuid": "LO_123",
            "title": "Test LO",
            "is_valid": True,
            "parent_nodes": {"sub_concepts": []},
            "child_nodes": {"learning_units": []},
            "is_archived": False,
            "is_deleted": False
            }

LEARNING_RESOURCE = {
            "uuid": "LR_123",
            "title": "Test LR",
            "description": "Test description",
            "document_type": "Test doc type",
            "gcs_path": "Test GCS Path",
            "child_nodes": {"concepts": []},
            "is_archived": False,
            "is_deleted": False
          }


incorrect_skill_id = "dummy_skill_id"
incorrect_competency_id = "dummy_competency_id"
incorrect_category_id = "dummy_category_id"
incorrect_domain_id = "dummy_domain_id"
incorrect_sub_domain_id = "dummy_subdomain_id"
incorrect_concept_id = "dummy_concept_id"
incorrect_sub_concept_id = "dummy_subconcept_id"
incorrect_learning_unit_id = "dummy_lu_id"
incorrect_learning_obj_id = "dummy_lo_id"
incorrect_learning_resource_id = "dummy_lr_id"


#Scenario 1: Successfully delete skill from skill-graph
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a skill.")
def step_impl_1(context):
  test_skill = deepcopy(TEST_SKILL)
  test_skill["parent_nodes"] = {"competencies": [context.competency_id]}
  post_url = f"{API_URL_SKILL_SERVICE}/skill"
  post_res = post_method(url=post_url, request_body=test_skill)
  post_res_data = post_res.json()
  context.new_skill_id = post_res_data["data"]["uuid"]
  context.skill_url = f"{API_URL_SKILL_SERVICE}/skill/{context.new_skill_id}"

  # get requests to check if created skill is present in firestore DB
  get_skill_response = get_method(url=context.skill_url)
  assert get_skill_response.status_code == 200, "Status 200"
  get_skill_response_data = get_skill_response.json()
  assert get_skill_response_data.get("success") is True, "Success not true"
  assert get_skill_response_data.get("message") == "Successfully fetched the skill", "Expected response not same"
  assert context.competency_id in get_skill_response_data["data"]["parent_nodes"]["competencies"]
  # Check if skill ID has been updated in child nodes of competency:
  comp_url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"
  comp_request = get_method(comp_url)
  comp_data = comp_request.json()
  assert comp_request.status_code == 200
  assert context.new_skill_id in comp_data["data"]["child_nodes"]["skills"]


@behave.when("the skill is deleted within the management interface with correct skill id.")
def step_impl_2(context):
  context.del_skill_res = delete_method(url=context.skill_url)
  assert context.del_skill_res.status_code == 200, "Status 200"
  context.del_skill_res_data = context.del_skill_res.json()
  assert context.del_skill_res_data.get("success") is True, "Success not true"
  assert context.del_skill_res_data.get("message") == "Successfully deleted the skill", "Expected response not same"


@behave.then("that skill will be deleted from the Skill graph and its subtree will also get deleted.")
def step_impl_3(context):
  context.get_skill_res = get_method(url=context.skill_url)
  assert context.get_skill_res.status_code != 200, "Status 200"
  # Check if skill ID has been deleted from child nodes of competency:
  comp_url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"
  comp_request = get_method(comp_url)
  comp_data = comp_request.json()
  assert comp_request.status_code == 200
  assert context.new_skill_id not in comp_data["data"]["child_nodes"]["skills"]


#Scenario 2: Unable to delete skill successfully 
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a skill")
def step_impl_1(context):
  skill_1 = Skill.from_dict(SKILL)
  skill_1.save()
  skill_1.uuid = skill_1.id
  skill_1_id = skill_1.id
  context.skill_1_id = skill_1_id
  skill_1.update()

  context.skill_url = f"{API_URL_SKILL_SERVICE}/skill"

  # get requests to check if created skill is present in firestore DB
  correct_skill_url = f"{context.skill_url}/{skill_1_id}"
  get_skill_response = get_method(url=correct_skill_url)
  assert get_skill_response.status_code == 200, "Status 200"
  get_skill_response_data = get_skill_response.json()
  assert get_skill_response_data.get("success") is True, "Success not true"
  assert get_skill_response_data.get("message") == "Successfully fetched the skill", "Expected response not same"


@behave.when("the skill is deleted within the management interface with incorrect skill id")
def step_impl_2(context):
  incorrect_skill_url = f"{context.skill_url}/{incorrect_skill_id}"
  context.del_skill_res = delete_method(url=incorrect_skill_url)
  Skill.delete_by_id(context.skill_1_id)


@behave.then("the Skill Service will throw an error message while trying to delete skill")
def step_impl_3(context):
  assert context.del_skill_res.status_code != 200, "Status 200"



#Scenario 3: Successfully delete Competency from skill-graph
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a competency.")
def step_impl_1(context):
  test_competency = {
      "name": "Regression Analysis",
      "description": "Perform regression analysis to address an authentic problem",
      "keywords": ["tbn"],
      "level" : 2,
      "subject_code": "MAT",
      "course_code": "MAT-240",
      "parent_nodes": {
          "sub_domains": [],
          "categories": [context.category_id]
      },
      "child_nodes": {
          "skills": [context.skill_id]
      },
      "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
      "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
      "source_name": "Credentialengine"
  }
  post_url = f"{API_URL_SKILL_SERVICE}/competency"
  post_res = post_method(url=post_url, request_body=test_competency)
  post_res_data = post_res.json()
  context.new_competency_id = post_res_data["data"]["uuid"]
  context.competency_url = f"{API_URL_SKILL_SERVICE}/competency/{context.new_competency_id}"

  # get requests to check if created competency is present in firestore DB
  get_competency_response = get_method(url=context.competency_url)
  assert get_competency_response.status_code == 200, "Status 200"
  get_competency_response_data = get_competency_response.json()
  assert get_competency_response_data.get("success") is True, "Success not true"
  assert get_competency_response_data.get("message") == "Successfully fetched the competency", "Expected response not same"
  assert context.category_id in get_competency_response_data["data"]["parent_nodes"]["categories"]
  assert context.skill_id in get_competency_response_data["data"]["child_nodes"]["skills"]

  # Check if competency ID has been updated in child nodes of category:
  cat_url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"
  cat_request = get_method(cat_url)
  cat_data = cat_request.json()
  assert cat_request.status_code == 200
  assert context.new_competency_id in cat_data["data"]["child_nodes"]["competencies"]

  # Check if competency ID has been updated in parent nodes of skill:
  skill_url = f"{API_URL_SKILL_SERVICE}/skill/{context.skill_id}"
  skill_request = get_method(skill_url)
  skill_data = skill_request.json()
  assert skill_request.status_code == 200
  assert context.new_competency_id in skill_data["data"]["parent_nodes"]["competencies"]


@behave.when("the competency is deleted within the management interface with correct competency id.")
def step_impl_2(context):
  context.del_competency_res = delete_method(url=context.competency_url)
  assert context.del_competency_res.status_code == 200, "Status 200"
  context.del_competency_res_data = context.del_competency_res.json()
  assert context.del_competency_res_data.get("success") is True, "Success not true"
  assert context.del_competency_res_data.get("message") == "Successfully deleted the competency", "Expected response not same"


@behave.then("that competency will be deleted from the Skill graph and its subtree will also get deleted.")
def step_impl_3(context):
  context.get_competency_res = get_method(url=context.competency_url)
  assert context.get_competency_res.status_code != 200, "Status 200"

  # Check if competency ID has been deleted from child nodes of category:
  cat_url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"
  cat_request = get_method(cat_url)
  cat_data = cat_request.json()
  assert cat_request.status_code == 200
  assert context.new_competency_id not in cat_data["data"]["child_nodes"]["competencies"]

  # Check if competency ID has been deleted from parent nodes of skill:
  skill_url = f"{API_URL_SKILL_SERVICE}/skill/{context.skill_id}"
  skill_request = get_method(skill_url)
  skill_data = skill_request.json()
  assert skill_request.status_code == 200
  assert context.new_competency_id not in skill_data["data"]["parent_nodes"]["competencies"]



#Scenario 4: Unable to delete Competency successfully 
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a competency")
def step_impl_1(context):
  competency_1 = SkillServiceCompetency.from_dict(COMPETENCY)
  competency_1.save()
  competency_1.uuid = competency_1.id
  competency_1_id = competency_1.id
  context.competency_1_id = competency_1_id
  competency_1.update()

  context.competency_url = f"{API_URL_SKILL_SERVICE}/competency"

  # get requests to check if created skill is present in firestore DB
  correct_competency_url = f"{context.competency_url}/{competency_1_id}"
  get_competency_response = get_method(url=correct_competency_url)
  assert get_competency_response.status_code == 200, "Status 200"
  get_competency_response_data = get_competency_response.json()
  assert get_competency_response_data.get("success") is True, "Success not true"
  assert get_competency_response_data.get("message") == "Successfully fetched the competency", "Expected response not same"


@behave.when("the competency is deleted within the management interface with incorrect competency id")
def step_impl_2(context):
  incorrect_competency_url = f"{context.competency_url}/{incorrect_competency_id}"
  context.del_competency_res = delete_method(url=incorrect_competency_url)
  SkillServiceCompetency.delete_by_id(context.competency_1_id)


@behave.then("the Skill Service will throw an error message while trying to delete competency")
def step_impl_3(context):
  assert context.del_competency_res.status_code != 200, "Status 200"



#Scenario 5: Successfully delete Category from skill-graph
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a category.")
def step_impl_1(context):
  test_category = {
        "name": "Regression Analysis",
        "description": "Perform regression analysis to address an authentic problem",
        "keywords": ["tbn"],
        "parent_nodes": {
            "sub_domains": [context.sub_domain_id]
        },
        "child_nodes": {
            "competencies": [context.competency_id]
        },
        "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_name": "Credentialengine"
  }
  post_url = f"{API_URL_SKILL_SERVICE}/category"
  post_res = post_method(url=post_url, request_body=test_category)
  post_res_data = post_res.json()
  context.new_category_id = post_res_data["data"]["uuid"]

  context.category_url = f"{API_URL_SKILL_SERVICE}/category/{context.new_category_id}"

  # get requests to check if created category is present in firestore DB
  get_category_response = get_method(url=context.category_url)
  assert get_category_response.status_code == 200, "Status 200"
  get_category_response_data = get_category_response.json()
  assert get_category_response_data.get("success") is True, "Success not true"
  assert get_category_response_data.get("message") == "Successfully fetched the category", "Expected response not same"
  assert context.sub_domain_id in get_category_response_data["data"]["parent_nodes"]["sub_domains"]
  assert context.competency_id in get_category_response_data["data"]["child_nodes"]["competencies"]

  # Check if category ID has been updated in child nodes of sub-domain:
  subdomain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"
  subdomain_request = get_method(subdomain_url)
  subdomain_data = subdomain_request.json()
  assert subdomain_request.status_code == 200
  assert context.new_category_id in subdomain_data["data"]["child_nodes"]["categories"]

  # Check if category ID has been updated in parent nodes of competency:
  comp_url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"
  comp_request = get_method(comp_url)
  comp_data = comp_request.json()
  assert comp_request.status_code == 200
  assert context.new_category_id in comp_data["data"]["parent_nodes"]["categories"]


@behave.when("the category is deleted within the management interface with correct category id.")
def step_impl_2(context):
  context.del_category_res = delete_method(url=context.category_url)
  assert context.del_category_res.status_code == 200, "Status 200"
  context.del_category_res_data = context.del_category_res.json()
  assert context.del_category_res_data.get("success") is True, "Success not true"
  assert context.del_category_res_data.get("message") == "Successfully deleted the category", "Expected response not same"


@behave.then("that category will be deleted from the Skill graph and its subtree will also get deleted.")
def step_impl_3(context):
  context.get_category_res = get_method(url=context.category_url)
  assert context.get_category_res.status_code != 200, "Status 200"

  # Check if category ID has been deleted from child nodes of sub-domain:
  subdomain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"
  subdomain_request = get_method(subdomain_url)
  subdomain_data = subdomain_request.json()
  assert subdomain_request.status_code == 200
  assert context.new_category_id not in subdomain_data["data"]["child_nodes"]["categories"]

  # Check if category ID has been deleted from parent nodes of competency:
  comp_url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"
  comp_request = get_method(comp_url)
  comp_data = comp_request.json()
  assert comp_request.status_code == 200
  assert context.new_category_id not in comp_data["data"]["parent_nodes"]["categories"]

#Scenario 6: Unable to delete Category successfully
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a category")
def step_impl_1(context):
  category_1 = Category.from_dict(CATEGORY)
  category_1.save()
  category_1.uuid = category_1.id
  category_1_id = category_1.id
  context.category_1_id = category_1_id
  category_1.update()

  context.category_url = f"{API_URL_SKILL_SERVICE}/category"

  # get requests to check if created category is present in firestore DB
  correct_category_url = f"{context.category_url}/{category_1_id}"
  get_category_response = get_method(url=correct_category_url)
  assert get_category_response.status_code == 200, "Status 200"
  get_category_response_data = get_category_response.json()
  assert get_category_response_data.get("success") is True, "Success not true"
  assert get_category_response_data.get("message") == "Successfully fetched the category", "Expected response not same"


@behave.when("the category is deleted within the management interface with incorrect category id")
def step_impl_2(context):
  incorrect_category_url = f"{context.category_url}/{incorrect_category_id}"
  context.del_category_res = delete_method(url=incorrect_category_url)
  Category.delete_by_id(context.category_1_id)


@behave.then("the Skill Service will throw an error message while trying to delete category")
def step_impl_3(context):
  assert context.del_category_res.status_code != 200, "Status 200"



#Scenario 7: Successfully delete Domain from skill-graph
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a domain.")
def step_impl_1(context):
  test_domain = {
        "name": "Regression Analysis",
        "description": "Perform regression analysis to address an authentic problem",
        "keywords": ["tbn"],
        "parent_nodes": {},
        "child_nodes": {
            "sub_domains": [context.sub_domain_id]
        },
        "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_name": "Credentialengine"
  }
  post_url = f"{API_URL_SKILL_SERVICE}/domain"
  post_res = post_method(url=post_url, request_body=test_domain)
  post_res_data = post_res.json()
  context.new_domain_id = post_res_data["data"]["uuid"]

  context.domain_url = f"{API_URL_SKILL_SERVICE}/domain/{context.new_domain_id}"

  # get requests to check if created domain is present in firestore DB
  get_domain_response = get_method(url=context.domain_url)
  assert get_domain_response.status_code == 200, "Status 200"
  get_domain_response_data = get_domain_response.json()
  assert get_domain_response_data.get("success") is True, "Success not true"
  assert get_domain_response_data.get("message") == "Successfully fetched the domain", "Expected response not same"
  assert context.sub_domain_id in get_domain_response_data["data"]["child_nodes"]["sub_domains"]

  # Check if domain ID has been updated in parent nodes of sub-domain:
  subdomain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"
  subdomain_request = get_method(subdomain_url)
  subdomain_data = subdomain_request.json()
  assert subdomain_request.status_code == 200
  assert context.new_domain_id in subdomain_data["data"]["parent_nodes"]["domains"]


@behave.when("the domain is deleted within the management interface with correct domain id.")
def step_impl_2(context):
  context.del_domain_res = delete_method(url=context.domain_url)
  assert context.del_domain_res.status_code == 200, "Status 200"
  context.del_domain_res_data = context.del_domain_res.json()
  assert context.del_domain_res_data.get("success") is True, "Success not true"
  assert context.del_domain_res_data.get("message") == "Successfully deleted the domain", "Expected response not same"


@behave.then("that domain will be deleted from the Skill graph and its subtree will also get deleted.")
def step_impl_3(context):
  context.get_domain_res = get_method(url=context.domain_url)
  assert context.get_domain_res.status_code != 200, "Status 200"

  # Check if domain ID has been deleted from parent nodes of sub-domain:
  subdomain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"
  subdomain_request = get_method(subdomain_url)
  subdomain_data = subdomain_request.json()
  assert subdomain_request.status_code == 200
  assert context.new_domain_id not in subdomain_data["data"]["parent_nodes"]["domains"]



#Scenario 8: Unable to delete Domain successfully
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a domain")
def step_impl_1(context):
  domain_1 = Domain.from_dict(DOMAIN)
  domain_1.save()
  domain_1.uuid = domain_1.id
  domain_1_id = domain_1.id
  context.domain_1_id = domain_1_id
  domain_1.update()

  context.domain_url = f"{API_URL_SKILL_SERVICE}/domain"

  # get requests to check if created domain is present in firestore DB
  correct_domain_url = f"{context.domain_url}/{domain_1_id}"
  get_domain_response = get_method(url=correct_domain_url)
  assert get_domain_response.status_code == 200, "Status 200"
  get_domain_response_data = get_domain_response.json()
  assert get_domain_response_data.get("success") is True, "Success not true"
  assert get_domain_response_data.get("message") == "Successfully fetched the domain", "Expected response not same"


@behave.when("the domain is deleted within the management interface with incorrect domain id")
def step_impl_2(context):
  incorrect_domain_url = f"{context.domain_url}/{incorrect_domain_id}"
  context.del_domain_res = delete_method(url=incorrect_domain_url)
  Domain.delete_by_id(context.domain_1_id)


@behave.then("the Skill Service will throw an error message while trying to delete domain")
def step_impl_3(context):
  assert context.del_domain_res.status_code != 200, "Status 200"



#Scenario 9: Successfully delete Sub-Domain from skill-graph
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a sub_domain.")
def step_impl_1(context):
  test_sub_domain = {
        "name": "Regression Analysis",
        "description": "Perform regression analysis to address an authentic problem",
        "keywords": ["tbn"],
        "parent_nodes": {
            "domains": [context.domain_id]
        },
        "child_nodes": {
            "competencies": [],
            "categories": [context.category_id]
        },
        "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_name": "Credentialengine"
  }
  post_url = f"{API_URL_SKILL_SERVICE}/sub-domain"
  post_res = post_method(url=post_url, request_body=test_sub_domain)
  post_res_data = post_res.json()
  context.new_sub_domain_id = post_res_data["data"]["uuid"]

  context.sub_domain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.new_sub_domain_id}"

  # get requests to check if created sub_domain is present in firestore DB
  get_sub_domain_response = get_method(url=context.sub_domain_url)
  assert get_sub_domain_response.status_code == 200, "Status 200"
  get_sub_domain_response_data = get_sub_domain_response.json()
  assert get_sub_domain_response_data.get("success") is True, "Success not true"
  assert get_sub_domain_response_data.get("message") == "Successfully fetched the sub_domain", "Expected response not same"
  assert context.domain_id in get_sub_domain_response_data["data"]["parent_nodes"]["domains"]
  assert context.category_id in get_sub_domain_response_data["data"]["child_nodes"]["categories"]

  # Check if sub-domain ID has been updated in child nodes of domain:
  domain_url = f"{API_URL_SKILL_SERVICE}/domain/{context.domain_id}"
  domain_request = get_method(domain_url)
  domain_data = domain_request.json()
  assert domain_request.status_code == 200
  assert context.new_sub_domain_id in domain_data["data"]["child_nodes"]["sub_domains"]

  # Check if sub-domain ID has been updated in parent nodes of category:
  cat_url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"
  cat_request = get_method(cat_url)
  cat_data = cat_request.json()
  assert cat_request.status_code == 200
  assert context.new_sub_domain_id in cat_data["data"]["parent_nodes"]["sub_domains"]

@behave.when("the sub_domain is deleted within the management interface with correct sub_domain id.")
def step_impl_2(context):
  context.del_sub_domain_res = delete_method(url=context.sub_domain_url)
  assert context.del_sub_domain_res.status_code == 200, "Status 200"
  context.del_sub_domain_res_data = context.del_sub_domain_res.json()
  assert context.del_sub_domain_res_data.get("success") is True, "Success not true"
  assert context.del_sub_domain_res_data.get("message") == "Successfully deleted the sub_domain", "Expected response not same"


@behave.then("that sub_domain will be deleted from the Skill graph and its subtree will also get deleted.")
def step_impl_3(context):
  context.get_sub_domain_res = get_method(url=context.sub_domain_url)
  assert context.get_sub_domain_res.status_code != 200, "Status 200"

  # Check if sub-domain ID has been deleted from child nodes of domain:
  domain_url = f"{API_URL_SKILL_SERVICE}/domain/{context.domain_id}"
  domain_request = get_method(domain_url)
  domain_data = domain_request.json()
  assert domain_request.status_code == 200
  assert context.new_sub_domain_id not in domain_data["data"]["child_nodes"]["sub_domains"]

  # Check if sub-domain ID has been deleted from parent nodes of category:
  cat_url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"
  cat_request = get_method(cat_url)
  cat_data = cat_request.json()
  assert cat_request.status_code == 200
  assert context.new_sub_domain_id not in cat_data["data"]["parent_nodes"]["sub_domains"]



#Scenario 10: Unable to delete Sub-Domain successfully
@behave.given("that a developer or admin has access to Skill Service (via Competencies & Skill Management) and needs to delete a sub_domain")
def step_impl_1(context):
  sub_domain_1 = SubDomain.from_dict(SUB_DOMAIN)
  sub_domain_1.save()
  sub_domain_1.uuid = sub_domain_1.id
  sub_domain_1_id = sub_domain_1.id
  context.sub_domain_1_id = sub_domain_1_id
  sub_domain_1.update()

  context.sub_domain_url = f"{API_URL_SKILL_SERVICE}/sub-domain"

  # get requests to check if created sub_domain is present in firestore DB
  correct_sub_domain_url = f"{context.sub_domain_url}/{sub_domain_1_id}"
  get_sub_domain_response = get_method(url=correct_sub_domain_url)
  assert get_sub_domain_response.status_code == 200, "Status 200"
  get_sub_domain_response_data = get_sub_domain_response.json()
  assert get_sub_domain_response_data.get("success") is True, "Success not true"
  assert get_sub_domain_response_data.get("message") == "Successfully fetched the sub_domain", "Expected response not same"


@behave.when("the sub_domain is deleted within the management interface with incorrect sub_domain id")
def step_impl_2(context):
  incorrect_sub_domain_url = f"{context.sub_domain_url}/{incorrect_sub_domain_id}"
  context.del_sub_domain_res = delete_method(url=incorrect_sub_domain_url)
  SubDomain.delete_by_id(context.sub_domain_1_id)


@behave.then("the Skill Service will throw an error message while trying to delete sub-domain")
def step_impl_3(context):
  assert context.del_sub_domain_res.status_code != 200, "Status 200"



#Scenario 11: Successfully delete concept from knowledge-graph
@behave.given("that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a concept.")
def step_impl_1(context):
  learning_resource = KnowledgeServiceLearningContent.from_dict(LEARNING_RESOURCE)
  learning_resource.save()
  learning_resource.uuid = learning_resource.id
  learning_resource.update()

  concept_1 = Concept.from_dict(CONCEPT)
  concept_1.parent_nodes = {"learning_resource": [learning_resource.uuid]}
  concept_1.save()
  concept_1.uuid = concept_1.id
  concept_1_id = concept_1.id
  concept_1.update()

  learning_resource.child_nodes = {"concepts": [concept_1.uuid]}
  learning_resource.update()

  subconcept_1 = SubConcept.from_dict(SUB_CONCEPT)
  subconcept_1.uuid = ""
  subconcept_1.parent_nodes = {"concepts": [concept_1.uuid]}
  subconcept_1.save()
  subconcept_1.update()

  concept_1.child_nodes = {"sub_concepts": [subconcept_1.uuid]}
  concept_1.update()

  context.concept_uuid = concept_1.uuid
  context.subconcept_uuid = subconcept_1.uuid
  context.learning_resource_uuid = learning_resource.uuid
  context.concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{concept_1_id}"

  # get requests to check if created concept is present in firestore DB
  get_concept_response = get_method(url=context.concept_url)
  assert get_concept_response.status_code == 200, "Status not 200"
  get_concept_response_data = get_concept_response.json()
  assert get_concept_response_data.get("success") is True, "Success not true"
  assert get_concept_response_data.get("message") == "Successfully fetched the concept", "Expected response not same"


@behave.when("the concept is deleted within the management interface with correct concept id.")
def step_impl_2(context):
  context.del_concept_res = delete_method(url=context.concept_url)
  assert context.del_concept_res.status_code == 200, "Status 200"
  context.del_concept_res_data = context.del_concept_res.json()
  assert context.del_concept_res_data.get("success") is True, "Success not true"
  assert context.del_concept_res_data.get("message") == "Successfully deleted the concept", "Expected response not same"


@behave.then("that concept will be deleted from the knowledge graph and its subtree will also get deleted.")
def step_impl_3(context):
  # Checking if Concept ID removed from parent and child node
  lr = KnowledgeServiceLearningContent.find_by_uuid(context.learning_resource_uuid)
  sc = SubConcept.find_by_uuid(context.subconcept_uuid)
  assert context.concept_uuid not in lr.child_nodes["concepts"], "Concept id present in parent Learning Resource"
  assert context.concept_uuid not in sc.parent_nodes["concepts"], "Concept id present in child Sub Concept"
  # Checking if the Concept still exists as it is soft deleted
  context.get_concept_res = get_method(url=context.concept_url)
  assert context.get_concept_res.status_code == 404, "Node not soft deleted"


#Scenario 12: Unable to delete concept successfully 
@behave.given("that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a concept")
def step_impl_1(context):
  concept_1 = Concept.from_dict(CONCEPT)
  concept_1.save()
  concept_1.uuid = concept_1.id
  concept_1_id = concept_1.id
  context.concept_1_id = concept_1_id
  concept_1.update()

  context.concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/concept"

  # get requests to check if created concept is present in firestore DB
  correct_concept_url = f"{context.concept_url}/{concept_1_id}"
  get_concept_response = get_method(url=correct_concept_url)
  assert get_concept_response.status_code == 200, "Status 200"
  get_concept_response_data = get_concept_response.json()
  assert get_concept_response_data.get("success") is True, "Success not true"
  assert get_concept_response_data.get("message") == "Successfully fetched the concept", "Expected response not same"


@behave.when("the concept is deleted within the management interface with incorrect concept id")
def step_impl_2(context):
  incorrect_concept_url = f"{context.concept_url}/{incorrect_concept_id}"
  context.del_concept_res = delete_method(url=incorrect_concept_url)
  Concept.delete_by_id(context.concept_1_id)


@behave.then("the knowledge Service will throw an error message to the user while trying to delete concept")
def step_impl_3(context):
  assert context.del_concept_res.status_code != 200, "Status 200"



#Scenario 13: Successfully delete Sub-Concept from knowledge-graph
@behave.given("that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a sub_concept.")
def step_impl_1(context):
  concept_1 = Concept.from_dict(CONCEPT)
  concept_1.save()
  concept_1.uuid = concept_1.id
  concept_1.update()

  sub_concept_1 = SubConcept.from_dict(SUB_CONCEPT)
  sub_concept_1.parent_nodes = {"concepts": [concept_1.uuid]}
  sub_concept_1.save()
  sub_concept_1.uuid = sub_concept_1.id
  sub_concept_1_id = sub_concept_1.id
  sub_concept_1.update()

  concept_1.child_nodes = {"sub_concepts": [sub_concept_1.uuid]}
  concept_1.update()

  lo_1 = KnowledgeServiceLearningObjective.from_dict(LEARNING_OBJECTIVE)
  lo_1.uuid = ""
  lo_1.parent_nodes = {"sub_concepts": [sub_concept_1.uuid]}
  lo_1.save()
  lo_1.uuid = lo_1.id
  lo_1.update()

  sub_concept_1.child_nodes = {"learning_objectives": [lo_1.uuid]}
  sub_concept_1.update()

  context.concept_uuid = concept_1.uuid
  context.sub_concept_uuid = sub_concept_1.uuid
  context.learning_objective_uuid = lo_1.uuid
  context.sub_concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/{sub_concept_1_id}"

  # get requests to check if created sub_concept is present in firestore DB
  get_sub_concept_response = get_method(url=context.sub_concept_url)
  assert get_sub_concept_response.status_code == 200, "Status not 200"
  get_sub_concept_response_data = get_sub_concept_response.json()
  assert get_sub_concept_response_data.get("success") is True, "Success not true"
  assert get_sub_concept_response_data.get("message") == "Successfully fetched the subconcept", "Expected response not same"


@behave.when("the sub_concept is deleted within the management interface with correct sub_concept id.")
def step_impl_2(context):
  context.del_sub_concept_res = delete_method(url=context.sub_concept_url)
  assert context.del_sub_concept_res.status_code == 200, "Status 200"
  context.del_sub_concept_res_data = context.del_sub_concept_res.json()
  assert context.del_sub_concept_res_data.get("success") is True, "Success not true"
  assert context.del_sub_concept_res_data.get("message") == "Successfully deleted the subconcept", "Expected response not same"


@behave.then("that sub_concept will be deleted from the knowledge graph and its subtree will also get deleted.")
def step_impl_3(context):
  lo = KnowledgeServiceLearningObjective.find_by_uuid(context.learning_objective_uuid)
  con = Concept.find_by_uuid(context.concept_uuid)
  assert context.sub_concept_uuid not in lo.parent_nodes["sub_concepts"], "Sub Concept not unlinked from child node"
  assert context.sub_concept_uuid not in con.child_nodes["sub_concepts"]
  context.get_sub_concept_res = get_method(url=context.sub_concept_url)
  assert context.get_sub_concept_res.status_code == 404, "Node not soft deleted"


#Scenario 14: Unable to delete Sub-Concept successfully
@behave.given("that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a sub_concept")
def step_impl_1(context):
  sub_concept_1 = SubConcept.from_dict(SUB_CONCEPT)
  sub_concept_1.save()
  sub_concept_1.uuid = sub_concept_1.id
  sub_concept_1_id = sub_concept_1.id
  context.sub_concept_1_id = sub_concept_1_id
  sub_concept_1.update()

  context.sub_concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept"

  # get requests to check if created sub_concept is present in firestore DB
  correct_sub_concept_url = f"{context.sub_concept_url}/{sub_concept_1_id}"
  get_sub_concept_response = get_method(url=correct_sub_concept_url)
  assert get_sub_concept_response.status_code == 200, "Status 200"
  get_sub_concept_response_data = get_sub_concept_response.json()
  assert get_sub_concept_response_data.get("success") is True, "Success not true"
  assert get_sub_concept_response_data.get("message") == "Successfully fetched the subconcept", "Expected response not same"


@behave.when("the sub_concept is deleted within the management interface with incorrect sub_concept id")
def step_impl_2(context):
  incorrect_sub_concept_url = f"{context.sub_concept_url}/{incorrect_sub_concept_id}"
  context.del_sub_concept_res = delete_method(url=incorrect_sub_concept_url)
  SubConcept.delete_by_id(context.sub_concept_1_id)


@behave.then("the knowledge Service will throw an error message to the user while trying to delete sub-concept")
def step_impl_3(context):
  assert context.del_sub_concept_res.status_code != 200, "Status 200"



#Scenario 15: Successfully delete Learning Objective from knowledge-graph
@behave.given("that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a learning_objective.")
def step_impl_1(context):
  sub_concept_1 = SubConcept.from_dict(SUB_CONCEPT)
  sub_concept_1.save()
  sub_concept_1.uuid = sub_concept_1.id
  sub_concept_1.update()

  learning_obj_1 = KnowledgeServiceLearningObjective.from_dict(LEARNING_OBJECTIVE)
  learning_obj_1.parent_nodes= {"sub_concepts": [sub_concept_1.uuid]}
  learning_obj_1.save()
  learning_obj_1.uuid = learning_obj_1.id
  learning_obj_1_id = learning_obj_1.id
  learning_obj_1.update()

  sub_concept_1.child_nodes = {"learning_objectives": [learning_obj_1.uuid]}
  sub_concept_1.update()

  learning_unit_1 = KnowledgeServiceLearningUnit.from_dict(LEARNING_UNIT)
  learning_unit_1.uuid = ""
  learning_unit_1.parent_nodes = {"learning_objectives": [learning_obj_1.uuid]}
  learning_unit_1.save()
  learning_unit_1.uuid = learning_unit_1.id
  learning_unit_1.update()

  learning_obj_1.child_nodes = {"learning_units": [learning_unit_1.uuid]}
  learning_obj_1.update()

  context.sub_concept_uuid = sub_concept_1.uuid
  context.learning_obj_uuid = learning_obj_1.uuid
  context.learning_unit_uuid = learning_unit_1.uuid
  context.learning_obj_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{learning_obj_1_id}"

  # get requests to check if created learning_obj is present in firestore DB
  get_learning_obj_response = get_method(url=context.learning_obj_url)
  assert get_learning_obj_response.status_code == 200, "Status not 200"
  get_learning_obj_response_data = get_learning_obj_response.json()
  assert get_learning_obj_response_data.get("success") is True, "Success not true"
  assert get_learning_obj_response_data.get("message") == "Successfully fetched the learning objective", "Expected response not same"


@behave.when("the learning_objective is deleted within the management interface with correct learning_objective id.")
def step_impl_2(context):
  context.del_learning_obj_res = delete_method(url=context.learning_obj_url)
  assert context.del_learning_obj_res.status_code == 200, "Status 200"
  context.del_learning_obj_res_data = context.del_learning_obj_res.json()
  assert context.del_learning_obj_res_data.get("success") is True, "Success not true"
  assert context.del_learning_obj_res_data.get("message") == "Successfully deleted the learning objective", "Expected response not same"


@behave.then("that learning_objective will be deleted from the knowledge graph and its subtree will also get deleted.")
def step_impl_3(context):
  sc = SubConcept.find_by_uuid(context.sub_concept_uuid)
  lu = KnowledgeServiceLearningUnit.find_by_uuid(context.learning_unit_uuid)
  assert context.learning_obj_uuid not in lu.parent_nodes["learning_objectives"], "Learning Objective not unlinked from child node"
  assert context.learning_obj_uuid not in sc.child_nodes["learning_objectives"]
  context.get_learning_obj_res = get_method(url=context.learning_obj_url)
  assert context.get_learning_obj_res.status_code == 404, "Node not soft deleted"

#Scenario 16: Unable to delete Learning Objective successfully
@behave.given("that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a learning_objective")
def step_impl_1(context):
  learning_obj_1 = KnowledgeServiceLearningObjective.from_dict(LEARNING_OBJECTIVE)
  learning_obj_1.save()
  learning_obj_1.uuid = learning_obj_1.id
  learning_obj_1_id = learning_obj_1.id
  context.learning_obj_1_id = learning_obj_1_id
  learning_obj_1.update()

  context.learning_obj_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective"

  # get requests to check if created learning_objective is present in firestore DB
  correct_learning_obj_url = f"{context.learning_obj_url}/{learning_obj_1_id}"
  get_learning_obj_response = get_method(url=correct_learning_obj_url)
  assert get_learning_obj_response.status_code == 200, "Status 200"
  get_learning_obj_response_data = get_learning_obj_response.json()
  assert get_learning_obj_response_data.get("success") is True, "Success not true"
  assert get_learning_obj_response_data.get("message") == "Successfully fetched the learning objective", "Expected response not same"


@behave.when("the learning_objective is deleted within the management interface with incorrect learning_objective id")
def step_impl_2(context):
  incorrect_learning_obj_url = f"{context.learning_obj_url}/{incorrect_learning_obj_id}"
  context.del_learning_obj_res = delete_method(url=incorrect_learning_obj_url)
  KnowledgeServiceLearningObjective.delete_by_id(context.learning_obj_1_id)


@behave.then("the knowledge Service will throw an error message to the user while trying to delete learning-objective")
def step_impl_3(context):
  assert context.del_learning_obj_res.status_code != 200, "Status 200"



#Scenario 17: Successfully delete Learning Unit from knowledge-graph
@behave.given("that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a learning_unit.")
def step_impl_1(context):
  learning_obj_1 = KnowledgeServiceLearningObjective.from_dict(LEARNING_OBJECTIVE)
  learning_obj_1.save()
  learning_obj_1.uuid = learning_obj_1.id
  learning_obj_1.update()
  
  learning_unit_1 = KnowledgeServiceLearningUnit.from_dict(LEARNING_UNIT)
  learning_unit_1.parent_nodes = {"learning_objectives": [learning_obj_1.uuid]}
  learning_unit_1.save()
  learning_unit_1.uuid = learning_unit_1.id
  learning_unit_1_id = learning_unit_1.id
  learning_unit_1.update()

  learning_obj_1.child_nodes = {"learning_units": [learning_unit_1.uuid]}
  learning_obj_1.update()

  context.learning_obj_uuid = learning_obj_1.uuid
  context.learning_unit_uuid = learning_unit_1.uuid
  context.learning_unit_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{learning_unit_1_id}"

  # get requests to check if created learning_unit is present in firestore DB
  get_learning_unit_response = get_method(url=context.learning_unit_url)
  assert get_learning_unit_response.status_code == 200, "Status not 200"
  get_learning_unit_response_data = get_learning_unit_response.json()
  assert get_learning_unit_response_data.get("success") is True, "Success not true"
  assert get_learning_unit_response_data.get("message") == "Successfully fetched the learning unit", "Expected response not same"


@behave.when("the learning_unit is deleted within the management interface with correct learning_unit id.")
def step_impl_2(context):
  context.del_learning_unit_res = delete_method(url=context.learning_unit_url)
  assert context.del_learning_unit_res.status_code == 200, "Status 200"
  context.del_learning_unit_res_data = context.del_learning_unit_res.json()
  assert context.del_learning_unit_res_data.get("success") is True, "Success not true"
  assert context.del_learning_unit_res_data.get("message") == "Successfully deleted the learning unit", "Expected response not same"


@behave.then("that learning_unit will be deleted from the knowledge graph and its subtree will also get deleted.")
def step_impl_3(context):
  lo = KnowledgeServiceLearningObjective.find_by_uuid(context.learning_obj_uuid)
  assert context.learning_unit_uuid not in lo.child_nodes["learning_units"]
  context.get_learning_unit_res = get_method(url=context.learning_unit_url)
  assert context.get_learning_unit_res.status_code == 404, "Node not soft deleted"


#Scenario 18: Unable to delete Learning Unit successfully
@behave.given("that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a learning_unit")
def step_impl_1(context):
  learning_unit_1 = KnowledgeServiceLearningUnit.from_dict(LEARNING_UNIT)
  learning_unit_1.save()
  learning_unit_1.uuid = learning_unit_1.id
  learning_unit_1_id = learning_unit_1.id
  context.learning_unit_1_id = learning_unit_1_id
  learning_unit_1.update()

  context.learning_unit_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit"

  # get requests to check if created learning_unit is present in firestore DB
  correct_learning_unit_url = f"{context.learning_unit_url}/{learning_unit_1_id}"
  get_learning_unit_response = get_method(url=correct_learning_unit_url)
  assert get_learning_unit_response.status_code == 200, "Status 200"
  get_learning_unit_response_data = get_learning_unit_response.json()
  assert get_learning_unit_response_data.get("success") is True, "Success not true"
  assert get_learning_unit_response_data.get("message") == "Successfully fetched the learning unit", "Expected response not same"


@behave.when("the learning_unit is deleted within the management interface with incorrect learning_unit id")
def step_impl_2(context):
  incorrect_learning_unit_url = f"{context.learning_unit_url}/{incorrect_learning_unit_id}"
  context.del_learning_unit_res = delete_method(url=incorrect_learning_unit_url)
  KnowledgeServiceLearningUnit.delete_by_id(context.learning_unit_1_id)


@behave.then("the knowledge Service will throw an error message to the user while trying to delete learning-unit")
def step_impl_3(context):
  assert context.del_learning_unit_res.status_code != 200, "Status 200"



#Scenario 19: Successfully delete Learning Resource from knowledge-graph
@behave.given("that a developer or admin has access to Knowledge Service (via Competencies & Skill Management) and needs to delete a learning_resource.")
def step_impl_1(context):
  learning_resource_1 = KnowledgeServiceLearningContent.from_dict(LEARNING_RESOURCE)
  learning_resource_1.save()
  learning_resource_1.uuid = learning_resource_1.id
  learning_resource_1_id = learning_resource_1.id
  learning_resource_1.update()

  concept_1 = Concept.from_dict(CONCEPT)
  concept_1.parent_nodes = {"learning_resource": [learning_resource_1.uuid]}
  concept_1.save()
  concept_1.uuid = concept_1.id
  concept_1_id = concept_1.id
  concept_1.update()

  learning_resource_1.child_nodes = {"concepts": [concept_1.uuid]}
  learning_resource_1.update()

  context.concept_uuid = concept_1.uuid
  context.lr_uuid = learning_resource_1.uuid

  context.learning_resource_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{learning_resource_1_id}"

  # get requests to check if created learning_resource is present in firestore DB
  get_learning_resource_response = get_method(url=context.learning_resource_url)
  assert get_learning_resource_response.status_code == 200, "Status not 200"
  get_learning_resource_response_data = get_learning_resource_response.json()
  assert get_learning_resource_response_data.get("success") is True, "Success not true"
  assert get_learning_resource_response_data.get("message") == "Successfully fetched the learning resource", "Expected response not same"


@behave.when("the learning_resource is deleted within the management interface with correct learning_resource id.")
def step_impl_2(context):
  context.del_learning_resource_res = delete_method(url=context.learning_resource_url)
  assert context.del_learning_resource_res.status_code == 200, "Status 200"
  context.del_learning_resource_res_data = context.del_learning_resource_res.json()
  assert context.del_learning_resource_res_data.get("success") is True, "Success not true"
  assert context.del_learning_resource_res_data.get("message") == "Successfully deleted the learning resource", "Expected response not same"


@behave.then("that learning_resource will be deleted from the knowledge graph and its subtree will also get deleted.")
def step_impl_3(context):
  con = Concept.find_by_uuid(context.concept_uuid)
  assert context.lr_uuid not in con.parent_nodes["learning_resource"] 
  context.get_learning_resource_res = get_method(url=context.learning_resource_url)
  assert context.get_learning_resource_res.status_code == 404, "Status 200"


#Scenario 20: Unable to delete Learning Resource successfully
@behave.given("that a developer or admin has access to knowledge Service (via Competencies & Skill Management) and needs to delete a learning_resource")
def step_impl_1(context):
  learning_resource_1 = KnowledgeServiceLearningContent.from_dict(LEARNING_RESOURCE)
  learning_resource_1.save()
  learning_resource_1.uuid = learning_resource_1.id
  learning_resource_1_id = learning_resource_1.id
  context.learning_resource_1_id = learning_resource_1_id
  learning_resource_1.update()

  context.learning_resource_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"

  # get requests to check if created learning_resource is present in firestore DB
  correct_learning_resource_url = f"{context.learning_resource_url}/{learning_resource_1_id}"
  get_learning_resource_response = get_method(url=correct_learning_resource_url)
  assert get_learning_resource_response.status_code == 200, "Status 200"
  get_learning_resource_response_data = get_learning_resource_response.json()
  assert get_learning_resource_response_data.get("success") is True, "Success not true"
  assert get_learning_resource_response_data.get("message") == "Successfully fetched the learning resource", "Expected response not same"


@behave.when("the learning_resource is deleted within the management interface with incorrect learning_resource id")
def step_impl_2(context):
  incorrect_learning_resource_url = f"{context.learning_resource_url}/{incorrect_learning_resource_id}"
  context.del_learning_resource_res = delete_method(url=incorrect_learning_resource_url)
  KnowledgeServiceLearningContent.delete_by_id(context.learning_resource_1_id)


@behave.then("the knowledge Service will throw an error message to the user while trying to delete learning-resource")
def step_impl_3(context):
  assert context.del_learning_resource_res.status_code != 200, "Status 200"
