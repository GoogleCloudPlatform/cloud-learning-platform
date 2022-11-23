Feature: Create, Read, Retive all and delete APIs for Course Template

    Scenario: Create Course Template with correct request payload
        Given A user has access privileges and needs to create a Course Template Record
            When API request is sent to create Course Template Record with correct request payload
                Then Course Template Record will be created in a third party tool and classroom master course will be create with provided payload and all metadata will be ingested and stored in Cousre Template service and uuid for learning experiences will be stored in Cousre Template service

    Scenario: Unable to create Course Template with incorrect request payload
        Given A user has access to admin portal and wants to create a Course Template Record
            When API request is sent to create Course Template Record with incorrect request payload
                Then Course Template Record Record will not be created and Course Template API will throw a validation error

    @fixture.create.course_tepmlate
    Scenario: Retrieve Course Template Record by giving valid uuid
        Given A user has access privileges and needs to retrieve a Course Template Record
            When API request is sent to retrieve Course Template Record by providing correct uuid
                Then Course Template Record corresponding to given uuid will be returned successfully

    Scenario: Unable to retrieve Course Template Record when invalid uuid given
        Given A user has access to admin portal and wants to retrieve a Course Template Record
            When API request is sent to retrieve Course Template Record by providing invalid uuid
                Then Course Template Record will not be returned and API will throw a resource not found error

    @fixture.create.course_tepmlate
    Scenario: Delete Course Template Record by giving valid uuid
        Given A user has access privileges and needs to delete a Course Template Record
            When API request is sent to delete Course Template Record by providing correct uuid
                Then Course Template Record will be deleted successfully

    Scenario: Unable to delete Course Template Record when invalid uuid given
        Given A user has access to admin portal and wants to delete a Course Template Record
            When API request is sent to delete Course Template Record by providing invalid uuid
                Then Course Template Record will not be deleted and API will throw a resource not found error
    
    Scenario: Retrieve all Course Template Records
        Given A user has access privileges and needs to fetch all Course Template Records
            When API request is sent to fetch all Course Template Records
                Then Course Template API will return all existing Course Template Records successfully
    