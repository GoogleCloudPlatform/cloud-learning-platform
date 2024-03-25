"""
Create skills and concepts within skill graph and knowledge graph respectively
"""

import time
import behave
import sys
sys.path.append("../")
from setup import post_method, get_method
from copy import copy, deepcopy

from test_object_schemas import TEST_CONCEPT, TEST_SUBCONCEPT, TEST_LEARNING_OBJECTIVE, TEST_LEARNING_UNIT, LEARNING_CONTENT_OBJ_TEMPLATE,TEST_SKILL
from common.models import Concept, SubConcept, KnowledgeServiceLearningObjective, KnowledgeServiceLearningContent
from test_config import API_URL_SKILL_SERVICE, API_URL_KNOWLEDGE_SERVICE

# CREATE SKILL---------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a skill")
def step_impl_1(context):
    """ Defining skill item for creation"""
    test_skill = deepcopy(TEST_SKILL)
    test_skill["parent_nodes"] = {"competencies": [context.competency_id]}
    context.skill_dict = test_skill
    context.url = f"{API_URL_SKILL_SERVICE}/skill"


@behave.when("The node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required node as per the input """
    context.res = post_method(url=context.url, request_body=context.skill_dict)
    context.res_data = context.res.json()

@behave.then("That node will appear within the Skill Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the skill"
    id = context.res_data["data"]["uuid"]
    context.skillid = id
    url = f"{API_URL_SKILL_SERVICE}/skill/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the skill"
    assert opdata["data"]["name"] == "Regression Analysis"
    assert opdata["data"]["description"] == "Perform regression analysis to address an authentic problem"
    assert context.competency_id in opdata["data"]["parent_nodes"]["competencies"]
    # Check if created skill ID has been updated in child nodes of competency:
    comp_url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"
    comp_request = get_method(comp_url)
    comp_data = comp_request.json()
    assert comp_request.status_code == 200
    assert context.skillid in comp_data["data"]["child_nodes"]["skills"]


#-----------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create and align a skill")
def step_impl_1(context):
    """ Defining skill item for creation"""

    context.skill_dict = TEST_SKILL
    context.url = f"{API_URL_SKILL_SERVICE}/skill"


@behave.when("The node is created within the management interface with correct request payload and to be aligned")
def step_impl_2(context):
    """Creating the required node as per the input """
    updated_data = context.skill_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That node will be created within the Skill Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the skill"
    id = context.res_data["data"]["uuid"]
    context.skillid = id
    url = f"{API_URL_SKILL_SERVICE}/skill/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the skill"
    assert opdata["data"]["name"] == "Regression Analysis"
    assert opdata["data"]["description"] == "Perform regression analysis to address an authentic problem"

@behave.then("the skill node to be mapped accordingly")
def step_impl_3(context):
    alignment_url = f"{API_URL_SKILL_SERVICE}/unified-alignment/batch"
    internal_skill_id = context.res_data["data"]["uuid"]
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
    for i in range(40):
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

#------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a skill with incorrect payload")
def step_impl_1(context):
    """ Defining an incorrect skill item for creation"""

    context.payload= {
        "skill": "Regression Analysis",
        "details": "Perform regression analysis to address an authentic problem",
        "keywords": ["regression","analysis"],
        "type": {"id": "ST3","name": "Certification"},
        "parent_nodes": {
            "competencies": []
        },
        "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_name": "Credentialengine"
    }
    context.url = f"{API_URL_SKILL_SERVICE}/skill"

@behave.when("The node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Passing the query with incorrect params """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for skill")
def step_impl_3(context):
    assert context.res.status_code == 422
    context.res_data = context.res.json()
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#CREATE COMPETENCY -------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a competency")
def step_impl_1(context):
    """ Defining competency item for creation"""
    
    context.payload= {
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
    context.url = f"{API_URL_SKILL_SERVICE}/competency"


@behave.when("The competency node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required competnecy node as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()
    

@behave.then("That competency node will appear within the Skill Graph and be mapped accordingly")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the competency"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_SKILL_SERVICE}/competency/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the competency"
    assert opdata["data"]["name"] == "Regression Analysis"
    assert opdata["data"]["description"] == "Perform regression analysis to address an authentic problem"
    assert context.category_id in opdata["data"]["parent_nodes"]["categories"]
    assert context.skill_id in opdata["data"]["child_nodes"]["skills"]
    # Check if created competency ID has been updated in child nodes of category:
    category_url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"
    category_request = get_method(category_url)
    category_data = category_request.json()
    assert category_request.status_code == 200
    assert id in category_data["data"]["child_nodes"]["competencies"]
    # Check if created competency ID has been updated in parent nodes of skill:
    skill_url = f"{API_URL_SKILL_SERVICE}/skill/{context.skill_id}"
    skill_request = get_method(skill_url)
    skill_data = skill_request.json()
    assert skill_request.status_code == 200
    assert id in skill_data["data"]["parent_nodes"]["competencies"]

#-----------------------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a competency incorrect payload")
def step_impl_1(context):
    """ Defining an incorrect competency item for creation"""

    context.payload= {
        "competency": "Regression Analysis",
        "details": "Perform regression analysis to address an authentic problem",
        "keywords": ["tbn"],
        "level" : 2,
        "subject_code": "MAT",
        "course_code": "MAT-240",
        "parent_nodes": {
            "sub_domains": [],
            "categories": []
        },
        "child_nodes": {"skills": []},
    "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
    "source_name": "Credentialengine"
    }
    context.url = f"{API_URL_SKILL_SERVICE}/competency"


@behave.when("The competency node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Passing the query with incorrect params """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for competency")
def step_impl_3(context):
    assert context.res.status_code == 422
    context.res_data = context.res.json()
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#CREATE CATEGORY----------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a category")
def step_impl_1(context):
    """ Defining category item for creation"""

    context.payload= {
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
    context.url = f"{API_URL_SKILL_SERVICE}/category"


@behave.when("The category node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required category node as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("That category node will appear within the Skill Graph and be mapped accordingly")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the category"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_SKILL_SERVICE}/category/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the category"
    assert opdata["data"]["name"] == "Regression Analysis"
    assert opdata["data"]["description"] == "Perform regression analysis to address an authentic problem"
    assert context.sub_domain_id in opdata["data"]["parent_nodes"]["sub_domains"]
    assert context.competency_id in opdata["data"]["child_nodes"]["competencies"]
    # Check if created category ID has been updated in child nodes of sub-domain:
    subdomain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"
    subdomain_request = get_method(subdomain_url)
    subdomain_data = subdomain_request.json()
    assert subdomain_request.status_code == 200
    assert id in subdomain_data["data"]["child_nodes"]["categories"]
    # Check if created category ID has been updated in parent nodes of competency:
    comp_url = f"{API_URL_SKILL_SERVICE}/competency/{context.competency_id}"
    comp_request = get_method(comp_url)
    comp_data = comp_request.json()
    assert comp_request.status_code == 200
    assert id in comp_data["data"]["parent_nodes"]["categories"]

#-----------------------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a category incorrect payload")
def step_impl_1(context):
    """ Defining an incorrect category item for creation"""
    context.payload= {
        "category": "Regression Analysis",
        "details": "Perform regression analysis to address an authentic problem",
        "words": ["tbn"],
        "parent_nodes": {
            "sub_domains": []
        },
        "child_nodes": {
            "competencies": []
        },
        "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_name": "Credentialengine"
        }
    context.url = f"{API_URL_SKILL_SERVICE}/category"
    


@behave.when("The category node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Passing the query with incorrect params """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for category")
def step_impl_3(context):
    assert context.res.status_code == 422
    context.res_data = context.res.json()
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#CREATE SUB-DOMAIN----------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a Sub-domain")
def step_impl_1(context):
    """ Defining Sub-domain item for creation"""

    context.payload= {
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
    context.url = f"{API_URL_SKILL_SERVICE}/sub-domain"


@behave.when("The Sub-domain node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required sub-domain node as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()
    

@behave.then("That Sub-domain node will appear within the Skill Graph and be mapped accordingly")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the sub_domain"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_SKILL_SERVICE}/sub-domain/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the sub_domain"
    assert opdata["data"]["name"] == "Regression Analysis"
    assert opdata["data"]["description"] == "Perform regression analysis to address an authentic problem"
    assert context.domain_id in opdata["data"]["parent_nodes"]["domains"]
    assert context.category_id in opdata["data"]["child_nodes"]["categories"]
    # Check if created sub-domain ID has been updated in child nodes of domain:
    domain_url = f"{API_URL_SKILL_SERVICE}/domain/{context.domain_id}"
    domain_request = get_method(domain_url)
    domain_data = domain_request.json()
    assert domain_request.status_code == 200
    assert id in domain_data["data"]["child_nodes"]["sub_domains"]
    # Check if created sub-domain ID has been updated in parent nodes of category:
    category_url = f"{API_URL_SKILL_SERVICE}/category/{context.category_id}"
    category_request = get_method(category_url)
    category_data = category_request.json()
    assert category_request.status_code == 200
    assert id in category_data["data"]["parent_nodes"]["sub_domains"]

#-----------------------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a Sub-domain incorrect payload")
def step_impl_1(context):
    """ Defining an incorrect sub-domain item for creation"""
    context.payload= {
        "subdomain": "Regression Analysis",
        "details": "Perform regression analysis to address an authentic problem",
        "terms": ["tbn"],
        "parent_nodes": {
            "domains": []
        },
        "child_nodes": {
            "competencies": [],
            "categories": []
        },
        "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_name": "Credentialengine"
}
    context.url = f"{API_URL_SKILL_SERVICE}/sub-domain"
    

@behave.when("The Sub-domain node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Passing the query with incorrect params """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for Sub-domain")
def step_impl_3(context):
    assert context.res.status_code == 422
    context.res_data = context.res.json()
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#CREATE DOMAIN----------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a domain")
def step_impl_1(context):
    """ Defining domain item for creation"""

    context.payload= {
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
    context.url = f"{API_URL_SKILL_SERVICE}/domain"


@behave.when("The domain node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required domain node as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()
    

@behave.then("That domain node will appear within the Skill Graph and be mapped accordingly")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the domain"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_SKILL_SERVICE}/domain/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the domain"
    assert opdata["data"]["name"] == "Regression Analysis"
    assert opdata["data"]["description"] == "Perform regression analysis to address an authentic problem"
    assert opdata["data"]["source_name"] == "Credentialengine"
    assert context.sub_domain_id in opdata["data"]["child_nodes"]["sub_domains"]
    # Check if created domain ID has been updated in parent nodes of sub-domain:
    subdomain_url = f"{API_URL_SKILL_SERVICE}/sub-domain/{context.sub_domain_id}"
    subdomain_request = get_method(subdomain_url)
    subdomain_data = subdomain_request.json()
    assert subdomain_request.status_code == 200
    assert id in subdomain_data["data"]["parent_nodes"]["domains"]

#-----------------------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to Skill Service via Competencies & Skill Management and needs to create a domain incorrect payload")
def step_impl_1(context):
    """ Defining an incorrect domain item for creation"""
    context.payload= {
        "domain": "Regression Analysis",
        "details": "Perform regression analysis to address an authentic problem",
        "child_nodes": {
            "sub_domains": []
        },
        "reference_id": "ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_uri": "https://credentialengineregistry.org/resources/ce-e88e730a-b365-4cdf-b67c-e2e7ad58c13b",
        "source_name": "Credentialengine"
}
    context.url = f"{API_URL_SKILL_SERVICE}/domain"
    


@behave.when("The domain node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Passing the query with incorrect params """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for domain")
def step_impl_3(context):
    assert context.res.status_code == 422
    context.res_data = context.res.json()
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#-----------------------------------------------------------------------------------------------
#--------------------------KNOWLEDGE SERVICE----------------------------------------------------

@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a concept")
def step_impl_1(context):
    """ Defining concept item for creation"""
    learning_resource_dict = copy(LEARNING_CONTENT_OBJ_TEMPLATE)
    learning_resource = KnowledgeServiceLearningContent.from_dict(learning_resource_dict)
    learning_resource.uuid = ""
    learning_resource.save()
    learning_resource.uuid = learning_resource.id
    learning_resource.update()
    context.learning_resource_uuid = learning_resource.uuid

    context.concept_dict = copy(TEST_CONCEPT)

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{learning_resource.uuid}/concept"

@behave.when("The concept node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required concept as per the input """
    updated_data = context.concept_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That concept node will appear within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the concept"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{id}"
    context.conceptid = id
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the concept"
    assert opdata["data"]["title"] == "Idealism"
    assert opdata["data"]["description"] == "The belief that a perfect life, situation, etc. can be achieved, even when this is not very likely"
    assert opdata["data"]["is_valid"] is True
    lr = KnowledgeServiceLearningContent.find_by_uuid(context.learning_resource_uuid)
    assert id in lr.child_nodes["concepts"]

#-----------------------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create and align a concept")
def step_impl_1(context):
    """ Defining concept item for creation"""
    learning_resource_dict = copy(LEARNING_CONTENT_OBJ_TEMPLATE)
    learning_resource = KnowledgeServiceLearningContent.from_dict(learning_resource_dict)
    learning_resource.uuid = ""
    learning_resource.save()
    learning_resource.uuid = learning_resource.id
    learning_resource.update()
    context.learning_resource_uuid = learning_resource.uuid

    context.concept_dict = copy(TEST_CONCEPT)

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{learning_resource.uuid}/concept"

@behave.when("The concept node is created within the management interface with correct request payload and to be aligned")
def step_impl_2(context):
    """Creating the required concept as per the input """
    updated_data = context.concept_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That concept node will be created within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the concept"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{id}"
    context.conceptid = id
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the concept"
    assert opdata["data"]["title"] == "Idealism"
    assert opdata["data"]["description"] == "The belief that a perfect life, situation, etc. can be achieved, even when this is not very likely"
    assert opdata["data"]["is_valid"] is True
    lr = KnowledgeServiceLearningContent.find_by_uuid(context.learning_resource_uuid)
    assert id in lr.child_nodes["concepts"]

@behave.then("concept should be aligned")
def step_impl_4(context):
    alignment_url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"
    concept_id = context.conceptid
    req_body = {
      "ids": [concept_id],
      "top_k": 5,
      "alignment_sources": ["e2e_osn"],
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

    #check allginment
    concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{concept_id}"
    resp = get_method(url = concept_url)
    resp_data = resp.json()
    assert resp.status_code == 200
    assert resp_data["success"] == True
    assert len(resp_data["data"]["alignments"]["skill_alignment"]["e2e_osn"]["suggested"]) >0

    
#-------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a concept with incorrect payload")
def step_impl_1(context):
    """ Defining concept item for creation"""
    learning_resource_dict = LEARNING_CONTENT_OBJ_TEMPLATE
    learning_resource = KnowledgeServiceLearningContent.from_dict(learning_resource_dict)
    learning_resource.uuid = ""
    learning_resource.save()
    learning_resource.uuid = learning_resource.id
    learning_resource.update()
    context.learning_resource_uuid = learning_resource.uuid

    context.payload= {
        "cocnept": "Idealism",
        "describe": "The belief that a perfect life, situation, etc. can be achieved, even when this is not very likely",
        "label": "",
        "validity": True,
        "type": "concept"
}
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{learning_resource.uuid}/concept"

@behave.when("The concept node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Creating the required concept as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for concept")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#-----------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning objective")
def step_impl_1(context):
    """ Defining learning objective item for creation"""
    sub_concept_dict = TEST_SUBCONCEPT
    sub_concept = SubConcept.from_dict(sub_concept_dict)
    sub_concept.uuid = ""
    sub_concept.save()
    sub_concept.uuid = sub_concept.id
    sub_concept.update()
    context.sub_concept_uuid = sub_concept.uuid

    learning_objective_dict = copy(TEST_LEARNING_OBJECTIVE)
    learning_objective_dict["text"] = learning_objective_dict["text"].split("<p>")
    context.learning_objective_dict = learning_objective_dict

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/sub-concept/{sub_concept.uuid}/learning-objective"

@behave.when("The learning objective node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required learning objective as per the input """
    updated_data = context.learning_objective_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That learning objective node will appear within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the learning objective"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the learning objective"
    assert opdata["data"]["title"] == "State theorems"
    assert opdata["data"]["description"] == "A description for State theorems"
    assert opdata["data"]["is_valid"] is True
    assert opdata["data"]["type"] == "learning_objective"
    assert context.sub_concept_uuid in opdata["data"]["parent_nodes"]["sub_concepts"]

#----------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create and align a learning objective")
def step_impl_1(context):
    
    """ Defining learning objective item for creation"""
    sub_concept_dict = TEST_SUBCONCEPT
    sub_concept = SubConcept.from_dict(sub_concept_dict)
    sub_concept.uuid = ""
    sub_concept.save()
    sub_concept.uuid = sub_concept.id
    sub_concept.update()
    context.sub_concept_uuid = sub_concept.uuid

    learning_objective_dict = copy(TEST_LEARNING_OBJECTIVE)
    learning_objective_dict["text"] = learning_objective_dict["text"].split("<p>")
    context.learning_objective_dict = learning_objective_dict

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/sub-concept/{sub_concept.uuid}/learning-objective"

@behave.when("The learning objective node is created within the management interface with correct request payload and to be aligned")
def step_impl_2(context):
    """Creating the required learning objective as per the input """
    updated_data = context.learning_objective_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()
    

@behave.then("That learning objective node will be created within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the learning objective"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the learning objective"
    assert opdata["data"]["title"] == "State theorems"
    assert opdata["data"]["description"] == "A description for State theorems"
    assert opdata["data"]["is_valid"] is True
    assert opdata["data"]["type"] == "learning_objective"
    assert context.sub_concept_uuid in opdata["data"]["parent_nodes"]["sub_concepts"]

@behave.then("That learning objective nodes is aligned correctly")
def step_impl_4(context):
    alignment_url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"
    lo_id = context.res_data["data"]["uuid"]
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
    for i in range(40):
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

#-------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning objective with incorrect payload")
def step_impl_1(context):
    """ Defining learning objective item for creation"""
    sub_concept_dict = TEST_SUBCONCEPT
    sub_concept = SubConcept.from_dict(sub_concept_dict)
    sub_concept.uuid = ""
    sub_concept.save()
    sub_concept.uuid = sub_concept.id
    sub_concept.update()
    context.sub_concept_uuid = sub_concept.uuid

    context.subconcept_dict = TEST_SUBCONCEPT
    subconcept = SubConcept.from_dict(context.subconcept_dict)
    subconcept.uuid = ""
    subconcept.save()
    subconcept.uuid = subconcept.id
    subconcept.update()


    context.payload= {
        "leraning": "State theorems",
        "objective": "A description for State theorems",
        "parent": [],
        "is_valid": True,
        "type": "learning_objective"
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/sub-concept/{sub_concept.uuid}/learning-objective"

@behave.when("The learning objective node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Creating the required learning objective as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for learning objective")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#---------------------------------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning resource")
def step_impl_1(context):
    """ Defining learning resource item for creation"""

    context.learning_resource_dict = LEARNING_CONTENT_OBJ_TEMPLATE
    learning_resource = KnowledgeServiceLearningContent.from_dict(context.learning_resource_dict)
    learning_resource.uuid = ""
    learning_resource.save()
    learning_resource.uuid = learning_resource.id
    learning_resource.update()
    context.learning_resource_dict["uuid"] = learning_resource.id

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"

@behave.when("The learning resource node will appear within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required learning resource as per the input """
    updated_data = context.learning_resource_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That learning resource node will appear within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the learning resource"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the learning resource"
    assert opdata["data"]["title"] == "title"
    assert opdata["data"]["type"] == "learning_resource"

#-------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning resource with incorrect payload")
def step_impl_1(context):
    """ Defining learning resource item for creation"""

    context.payload= {
        "book": "Text Books",
        "describe": "",
        "document_type": "",
        "ids": [],
        "resource_path": "",
        "type": "learning_resource"
}
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-resource"

@behave.when("The learning resource node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Creating the required learning resource as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for learning resource")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#---------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning unit")
def step_impl_1(context):
    """ Defining learning unit item for creation"""
    learning_objective_dict = TEST_LEARNING_OBJECTIVE
    learning_objective = KnowledgeServiceLearningObjective.from_dict(learning_objective_dict)
    learning_objective.uuid = ""
    learning_objective.save()
    learning_objective.uuid = learning_objective.id
    learning_objective.update()
    context.learning_objective_uuid = learning_objective.uuid

    learning_unit_dict = copy(TEST_LEARNING_UNIT)
    learning_unit_dict["text"] = learning_unit_dict["text"].split("<p>")
    context.learning_unit_dict = learning_unit_dict

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{learning_objective.uuid}/learning-unit"

@behave.when("The learning unit node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required learning unit as per the input """
    updated_data = context.learning_unit_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That learning unit node will appear within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the learning unit"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the learning unit"
    assert opdata["data"]["title"] == "Elementary Data Types"
    assert opdata["data"]["text"] == "A data type is a class of data objects with a set of operations for creating and manipulating them."
    assert opdata["data"]["type"] == "learning_unit"
    assert context.learning_objective_uuid in opdata["data"]["parent_nodes"]["learning_objectives"]

#-------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create and align learning unit")
def step_impl_1(context):
    """ Defining learning unit item for creation"""
    learning_objective_dict = TEST_LEARNING_OBJECTIVE
    learning_objective = KnowledgeServiceLearningObjective.from_dict(learning_objective_dict)
    learning_objective.uuid = ""
    learning_objective.save()
    learning_objective.uuid = learning_objective.id
    learning_objective.update()
    context.learning_objective_uuid = learning_objective.uuid

    learning_unit_dict = copy(TEST_LEARNING_UNIT)
    learning_unit_dict["text"] = learning_unit_dict["text"].split("<p>")
    context.learning_unit_dict = learning_unit_dict

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{learning_objective.uuid}/learning-unit"

@behave.when("The learning unit node is created within the management interface with correct request payload and to be aligned")
def step_impl_2(context):
    """Creating the required learning unit as per the input """
    updated_data = context.learning_unit_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That learning unit node will ve created within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the learning unit"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the learning unit"
    assert opdata["data"]["title"] == "Elementary Data Types"
    assert opdata["data"]["text"] == "A data type is a class of data objects with a set of operations for creating and manipulating them."
    assert opdata["data"]["type"] == "learning_unit"
    assert context.learning_objective_uuid in opdata["data"]["parent_nodes"]["learning_objectives"]

@behave.then("the learning unit node to be mapped accordingly")
def step_impl_4(context):
    alignment_url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"
    lu_id = context.res_data["data"]["uuid"]
    req_body = {
        "ids": [lu_id],
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
    for i in range(40):
        res = get_method(url=url)
        data = res.json()
        if data["data"]["status"] in ["succeeded", "failed"]:
            break
        time.sleep(10)
    assert data["data"]["status"] == "succeeded"
    #check alignment
    concept_url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-unit/{lu_id}"
    resp = get_method(url = concept_url)
    resp_data = resp.json()
    assert resp.status_code == 200
    assert resp_data["success"] == True
    assert len(resp_data["data"]["alignments"]["skill_alignment"]["e2e_osn"]["suggested"]) >0
#-------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a learning unit with incorrect payload")
def step_impl_1(context):
    """ Defining learning unit item for creation"""
    learning_objective_dict = TEST_LEARNING_OBJECTIVE
    learning_objective = KnowledgeServiceLearningObjective.from_dict(learning_objective_dict)
    learning_objective.uuid = ""
    learning_objective.save()
    learning_objective.uuid = learning_objective.id
    learning_objective.update()
    context.learning_objective_uuid = learning_objective.uuid

    learning_objective_dict = copy(TEST_LEARNING_OBJECTIVE)
    learning_objective = KnowledgeServiceLearningObjective.from_dict(learning_objective_dict)
    learning_objective.uuid = ""
    learning_objective.save()
    learning_objective.uuid = learning_objective.id
    learning_objective.update()
    context.learning_objective_uuid = learning_objective.id

    context.payload= {
        "copy": "Text Books",
        "description": "",
        "doctype": "",
        "ids": [],
        "gcs_path": "",
        "type": "learning_unit"
}
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/learning-objective/{learning_objective.uuid}/learning-unit"

@behave.when("The learning unit node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Creating the required learning unit as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for learning unit")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"

#---------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a SubConcept")
def step_impl_1(context):
    """ Defining SubConcept item for creation"""
    concept_dict = TEST_CONCEPT
    concept = Concept.from_dict(concept_dict)
    concept.uuid = ""
    concept.save()
    concept.uuid = concept.id
    concept.update()
    context.concept_uuid = concept.uuid

    context.subconcept_dict = TEST_SUBCONCEPT

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{concept.uuid}/subconcept"

@behave.when("The SubConcept node is created within the management interface with correct request payload")
def step_impl_2(context):
    """Creating the required SubConcept as per the input """
    updated_data = context.subconcept_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That SubConcept node will appear within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the subconcept"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the subconcept"
    assert opdata["data"]["title"] == "Essentialism"
    assert opdata["data"]["description"] == "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods"
    assert opdata["data"]["type"] == "subconcept"
    assert context.concept_uuid in opdata["data"]["parent_nodes"]["concepts"]

#-------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create and align a SubConcept")
def step_impl_1(context):
    """ Defining SubConcept item for creation"""
    concept_dict = TEST_CONCEPT
    concept = Concept.from_dict(concept_dict)
    concept.uuid = ""
    concept.save()
    concept.uuid = concept.id
    concept.update()
    context.concept_uuid = concept.uuid

    context.subconcept_dict = TEST_SUBCONCEPT

    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{concept.uuid}/subconcept"

@behave.when("The SubConcept node is created within the management interface with correct request payload and to be aligned")
def step_impl_2(context):
    """Creating the required SubConcept as per the input """
    updated_data = context.subconcept_dict
    context.res = post_method(url=context.url, request_body=updated_data)
    context.res_data = context.res.json()

@behave.then("That SubConcept node will be created within the Knowledge Graph")
def step_impl_3(context):
    assert context.res.status_code == 200
    assert context.res_data["message"] == "Successfully created the subconcept"
    id = context.res_data["data"]["uuid"]
    url = f"{API_URL_KNOWLEDGE_SERVICE}/subconcept/{id}"
    request = get_method(url)
    opdata = request.json()
    assert request.status_code == 200
    assert opdata["message"] ==  "Successfully fetched the subconcept"
    assert opdata["data"]["title"] == "Essentialism"
    assert opdata["data"]["description"] == "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods"
    assert opdata["data"]["type"] == "subconcept"
    assert context.concept_uuid in opdata["data"]["parent_nodes"]["concepts"]

@behave.then("the subconcept node will be mapped accordingly")
def step_impl_4(context):
    alignment_url = f"{API_URL_KNOWLEDGE_SERVICE}/knowledge/skill-alignment/batch"
    subconcept_id = context.res_data["data"]["uuid"]
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
    for i in range(40):
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

#-------------------------------------------------------------------------------------------------------------------------------
@behave.given("A developer or admin has access to knowledge Service via Competencies & Skill Management and needs to create a SubConcept with incorrect payload")
def step_impl_1(context):
    """ Defining SubConcept item for creation"""
    concept_dict = TEST_CONCEPT
    concept = Concept.from_dict(concept_dict)
    concept.uuid = ""
    concept.save()
    concept.uuid = concept.id
    concept.update()
    context.concept_uuid = concept.uuid

    context.payload= {
        "subconcept": "Essentialism",
        "describe": "An educational theory that ideas and skills basic to a culture should be taught to all alike by time-tested methods",
        "learning_res": "",
        "parent_nodes":  {"concepts": []},
        "child_nodes": {"learning_objectives": []},
        "label": "",
        "total_lus": 0,
        "is_valid": True,
        "type": "subconcept",
}
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/concept/{concept.uuid}/subconcept"

@behave.when("The SubConcept node is created within the management interface with incorrect request payload")
def step_impl_2(context):
    """Creating the required SubConcept as per the input """
    context.res = post_method(url=context.url, request_body=context.payload)
    context.res_data = context.res.json()

@behave.then("The user will get an error message for SubConcept")
def step_impl_3(context):
    assert context.res.status_code == 422
    assert context.res_data["data"][0]["msg"] == "field required"
    assert context.res_data["data"][0]["type"] == "value_error.missing"
