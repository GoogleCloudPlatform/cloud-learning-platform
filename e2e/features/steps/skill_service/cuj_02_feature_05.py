"""
Search skills or concepts in skill graph or knowledge graph respectively
"""

import time
import behave
import json
import sys
sys.path.append("../")
from setup import post_method, get_method, put_method, delete_method
from test_config import API_URL_SKILL_SERVICE, API_URL_KNOWLEDGE_SERVICE

# ----------------------------- Scenario 01 ---------------------------------
@behave.given("User has the ability to perform syntactic search in skill service via Skill Management with correct params")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "name": "Implement Organizational Skills",
        "keyword": "Implement Organizational Skills",
        
        }
    context.url = f"{API_URL_SKILL_SERVICE}/syntactic-search"


@behave.when("Skill is searched using syntactic search pipeline within the management interface with correct params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Skill Service will perform syntactic search to retrieve and serve the data back to the management interface")
def step_impl_3(context):
    assert context.post_res.status_code == 200
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully fetched the skills"
    assert len(context.post_res_data["data"]["skill"]) == 1
    assert context.post_res_data["data"]["skill"][0]["name"] == "Implement Organizational Skills"
    assert context.post_res_data["data"]["skill"][0]["description"] =="Implement organizational skills to achieve a goal."

# ----------------------------- Scenario 02 ---------------------------------
@behave.given("User has the ability to perform syntactic search in skills service via Skill Management but with wrong params")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "test1": "Implement random Skills",
        "test2": "Implement random Skills",
        }
    context.url = f"{API_URL_SKILL_SERVICE}/syntactic-search"


@behave.when("Skill is searched using syntactic search pipeline within the management interface with incorrect params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Skill Service will throw error message to the user")
def step_impl_3(context):
    time.sleep(20)
    assert context.post_res.status_code == 422
    assert context.post_res_data.get("success") is False
    assert context.post_res_data.get("message") == "Both Name and Keyword cannot be empty."
    assert context.post_res_data.get("data") is None

# ----------------------------- Scenario 03 ---------------------------------
@behave.given("User has the ability to perform syntactic search in skills service via Skill Management and the correct node levels passed in the params")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "name": "Implement Organizational Skills",
        "keyword": "Implement Organizational Skills",
        "levels": ["skill"]
        
        }
    context.url = f"{API_URL_SKILL_SERVICE}/syntactic-search"

@behave.when("Node is searched within the management interface with correct params with the correct node levels passed in the params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Skill Service will perform syntactic search to retrieve data as per relevent node levels passed and serve that data back to the management interface")
def step_impl_3(context):
    assert context.post_res.status_code == 200
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully fetched the skills"
    assert len(context.post_res_data["data"]["skill"]) == 1
    assert context.post_res_data["data"]["skill"][0]["name"] == "Implement Organizational Skills"
    assert context.post_res_data["data"]["skill"][0]["description"] =="Implement organizational skills to achieve a goal."

# ----------------------------- Scenario 04 ---------------------------------
@behave.given("User has the ability to perform syntactic search in skills service via Skill Management and the node levels are not passed in the params")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "name": "Implement Organizational Skills",
        "keyword": "Implement Organizational Skills",
        "levels" : []
        }
    context.url = f"{API_URL_SKILL_SERVICE}/syntactic-search"

@behave.when("Node is searched using syntactic search pipeline within the management interface with correct params with the no node levels passed in the params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Skill Service will not retreive any data as node level was not specified in request payload for syntactic search")
def step_impl_3(context):
    assert context.post_res.status_code == 200
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully fetched the skills"
    assert context.post_res_data["data"] == {}


# ----------------------------- Scenario 05 ---------------------------------
@behave.given("User is priviledged to perform syntactic search nodes in skill graph via Skill Management")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "name": "Implement Organizational Skills",
        "keyword": "Implement Organizational Skills",
        "levels" : ["random_level"]
        }
    context.url = f"{API_URL_SKILL_SERVICE}/syntactic-search"

@behave.when("skill node is searched using syntactic search pipeline within the management interface by passing incorrect node level")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)

@behave.then("Skill Service will throw an internal error as incorrect skill node level was given in request payload for syntactic search")
def step_impl_3(context):
    assert context.post_res.status_code == 422


# ----------------------------- Scenario 06 ---------------------------------
@behave.given("User has the ability to perform syntactic search for concepts in the knowledge graph with correct params")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "Data Structure and Algorithms",
        "levels": ["concepts", "sub_concepts", "learning_units", "learning_objectives"],
        
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/syntactic-search"

@behave.when("Concept is searched using syntactic search pipeline within the management interface with correct params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Knowledge service will perform syntactic search to retreive the relevant data and serve that data back to the interface")
def step_impl_3(context):
    assert context.post_res.status_code == 200
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully fetched the Knowledge Nodes"
    assert context.post_res_data["data"]["query"] == "Data Structure and Algorithms"

# ----------------------------- Scenario 07 ---------------------------------

