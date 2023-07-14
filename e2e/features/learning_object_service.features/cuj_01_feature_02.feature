Feature: Integration with 3rd Party Tool | Frost (learning experience storage)

    Scenario: Retrieve a learning experience using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view the learning experience
            When there is a request to view a particular learning experience with correct id
                Then the requested learning experience will be retrieved

    Scenario: Retrieve all versions of learning experience using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view all versions of the learning experience
            When there is a request to view all versions of learning experience with correct id
                Then all the versions of the requested learning experience will be retrieved

    Scenario: Retrieve a specific version of learning experience using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view a specific version of the learning experience
            When there is a request to view a particular version of the learning experience with correct id
                Then the requested version of the learning experience will be retrieved

    Scenario: Retrieve a learning experience using incorrect id
        Given an LXE or CD has access to the content authoring tool and needs to view the learning experience
            When there is a request to view a particular learning experience with incorrect id
                Then Learning Object Service will throw an error message for accessing invalid learning experience

    Scenario: Retrieve a learning object using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view the learning object
            When there is a request to view a particular learning object with correct id
                Then the requested learning object will be retrieved

    Scenario: Retrieve all versions of learning object using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view all versions of the learning object
            When there is a request to view all versions of the learning object with correct id
                Then all the versions of the requested learning object will be retrieved

    Scenario: Retrieve a specific version of learning object using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view a specific version of the learning object
            When there is a request to view a specific version of the learning object with correct id
                Then the requested version of the learning object will be retrieved

    Scenario: Retrieve a learning object using incorrect id
        Given an LXE or CD has access to the content authoring tool and needs to view the learning object
            When there is a request to view a particular learning object with incorrect id
                Then Learning Object Service will throw an error message for accessing invalid learning object
    
    Scenario: Retrieve a learning resource using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view the learning resource with the correct id
            When there is a request to view a particular learning resource with correct id
                Then the requested learning resource will be retrieved

    Scenario: Retrieve a learning resource using incorrect id
        Given that an LXE or CD has access to the content authoring tool and needs to view the learning resource with the incorrect id
            When there is a request to view a particular learning resource with incorrect id
                Then Learning Object Service will throw an error message for accessing invalid learning resource