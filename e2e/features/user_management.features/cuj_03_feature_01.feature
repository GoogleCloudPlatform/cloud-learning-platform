Feature: CRUD for managing Application in user management

	Scenario: Create Application with correct request payload
		Given A user has permission to user management and wants to create a Application
			When API request is sent to create Application with correct request payload
				Then that Application object will be created in the database

    Scenario: Unable to create Application with incorrect request payload
		Given A user has permission to user management and wants to create a Application with incorrect payload
			When API request is sent to create Application with incorrect request payload
				Then that Application object will not be created and a validation error is thrown

    Scenario: Unable to create Application with name that already exists in database
		Given A user has permission to user management and wants to create a Application with name already existing in database
			When API request is sent to create Application with name already existing in database
				Then Application object will not be created and a conflict error is thrown

    Scenario: Retrieve Application from User management by giving valid uuid
        Given A user has access privileges to User management and needs to fetch a Application
            When API request is sent to fetch Application by providing correct uuid
                Then Application object corresponding to given uuid will be returned successfully

    Scenario: Unable to retrieve Application when incorrect uuid is given
        Given A user has access to User management and needs to fetch a Application
            When API request is sent to fetch Application by providing invalid uuid
                Then Application object will not be returned and Resource not found error will be thrown by User management

    Scenario: Retrieve all Applications from User management
        Given A user has access to User management and needs to fetch all Applications
            When API request is sent to fetch all Applications
                Then User management will return all existing Application objects successfully

    Scenario: Unable to retrieve all Applications from User management when incorrect params given
        Given A user can access User management and needs to fetch all Applications
            When API request is sent to fetch all Applications with incorrect request payload
                Then The Applications will not be fetched and User management will throw a Validation error

    Scenario: Update Application object within User management with correct request payload
        Given A user has access to User management and needs to update a Application
            When API request is sent to update Application with correct request payload
                Then Application object will be updated successfully
    
    Scenario: Unable to update Users in Application object with incorrect payload
        Given A user has access to User management and needs to update users in a Application
            When API request is sent to update users in a Application with incorrect payload
                Then Users in Application object will not be updated

    Scenario: Unable to update Application object within User management when invalid uuid given
        Given A user has access privileges to User management and needs to update a Application
            When API request is sent to update Application by providing invalid uuid
                Then Application object will not be updated and User management will throw a resource not found error

    Scenario: Delete Application object within User management by giving valid uuid
        Given A user has access to User management and needs to delete a Application and usergroups have access to the application 
            When API request is sent to delete Application by providing correct uuid
                Then the reference of deleted Applicationis removed from usergroups
                    And the permissions related to the application are also deleted
                        And Application object will be deleted successfully


    Scenario: Unable to delete Application object within User management when invalid uuid given
        Given A user has access privileges to User management and needs to delete a Application
            When API request is sent to delete Application by providing invalid uuid
                Then Application object will not be deleted and User management will throw a resource not found error
