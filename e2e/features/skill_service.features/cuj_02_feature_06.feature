@skill-service
Feature: Filter data in skill and knowledge graph

    @filter-api
    Scenario: Filter skills in skill graph
        Given That a user has the ability to filter skill data in skill graph
            When A filter for skill is applied within the management interface with permitted filters
                Then Skill Service will retrieve the relevant filtered data for skill and serve that data back to the management interface

    Scenario: Filter skills in skill graph for negative scenario
        Given That a user has the ability to filter skill data in skill graph for negative scenario
            When A filter for skill is applied within the management interface with invalid filters for negative scenario
                Then Skill Service will raise error for invalid skills filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter competencies in skill graph
        Given That a user has the ability to filter competency data in skill graph
            When A filter for competency is applied within the management interface with permitted filters
                Then Skill Service will retrieve the relevant filtered data for competency and serve that data back to the management interface

    Scenario: Filter competencies in skill graph for negative scenario
        Given That a user has the ability to filter competency data in skill graph for negative scenario
            When A filter for competency is applied within the management interface with invalid filters for negative scenario
                Then Skill Service will raise error for invalid competencies filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter category in skill graph
        Given That a user has the ability to filter category data in skill graph
            When A filter for category is applied within the management interface with permitted filters
                Then Skill Service will retrieve the relevant filtered data for category and serve that data back to the management interface

    Scenario: Filter category in skill graph for negative scenario
        Given That a user has the ability to filter category data in skill graph for negative scenario
            When A filter for category is applied within the management interface with invalid filters for negative scenario
                Then Skill Service will raise error for invalid category filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter sub domain in skill graph
        Given That a user has the ability to filter sub domain data in skill graph
            When A filter for sub domain is applied within the management interface with permitted filters
                Then Skill Service will retrieve the relevant filtered data for sub domain and serve that data back to the management interface

    Scenario: Filter sub domain in skill graph for negative scenario
        Given That a user has the ability to filter sub domain data in skill graph for negative scenario
            When A filter for sub domain is applied within the management interface with invalid filters for negative scenario
                Then Skill Service will raise error for invalid sub domain filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter domain in skill graph
        Given That a user has the ability to filter domain data in skill graph
            When A filter for domain is applied within the management interface with permitted filters
                Then Skill Service will retrieve the relevant filtered data for domain and serve that data back to the management interface

    Scenario: Filter domain in skill graph for negative scenario
        Given That a user has the ability to filter domain data in skill graph for negative scenario
            When A filter for domain is applied within the management interface with invalid filters for negative scenario
                Then Skill Service will raise error for invalid domain filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter concepts in knowledge graph
        Given Given that a user has the ability to filter concept data in knowledge graph
            When A filter for concept is applied within the management interface with permitted filters
                Then Knowledge Service will retrieve the relevant filtered data for concept and serve that data back to the management interface

    Scenario: Filter concepts in knowledge graph for negative scenario
        Given Given that a user has the ability to filter concept data in knowledge graph for negative scenario
            When A filter for concept is applied within the management interface with invalid filters for negative scenario
                Then Knowledge Service will raise error for invalid concepts filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter subconcepts in knowledge graph
        Given Given that a user has the ability to filter subconcept data in knowledge graph
            When A filter for subconcept is applied within the management interface with permitted filters
                Then Knowledge Service will retrieve the relevant filtered data for subconcept and serve that data back to the management interface

    Scenario: Filter subconcepts in knowledge graph for negative scenario
        Given Given that a user has the ability to filter subconcept data in knowledge graph for negative scenario
            When A filter for subconcept is applied within the management interface with invalid filters for negative scenario
                Then Knowledge Service will raise error for invalid subconcepts filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter learning objective in knowledge graph
        Given Given that a user has the ability to filter learning objective data in knowledge graph
            When A filter for learning objective is applied within the management interface with permitted filters
                Then Knowledge Service will retrieve the relevant filtered data for learning objective and serve that data back to the management interface

    Scenario: Filter learning objective in knowledge graph for negative scenario
        Given Given that a user has the ability to filter learning objective data in knowledge graph for negative scenario
            When A filter for learning objective is applied within the management interface with invalid filters for negative scenario
                Then Knowledge Service will raise error for invalid learning objective filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter learning unit in knowledge graph
        Given Given that a user has the ability to filter learning unit data in knowledge graph
            When A filter for learning unit is applied within the management interface with permitted filters
                Then Knowledge Service will retrieve the relevant filtered data for learning unit and serve that data back to the management interface

    Scenario: Filter learning unit in knowledge graph for negative scenario
        Given Given that a user has the ability to filter learning unit data in knowledge graph for negative scenario
            When A filter for learning unit is applied within the management interface with invalid filters for negative scenario
                Then Knowledge Service will raise error for invalid learning unit filter and send back to the management interface as negative scenario

    @filter-api
    Scenario: Filter learning resource in knowledge graph
        Given Given that a user has the ability to filter learning resource data in knowledge graph
            When A filter for learning resource is applied within the management interface with permitted filters
                Then Knowledge Service will retrieve the relevant filtered data for learning resource and serve that data back to the management interface

    Scenario: Filter learning resource in knowledge graph for negative scenario
        Given Given that a user has the ability to filter learning resource data in knowledge graph for negative scenario
            When A filter for learning resource is applied within the management interface with invalid filters for negative scenario
                Then Knowledge Service will raise error for invalid learning resource filter and send back to the management interface as negative scenario
