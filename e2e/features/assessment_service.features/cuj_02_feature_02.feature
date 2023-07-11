Feature: Establishing a relationship between the Assessment and Learning Object

    Scenario: LXE wants to associate the Assessment with the Learning Object
        Given that a LXE has access Learning Object Service and Assessment Service
            When API request is sent to create Assessment and Learning Object with correct request payload 
                Then Assessment and Learning Object will be created in the database 
                    And Assessment gets associated with Learning Object

    Scenario: LXE adds the incorrect reference of the given Learning Object in the Assessment
        Given that an LXE create a Assessment providing the reference of the given Learning Object with incorrect uuid
            When API request is sent to create Assessment
                Then the LXE will get an error message of not found the reference to the Learning Object

    
    Scenario: LXE wants to update the reference of the Assessment with the new Learning Object
        Given that an LXE  wants to replace an old reference of the Learning Object with a new reference in the Assessment
            When API request is sent to update the Assessment with new reference of Learning Object
                Then the Assessment gets associated with the new Learning Object
   
    Scenario: LXE updating the incorrect reference of Learning Object in the Assessment
        Given that an LXE wants to add a reference to one more Learning Object in the Assessment
            When API request is sent to update the Assessment with incorrect reference of Learning Object
                Then the user gets error message of not found the reference to the Learning Object

    
    Scenario: LXE wants to update the reference from the previous Assessment with the current Assessment in the given Learning Object
        Given that an LXE or CD wants to update the reference of the Assessment in the Learning Object
            When they add the new reference and delete the old reference of the Assessment using an API request
                Then the old Assessment will get untagged and the new Assessment will get tagged to the Learning Object

    Scenario: LXE wants to link an authored assessment to a placeholder assessment in the heirarchy
        Given there exists a learning heirarchy with a placeholder assessment and a new authored assessment has been created
            When the LXE wants to link the authored assessment to the placeholder and ingest it into the hierarchy
                Then the authored assessment gets ingested and linked into the hierarchy
                    And the pre-reqs for subsequent nodes in the hierarchy are also updated 
                        And the placeholder assessment is delinked from the hierarchy