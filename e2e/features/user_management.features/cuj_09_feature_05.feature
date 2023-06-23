Feature: CRUD for managing Association Group in user management

    Scenario: Fetch Association Groups from User management by searching with a valid name
        Given A user has access to User management and needs to search Association Group
            When API request is sent to fetch Association Group by providing valid name
                Then A list of Association Group objects corresponding to given name will be returned

    Scenario: Fetch Association Groups from User management by searching with an invalid name
        Given A user has access to User management and needs to fetch a Association Group
            When API request is sent to fetch Association Group by providing invalid name
                Then An empty list will be returned for the search
    
    Scenario: Fetch Association Groups from User management by searching with empty search_query
        Given A user has access to User management and wants to search Association Group
            When API request is sent to fetch Association Group by providing empty search_query
                Then A ValidationError will be thrown

    @filter-api
	Scenario: Get Association Group with correct request payload
		Given A user has permission to user management and wants to retrieve Association Group
			When API request is sent to retrieve Association Group with correct request payload
				Then A list of Association Group will be retrieved from the database as per given request payload

    Scenario: Get Association Group with incorrect request payload
		Given A user has permission to user management and wants to fetch Association Group
			When API request is sent to retrieve Association Group with incorrect request payload
				Then A list of Association Group will be not retrieved and a validation error is thrown

    Scenario: Retrieve Users addable to an assocation group for a given user type
        Given A user has access to fetch users for a given user type
            When A GET api call is made to the User Management Service to fetch users
                Then A list of users for the given user type is returned

    Scenario: Retrieve Users for type learner which are already associated with learner assocation groups
        Given A user has access to to fetch users of type learner which are already associated with learner assocation groups
            When A GET api call is made to the User Management Service to fetch users of type learner
                Then A empty list of users for user type learner is returned