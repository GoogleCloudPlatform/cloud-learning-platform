Feature: CRUD APIs for managing Verb data in Learning Record Service
    
    Scenario: Create verb object within Learning Record Service with correct request payload
        Given A user has access to Learning Record Service and needs to create a verb
            When API request is sent to create verb with correct request payload
                Then Verb object will be created successfully

    Scenario: Unable to create verb object within Learning Record Service with incorrect request payload
        Given A user has access privileges to Learning Record Service and needs to create a verb
            When API request is sent to create verb with incorrect request payload
                Then verb object will not be created and Learning Record Service will throw a validation error

    Scenario: Retrieve verb from Learning Record Service by giving valid uuid
        Given A user has access to Learning Record Service and needs to fetch a verb
            When API request is sent to fetch verb by providing correct uuid
                Then Verb object corresponding to given uuid will be returned successfully

    Scenario: Unable to retrieve verb when incorrect uuid is given
        Given A user has access privileges to Learning Record Service and needs to fetch a verb
            When API request is sent to fetch verb by providing invalid uuid
                Then verb object will not be returned and Resource not found error will be thrown by Learning Record Service

    Scenario: Retrieve all verbs from Learning Record Service
        Given A user has access to Learning Record Service and needs to fetch all verbs
            When API request is sent to fetch all verbs
                Then Learning Record Service will return all existing verb objects successfully

    Scenario: Unable to retrieve all verbs from Learning Record Service when incorrect params given
        Given A user can access Learning Record Service and needs to fetch all verbs
            When API request is sent to fetch all verbs with incorrect request payload
                Then The verbs will not be fetched and Learning Record Service will throw a Validation error

    Scenario: Update verb object within Learning Record Service with correct request payload
        Given A user has access to Learning Record Service and needs to update a verb
            When API request is sent to update verb with correct request payload
                Then Verb object will be updated successfully

    Scenario: Unable to update verb object within Learning Record Service when invalid uuid given
        Given A user has access privileges to Learning Record Service and needs to update a verb
            When API request is sent to update verb by providing invalid uuid
                Then verb object will not be updated and Learning Record Service will throw a resource not found error

    Scenario: Delete verb object within Learning Record Service by giving valid uuid
        Given A user has access to Learning Record Service and needs to delete a verb
            When API request is sent to delete verb by providing correct uuid
                Then Verb object will be deleted successfully

    Scenario: Unable to delete verb object within Learning Record Service when invalid uuid given
        Given A user has access privileges to Learning Record Service and needs to delete a verb
            When API request is sent to delete verb by providing invalid uuid
                Then verb object will not be deleted and Learning Record Service will throw a resource not found error

    Scenario: Import verb data from a json file with correct request payload
        Given We have access to raw data in json format for verb
            When Learning Record Service accesses this verb json data with correct payload request
                Then verb json data will be imported into Learning Record Service

    Scenario: Unable to import verb data from a json file with invalid json schema
        Given We have access to raw data of json type with invalid json schema for verb
            When Learning Record Service accesses this verb json data with invalid json schema
                Then verb data from given json file will not get imported and Learning Record Service will throw a validation error

    Scenario: Unable to import verb data when CSV file is provided instead of JSON file
        Given We have access to raw data for verb in csv format
            When Learning Record Service accesses this verb data in csv format instead of JSON
                Then verb data from given csv file will not get imported and Learning Record Service will throw a validation error