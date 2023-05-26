Feature: Search achievement, goal, learner account and learner profile data based on various Student Learner Profile attributes

    Scenario: Administrator wants to search for learner based on correct first name
        Given Administrator has access to SLP service to search learner by first name
            When Administrator wants to search learner based on correct first name
                Then the relevant learner corresponding to given first name is retrieved and returned to user
    
    Scenario: Administrator wants to search for learner based on incorrect first name
        Given Administrator has privilege to access SLP service to search learner by first name
            When Administrator wants to search learner based on incorrect first name
                Then SLP service will return empty response as no learner exists for given incorrect first name

    Scenario: Administrator wants to search for learner based on correct email address
        Given Administrator has access to SLP service to search learner by email address
            When Administrator wants to search learner based on correct email address
                Then the relevant learner corresponding to given email address is retrieved and returned to user

    Scenario: Administrator wants to search for learner based on incorrect email address format
        Given Administrator has access to SLP service to search learner by incorrect email address format
            When Administrator wants to search learner based on incorrect email address format
                Then getting error response learner email invalid
    
    Scenario: Administrator wants to search for learner based on incorrect email address
        Given Administrator has privilege to access SLP service to search learner by email address
            When Administrator wants to search learner based on incorrect email address
                Then SLP service will return empty response as no learner exists for given incorrect email address

    Scenario: Administrator wants to search for goal by providing correct goal name
        Given Administrator has access to SLP service to search goal by goal name
            When Administrator wants to search goal based on correct goal name
                Then the relevant goal corresponding to given goal name is retrieved and returned to user
    
    Scenario: Administrator wants to search for goal by providing an incorrect goal name
        Given Administrator has privilege to access SLP service to search goal by goal name
            When Administrator wants to search goal by providing an incorrect goal name
                Then SLP service will return empty response as no goal exists for given incorrect goal name

    Scenario: Administrator wants to search for achievements by providing achievement type
        Given Administrator has access to SLP service to search achievements by achievement type
            When Administrator wants to search achievements based on correct achievement type
                Then the relevant achievements corresponding to given achievement type is retrieved and returned to user

    Scenario: Administrator wants to search for learner profile by providing correct learner_id
        Given Administrator has access to SLP service to search learner profile by learner_id
            When Administrator wants to search learner profile based on correct learner_id
                Then the relevant learner profile corresponding to given learner_id is retrieved and returned to user
    
    Scenario: Administrator wants to search for learner profile by providing an incorrect learner_id
        Given Administrator has privilege to access SLP service to search learner profile by learner_id
            When Administrator wants to search learner profile by providing an incorrect learner_id
                Then SLP service will return empty response as no learner profile exists for given incorrect learner_id