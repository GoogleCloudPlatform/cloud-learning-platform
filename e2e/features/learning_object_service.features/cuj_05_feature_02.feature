Feature: Integration with 3rd Party Tool | Frost (curriculum pathway storage)

    Scenario: Retrieve a curriculum pathway using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view the curriculum pathway
            When there is a request to view a particular curriculum pathway with correct id
                Then the requested curriculum pathway will be retrieved

    Scenario: Retrieve all versions of curriculum pathway using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view all versions of the curriculum pathway
            When there is a request to view all versions of curriculum pathway with correct id
                Then all the versions of the requested curriculum pathway will be retrieved

    Scenario: Retrieve a specific version of curriculum pathway using correct id
        Given that an LXE or CD has access to the content authoring tool and needs to view a specific version of the curriculum pathway
            When there is a request to view a particular version of the curriculum pathway with correct id
                Then the requested version of the curriculum pathway will be retrieved

    Scenario: Retrieve a curriculum pathway using incorrect id
        Given an LXE or CD has access to the content authoring tool and needs to view the curriculum pathway
            When there is a request to view a particular curriculum pathway with incorrect id
                Then Learning Object Service will throw an error message for accessing invalid curriculum pathway