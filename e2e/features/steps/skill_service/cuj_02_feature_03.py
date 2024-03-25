"""
Update skills and concepts within skill graph and knowledge graph respectively
"""

import time
import behave
import json
from copy import copy, deepcopy
import sys 
sys.path.append("../")
from setup import post_method, get_method, put_method

from unittest import mock

from common.models import Concept, SubConcept, KnowledgeServiceLearningObjective, KnowledgeServiceLearningUnit
from common.models import Skill, SkillServiceCompetency, Domain, SubDomain, Category

from test_object_schemas import (DOMAIN_OBJ_TEMPLATE, SUB_DOMAIN_OBJ_TEMPLATE,
  CATEGORY_OBJ_TEMPLATE, COMPETENCY_OBJ_TEMPLATE, LEARNING_OBJECTIVE_OBJ_TEMPLATE,
  LEARNING_UNIT_OBJ_TEMPLATE, CONCEPT_OBJ_TEMPLATE,
  SUBCONCEPT_OBJ_TEMPLATE, SKILL_OBJ_TEMPLATE)
from test_config import API_URL_SKILL_SERVICE, API_URL_KNOWLEDGE_SERVICE

#concepts
@behave.given("that a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a concept")
def step_impl_1(context):
  context.concept_dict = CONCEPT_OBJ_TEMPLATE
  concept = Concept.from_dict(context.concept_dict)
  concept.uuid = ""
  concept.save()
  concept.uuid = concept.id
  concept.update()
  context.concept_uuid = concept.id
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{context.concept_uuid}"

