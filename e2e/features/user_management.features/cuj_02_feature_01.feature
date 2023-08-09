Feature: CRUD for managing UserGroup in user management

	Scenario: Create UserGroup with correct request payload
		Given A user has permission to user management and wants to create a UserGroup
			When API request is sent to create UserGroup with correct request payload
				Then that UserGroup object will be created in the database

    Scenario: Unable to create UserGroup with incorrect request payload
		Given A user has permission to user management and wants to create a UserGroup with incorrect payload
			When API request is sent to create UserGroup with incorrect request payload
				Then that UserGroup object will not be created and a validation error is thrown

    Scenario: Retrieve UserGroup from User management by giving valid uuid
        Given A user has access privileges to User management and needs to fetch a UserGroup
            When API request is sent to fetch UserGroup by providing correct uuid
                Then UserGroup object corresponding to given uuid will be returned successfully

    Scenario: Unable to retrieve UserGroup when incorrect uuid is given
        Given A user has access to User management and needs to fetch a UserGroup
            When API request is sent to fetch UserGroup by providing invalid uuid
                Then UserGroup object will not be returned and Resource not found error will be thrown by User management

    Scenario: Retrieve all UserGroups from User management
        Given A user has access to User management and needs to fetch all UserGroups
            When API request is sent to fetch all UserGroups
                Then User management will return all existing UserGroup objects successfully

    Scenario:  sort UserGroup records from User management
        Given A user has access to User management and needs to sort user groups
            When API request is sent to sort user groups
                Then User management will return all existing UserGroup objects by sorted order

    Scenario: Unable to retrieve all UserGroups from User management when incorrect params given
        Given A user can access User management and needs to fetch all UserGroups
            When API request is sent to fetch all UserGroups with incorrect request payload
                Then The UserGroups will not be fetched and User management will throw a Validation error

    Scenario: Update UserGroup object within User management with correct request payload
        Given A user has access to User management and needs to update a UserGroup
            When API request is sent to update UserGroup with correct request payload
                Then UserGroup object will be updated successfully

    Scenario: Unable to update UserGroup object within User management when invalid uuid given
        Given A user has access privileges to User management and needs to update a UserGroup
            When API request is sent to update UserGroup by providing invalid uuid
                Then UserGroup object will not be updated and User management will throw a resource not found error

    Scenario: Delete UserGroup object within User management by giving valid uuid
        Given A user has access to User management and needs to delete a UserGroup
            When API request is sent to delete UserGroup by providing correct uuid
                Then UserGroup object will be deleted successfully
                    Then And the deleted UserGroup is unassigned from all the users and permissions

    Scenario: Unable to delete UserGroup object within User management when invalid uuid given
        Given A user has access privileges to User management and needs to delete a UserGroup
            When API request is sent to delete UserGroup by providing invalid uuid
                Then UserGroup object will not be deleted and User management will throw a resource not found error

    Scenario: Add users to the UserGroup within User management
        Given A user has access to User management and needs to add users to UserGroup
            When API request is sent to add users to UserGroup
                Then The users are added to UserGroup 
                    Then the UserGroup is assigned to the users in request

    Scenario: Remove users from the UserGroup within User management
        Given A user has access to User management and needs to remove users from UserGroup
            When API request is sent to remove users to UserGroup
                Then The users are removed from the UserGroup 
                    Then the UserGroup is unassigned from the users in request

    Scenario: Retrieve UserGroup from User management by searching with a valid name
        Given A user has access privileges to User management and needs to search for a UserGroup
            When API request is sent to search UserGroup by providing correct name
                Then UserGroups corresponding to given name will be returned successfully

    Scenario: Unable to retrieve UserGroup by searching with an invalid name
        Given A user has access to User management and needs to search for a UserGroup
            When API request is sent to search UserGroup by providing invalid name
                Then An empty list would be returned for the search

    Scenario: Retrieve Users that can be added to UserGroup
        Given A user has access to User management and needs to retrieve users that can be added to a UserGroup
            When API request is sent to fetch users by providing valid UserGroup uuid
                Then List of users that can be added to provided UserGroup will be returned

    Scenario: Unable to retrieve Users that can be added to UserGroup
        Given A user has access to User management and needs to retrieve users that can be added to a UserGroup which does not exist
            When API request is sent to fetch users by providing invalid UserGroup uuid
                Then Resource not Found error will be thrown for providing invalid UserGroup uuid