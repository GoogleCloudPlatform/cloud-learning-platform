Feature: CRUD for managing Learner Association Group in user management

	Scenario: Create Learner Association Group with correct request payload
		Given A user has permission to user management and wants to create a Learner Association Group
			When API request is sent to create Learner Association Group with correct request payload
				Then Learner Association Group object will be created in the database as per given request payload

    Scenario: Unable to create Learner Association Group with incorrect request payload
		Given A user has permission to user management and wants to create a Learner Association Group with incorrect payload
			When API request is sent to create Learner Association Group with incorrect request payload
				Then Learner Association Group object will not be created and a validation error is thrown

    Scenario: Unable to create Learner Association Group with name that already exists in database
		Given A user has permission to user management and wants to create a Learner Association Group with name already existing in database
			When API request is sent to create Learner Association Group with name already existing in database
				Then Learner Association Group object will not be created and a conflict error is thrown

    Scenario: Retrieve Learner Association Group from User management by giving valid uuid
        Given A user has access privileges to User management and needs to fetch a Learner Association Group
            When API request is sent to fetch Learner Association Group by providing correct uuid
                Then Learner Association Group object corresponding to given uuid will be returned successfully

    Scenario: Unable to retrieve Learner Association Group when incorrect uuid is given
        Given A user has access to User management and needs to fetch a Learner Association Group
            When API request is sent to fetch Learner Association Group by providing invalid uuid
                Then Learner Association Group object will not be returned and Resource not found error will be thrown by User management

    Scenario: Unable to retrieve Learner Association Group when uuid for Discipline Association Group is given
        Given A user has access to User management and needs to fetch a Association Group of Learner Type
            When API request is sent to fetch Learner Association Group by providing uuid for Discipline Association Group
                Then Learner Association Group object will not be returned and Validation error will be thrown by User management

    @filter-api
    Scenario: Retrieve all Learner Association Groups from User management
        Given A user has access to User management and needs to fetch all Learner Association Groups
            When API request is sent to fetch all Learner Association Groups
                Then User management will return all existing Learner Association Group objects successfully

    Scenario: Unable to retrieve all Learner Association Groups from User management when incorrect params given
        Given A user can access User management and needs to fetch all Learner Association Groups
            When API request is sent to fetch all Learner Association Groups with incorrect params
                Then No Learner Association Groups will be fetched and User management will throw a Validation error

    Scenario: Update Learner Association Group object within User management with correct request payload
        Given A user has access to User management and needs to update a Learner Association Group
            When API request is sent to update Learner Association Group with correct request payload
                Then The corresponding Learner Association Group object will be updated successfully

    Scenario: Unable to update Learner Association Group object within User management when invalid uuid given
        Given A user has access privileges to User management and needs to update a Learner Association Group
            When API request is sent to update Learner Association Group by providing invalid uuid
                Then Learner Association Group object will not be updated and User management will throw a resource not found error
  
    Scenario: Unable to update Learner Association Group with name that already exists in database
		Given A user has permission to user management and wants to update name thats already exists in database
			When API request is sent to update Learner Association Group with name already existing in database
				Then Learner Association Group object will not be updated and a conflict error is thrown

    Scenario: Unable to update Learner Association Group when uuid for Discipline Association Group is given
        Given A user has access to User management and needs to update a Association Group of Learner Type
            When API request is sent to update Learner Association Group by providing uuid for Discipline Association Group
                Then Learner Association Group object will not be updated and Validation error will be thrown by User management

    Scenario: Delete Learner Association Group object within User management by giving valid uuid
        Given A user has access to User management and needs to delete a Learner Association Group
            When API request is sent to delete Learner Association Group by providing correct uuid
                Then Learner Association Group object will be deleted successfully

    Scenario: Unable to delete Learner Association Group object within User management when invalid uuid given
        Given A user has access privileges to User management and needs to delete an Learner Association Group
            When API request is sent to delete Learner Association Group by providing invalid uuid
                Then Learner Association Group object will not be deleted and User management will throw a resource not found error

    Scenario: Unable to delete Learner Association Group when uuid for Discipline Association Group is given
        Given A user has access to User management and needs to delete a Association Group of Learner Type
            When API request is sent to delete Learner Association Group by providing uuid for Discipline Association Group
                Then Learner Association Group object will not be deleted and Validation error will be thrown by User management

    Scenario: Update User/Association Status within Learner Association Group object with correct request payload
        Given A Learner Association Group exists and user has access to User management to update User/Association Status
            When API request is sent to update User/Association Status of a Learner Association Group with correct request payload
                Then The status of User/Association within the Learner Association Group object will be updated successfully

    Scenario: Activate an instructor within Learner Association Group object for given instructor_id and curriculum_pathway_id
        Given A Learner Association Group, Discipline Association Group exists with actively associated user & discipline
            When API request is sent to activate an instructor for given instructor_id and curriculum_pathway_id
                Then The instructor for given instructor_id and curriculum_pathway_id within the Learner Association Group object will be activated successfully

    Scenario: Unable to Activate an instructor within Learner Association Group object for given instructor_id and curriculum_pathway_id
        Given A Learner Association Group, Discipline Association Group exists with user & discipline in inactive status
            When API request is sent to activate an instructor for given instructor_id
                Then The instructor for given instructor_id and curriculum_pathway_id will not get activated and ValidationError will be thrown

    Scenario: Unable to update User/Association Status within Learner Association Group object when invalid association group uuid given
        Given A Learner Association Group exists and user has access to update User/Association Status
            When API request is sent to update User/Association status within Learner Association Group by providing invalid group uuid
                Then User/Association Status will not be updated and User management will throw a resource not found error

    Scenario: Unable to update User/Association Status within Learner Association Group object when invalid document id given in request payload
        Given A Learner Association Group exists and user has access privileges to update User/Association Status
            When API request is sent to update User/Association status within Learner Association Group by providing invalid document id
                Then User/Association Status will not be updated and User management will throw a Validation error

    Scenario: Unable to update User/Association Status within Learner Association Group object when invalid status given in request payload
        Given A Learner Association Group exists and user has privileges to update User/Association Status
            When API request is sent to update User/Association status within Learner Association Group by providing invalid status
                Then User/Association Status will not be updated and User management will return a Validation error

    @filter-api
    Scenario: Add instructor into the learning association group with correct request payload
        Given A user has permission to access user management, create correct request payload to add instructor and instructor is associated actively in discipline association group
            When API request sent to add instructor to the learning association group
                Then ensure the API response the instructor has been added

    Scenario: Add Instructor into learning association group with incorrect request payload
        Given A user has permission to access user management, create incorrect request payload to add instructor
            When API request sent to add instructor to the learning association group with incorrect payload
                Then ensure the API response failed to add instructor

    @filter-api
    Scenario: Add given instructor for curriculum pathway in learner association group when instructor is not associated to curriculum pathway in discipline association group
        Given A user has permission to access user management, create correct request payload to add instructor and instructor is not associated actively in discipline association group
            When API request sent to add instructor to the learner association group
                Then instructor will not get added and a ValidationError will be thrown

    @filter-api
    Scenario: Retrieve all active users associated to a valid instructor from all Learner Association Groups
        Given A user has access to User management and needs to fetch all users associated to a valid instructor from all Learner Association Groups
            When API request is sent to fetch all users associated to a valid active instructor
                Then User management will return a list of all active users associated to the instructor

    @filter-api
    Scenario: Retrieve all active users associated to a valid coach from all Learner Association Groups
        Given A user has access to User management and needs to fetch all users associated to a valid coach from all Learner Association Groups
            When API request is sent to fetch all users associated to a valid active coach
                Then User management will return a list of all active users associated to the coach

    Scenario: Unable to retrieve all active users associated to an invalid coach from all Learner Association Groups
        Given A user has access to User management and needs to fetch all users associated to an invalid coach from all Learner Association Groups
            When API request is sent to fetch all users associated to an invalid coach
                Then Users will not be returned and Resource not found error will be thrown by User management

    @filter-api
    Scenario: Remove instructor into the learning association group with correct request payload
        Given A user has permission to access user management, create correct request payload to remove instructor
            When API request sent to remove instructor to the learning association group
                Then ensure the API response the instructor has been removed

    Scenario: Remove Instructor into learning association group with incorrect request payload
        Given A user has permission to access user management, create incorrect request payload to remove instructor
            When API request sent to remove instructor to the learning association group with incorrect payload
                Then ensure the API response failed to remove instructor
    
    @filter-api
    Scenario: Add Instructor into learning association group with incorrect discipline_id in the payload
        Given A user had permission to access user management, create incorrect request payload to add instructor
            When API request sent to add instructor in the learning association group incorrect discipline_id in the payload
                Then validation error will thrown
