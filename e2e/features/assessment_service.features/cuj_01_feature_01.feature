Feature: CRUD for managing Assessment Item model in Assessment services

    Scenario: Create an Assessment Item with correct request payload
        Given that a LXE  has access to Assessment Service and need to create an Assessment Item
            When API request is sent to create an Assessment Item with correct request payload
                Then that Assessment Item object will be created in the database

    Scenario: Create an Assessment Item with incorrect request payload
        Given that a LXE has access to Assessment Service and need to create an Assessment Item
            When API request is sent to create Assessment Item with incorrect request payload
                Then Assessment Item object will not be created and Assessment Service will throw a Validation error
    
    Scenario: Read a particular Assessment Item
    using correct Assessment Item id
        Given that a LXE has access to Assessment Service and need to fetch an Assessment Item
            When API request is sent to fetch the Assessment Item with correct Assessment Item id
                Then the Assessment Service will serve up the requested Assessment Item
    
    Scenario: Read a particular Assessment Item using incorrect Assessment Item id
        Given that LXE has access to Assessment Service and need to fetch an Assessment Item
            When API request is sent to fetch the Assessment Item with incorrect Assessment Item id
				Then The Assessment Item will not be fetched and Assessment Service will throw ResourceNotFound error
    

    Scenario: Read all Assessment Items with correct request payload
		Given that a LXE has access to Assessment Service and needs to fetch all Assessment Item
			When API request is sent to fetch all Assessment Item with correct request payload
				Then the Assessment Service will show all the Assessment Item

	Scenario: Read all Assessment Item with incorrect request payload
		Given that a LXE can access Assessment Service and needs to fetch all Assessment Item
			When API request is sent to fetch all Assessment Item with incorrect request payload
				Then the Assessment Item will not be fetched and Assessment Service will throw a Validation error

	Scenario: Update Assessment Item with correct request payload
		Given that a LXE has access to Assessment Service and needs to update an Assessment Item
			When API request is sent to update the Assessment Item with correct request payload
				Then that Assessment Item will be updated in the database

	Scenario: Update Assessment Item with incorrect Assessment Item id
		Given that a LXE can access Assessment Service and needs to update an Assessment Item
			When API request is sent to update the Assessment Item with incorrect Assessment Item id
				Then the Assessment Item will not be updated and Assessment Service will throw ResourceNotFound error

	Scenario: Delete a particular Assessment Item using correct Assessment Item id
		Given that a LXE has access to Assessment Service and needs to delete an Assessment Item
			When API request is sent to delete the Assessment Item with correct Assessment Item id
				Then that Assessment Item will be deleted from the database


	Scenario: Delete a particular Assessment Item using incorrect Assessment Item id
		Given that a LXE can access Assessment Service and needs to delete an Assessment Item
			When API request is sent to delete the Assessment Item with incorrect Assessment Item id
				Then the Assessment Item will not be deleted and Assessment Service will throw ResourceNotFound error


	Scenario: Import Assessment Item with correct JSON in request payload
		Given that a LXE has access to Assessment Service and needs to import Assessment Item from JSON file
			When the Assessment Item are imported from correct JSON in request payload
				Then those Assessment Item will be added in the database

	Scenario: Import Assessment Item with incorrect JSON in request payload
		Given that a LXE can access Assessment Service and needs to import Assessment Item from JSON file
			When the Assessment Item are imported from incorrect JSON in request payload
				Then the Assessment Item will not be imported and Assessment Service will throw Validation error
