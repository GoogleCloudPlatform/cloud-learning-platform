@skill-service
Feature: Search skills or concepts in skill graph or knowledge graph respectively

    Scenario: Search skills in skill graph with correct params 
        Given User has the ability to perform syntactic search in skill service via Skill Management with correct params
            When Skill is searched using syntactic search pipeline within the management interface with correct params
                Then Skill Service will perform syntactic search to retrieve and serve the data back to the management interface
    
    Scenario: Search skills in skill graph with incorrect params 
        Given User has the ability to perform syntactic search in skills service via Skill Management but with wrong params
            When Skill is searched using syntactic search pipeline within the management interface with incorrect params
                Then Skill Service will throw error message to the user
    
    Scenario: Search nodes in skill graph with correct node level paased in params
        Given User has the ability to perform syntactic search in skills service via Skill Management and the correct node levels passed in the params
            When Node is searched within the management interface with correct params with the correct node levels passed in the params
                Then Skill Service will perform syntactic search to retrieve data as per relevent node levels passed and serve that data back to the management interface

    Scenario: Search nodes in skill graph without passing node levels in params
        Given User has the ability to perform syntactic search in skills service via Skill Management and the node levels are not passed in the params
            When Node is searched using syntactic search pipeline within the management interface with correct params with the no node levels passed in the params
                Then Skill Service will not retreive any data as node level was not specified in request payload for syntactic search

    Scenario: Search nodes in skill graph by passing an invalid node level
        Given User is priviledged to perform syntactic search nodes in skill graph via Skill Management 
            When skill node is searched using syntactic search pipeline within the management interface by passing incorrect node level
                Then Skill Service will throw an internal error as incorrect skill node level was given in request payload for syntactic search

    Scenario: Search concepts in knowledge graph with correct params
        Given User has the ability to perform syntactic search for concepts in the knowledge graph with correct params
            When Concept is searched using syntactic search pipeline within the management interface with correct params
                Then Knowledge service will perform syntactic search to retreive the relevant data and serve that data back to the interface

    Scenario: Search concepts in knowledge graph with inccorrect params
        Given User has the ability to perform syntactic search for concepts in the knowledge graph with incorrect params
            When Concept is searched using syntactic search pipeline within the management interface with incorrect params
                Then Knowledge service will throw an internal error message to the user as incorrect argument was given to syntactic search pipeline

    Scenario: Search nodes in knowledge graph by passing the correct node level
        Given User has the ability to perform syntactic search for nodes in knowledge graph via Competency Management 
            When Node is searched within the management interface by passing correct node levels in request payload
                Then Knowledge Service will perform syntactic search retrieve the documents relevant to search data from the provided node level collection

    Scenario: Search nodes in knowledge graph without passing the node level
        Given User has access to perform syntactic search for nodes in knowledge graph via Competency Management 
            When Node is searched within the management interface without passing node level to syntactic search pipeline
                Then Knowledge Service will not retreive any data as node level was not specified to syntactic search pipeline

    Scenario: Search nodes in knowledge graph by passing an invalid node level
        Given User is priviledged to perform syntactic search for nodes in knowledge graph via Competency Management 
            When Node is searched within the management interface by passing incorrect node level to syntactic search pipeline
                Then Knowledge Service will throw an internal error as incorrect knowledge node level was given to syntactic search pipeline

    @matching-engine
    Scenario: Search skills in skill graph with correct params 
        Given User has the ability to perform semantic search in skill service via Skill Management with correct params
            When Skill is searched within the management interface with correct params
                Then Skill Service will perform semantic search to retrieve and serve the data back to the management interface
    
    Scenario: Search skills in skill graph with incorrect params 
        Given User has the ability to perform semantic search in skills service via Skill Management but with wrong params
            When Skill is searched within the management interface with incorrect params
                Then Skill Service will throw error message to the user as incorrect params given
    
    Scenario: Search nodes in skill graph without passing node levels in params
        Given User has the ability to perform semantic search in skills service via Skill Management and the node levels are not passed in the params
            When Node is searched using semantic search pipeline within the management interface with correct params with the no node levels passed in the params
                Then Skill Service will not retreive any data as node level was not specified in request payload for semantic search

    Scenario: Search nodes in skill graph by passing an invalid node level
        Given User is priviledged to perform semantic search nodes in skill graph via Skill Management 
            When skill node is searched using semantic search pipeline within the management interface by passing incorrect node level
                Then Skill Service will throw an internal error as incorrect skill node level was given in request payload for semantic search

    @matching-engine
    Scenario: Search concepts in knowledge graph with correct params
        Given User has the ability to perform semantic search for concepts in the knowledge graph with correct params
            When Concept is searched using semantic search pipeline within the management interface with correct params
                Then Knowledge service will perform semantic search to retreive the relevant data and serve that data back to the interface

    Scenario: Search concepts in knowledge graph with inccorrect params
        Given User has the ability to perform semantic search for concepts in the knowledge graph with incorrect params
            When Concept is searched using semantic search pipeline within the management interface with incorrect params
                Then Knowledge service will throw an internal error message to the user as incorrect argument was given to semantic search pipeline

    Scenario: Search nodes in knowledge graph without passing the node level
        Given User has access to perform semantic search for nodes in knowledge graph via Competency Management 
            When Node is searched within the management interface without passing node level to semantic search pipeline
                Then Knowledge Service will not retreive any data as node level was not specified to semantic search pipeline

    Scenario: Search nodes in knowledge graph by passing an invalid node level
        Given User is priviledged to perform semantic search for nodes in knowledge graph via Competency Management 
            When Node is searched within the management interface by passing incorrect node level to semantic search pipeline
                Then Knowledge Service will throw an internal error as incorrect knowledge node level was given to semantic search pipeline

    Scenario: Search nodes in knowledge graph by passing an invalid node level
        Given User has access priviledges to perform semantic search for nodes in knowledge graph via Competency Management
            When Node is searched within the Competency management interface by passing empty query to semantic search pipeline
                Then Knowledge Service will throw a validation error as empty query was given to semantic search pipeline

    Scenario: Search nodes in knowledge graph by passing an invalid node level
        Given User has access priviledges to perform semantic search for nodes in knowledge graph via SKill Management
            When Node is searched within the Skill management interface by passing empty query to semantic search pipeline
                Then Skill Service will throw a validation error as empty query was given to semantic search pipeline