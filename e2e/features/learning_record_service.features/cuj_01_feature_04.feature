Feature: CRUD APIs for managing Agent data in Learning Record Service

    Scenario: Create Agent object within Learning Record Service with correct request payload
        Given A user has access to Learning Record Service and needs to create a Agent
            When API request is sent to create Agent with correct request payload
                Then Agent object will be created successfully

    Scenario: Unable to create Agent object within Learning Record Service with incorrect request payload
        Given A user has access privileges to Learning Record Service and needs to create a Agent
            When API request is sent to create Agent with incorrect request payload
                Then Agent object will not be created and Learning Record Service will throw a validation error

    Scenario: Retrieve Agent from Learning Record Service by giving valid uuid
        Given A user has access to Learning Record Service and needs to fetch a Agent
            When API request is sent to fetch Agent by providing correct uuid
                Then Agent object corresponding to given uuid will be returned successfully
    
    Scenario: Retrieve Agent from Learning Record Service by giving user id
        Given A user has access to Learning Record Service and needs to fetch Agent associated with a User
            When API request is sent to fetch Agent by providing user id associated with that agent
                Then Agent object corresponding to given user id will be returned successfully


    Scenario: Unable to retrieve Agent when incorrect uuid is given
        Given A user has access privileges to Learning Record Service and needs to fetch a Agent
            When API request is sent to fetch Agent by providing invalid uuid
                Then Agent object will not be returned and Resource not found error will be thrown by Learning Record Service

    Scenario: Retrieve all Agents from Learning Record Service
        Given A user has access to Learning Record Service and needs to fetch all Agents
            When API request is sent to fetch all Agents
                Then Learning Record Service will return all existing Agent objects successfully

    Scenario: Update Agent object within Learning Record Service with correct request payload
        Given A user has access to Learning Record Service and needs to update a Agent
            When API request is sent to update Agent with correct request payload
                Then Agent object will be updated successfully

    Scenario: Unable to update Agent object within Learning Record Service with incorrect request payload
        Given A user has access privileges to Learning Record Service and needs to update an already existing Agent
            When API request is sent to update Agent with incorrect request payload
                Then Agent object will not be updated and Learning Record Service will throw a validation error

    Scenario: Unable to update Agent object within Learning Record Service when invalid uuid given
        Given A user has access privileges to Learning Record Service and needs to update a Agent
            When API request is sent to update Agent by providing invalid uuid
                Then Agent object will not be updated and Learning Record Service will throw a resource not found error

    Scenario: Delete Agent object within Learning Record Service by giving valid uuid
        Given A user has access to Learning Record Service and needs to delete a Agent
            When API request is sent to delete Agent by providing correct uuid
                Then Agent object will be deleted successfully

    Scenario: Unable to delete Agent object within Learning Record Service when invalid uuid given
        Given A user has access privileges to Learning Record Service and needs to delete a Agent
            When API request is sent to delete Agent by providing invalid uuid
                Then Agent object will not be deleted and Learning Record Service will throw a resource not found error

    Scenario: Import Agent data from a json file with correct request payload
        Given We have access to raw data in json format for Agent
            When Learning Record Service accesses this Agent json data with correct payload request
                Then Agent json data will be imported into Learning Record Service

    Scenario: Unable to import Agent data from a json file with invalid json schema
        Given We have access to raw data of json type with invalid json schema for Agent
            When Learning Record Service accesses this Agent json data with invalid json schema
                Then Agent data from given json file will not get imported and Learning Record Service will throw a validation error