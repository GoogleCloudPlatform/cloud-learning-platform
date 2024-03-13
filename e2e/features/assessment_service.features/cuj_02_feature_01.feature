@assessment
Feature: CRUD for managing Assessment model in Assessment services

    Scenario: Create an Assessment with correct request payload
        Given that a LXE  has access to Assessment Service and need to create an Assessment
            When API request is sent to create an Assessment with correct request payload
                Then that Assessment object will be created in the database

    Scenario: Create an Assessment with incorrect request payload
        Given that a LXE has access to Assessment Service and need to create an Assessment
            When API request is sent to create Assessment with incorrect request payload
                Then Assessment object will not be created and Assessment Service will throw a Validation error
    
    Scenario: Read a particular Assessment
    using correct Assessment id
        Given that a LXE has access to Assessment Service and need to fetch an Assessment
            When API request is sent to fetch the Assessment with correct Assessment id
                Then the Assessment Service will serve up the requested Assessment
    
		Scenario: Read a particular Assessment and fetch all its child nodes using correct Assessment id
        Given that a LXE has access to Assessment Service and need to fetch an Assessment and all of its child nodes
            When API request is sent to fetch the Assessment and its child nodes with correct Assessment id
                Then the Assessment Service will serve up the requested Assessment and its child nodes

    Scenario: Read a particular Assessment using incorrect Assessment id
        Given that LXE has access to Assessment Service and need to fetch an Assessment
            When API request is sent to fetch the Assessment with incorrect Assessment id
				Then The Assessment will not be fetched and Assessment Service will throw ResourceNotFound error
    

    Scenario: Filter/Read all Assessments with correct query parameters
		Given that a LXE has access to Assessment Service and needs to fetch all Assessment
			When API request is sent to fetch all Assessment with correct query parameters
				Then the Assessment Service will show all the Assessment

	Scenario: FilterRead all Assessment with incorrect query parameters
		Given that a LXE can access Assessment Service and needs to fetch all Assessment
			When API request is sent to fetch all Assessment with incorrect query parameters
				Then the Assessment will not be fetched and Assessment Service will throw a Validation error

	Scenario: Update Assessment with correct request payload
		Given that a LXE has access to Assessment Service and needs to update an Assessment
			When API request is sent to update the Assessment with correct request payload
				Then that Assessment will be updated in the database

	Scenario: Update Assessment with incorrect Assessment id
		Given that a LXE can access Assessment Service and needs to update an Assessment
			When API request is sent to update the Assessment with incorrect Assessment id
				Then the Assessment will not be updated and Assessment Service will throw ResourceNotFound error

	Scenario: Delete a particular Assessment using correct Assessment id
		Given that a LXE has access to Assessment Service and needs to delete an Assessment
			When API request is sent to delete the Assessment with correct Assessment id
				Then that Assessment will be deleted from the database


	Scenario: Delete a particular Assessment using incorrect Assessment id
		Given that a LXE can access Assessment Service and needs to delete an Assessment
			When API request is sent to delete the Assessment with incorrect Assessment id
				Then the Assessment will not be deleted and Assessment Service will throw ResourceNotFound error


	Scenario: Import Assessment with correct JSON in request payload
		Given that a LXE has access to Assessment Service and needs to import Assessment from JSON file
			When the Assessment are imported from correct JSON in request payload
				Then those Assessment will be added in the database

	Scenario: Import Assessment with incorrect JSON in request payload
		Given that a LXE can access Assessment Service and needs to import Assessment from JSON file
			When the Assessment are imported from incorrect JSON in request payload
				Then the Assessment will not be imported and Assessment Service will throw Validation error