@behave.given("User has the ability to perform syntactic search for concepts in the knowledge graph with incorrect params")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "name": "Data Structure and Algorithms",
        "levels": ["concepts"]
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/syntactic-search"

@behave.when("Concept is searched using syntactic search pipeline within the management interface with incorrect params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Knowledge service will throw an internal error message to the user as incorrect argument was given to syntactic search pipeline")
def step_impl_3(context):
    assert context.post_res.status_code == 422
    assert context.post_res_data["data"][0]["msg"] == "field required"
    assert context.post_res_data["data"][0]["type"] == "value_error.missing"


# ----------------------------- Scenario 08 ---------------------------------

@behave.given("User has the ability to perform syntactic search for nodes in knowledge graph via Competency Management")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "Data Structure and Algorithms",
        "levels": ["concepts"]
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/syntactic-search"

@behave.when("Node is searched within the management interface by passing correct node levels in request payload")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Knowledge Service will perform syntactic search retrieve the documents relevant to search data from the provided node level collection")
def step_impl_3(context):
    assert context.post_res.status_code == 200, "Status code not 200"
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully fetched the Knowledge Nodes"
    assert context.post_res_data.get("data").get("query") == context.params.get("query")
    assert context.post_res_data.get("data").get(context.params["levels"][0])


# ----------------------------- Scenario 09 ---------------------------------

@behave.given("User has access to perform syntactic search for nodes in knowledge graph via Competency Management")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "Data Structure and Algorithms",
        "levels": []
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/syntactic-search"

@behave.when("Node is searched within the management interface without passing node level to syntactic search pipeline")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Knowledge Service will not retreive any data as node level was not specified to syntactic search pipeline")
def step_impl_3(context):
    assert context.post_res.status_code == 200, "Status code not 200"
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully fetched the Knowledge Nodes"
    assert context.post_res_data.get("data").get("query") == context.params.get("query")
    assert context.post_res_data.get("data").get("learning_resources") == []
    assert context.post_res_data.get("data").get("concepts") == []
    assert context.post_res_data.get("data").get("sub_concepts") == []
    assert context.post_res_data.get("data").get("learning_objectives") == []
    assert context.post_res_data.get("data").get("learning_units") == []


# ----------------------------- Scenario 10 ---------------------------------
@behave.given("User is priviledged to perform syntactic search for nodes in knowledge graph via Competency Management")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "Data Structure and Algorithms",
        "levels": ["random_level"]
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/syntactic-search"

@behave.when("Node is searched within the management interface by passing incorrect node level to syntactic search pipeline")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)

@behave.then("Knowledge Service will throw an internal error as incorrect knowledge node level was given to syntactic search pipeline")
def step_impl_3(context):
    assert context.post_res.status_code == 422




# ----------------------------- Scenario 11 ---------------------------------
@behave.given("User has the ability to perform semantic search in skill service via Skill Management with correct params")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "query": "Guideline Development",
        "levels": ["skill"],
        "top_k": 1
        }
    context.url = f"{API_URL_SKILL_SERVICE}/semantic-search"


@behave.when("Skill is searched within the management interface with correct params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Skill Service will perform semantic search to retrieve and serve the data back to the management interface")
def step_impl_3(context):
    assert context.post_res.status_code == 200
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully searched results for given query"
    assert context.post_res_data.get("data").get("query") == context.params.get("query")
    assert context.post_res_data.get("data").get(context.params["levels"][0])


# ----------------------------- Scenario 12 ---------------------------------
@behave.given("User has the ability to perform semantic search in skills service via Skill Management but with wrong params")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "test1": "Implement random Skills",
        "test2": "Implement random Skills",
        "top_k": 1
        }
    context.url = f"{API_URL_SKILL_SERVICE}/semantic-search"

@behave.when("Skill is searched within the management interface with incorrect params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)

@behave.then("Skill Service will throw error message to the user as incorrect params given")
def step_impl_3(context):
    time.sleep(20)
    assert context.post_res.status_code == 422


# ----------------------------- Scenario 13 ---------------------------------
@behave.given("User has the ability to perform semantic search in skills service via Skill Management and the node levels are not passed in the params")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "query": "Implement Organizational Skills",
        "levels" : [],
        "top_k": 1
        }
    context.url = f"{API_URL_SKILL_SERVICE}/semantic-search"

@behave.when("Node is searched using semantic search pipeline within the management interface with correct params with the no node levels passed in the params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Skill Service will not retreive any data as node level was not specified in request payload for semantic search")
def step_impl_3(context):
    assert context.post_res.status_code == 200
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully searched results for given query"
    assert context.post_res_data.get("data").get("query") == context.params.get("query")
    assert context.post_res_data.get("data").get("domain") == []
    assert context.post_res_data.get("data").get("sub_domain") == []
    assert context.post_res_data.get("data").get("category") == []
    assert context.post_res_data.get("data").get("competency") == []
    assert context.post_res_data.get("data").get("skill") == []

