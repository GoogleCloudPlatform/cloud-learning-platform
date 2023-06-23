Feature: Relationship between User and Group

    Scenario: Add new user to the group within User management
        Given A user has privilege to create a user and wants to assign Group to the new user during creation
            When A API request to create user is sent to User management
                Then the new user is successfully created by user management 
                    Then the new user is added to the assigned groups

    Scenario: Update groups of a existing user within User management
        Given A user has privilege to update a user and wants to update groups of a user
            When A API request to update user is sent to User management
                Then the groups of the user are successfully updated 
                    Then the user is added to the assigned groups and removed from the unassiged groups

    Scenario: Update Group documents when a user is deleted
        Given A user has privilege to delete a user and wants to delete a user
            When A API request to delete a user is sent to User management 
                Then the user is successfully deleted by the user management
                    Then the user should be removed from all the assigned groups

    Scenario: Update the status of a user to inactive
        Given A Admin wants deactivate a user 
            When A API request to deactivate a user is sent to User management
                Then the user should be deactivated 
                    Then the user should be removed from all the groups 
