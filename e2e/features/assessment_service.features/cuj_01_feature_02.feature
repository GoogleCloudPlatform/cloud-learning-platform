Feature: Establishing a relationship between the Assessment and Learning Experience

    Scenario: LXE wants to associate the Assessment with the Learning Experience
        Given that a LXE has access Learning Object Service and Assessment Service to establish relationship with LE
            When API request is sent to create Assessment and Learning Experience with correct request payload
                Then Assessment and Learning Experience will be created in the database
                    And Assessment gets associated with Learning Experience

    Scenario: LXE adds the incorrect reference of the given Learning Experience in the Assessment
        Given that an LXE create a Assessment providing the reference of the given Learning Experience with incorrect uuid
            When API request is sent to create Assessment and LE with incorrect reference
                Then LXE will get an error message for the Learning Experience not found

    
    Scenario: LXE wants to update the reference of the Assessment with the new Learning Experience
        Given that an LXE  wants to replace an old reference of the Learning Experience with a new reference in the Assessment
            When API request is sent to update the Assessment with new reference of Learning Experience
                Then the Assessment gets associated with the new Learning Experience
   
    Scenario: LXE updating the incorrect reference of Learning Experience in the Assessment
        Given that an LXE wants to add a reference to one more Learning Experience in the Assessment
            When API request is sent to update the Assessment with incorrect reference of Learning Experience
                Then the user gets error message of not found for the reference to the Learning Experience

    
    Scenario: LXE wants to update the reference from the previous Assessment with the current Assessment in the given Learning Experience
        Given that an LXE or CD wants to update the reference of the Assessment in the Learning Experience
            When they add the new reference and delete the old reference of the Assessment using an API request to Assessment Service
                Then the old Assessment will get untagged and the new Assessment will get tagged to the Learning Experience