@behave.when("the concept is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.concept_dict
  updated_data["title"] = "Imagination"
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()


@behave.then("that concept should be updated within the knowledge graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the concept", "Expected response not same"
  assert context.resp_data.get("data").get("title") == "Imagination"
  
#-------------------------------------------------------------------------------------------

@behave.given("that a user has access to Knowledge Service and needs to update a concept")
def step_impl_1(context):  
  context.concept_dict = CONCEPT_OBJ_TEMPLATE
  concept = Concept.from_dict(context.concept_dict)
  concept.uuid = ""
  concept.save()
  concept.uuid = concept.id
  concept.update()
  context.concept_uuid = concept.id
  context.concept_dict["uuid"] = concept.id
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{context.concept_uuid}"

@behave.when("that concept is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.concept_dict
  updated_data["description"] = "Develop goals with organizational team leads"
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that concept should be updated successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the concept", "Expected response not same"
  assert context.resp_data.get("data").get("description") == "Develop goals with organizational team leads"

@behave.then("the concept alignments should be recalculated successfully")
def step_impl_4(context):
  alignment_url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"
  concept_id = context.concept_dict["uuid"]
  req_body = {
      "ids": [concept_id],
      "top_k": 5,
      "alignment_sources" : ["e2e_osn"],
      "knowledge_level": "concepts"
  }
  response = post_method(url = alignment_url, request_body = req_body)
  res_data = response.json()
  time.sleep(20)
  assert response.status_code == 200
  assert res_data["success"] is True
  assert res_data["data"]["status"] == "active"
  #check if job succeeded
  job_name = res_data["data"]["job_name"]
  url = f"{API_URL_KNOWLEDGE_SERVICE}/jobs/skill_alignment/{job_name}"
  for i in range(50):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"
  #check alignment
  concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{concept_id}"
  resp = get_method(url = concept_url)
  resp_data = resp.json()
  assert resp.status_code == 200
  assert resp_data["success"] == True
  assert len(resp_data["data"]["alignments"]["skill_alignment"]["e2e_osn"]["suggested"]) >0

#-------------------------------------------------------------------------------------------

@behave.given("a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a concept")
def step_impl_1(context):
  context.concept_dict = CONCEPT_OBJ_TEMPLATE
  concept = Concept.from_dict(context.concept_dict)
  concept.uuid = ""
  concept.save()
  concept.uuid = concept.id
  concept.update()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/U2DDBkl3Ayg0PWudzhI"

@behave.when("the concept is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.resp = put_method(url = context.url, request_body = context.concept_dict)
  context.resp_data = context.resp.json()


@behave.then("concept update process should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False
  assert context.resp_data["data"] is None
  assert context.resp_data["message"] == "Concept with uuid U2DDBkl3Ayg0PWudzhI not found"

#-------------------------------------------------------------------------------------------

#subconcepts
@behave.given("that a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a subconcept")
def step_impl_1(context):
  context.subconcept_dict = SUBCONCEPT_OBJ_TEMPLATE
  subconcept = SubConcept.from_dict(context.subconcept_dict)
  subconcept.uuid = ""
  subconcept.save()
  subconcept.uuid = subconcept.id
  subconcept.update()
  context.subconcept_uuid = subconcept.id
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/{context.subconcept_uuid}"

@behave.when("the subconcept is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.subconcept_dict
  updated_data["title"] = "Perennialism"
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that subconcept should be updated within the knowledge graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the subconcept", "Expected response not same"
  assert context.resp_data.get("data").get("title") == "Perennialism"
  
#-------------------------------------------------------------------------------------------

@behave.given("that a user has access to Knowledge Service and needs to update a subconcept")
def step_impl_1(context):
  context.subconcept_dict = SUBCONCEPT_OBJ_TEMPLATE
  subconcept = SubConcept.from_dict(context.subconcept_dict)
  subconcept.uuid = ""
  subconcept.save()
  subconcept.uuid = subconcept.id
  subconcept.update()
  context.subconcept_uuid = subconcept.id
  context.subconcept_dict["uuid"] = subconcept.id
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/{context.subconcept_uuid}"

@behave.when("that subconcept is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.subconcept_dict
  updated_data["description"] = "Develop goals with organizational team leads"
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that subconcept should be updated successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the subconcept", "Expected response not same"
  assert context.resp_data.get("data").get("description") == "Develop goals with organizational team leads"

@behave.then("its alignments should be recalculated successfully")
def step_impl_4(context):
  alignment_url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"
  subconcept_id = context.subconcept_dict["uuid"]
  req_body = {
      "ids": [subconcept_id],
      "top_k": 5,
      "alignment_sources" : ["e2e_osn"],
      "knowledge_level": "sub_concepts"
  }
  response = post_method(url = alignment_url, request_body = req_body)
  res_data = response.json()
  time.sleep(10)
  assert response.status_code == 200
  assert res_data["success"] is True
  assert res_data["data"]["status"] == "active"
  #check if job succeeded
  job_name = res_data["data"]["job_name"]
  url = f"{API_URL_KNOWLEDGE_SERVICE}/jobs/skill_alignment/{job_name}"
  for i in range(50):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"
  #check alignment
  concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/{subconcept_id}"
  resp = get_method(url = concept_url)
  resp_data = resp.json()
  assert resp.status_code == 200
  assert resp_data["success"] == True
  assert len(resp_data["data"]["alignments"]["skill_alignment"]["e2e_osn"]["suggested"]) >0

#-------------------------------------------------------------------------------------------


@behave.given("a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a subconcept")
def step_impl_1(context):
  context.subconcept_dict = SUBCONCEPT_OBJ_TEMPLATE
  subconcept = SubConcept.from_dict(context.subconcept_dict)
  subconcept.uuid = ""
  subconcept.save()
  subconcept.uuid = subconcept.id
  subconcept.update()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/U2DDBkl3Ayg0PWudzhI"

@behave.when("the subconcept is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.resp = put_method(url = context.url, request_body = context.subconcept_dict)
  context.resp_data = context.resp.json()

@behave.then("subconcept update process should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False
  assert context.resp_data["data"] is None
  assert context.resp_data["message"] == "SubConcept with uuid U2DDBkl3Ayg0PWudzhI not found"

#-------------------------------------------------------------------------------------------


#knowledge-service learning_objective
@behave.given("that a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a learning objective")
def step_impl_1(context):
  context.learning_objective_dict = LEARNING_OBJECTIVE_OBJ_TEMPLATE
  learning_objective = KnowledgeServiceLearningObjective.from_dict(
      context.learning_objective_dict)
  learning_objective.uuid = ""
  learning_objective.save()
  learning_objective.uuid = learning_objective.id
  learning_objective.update()
  context.learning_objective_uuid = learning_objective.id
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{context.learning_objective_uuid}"

@behave.when("the learning objective is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.learning_objective_dict
  updated_data["title"] = "Prove theorems"
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that learning objective should be updated within the knowledge graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the learning objective", "Expected response not same"
  assert context.resp_data.get("data").get("title") == "Prove theorems"

#-------------------------------------------------------------------------------------------


@behave.given("that a user has access to Knowledge Service and needs to update a learning objective")
def step_impl_1(context):
  context.learning_objective_dict = LEARNING_OBJECTIVE_OBJ_TEMPLATE
  learning_objective = KnowledgeServiceLearningObjective.from_dict(
      context.learning_objective_dict)
  learning_objective.uuid = ""
  learning_objective.save()
  learning_objective.uuid = learning_objective.id
  learning_objective.update()
  context.learning_objective_uuid = learning_objective.id
  context.learning_objective_dict["uuid"] = learning_objective.id
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{context.learning_objective_uuid}"

@behave.when("the learning objective is updated with correct request payload")
def step_impl_2(context):
  updated_data = context.learning_objective_dict
  updated_data["description"] = "Develop goals with organizational team leads"
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that learning objective should be updated successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the learning objective", "Expected response not same"
  assert context.resp_data.get("data").get("description") == "Develop goals with organizational team leads"

@behave.then("learning objective alignments should be recalculated successfully")
def step_impl_4(context):
  alignment_url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"
  lo_id = context.learning_objective_dict["uuid"]
  req_body = {
      "ids": [lo_id],
      "top_k": 5,
      "alignment_sources" : ["e2e_osn"],
      "knowledge_level": "learning_objectives"
  }
  response = post_method(url = alignment_url, request_body = req_body)
  res_data = response.json()
  time.sleep(10)
  assert response.status_code == 200
  assert res_data["success"] is True
  assert res_data["data"]["status"] == "active"
  #check if job succeeded
  job_name = res_data["data"]["job_name"]
  url = f"{API_URL_KNOWLEDGE_SERVICE}/jobs/skill_alignment/{job_name}"
  for i in range(50):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"
  #check alignment
  concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{lo_id}"
  resp = get_method(url = concept_url)
  resp_data = resp.json()
  assert resp.status_code == 200
  assert resp_data["success"] == True
  assert len(resp_data["data"]["alignments"]["skill_alignment"]["e2e_osn"]["suggested"]) >0

#-------------------------------------------------------------------------------------------


@behave.given("a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a learning objective")
def step_impl_1(context):
  context.learning_objective_dict = LEARNING_OBJECTIVE_OBJ_TEMPLATE
  learning_objective = KnowledgeServiceLearningObjective.from_dict(
      context.learning_objective_dict)
  learning_objective.uuid = ""
  learning_objective.save()
  learning_objective.uuid = learning_objective.id
  learning_objective.update()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/U2DDBkl3Ayg0PWudzhI"

@behave.when("the learning objective is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.resp = put_method(url = context.url, request_body = context.learning_objective_dict)
  context.resp_data = context.resp.json()

@behave.then("learning objective update process should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False
  assert context.resp_data["data"] is None
  assert context.resp_data["message"] == "Learning Objective with uuid U2DDBkl3Ayg0PWudzhI not found"

#-------------------------------------------------------------------------------------------


#KnowledgeServiceLearningUnit
@behave.given("that a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a learning unit")
def step_impl_1(context):
  context.learning_unit_dict = copy(LEARNING_UNIT_OBJ_TEMPLATE)
  learning_unit = KnowledgeServiceLearningUnit.from_dict(context.learning_unit_dict)
  learning_unit.uuid = ""
  learning_unit.save()
  learning_unit.uuid = learning_unit.id
  learning_unit.update()
  context.learning_unit_uuid = learning_unit.id
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{context.learning_unit_uuid}"

@behave.when("the learning unit is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = copy(context.learning_unit_dict)
  updated_data["title"] = "Advanced Data Types"
  updated_data["text"] = updated_data["text"].split("<p>")
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that learning unit should be updated within the knowledge graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the learning unit", "Expected response not same"
  assert context.resp_data.get("data").get("title") == "Advanced Data Types"
  
#-------------------------------------------------------------------------------------------


@behave.given("that a user has access to Knowledge Service and needs to update a learning unit")
def step_impl_1(context):
  context.learning_unit_dict = copy(LEARNING_UNIT_OBJ_TEMPLATE)
  learning_unit = KnowledgeServiceLearningUnit.from_dict(context.learning_unit_dict)
  learning_unit.uuid = ""
  learning_unit.save()
  learning_unit.uuid = learning_unit.id
  learning_unit.update()
  context.learning_unit_uuid = learning_unit.id
  context.learning_unit_dict["uuid"] = learning_unit.id
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{context.learning_unit_uuid}"

@behave.when("the learning unit is updated with correct request payload")
def step_impl_2(context):
  updated_data = copy(context.learning_unit_dict)
  updated_data["text"] = ["Develop goals with organizational team leads"]
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that learning unit should be updated successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the learning unit", "Expected response not same"
  assert context.resp_data.get("data").get("text") == "Develop goals with organizational team leads"

@behave.then("learning unit alignments should be recalculated successfully")
def step_impl_4(context):
  alignment_url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"
  concept_id = context.learning_unit_dict["uuid"]
  req_body = {
      "ids": [concept_id],
      "top_k": 5,
      "alignment_sources" : ["e2e_osn"],
      "knowledge_level": "learning_units"
  }
  response = post_method(url = alignment_url, request_body = req_body)
  res_data = response.json()
  time.sleep(10)
  assert response.status_code == 200
  assert res_data["success"] is True
  assert res_data["data"]["status"] == "active"
  #check if job succeeded
  job_name = res_data["data"]["job_name"]
  url = f"{API_URL_KNOWLEDGE_SERVICE}/jobs/skill_alignment/{job_name}"
  for i in range(50):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"
  #check alignment
  concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{concept_id}"
  resp = get_method(url = concept_url)
  resp_data = resp.json()
  assert resp.status_code == 200
  assert resp_data["success"] == True
  assert len(resp_data["data"]["alignments"]["skill_alignment"]["e2e_osn"]["suggested"]) >0

#-------------------------------------------------------------------------------------------


@behave.given("a user has access to Knowledge Service (via Competencies & Skill Management) and needs to update a learning unit")
def step_impl_1(context):
  context.learning_unit_dict = copy(LEARNING_UNIT_OBJ_TEMPLATE)
  learning_unit = KnowledgeServiceLearningUnit.from_dict(context.learning_unit_dict)
  learning_unit.uuid = ""
  learning_unit.save()
  learning_unit.uuid = learning_unit.id
  learning_unit.update()
  context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/U2DDBkl3Ayg0PWudzhI"

@behave.when("the learning unit is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.learning_unit_dict["text"] = context.learning_unit_dict["text"].split("<p>")
  context.resp = put_method(url = context.url, request_body = context.learning_unit_dict)
  context.resp_data = context.resp.json()

@behave.then("learning unit update process should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False
  assert context.resp_data["data"] is None
  assert context.resp_data["message"] == "Learning Unit with uuid U2DDBkl3Ayg0PWudzhI not found"

#-------------------------------------------------------------------------------------------


#domain
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a domain")
def step_impl_1(context):

  context.domain_dict = deepcopy(DOMAIN_OBJ_TEMPLATE)

  domain = Domain.from_dict(context.domain_dict)
  domain.uuid = ""
  domain.save()
  domain.uuid = domain.id
  domain.update()
  context.domain_dict["uuid"] = domain.id
  context.url = f"{API_URL_SKILL_SERVICE}/domain/{domain.id}"

@behave.when("the domain is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.domain_dict  
  updated_data["name"] = "some random name"
  updated_data["child_nodes"] = {"sub_domains": [context.sub_domain_id]}
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that domain should be updated within the skill graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the domain", "Expected response not same"
  assert context.resp_data.get("data").get("name") == "some random name"
  assert context.sub_domain_id in context.resp_data["data"]["child_nodes"]["sub_domains"]
  # Check if domain ID has been updated in parent nodes of sub-domain:
  subdomain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"
  subdomain_request = get_method(subdomain_url)
  subdomain_data = subdomain_request.json()
  assert subdomain_request.status_code == 200
  assert  context.domain_dict["uuid"] in subdomain_data["data"]["parent_nodes"]["domains"]
  
#-------------------------------------------------------------------------------------------


@behave.given("that a user has access to Skill Service and needs to update a domain")
def step_impl_1(context):
  context.url = f"{API_URL_SKILL_SERVICE}/domain"
  context.domain_dict = DOMAIN_OBJ_TEMPLATE

  domain = Domain.from_dict(context.domain_dict)
  domain.uuid = ""
  domain.save()
  domain.uuid = domain.id
  domain.update()
  context.domain_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"
  context.url = f"{API_URL_SKILL_SERVICE}/domain/{context.domain_dict['uuid']}"

@behave.when("the domain is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.resp = put_method(url = context.url, request_body = context.domain_dict)
  context.resp_data = context.resp.json()

@behave.then("domain update process should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False
  assert context.resp_data["data"] is None
  assert context.resp_data["message"] == "Domain with uuid U2DDBkl3Ayg0PWudzhI not found"

#-------------------------------------------------------------------------------------------


 #subdomain
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a subdomain")
def step_impl_1(context):
  
  context.subdomain_dict = deepcopy(SUB_DOMAIN_OBJ_TEMPLATE)
  subdomain = SubDomain.from_dict(context.subdomain_dict)
  subdomain.uuid = ""
  subdomain.save()
  subdomain.uuid = subdomain.id
  subdomain.update()
  context.subdomain_dict["uuid"] = subdomain.id
  context.url = f"{API_URL_SKILL_SERVICE}/sub-domain/{subdomain.id}"

@behave.when("the subdomain is updated within the management interface with correct request payload")
def step_impl_2(context):
  
  updated_data = context.subdomain_dict
  updated_data["name"] = "some random name"
  updated_data["parent_nodes"] = {"domains": [context.domain_id]}
  updated_data["child_nodes"] = {
        "competencies": [],
        "categories": [context.category_id]
        }
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that subdomain should be updated within the skill graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the sub_domain", "Expected response not same"
  assert context.resp_data.get("data").get("name") == "some random name"
  assert context.domain_id in context.resp_data["data"]["parent_nodes"]["domains"]
  assert context.category_id in context.resp_data["data"]["child_nodes"]["categories"]
  # Check if subdomain ID has been updated in parent nodes of categories:
  category_url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"
  category_request = get_method(category_url)
  category_data = category_request.json()
  assert category_request.status_code == 200
  assert  context.subdomain_dict["uuid"] in category_data["data"]["parent_nodes"]["sub_domains"]
  # Check if subdomain ID has been updated in child nodes of domain:
  domain_url = f"{API_URL_SKILL_SERVICE}/domain/{context.domain_id}"
  domain_request = get_method(domain_url)
  domain_data = domain_request.json()
  assert domain_request.status_code == 200
  assert  context.subdomain_dict["uuid"] in domain_data["data"]["child_nodes"]["sub_domains"]

#-------------------------------------------------------------------------------------------
@behave.given("that a user has access to Skill Service and needs to update a subdomain")
def step_impl_1(context):
  
  context.subdomain_dict = SUB_DOMAIN_OBJ_TEMPLATE
  subdomain = SubDomain.from_dict(context.subdomain_dict)
  subdomain.uuid = ""
  subdomain.save()
  subdomain.uuid = subdomain.id
  subdomain.update()
  context.subdomain_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"
  context.url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.subdomain_dict['uuid']}"

@behave.when("the subdomain is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.resp = put_method(url = context.url, request_body = context.subdomain_dict)
  context.resp_data = context.resp.json()

@behave.then("subdomain update process should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False
  assert context.resp_data["data"] is None
  assert context.resp_data["message"] == "Sub Domain with uuid U2DDBkl3Ayg0PWudzhI not found"

#-------------------------------------------------------------------------------------------


#category
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a category")
def step_impl_1(context):
  
  context.category_dict = deepcopy(CATEGORY_OBJ_TEMPLATE)
  category = Category.from_dict(context.category_dict)
  category.uuid = ""
  category.save()
  category.uuid = category.id
  category.update()
  context.category_dict["uuid"] = category.id
  context.url = f"{API_URL_SKILL_SERVICE}/category/{category.id}"

@behave.when("the category is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.category_dict
  updated_data["name"] = "some random name"
  updated_data["parent_nodes"] = {"sub_domains": [context.sub_domain_id]}
  updated_data["child_nodes"] = {"competencies": [context.competency_id]}
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that category should be updated within the skill graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the category", "Expected response not same"
  assert context.resp_data.get("data").get("name") == "some random name"
  assert context.sub_domain_id in context.resp_data["data"]["parent_nodes"]["sub_domains"]
  assert context.competency_id in context.resp_data["data"]["child_nodes"]["competencies"]
  # Check if category ID has been updated in parent nodes of competency:
  comp_url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"
  comp_request = get_method(comp_url)
  comp_data = comp_request.json()
  assert comp_request.status_code == 200
  assert  context.category_dict["uuid"] in comp_data["data"]["parent_nodes"]["categories"]
  # Check if category ID has been updated in child nodes of sub-domain:
  subdomain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"
  subdomain_request = get_method(subdomain_url)
  subdomain_data = subdomain_request.json()
  assert subdomain_request.status_code == 200
  assert  context.category_dict["uuid"] in subdomain_data["data"]["child_nodes"]["categories"]
#-------------------------------------------------------------------------------------------


@behave.given("that a user has access to Skill Service and needs to update a category")
def step_impl_1(context):
  
  context.category_dict = CATEGORY_OBJ_TEMPLATE
  category = Category.from_dict(context.category_dict)
  category.uuid = ""
  category.save()
  category.uuid = category.id
  category.update()
  del context.category_dict["child_nodes"]
  context.category_dict["uuid"] = "random_id"
  context.url = f"{API_URL_SKILL_SERVICE}/category/{context.category_dict['uuid']}"

@behave.when("the category is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.resp = put_method(url = context.url, request_body = context.category_dict)
  context.resp_data = context.resp.json()

@behave.then("category update process should fail")
def step_impl_3(context):
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False

#-------------------------------------------------------------------------------------------


#Competency
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a competency")
def step_impl_1(context):
  
  context.competency_dict = deepcopy(COMPETENCY_OBJ_TEMPLATE)
  competency = SkillServiceCompetency.from_dict(context.competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()
  context.competency_dict["uuid"] = competency.id
  context.url = f"{API_URL_SKILL_SERVICE}/competency/{competency.id}"

@behave.when("the competency is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.competency_dict
  updated_data["name"] = "some random name"
  updated_data["parent_nodes"] = {
        "categories": [context.category_id],
        "sub_domains": []
    }
  updated_data["child_nodes"] = {"skills": [context.skill_id]}
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that competency should be updated within the skill graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the competency", "Expected response not same"
  assert context.resp_data.get("data").get("name") == "some random name"
  assert context.category_id in context.resp_data["data"]["parent_nodes"]["categories"]
  assert context.skill_id in context.resp_data["data"]["child_nodes"]["skills"]
  # Check if competency ID has been updated in parent nodes of skill:
  skill_url = f"{API_URL_SKILL_SERVICE}/skill/{context.skill_id}"
  skill_request = get_method(skill_url)
  skill_data = skill_request.json()
  assert skill_request.status_code == 200
  assert  context.competency_dict["uuid"] in skill_data["data"]["parent_nodes"]["competencies"]
  # Check if competency ID has been updated in child nodes of category:
  category_url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"
  category_request = get_method(category_url)
  category_data = category_request.json()
  assert category_request.status_code == 200
  assert  context.competency_dict["uuid"] in category_data["data"]["child_nodes"]["competencies"]
#-------------------------------------------------------------------------------------------


@behave.given("that a user has access to Skill Service and needs to update a competency")
def step_impl_1(context):
  
  context.competency_dict = COMPETENCY_OBJ_TEMPLATE
  competency = SkillServiceCompetency.from_dict(context.competency_dict)
  competency.uuid = ""
  competency.save()
  competency.uuid = competency.id
  competency.update()
  context.competency_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"
  context.url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_dict['uuid']}"

@behave.when("the competency is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.resp = put_method(url = context.url, request_body = context.competency_dict)
  context.resp_data = context.resp.json()

@behave.then("competency update process should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False
  assert context.resp_data["data"] is None
  assert context.resp_data["message"] == "Competency with uuid U2DDBkl3Ayg0PWudzhI not found"

#-------------------------------------------------------------------------------------------


#Skill 
@behave.given("that a user has access to Skill Service (via Competencies & Skill Management) and needs to update a skill")
def step_impl_1(context):
  
  context.skill_dict = deepcopy(SKILL_OBJ_TEMPLATE)
  skill = Skill.from_dict(context.skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()
  context.skill_dict["uuid"] = skill.id
  context.url = f"{API_URL_SKILL_SERVICE}/skill/{skill.id}"

@behave.when("the skill is updated within the management interface with correct request payload")
def step_impl_2(context):
  updated_data = context.skill_dict
  updated_data["name"] = "some random name"
  updated_data["parent_nodes"] = {"competencies": [context.competency_id]}
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that skill should be updated within the skill graph successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the skill", "Expected response not same"
  assert context.resp_data.get("data").get("name") == "some random name"
  assert context.competency_id in context.resp_data["data"]["parent_nodes"]["competencies"]
  # Check if skill ID has been updated in child nodes of competency:
  comp_url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"
  comp_request = get_method(comp_url)
  comp_data = comp_request.json()
  assert comp_request.status_code == 200
  assert  context.skill_dict["uuid"] in comp_data["data"]["child_nodes"]["skills"]
#-------------------------------------------------------------------------------------------


@behave.given("that a user has access to Skill Service and needs to update a skill")
def step_impl_1(context):
  
  context.skill_dict = SKILL_OBJ_TEMPLATE
  skill = Skill.from_dict(context.skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()
  context.skill_dict["uuid"] = skill.id
  context.url = f"{API_URL_SKILL_SERVICE}/skill/{skill.id}"

@behave.when("that skill is updated with correct request payload")
def step_impl_2(context):
  updated_data = context.skill_dict
  updated_data["description"] = "Apply the appropriate accounting method to achieve an organizational goal"
  context.resp = put_method(url = context.url, request_body = updated_data)
  context.resp_data = context.resp.json()

@behave.then("that skill should be updated successfully")
def step_impl_3(context):
  assert context.resp_data.get("success") is True, "Success not true"
  assert context.resp_data.get("message") == "Successfully updated the skill", "Expected response not same"
  assert context.resp_data.get("data").get("description") == "Apply the appropriate accounting method to achieve an organizational goal"

@behave.then("skill alignments should be recalculated successfully")
def step_impl_4(context):
  alignment_url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"
  internal_skill_id = context.skill_dict["uuid"]
  req_body = {
      "ids": [internal_skill_id],
      "input_type": "skill",
      "top_k": 5,
      "output_alignment_sources" : {"skill_sources": ["e2e_osn"],
            "learning_resource_ids": [] },
      "update_aligned_skills": True
  }
  response = post_method(url = alignment_url, request_body = req_body)
  res_data = response.json()
  time.sleep(10)
  assert response.status_code == 200
  assert res_data["success"] is True
  assert res_data["data"]["status"] == "active"
  #check if job succeeded
  job_name = res_data["data"]["job_name"]
  url = f"{API_URL_SKILL_SERVICE}/jobs/unified_alignment/{job_name}"
  for i in range(60):
    res = get_method(url=url)
    data = res.json()
    if data["data"]["status"] in ["succeeded", "failed"]:
      break
    time.sleep(10)
  assert data["data"]["status"] == "succeeded"
  #check alignment
  skill_url = f"{API_URL_SKILL_SERVICE}/skill/{internal_skill_id}"
  resp = get_method(url = skill_url)
  resp_data = resp.json()
  assert resp.status_code == 200
  assert resp_data["success"] == True
  assert len(resp_data["data"]["alignments"]["skill_alignment"]["e2e_osn"]["suggested"]) >0

#-------------------------------------------------------------------------------------------


@behave.given("a user has access to Skill Service (via Competencies & Skill Management) and needs to update a skill")
def step_impl_1(context):

  context.skill_dict = SKILL_OBJ_TEMPLATE
  skill = Skill.from_dict(context.skill_dict)
  skill.uuid = ""
  skill.save()
  skill.uuid = skill.id
  skill.update()
  context.skill_dict["uuid"] = "U2DDBkl3Ayg0PWudzhI"
  context.url = f"{API_URL_SKILL_SERVICE}/skill/{context.skill_dict['uuid']}"

@behave.when("the skill is updated within the management interface with incorrect request payload")
def step_impl_2(context):
  context.resp = put_method(url = context.url, request_body = context.skill_dict)
  context.resp_data = context.resp.json()

@behave.then("skill update process should fail")
def step_impl_3(context):
  time.sleep(20)
  assert context.resp.status_code == 404
  assert context.resp_data["success"] is False
  assert context.resp_data["data"] is None
  assert context.resp_data["message"] == "Skill with uuid U2DDBkl3Ayg0PWudzhI not found"

