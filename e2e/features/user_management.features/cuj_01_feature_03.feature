Feature: User information is to be updated/deleted
    Scenario: User information is to be updated 
        Given User which needs to be updated already exists in the database
            When The PUT api call is to be made with the correct uuid and fields
                Then The User data is successfully updated

    Scenario: Name of User of type learner is to be updated
        Given User of type learner which needs to be updated already exists in the database
            When The UPDATE api call is made with the correct uuid and fields
                Then The user, learner and agent name is successfully updated

    Scenario: User of staff type is to be deleted
        Given User of staff type which needs to be deleted already exists in the database
            When The DELETE api call is made with the correct uuid and fields
                Then The User and the Staff data is successfully deleted
    
    Scenario: User of type learner is to be deleted
        Given User of type learner needs to be deleted already exists in the database
            When The DELETE api call is to be made with the correct user uuid of type learner and fields
                Then The User data along with Agent, learner, learner profile data gets successfully deleted
