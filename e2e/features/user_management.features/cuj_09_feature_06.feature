Feature: Add or Remove Discipline Associations from Discipline Association Group

	Scenario: Add a Discipline to associations in an already created Discipline Association Group
		Given A user has permission to user management and wants to add a discipline to the Discipline Association Group
			When API request is sent to add a Discipline to the Discipline Association Group with correct request payload
				Then Discipline Association Group object will be updated in the database with updated association from the request payload

    Scenario: Add a Discipline to associations in an already created Discipline Association Group with invalid Discipline Association Group ID
		Given A user has permission to user management and wants to add a discipline to the Discipline Association Group with invalid ID
			When API request is sent to add a Discipline to the Discipline Association Group with correct request payload but invalid Discipline Association Group ID
				Then the API would raise ResourceNotFoundException

    Scenario: Add a Discipline to associations in an already created Discipline Association Group with invalid request body
		Given A user has permission to user management and wants to add a discipline to the Discipline Association Group with invalid request body
			When API request is sent to add a Discipline to the Discipline Association Group with incorrect request payload
				Then the API would raise ValidationError

    Scenario: Add a already associated Discipline to associations in an already created Discipline Association Group    
		Given A user has permission to user management and wants to add an already associated discipline to the Discipline Association Group
			When API request is sent to add already associated Discipline to the Discipline Association Group
				Then the API would raise ValidationError for the given discipline

    
    Scenario: Remove a Discipline to associations in an already created Discipline Association Group
		Given A user has permission to user management and wants to remove a discipline to the Discipline Association Group
			When API request is sent to remove a Discipline to the Discipline Association Group with correct request payload
				Then Discipline Association Group object will be updated in the database and the discipline will be removed
    
    Scenario: Remove a Discipline to associations in an already created Discipline Association Group with invalid association group ID
		Given A user has permission to user management and wants to remove a discipline to the Discipline Association Group with invalid association group ID
			When API request is sent to remove a Discipline to the Discipline Association Group with invalid assoication group ID
				Then the API would raise ResourceNotFoundException with 404 status code
	@filter-api
    Scenario: Remove a Discipline to associations in an already created Discipline Association Group with invalid payload
		Given A user has permission to user management and wants to remove a discipline to the Discipline Association Group with invalid payload
			When API request is sent to remove a Discipline to the Discipline Association Group with invalid payload
				Then the API would raise ValidationError with 422 status code

	@filter-api
    Scenario: Remove the Discipline from the discipline association group with the correct request payload
        Given Discipline association group already exists with a user (instructor) actively associated to a discipline
            When an API request sent to remove the Discipline from the discipline association group with correct request payload
                Then discipline will get removed from the corresponding discipline association group object
                    And the user of instructor type associated to the discipline will also get removed from all Learner Association Group where it exists
						And the user of assessor type associated to the discipline will also get removed from all submitted assessments where it exists
