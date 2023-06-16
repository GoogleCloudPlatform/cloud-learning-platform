Feature: Managing Immutable UserGroups in user management

    Scenario: Update name of a Immutable UserGroup with correct request payload
        Given A user has permission to user management and wants to update name of a Immutable UserGroup
            When API request is sent to update Immutable UserGroup with correct request payload
                Then UserGroup document will not be updated and user management service will throw a validation error

    Scenario: Add users to a Immutable UserGroup within User management
        Given A user has access to User management and needs to add users with comaptible user_type to a immutable UserGroup
            When API request is sent to add users with type learner to a immutable UserGroup with name learner
                Then The users are successfully added to the learner UserGroup

    Scenario: Add users with incompatible user_type to a Immutable UserGroup within User management
        Given A user has access to User management and needs to add users with incompatible user_type to a immutable UserGroup
            When API request is sent to add users with user_type instructor to a immutable UserGroup with name learner
                Then The users will not be added to UserGroup user management service will throw validation error

    Scenario: A Immutable UserGroup cannot be deleted
        Given A user has access privileges to User management and wants to delete a immutable UserGroup
            When API request is sent to delete UserGroup whose is_immutable field is true by providing uuid
                Then UserGroup object will not be deleted and User management will throw a Validation error