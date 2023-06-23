Feature: New User/Users is/are to be created
    Scenario: A user wants to be registered with correct account details
        Given A user has access to the application and submits correct form
            When A POST api call is made to the User Management Service with correct details
                Then The User is successfully created
                    And The respective Agent, Learner, Learner Profile are also created

    Scenario: A user wants to be registered with incorrect account details
        Given A user has access to the application and will submits incorrect form
            When A POST api call is made to the User Management Service with incorrect details
                Then User will not be created and appropriate error response will be sent

    Scenario: Multiple users are to be created
        Given A faculty/admin has access to the application
            When A POST api call is made to the User Management Service Bulk Import api with correct input json file
                Then The Users are successfully created
                    And The respective Agent, Learner, Learner Profile for each user are also created

    Scenario: Create User with incorrect firstname
        Given A User has access to the application and will submit form with incorrect firstname
            When Send API request to create User with incorrect request payload
                Then Failed to create User with incorrect firstname and appropriate error response will be sent

    Scenario: Create User with incorrect lastname
        Given A User has access to the application and will submit form with incorrect lastname
            When Send API request to create User with incorrect lastname request payload
                Then Failed to create User with incorrect lastname and appropriate error response will be sent

    Scenario: Create User with incorrect Email ID format
        Given A User has access to the application and will submit form with incorrect Email ID format
            When Send API request to create User with incorrect Email ID request payload
                Then Failed to create User with incorrect Email ID and appropriate error response will be sent

    Scenario: Create User of type Faculty
        Given A user has access to the application and submits correct form for user type faculty
            When A POST api call is made to the User Management Service with user type faculty
                Then The User should be successfully created
                    And The respective Staff and Agent will also be created