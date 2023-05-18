Feature: Integration with 3rd Party Tool | Frost (Clone Functionality)

    Scenario: Clone a learning experience using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to copy a learning experience
            When there is a request to copy a particular learning experience with correct id
                Then a copy of the requested learning experience will be returned
    
    Scenario: Clone a learning experience using incorrect id
        Given an LXE or CD has access to the content authoring tool and needs to copy a learning experience
            When there is a request to copy a particular learning experience with incorrect id
                Then Learning Object Service will fail to copy the learning experience due to invalid learning experience id
    
    Scenario: Clone a learning object using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to copy a learning object
            When there is a request to copy a particular learning object with correct id
                Then a copy of the requested learning object will be returned
    
    Scenario: Clone a learning object using incorrect id
        Given an LXE or CD has access to the content authoring tool and needs to copy a learning object
            When there is a request to copy a particular learning object with incorrect id
                Then Learning Object Service will fail to copy the learning experience due to invalid learning object id
    
    Scenario: Cloning a learning Resource with a correct uuid
        Given that an LXE or CD has access to the content authoring tool and needs to copy a learning resource with correct uuid
            When there is a request to copy a particular learning resource with correct uuid
                Then a copy of the requested learning resource will be returned along with associated data
    
    Scenario: Cloning a learning Resource with a incorrect uuid
        Given that an LXE or CD has access to the content authoring tool and needs to create a copy of a learning resource with an incorrect uuid
            When there is a request to copy a particular the learning resource with incorrect uuid
                Then user fails to create the clone of the LR and gets an error message