Feature: Adding users to the discipline association group

    Scenario: add the user into the discipline association group with the correct request payload
        Given discipline association group already exist
            When an API request sent to add the user into the discipline association group with the correct request payload
                Then the corresponding discipline association group object will be updated and also contain the list of user
    
    Scenario: unable to add the user into the discipline association group with the incorrect request payload
        Given discipline association group already exists
            When an API request sent to add the user into the discipline association group with an incorrect request payload
                Then a validation error will thrown
    
    Scenario: unable to add duplicate user into the discipline association group
        Given discipline association group already exists with a user added
            When an API request sent to add the same existing user into the discipline association group
                Then a validation error will be thrown

    Scenario: remove the user from the discipline association group with the correct request payload
        Given discipline association group is an already exist
            When an API request sent to remove the user from the discipline association group with the correct request payload
                Then the user will remove from the corresponding discipline association group object

    Scenario: remove the user of instructor type from the discipline association group with the correct request payload
        Given discipline association group already exists with a user of instructor type and discipline
            When an API request sent to remove the user of instructor type from the discipline association group with correct request payload
                Then the user of instructor type will get removed from the corresponding discipline association group object
                    And the instructor will also get removed from the Learner Association Group where it exists

    Scenario: unable to remove the user from the discipline association group with the incorrect request payload
        Given discipline association group is already been exist
            When an API request sent to remove the user from the discipline association group with the incorrect request payload
                Then a validations error is thrown
