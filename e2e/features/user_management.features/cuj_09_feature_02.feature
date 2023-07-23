Feature: CRUD for managing Discipline Association Group in user management

	Scenario: Create Discipline Association Group with correct request payload
		Given A user has permission to user management and wants to create a Discipline Association Group
			When API request is sent to create Discipline Association Group with correct request payload
				Then Discipline Association Group object will be created in the database as per given request payload

    Scenario: Unable to create Discipline Association Group with incorrect request payload
		Given A user has permission to user management and wants to create a Discipline Association Group with incorrect payload
			When API request is sent to create Discipline Association Group with incorrect request payload
				Then Discipline Association Group object will not be created and a validation error is thrown

    Scenario: Unable to create Discipline Association Group with name that already exists in database
		Given A user has permission to user management and wants to create a Discipline Association Group with name already existing in database
			When API request is sent to create Discipline Association Group with name already existing in database
				Then Discipline Association Group object will not be created and a conflict error is thrown

    Scenario: Retrieve Discipline Association Group from User management by giving valid uuid
        Given A user has access privileges to User management and needs to fetch a Discipline Association Group
            When API request is sent to fetch Discipline Association Group by providing correct uuid
                Then Discipline Association Group object corresponding to given uuid will be returned successfully

    Scenario: Unable to retrieve Discipline Association Group when incorrect uuid is given
        Given A user has access to User management and needs to fetch a Discipline Association Group
            When API request is sent to fetch Discipline Association Group by providing invalid uuid
                Then Discipline Association Group object will not be returned and Resource not found error will be thrown by User management

    Scenario: Unable to retrieve Discipline Association Group when uuid for Learner Association Group is given
        Given A user has access to User management and needs to fetch a Association Group of Discipline Type
            When API request is sent to fetch Discipline Association Group by providing uuid for Learner Association Group
                Then Discipline Association Group object will not be returned and Validation error will be thrown by User management

    @filter-api
    Scenario: Retrieve all Discipline Association Groups from User management
        Given A user has access to User management and needs to fetch all Discipline Association Groups
            When API request is sent to fetch all Discipline Association Groups
                Then User management will return all existing Discipline Association Group objects successfully

    Scenario: Unable to retrieve all Discipline Association Groups from User management when incorrect params given
        Given A user can access User management and needs to fetch all Discipline Association Groups
            When API request is sent to fetch all Discipline Association Groups with incorrect params
                Then No Discipline Association Groups will be fetched and User management will throw a Validation error

    Scenario: Update Discipline Association Group object within User management with correct request payload
        Given A user has access to User management and needs to update a Discipline Association Group
            When API request is sent to update Discipline Association Group with correct request payload
                Then The corresponding Discipline Association Group object will be updated successfully

    Scenario: Unable to update Discipline Association Group object within User management when invalid uuid given
        Given A user has access privileges to User management and needs to update a Discipline Association Group
            When API request is sent to update Discipline Association Group by providing invalid uuid
                Then Discipline Association Group object will not be updated and User management will throw a resource not found error
  
      Scenario: Unable to update Discipline Association Group with name that already exists in database
		Given A user has permission to user management and wants to update name in Discipline Group thats already exists in database
			When API request is sent to update Discipline Association Group with name already existing in database
				Then Discipline Association Group object will not be updated and a conflict error is thrown

    Scenario: Unable to update Discipline Association Group when uuid for Learner Association Group is given
        Given A user has access to User management and needs to update a Association Group of Discipline Type
            When API request is sent to update Discipline Association Group by providing uuid for Learner Association Group
                Then Discipline Association Group object will not be updated and Validation error will be thrown by User management

    Scenario: Delete Discipline Association Group object within User management by giving valid uuid
        Given A user has access to User management and needs to delete a Discipline Association Group
            When API request is sent to delete Discipline Association Group by providing correct uuid
                Then Discipline Association Group object will be deleted successfully
                    Then the discipline association will also get removed from all Learner Association Group where it exists

    Scenario: Unable to delete Discipline Association Group object within User management when invalid uuid given
        Given A user has access privileges to User management and needs to delete an Discipline Association Group
            When API request is sent to delete Discipline Association Group by providing invalid uuid
                Then Discipline Association Group object will not be deleted and User management will throw a resource not found error

    Scenario: Unable to delete Discipline Association Group when uuid for Learner Association Group is given
        Given A user has access to User management and needs to delete a Association Group of Discipline Type
            When API request is sent to delete Discipline Association Group by providing uuid for Learner Association Group
                Then Discipline Association Group object will not be deleted and Validation error will be thrown by User management

    @filter-api
    Scenario: Retrieve all users associated with a discipline when discipline uuid is given
        Given A user has access to User management and needs to fetch all users belonging to given discipline
            When API request is sent to fetch all users by providing uuid for discipline
                Then Users associated with provided discipline uuid will be returned

    @filter-api
    Scenario: Retrieve all instructors associated with a discipline when discipline uuid is given
        Given A user has access to User management and needs to fetch all instructors belonging to given discipline
            When API request is sent to fetch all instructors by providing uuid for discipline
                Then Instructors associated with provided discipline uuid will be returned

    Scenario: Unable to fetch assessors associated with a discipline when non-existing discipline uuid is given
        Given A user has access to User management and needs to fetch all assessors belonging to given discipline using non-existent discipline uuid
            When API request is sent to fetch all assessors by providing non-existent uuid for discipline
                Then Assessors will not be returned and resource not found error will be thrown

    Scenario: Unable to fetch assessors associated with a discipline when wrong filter type is provided
        Given A user has access to User management and needs to fetch all assessors belonging to given discipline
            When API request is sent to fetch all assessors by providing incorrect filter parameter
                Then Assessors will not be returned and validation error will be thrown

    Scenario: Unable to fetch instructors associated with a discipline when alias of curriculum pathway is not discipline
        Given A user has access to User management and needs to fetch all instructors belonging to given discipline whose alias is not discipline
            When API request is sent to fetch all instructors by providing invalid discipline uuid
                Then Instructors will not be returned and validation error will be thrown for invalid alias

    Scenario: Update User/Association Status within Discipline Association Group object with correct request payload
        Given A Discipline Association Group exists and user has access to User management to update User/Association Status
            When API request is sent to update User/Association Status of a Discipline Association Group with correct request payload
                Then The status of User/Association within the Discipline Association Group object will be updated successfully

    Scenario: Update Status of instructor type of user within Discipline Association Group object with correct request payload
        Given A Discipline Association Group exists and user has access to User management to update User Status
            When API request is sent to update Status of user type of instructor in Discipline Association Group with correct request payload
                Then The status of Instructor type of User within the Discipline Association Group object will be updated successfully
                    And status of the same Instructor existing in Learner ASsociation Group object will also be updated successfully

    Scenario: De-activate a discipline within Discipline Association Group object with correct request payload
        Given A Discipline Association Group exists and user has access to User management to update assocaition status
            When API request is sent to de-activate a discipline in Discipline Association Group with correct request payload
                Then The status of discipline within the Discipline Association Group object will be updated as inactive
                    And status of the same Instructor associated to the disicpline existing in any Learner ASsociation Group object will also be updated as Inactive

    Scenario: Unable to update User/Association Status within Discipline Association Group object when invalid association group uuid given
        Given A Discipline Association Group exists and user has access to update User/Association Status
            When API request is sent to update User/Association status within Discipline Association Group by providing invalid group uuid
                Then User/Association Status will not be updated and a resource not found error will be returned

    Scenario: Unable to update User/Association Status within Discipline Association Group object when invalid document id given in request payload
        Given A Discipline Association Group exists and user has access privileges to update User/Association Status
            When API request is sent to update User/Association status within Discipline Association Group by providing invalid document id
                Then User/Association Status will not be updated and a Validation error will be returned

    Scenario: Unable to update User/Association Status within Discipline Association Group object when invalid status given in request payload
        Given A Discipline Association Group exists and user has privileges to update User/Association Status
            When API request is sent to update User/Association status within Discipline Association Group by providing invalid status
                Then User/Association Status will not get updated and User management will return a Validation Error
