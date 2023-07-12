Feature: Creation, Updation (with version control) and Deletion of LOs, LEs and LRs from content authoring tool by LXE or CD

    Scenario: Create Learning Experience with correct request payload
        Given that a LXE or CD has access to the content authoring tool
            When they design the learning experience using a third party tool
                Then the learning experiences will be created in a third-party tool
                    And all metadata will be ingested and stored in learning object service
                        And uuid for learning experiences will be stored in learning object service

    Scenario: Create Learning Experience with incorrect request payload
        Given that a LXE or CD has access to content authoring tool
            When they design the learning experience using a third party tool with invalid request
                Then the learning experiences will not be created in learning object service

    Scenario: Update Learning Experience with correct request payload
        Given that an LXE or CD has access to the content authoring tool
            When they update the learning experience using a third-party tool
                Then the learning experiences will be updated in a third-party tool
                    And all metadata will be updated in learning object service
    
    Scenario: Update Learning Experience with correct request payload and create version
        Given that an LXE or CD has access to the content authoring tool to create version of learning experience
            When they update the learning experience using a third-party tool to create version
                Then a version of learning experience will be created
                    And all metadata for the learning experience will be updated learning object service
                        And a version document for the learning experience will be created in learing object service
    
    Scenario: Update Learning Experience with invalid uuid in request payload
        Given that an LXE or CD has access to content authoring tool
            When they update the learning experience using a third-party tool with invalid uuid
                Then the learning experiences will not be updated in learning object service
    
    Scenario: Update Learning Experience with invalid request payload
        Given that a LXE has access to content authoring tool
            When they update the learning experience using a third-party tool with invalid request
                Then the learning experience will not be updated in learning object service
    
    Scenario: Delete Learning Experience with correct request payload
        Given that an LXE has access to content authoring tool
            When they delete the learning experience using a third-party tool
                Then the learning experiences will be deleted from a third-party tool
                    And all metadata will be deleted from learning object service
    
    Scenario: Delete Learning Experience with incorrect uuid in request payload
        Given that an LXE has access to the content authoring tool
            When they delete the learning experience using a third-party tool wiht incorrect uuid
                Then the learning experiences will not be deleted from learning object service
    
    Scenario: Import Learning Experience with correct JSON in request payload
        Given that an CD or LXE has access to the content authoring tool
            When Learning Experience JSON data with correct payload request is imported
                Then That Learning Experience JSON data should be ingested into learning object service
    
    Scenario: Import Learning Experience with incorrect JSON in request payload
        Given that a CD or LXE has access to the content authoring tool
            When Learning Experience JSON data with incorrect payload request is imported
                Then ingestion of Learning Experience JSON data into learning object service should fail

    Scenario: Creation of LOS from third party content authoring tool with correct payload
        Given that an LXE or CD has access to the content authoring tool for creation of learning object with correct payload
            When they design the learning object using a third party content authoring tool with correct payload
                Then the learning object and their components will be created in the learning object service with correct payload
                    And all the associated metadata will will be created in learning object service
                        And Unique IDs for learning objects will be stored in learning object service
    
    Scenario: Creation of LOS from third party content authoring tool with incorrect payload
        Given that an LXE or CD has access to the content authoring tool for creation of learning object with incorrect payload
            When they design the learning object using a third party content authoring tool with incorrect payload
                Then the learning object and their components will not be created in the learning object service
                    And the user gets an error message for create
    
    Scenario: Updation of LOS from third party content authoring tool with correct payload
        Given that an LXE or CD has access to the content authoring tool for updation of learning object with correct payload
            When they updated the design of the learning object using a third party content authoring tool with correct payload 
                Then the learning object and their components will be updated in the learning object service with correct payload
                    And all the associated metadata will will be updated in learning object service
                        And Unique IDs for the updated learning objects will be stored in learning object service

    Scenario: Update Learning Object with correct request payload and create version
        Given that an LXE or CD has access to the content authoring tool to create version of learning object
            When they update the learning object using a third-party tool to create version
                Then a version of learning object will be created
                    And all metadata for the learning object will be updated in learning object service
                        And a version for the learning object document will be created in learing object service

    Scenario: Updation of LOS from third party content authoring tool with incorrect payload
        Given that an LXE or CD has access to the content authoring tool for updation of learning object with incorrect payload
            When they updated the design of the learning object using a third party content authoring tool with incorrect payload 
                Then the learning object and their components will not be updated in the learning object service
                    And the user will get an error message for update
    
    Scenario: Deletion of LO from third party content authoring tool with correct payload
        Given that an LXE or CD has access to the content authoring tool for deletion of learning object with correct payload
            When they delete the learning object using a third party content authoring tool with correct payload 
                Then the learning object and their components will be deleted in the learning object service with correct payload
                    And all the associated metadata will will be deleted in learning object service
    
    Scenario: Deletion of LO from third party content authoring tool with incorrect payload
        Given that an LXE or CD has access to the content authoring tool for deletion of learning object with incorrect payload
            When they delete the learning object using a third party content authoring tool with incorrect payload
                Then the learning object and their components will not be deleted in the learning object service
                    And the user will get an error message
    
    Scenario: Import Learning Object with correct JSON in request payload
        Given that an CD or LXE has access to the content authoring tool with correct request payload
            When Learning object JSON data with correct payload request is imported
                Then That Learning object JSON data should be ingested into learning object service
    
    Scenario: Import Learning Object with incorrect JSON in request payload
        Given that an CD or LXE has access to the content authoring tool with incorrect request payload
            When Learning object JSON data with incorrect payload request is not imported
                Then That user gets an error message
    
    Scenario: Create Learning Resource with correct request payload
        Given that a LXE or CD has access to the content authoring tool for creating LR
            When they design the learning resource using a third party tool
                Then the learning resource will be created in a third-party tool
                    And all LR metadata will be ingested and stored in learning object service
                        And Unique IDs for learning resources will be stored in learning object service
    
    Scenario: Create Learning Resource with incorrect request payload
        Given that a LXE or CD has access to content authoring tool with incorrect LR payload
            When they design the learning resource using a third party tool with invalid request
                Then the learning resource will not be created in learning object service
                     And the user gets an error message for LR create
    
    Scenario: Update Learning Resource with correct request payload and not create version
        Given that an LXE or CD has access to the content authoring tool for updation of learning resource with correct payload
            When they updated the learning resource using a third party content authoring tool with correct payload
                Then the learning resource and their components will be updated in the learning object service with correct payload
                    And all the learning resource associated metadata will will be updated in learning object service
                        And Unique IDs for the updated learning resource will be stored in learning object service

    Scenario: Update Learning Resource with correct request payload and create version
        Given that an LXE or CD has access to the content authoring tool to create version of learning resource
            When they update the learning resource using a third-party tool to create version
                Then a version of learning resource will be created
                    And all metadata for the learning resource will be updated learning object service
                        And a version document for the learning resource will be created in learing object service

    Scenario: Updation of Learning Resoruce from third party content authoring tool with incorrect payload
        Given that an LXE or CD has access to the content authoring tool for updation of learning resource with incorrect payload
            When they updated the learning resource using a third party content authoring tool with incorrect payload 
                Then the learning resource and their components will not be updated in the learning object service
                    And the user will get an error message for Learning resource update


    Scenario: Update Learning Resource with invalid uuid in request payload
        Given that an LXE or CD has access to content authoring tool to update the learning resource
            When they update the learning resource using a third-party tool with invalid uuid
                Then the learning resource will not be updated in learning object service
                    And the user will get an error message for invalid uuid for Learning Resource update

    
    Scenario: Deletion of LR from third party content authoring tool with correct payload
        Given that an LXE has access to content authoring tool for deleting LR
            When they delete the learning resource using a third-party tool 
                Then the learning resources will be deleted from a third-party tool
                    And all LR associated metadata will be deleted from learning object service

    Scenario: Deletion of LR from third party content authoring tool with incorrect payload
        Given that an LXE has access to the content authoring tool for deletion with an incorrect LR payload
            When they delete the learning resource using a third-party tool with incorrect uuid 
                Then the learning resource will not be deleted from learning object service
                    And the user will get an error message for incorrect LR delete request
    

    Scenario: Import Learning Resource with correct JSON in request payload
        Given that an LXE or CD has access to the content authoring tool with correct Learning Resource request payload
            When Learning resource JSON data with correct payload request is imported
                Then That Learning resoruce JSON data should be ingested into learning object service
    
    Scenario: Import Learning Resource with incorrect JSON in request payload
        Given that an LXE or CD has access to the content authoring tool with incorrect Learning resource request payload
            When Learning resource JSON data with incorrect payload request is not imported
                Then That user gets an error message for Learning Resrouce
    


    