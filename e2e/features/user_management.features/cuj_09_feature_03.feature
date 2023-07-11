Feature: Adding users and coaches to the learner association group

    Scenario: add the user into the learner association group with the correct request payload
        Given learner association group already exist
            When an API request sent to add the user into the learner association group with the correct request payload
                Then the corresponding learner association group object will be updated and also contain the list of user
    
    Scenario: unable to add the user into the learner association group with the incorrect request payload
        Given learner association group already exists
            When an API request sent to add the user into the learner association group with an incorrect request payload
                Then a validation error thrown

    Scenario: remove the user from the learner association group with the correct request payload
        Given learner association group is an already exist
            When an API request sent to remove the user from the learner association group with the correct request payload
                Then the user will remove from the corresponding learner association group object

    Scenario: unable to remove user from learner association group when user does not exist in learner association group
        Given learner association group already exists with no users added
            When an API request sent to remove a user that does not exist in the learner association group
                Then a ValidationError stating that the user does not exist in Learner association group will be thrown

    Scenario: add coach into the learner association group with the correct request payload
        Given learner association group already exist of type learner
            When a API request sent to add the coach into the learner association group with the correct request payload
                Then the corresponding learner association group object will be updated and also contain the list of coach
    
    Scenario: unable to add coach into the learner association group with the incorrect request payload
        Given learner association group already exists of type learner
            When an API request sent to add the coach into the learner association group with the incorrect request payload
                Then validation error is thrown
    
    Scenario: remove the coach from the learner association group with the correct request payload
        Given learner association group is already existing
            When an API request sent to remove the coach from the learner association group with the correct request payload
                Then the coach will remove from the corresponding learner association group object

    Scenario: unable to remove coach from learner association group when coach does not exist in learner association group
        Given learner association group already exists with no coaches added
            When an API request sent to remove the coach that does not exist in the learner association group
                Then a ValidationError stating that the coach does not exist in Learner association group will be thrown