# ----------------------------- Scenario 14 ---------------------------------
@behave.given("User is priviledged to perform semantic search nodes in skill graph via Skill Management")
def step_impl_1(context):
    """Defining the user skill search data"""

    context.params ={
        "query": "Implement Organizational Skills",
        "levels" : ["random_level"],
        "top_k": 1
        }
    context.url = f"{API_URL_SKILL_SERVICE}/semantic-search"

@behave.when("skill node is searched using semantic search pipeline within the management interface by passing incorrect node level")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)

@behave.then("Skill Service will throw an internal error as incorrect skill node level was given in request payload for semantic search")
def step_impl_3(context):
    assert context.post_res.status_code == 422



# ----------------------------- Scenario 15 ---------------------------------
@behave.given("User has the ability to perform semantic search for concepts in the knowledge graph with correct params")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "Data Structure and Algorithms",
        "levels": ["concepts"],
        "top_k": 1
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/semantic-search"

@behave.when("Concept is searched using semantic search pipeline within the management interface with correct params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Knowledge service will perform semantic search to retreive the relevant data and serve that data back to the interface")
def step_impl_3(context):
    assert context.post_res.status_code == 200
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully searched results for given query"
    assert context.post_res_data["data"]["query"] == context.params["query"]
    assert context.post_res_data.get("data").get(context.params["levels"][0])

# ----------------------------- Scenario 16 ---------------------------------

@behave.given("User has the ability to perform semantic search for concepts in the knowledge graph with incorrect params")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "name": "Data Structure and Algorithms",
        "levels": ["concepts"],
        "top_k": 1
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/semantic-search"

@behave.when("Concept is searched using semantic search pipeline within the management interface with incorrect params")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Knowledge service will throw an internal error message to the user as incorrect argument was given to semantic search pipeline")
def step_impl_3(context):
    assert context.post_res.status_code == 422
    assert context.post_res_data["data"][0]["msg"] == "field required"
    assert context.post_res_data["data"][0]["type"] == "value_error.missing"


# ----------------------------- Scenario 17 ---------------------------------

@behave.given("User has access to perform semantic search for nodes in knowledge graph via Competency Management")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "Data Structure and Algorithms",
        "levels": [],
        "top_k": 1
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/semantic-search"

@behave.when("Node is searched within the management interface without passing node level to semantic search pipeline")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Knowledge Service will not retreive any data as node level was not specified to semantic search pipeline")
def step_impl_3(context):
    assert context.post_res.status_code == 200, "Status code not 200"
    assert context.post_res_data.get("success") is True
    assert context.post_res_data.get("message") == "Successfully searched results for given query"
    assert context.post_res_data.get("data").get("query") == context.params.get("query")
    assert context.post_res_data.get("data").get("learning_resources") == []
    assert context.post_res_data.get("data").get("concepts") == []
    assert context.post_res_data.get("data").get("sub_concepts") == []
    assert context.post_res_data.get("data").get("learning_objectives") == []
    assert context.post_res_data.get("data").get("learning_units") == []


# ----------------------------- Scenario 18 ---------------------------------
@behave.given("User is priviledged to perform semantic search for nodes in knowledge graph via Competency Management")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "Data Structure and Algorithms",
        "levels": ["random_level"],
        "top_k": 1
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/semantic-search"

@behave.when("Node is searched within the management interface by passing incorrect node level to semantic search pipeline")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)

@behave.then("Knowledge Service will throw an internal error as incorrect knowledge node level was given to semantic search pipeline")
def step_impl_3(context):
    assert context.post_res.status_code == 422


# ----------------------------- Scenario 19 ---------------------------------
@behave.given("User has access priviledges to perform semantic search for nodes in knowledge graph via Competency Management")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "",
        "levels": ["concepts"],
        "top_k": 1
        }
    context.url = f"{API_URL_KNOWLEDGE_SERVICE}/semantic-search"

@behave.when("Node is searched within the Competency management interface by passing empty query to semantic search pipeline")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Knowledge Service will throw a validation error as empty query was given to semantic search pipeline")
def step_impl_3(context):
    assert context.post_res.status_code == 422, "Status is not 422"
    assert context.post_res_data.get("success") is False, "Success is not False"
    assert context.post_res_data.get("message") == "Query should be present to search"


# ----------------------------- Scenario 20 ---------------------------------
@behave.given("User has access priviledges to perform semantic search for nodes in knowledge graph via SKill Management")
def step_impl_1(context):
    """Defining the user concept search data"""

    context.params ={
        "query": "",
        "levels": ["skill"],
        "top_k": 1
        }
    context.url = f"{API_URL_SKILL_SERVICE}/semantic-search"

@behave.when("Node is searched within the Skill management interface by passing empty query to semantic search pipeline")
def step_impl_2(context):
    context.post_res = post_method(url= context.url, request_body= context.params)
    context.post_res_data = context.post_res.json()

@behave.then("Skill Service will throw a validation error as empty query was given to semantic search pipeline")
def step_impl_3(context):
    assert context.post_res.status_code == 422, "Status is not 422"
    assert context.post_res_data.get("success") is False, "Success is not False"
    assert context.post_res_data.get("message") == "Query should be present to search"
