@inspace
Feature: To fetch Inspace token

    Scenario: Fetch inpsace token for extisting inspace user
        Given The inspace user already exists
            When API request is sent to fetch the inspace token
                Then The inspace token for existing user is returned

    Scenario: Fetch inpsace token for when inspace_user is false
        Given The inspace user does not exists
            When API request is sent to retrieve the inspace token
                Then Error in creating inpsace token message will be returned
