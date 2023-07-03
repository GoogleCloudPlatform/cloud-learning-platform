Feature: For the given learner get the curriculum pathway

    Scenario: Get the curriculum pathway for a learner with correct uuid
        Given learner was already created, this learner should be present in the learner association group and curriculum pathway is also exists in the database
            When an API request sent to get the pathway for the given learner with correct uuid
               Then the pathway detail correctly fetched

    @filter-api
    Scenario: Get the curriculum pathway for learner with correct uuid
        """ Filtering this scenario as pathway will always exist in the
            database when E2E tests are running
        """
        Given learner was already created, this learner should be present in the learner association group and curriculum pathway is not exist in the database
            When an API request is sent to get the pathway for the given learner with correct uuid
               Then error response returned
    

    Scenario: Get the curriculum pathway for the learner with correct uuid
        Given learner was already created, this learner is not be present in any of the learner association group and curriculum pathway is not exist in the database
            When an API request is sent to get pathway for the given learner with correct uuid
               Then error response is returned

    
    Scenario: Get the curriculum pathway for a learner with incorrect uuid
        Given learner is already created, this learner should be present in the learner association group
            When an API request sent to get pathway for the given learner with incorrect uuid
               Then error response is return
    
