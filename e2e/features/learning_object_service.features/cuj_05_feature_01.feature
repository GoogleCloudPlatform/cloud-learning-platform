Feature: Creation, Updation (with version control) and Deletion of Curriculum Pathways from content authoring tool by LXE or CD

    Scenario: Create Curriculum Pathway with correct request payload
        Given that a LXE or CD has access to the content authoring tool to create curriculum pathway
            When they design the curriculum pathway using a third party tool
                Then the curriculum pathways will be created in a third-party tool and stored inside LOS
                    And all metadata for curriculum pathway will be ingested and stored in learning object service
                        And uuid for curriculum pathways will be stored in learning object service

    Scenario: Create Curriculum Pathway with incorrect request payload
        Given that a LXE or CD has access to content authoring tool to create curriculum pathway with invalid request
            When they design the curriculum pathway using a third party tool with invalid request
                Then the curriculum pathways will not be created in learning object service

    Scenario: Update Curriculum Pathway with correct request payload
        Given that an LXE or CD has access to the content authoring tool to update the curriculum pathway with correct payload
            When they update the curriculum pathway using a third-party tool
                Then the curriculum pathways will be updated in a third-party tool
                    And all metadata will be updated in learning object service for the curriculum pathway
    
    Scenario: Update Curriculum Pathway with correct request payload and create version
        Given that an LXE or CD has access to the content authoring tool to create version of curriculum pathway
            When they update the curriculum pathway using a third-party tool to create version
                Then a version of curriculum pathway will be created
                    And all metadata for the curriculum pathway will be updated learning object service
                        And a version document for the curriculum pathway will be created in learing object service
    
    Scenario: Update Curriculum Pathway with invalid uuid in request payload
        Given that an LXE or CD has access to content authoring tool with invalid uuid for the curriculum pathway
            When they update the curriculum pathway using a third-party tool with invalid uuid
                Then the curriculum pathways will not be updated in learning object service
    
    Scenario: Update Curriculum Pathway with invalid request payload
        Given that a LXE has access to content authoring tool with invalid request payload for the curriculum pathway
            When they update the curriculum pathway using a third-party tool with invalid request
                Then the curriculum pathway will not be updated in learning object service
    
    Scenario: Delete Curriculum Pathway with correct request payload
        Given that an LXE has access to content authoring tool to delete curriculum pathway with correct payload
            When they delete the curriculum pathway using a third-party tool
                Then the curriculum pathways will be deleted from a third-party tool
                    And all metadata will be deleted from learning object service for the curriculum pathway
    
    Scenario: Delete Curriculum Pathway with incorrect uuid in request payload
        Given that an LXE has access to the content authoring tool to delete curriculum pathway with incorrect uuid
            When they delete the curriculum pathway using a third-party tool wiht incorrect uuid
                Then the curriculum pathways will not be deleted from learning object service
    
    Scenario: Import Curriculum Pathway with correct JSON in request payload
        Given that an CD or LXE has access to the content authoring tool to import curriculum pathway with correct json
            When Curriculum Pathway JSON data with correct payload request is imported
                Then That Curriculum Pathway JSON data should be ingested into learning object service
    
    Scenario: Import Curriculum Pathway with incorrect JSON in request payload
        Given that a CD or LXE has access to the content authoring tool to import curriculum pathway with incorrect json
            When Curriculum Pathway JSON data with incorrect payload request is imported
                Then ingestion of Curriculum Pathway JSON data into learning object service should fail

    Scenario: Fetch all nodes under a Program for a given alias
        Given that a CD or LXE wants to fetch all nodes of the given alias under a program
            When API request is sent to fetch all nodes with alias and correct program id
                Then All nodes of the given alias under that program will be fetched