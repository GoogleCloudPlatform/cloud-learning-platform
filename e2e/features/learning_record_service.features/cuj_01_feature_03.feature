Feature: CRUD for managing Activities in Learning Record Service
    
    Scenario: Create activity with correct payload
        Given User has the ability to create activity and tries to create activity with correct payload
            When API request is sent to create Activity with correct request payload
                Then That activity is created successfully with the given request payload

    Scenario: Create activity with incorrect payload
        Given User has the ability to create activity and tries to create activity with incorrect payload
            When API request is sent to create Activity with incorrect request payload
                Then Learning Record Service doesn't create Activity and throws validation error
    
    Scenario: Get a particular activity using correct activity id
        Given User has access to learning record service and needs to view a particular activity using correct activity uuid
            When API request is sent to get Activity with correct activity uuid
                Then Learning record Service will serve up the requested activity
    
    Scenario: Get a particular activity using incorrect activity id
        Given User has access to learning record service and needs to view a particular activity using incorrect activity uuid
            When API request is sent to get Activity with incorrect activity uuid
                Then Learning Record Service will return resource not found

    Scenario: Get all activities with correct request params 
        Given User has the ability to get list of activities with correct request parameters
            When API request is sent to get Activities with correct activity parameters
                Then Learning Record Service will serve list of activities based on correct request params

    Scenario: Get all activities with incorrect request params 
        Given User has the ability to get list of activities but provided incorrect parameters
            When API request is sent to get Activities with incorrect activity parameters
                Then Learning Record Service will throw validation error for incorrect paramaters

    Scenario: Update activity with correct request payload and correct activity id
        Given User has access to learning record Service and needs to update a activity
            When Api request is sent to update activity with correct request payload
                Then that activity should be updated successfully 

    Scenario: Unable to update activity object within Learning Record Service when invalid uuid given
        Given User has access to Learning Record Service and needs to update a activity using invalid uuid
            When API request is sent to update activity by providing invalid uuid
                Then Activity is not updated and Learning Record Service will throw a resource not found error
    
    Scenario: Delete activity object within Learning Record Service by giving valid uuid
        Given User has access to Learning Record Service and needs to delete a activity
            When API request is sent to delete activity by providing correct uuid
                Then Activity object will be deleted successfully

    Scenario: Unable to delete activity object within Learning Record Service when invalid uuid given
        Given User has access to Learning Record Service and needs to delete a activity using incorrect uuid
            When API request is sent to delete activity by providing incorrect uuid
                Then Activity object will not be deleted and Learning Record Service will throw a resource not found error

    Scenario: Import activity data from a json file with correct request payload
        Given We have access to raw data in json format for activity
            When Learning Record Service accesses this activity json data with correct payload request
                Then activity json data will be imported into Learning Record Service

    Scenario: Unable to import activity data from a json file with invalid json schema
        Given We have access to raw data of json type with invalid json schema for activity
            When Learning Record Service accesses this activity json data with invalid json schema
                Then activity data from given json file will not get imported and Learning Record Service will throw a validation error

    Scenario: Unable to import activity data when CSV file is provided instead of JSON file
        Given We have access to raw data for activity in csv format
            When Learning Record Service accesses this activity data in csv format instead of JSON
                Then activity data from given csv file will not get imported and Learning Record Service will throw a validation error