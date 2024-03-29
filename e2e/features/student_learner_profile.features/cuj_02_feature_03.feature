@filter-api
Feature: Filter achievement data, learner account data, and learner profile data based on various Student Learner Profile attributes

    Scenario: Administrator wants to get learner profiles based on correct filter payloads
        Given Administrator has access to SLP service with the correct filter payloads
            When Administrator wants to filter learner profiles based on correct filter payloads
                Then the relevant learner profiles are retrieved as per the correct filters
    
    Scenario: Administrator wants to get learner profiles based on correct filter payloads for more than one list filters
        Given Administrator has access to SLP service with the correct filter payloads for more than one list filters
            When Administrator wants to filter learner profiles based on correct filter payloads for more than one list filters
                Then the administrator gets the right error message
    
    Scenario: Administrator wants to get learner specific achievements based on correct filter payloads
        Given Administrator has access to SLP service with the correct learner specific achievements filter payloads
            When Administrator wants to filter learner specific achievements based on correct filter payloads
                Then the relevant learner specific achievements are retrieved as per the correct filters
    
    Scenario: Administrator wants to get learner specific achievements based on incorrect learner id
        Given Administrator has access to SLP service with the incorrect learner id
            When Administrator wants to filter learner specific achievements based on incorrect learner id
                Then the relevant learner specific achievements are retrieved as per the incorrect learner id
    
    Scenario: Administrator wants to get achievements based on correct filter payloads
        Given Administrator has access to SLP service with the correct achievements filter payloads
            When Administrator wants to filter achievements based on correct filter payloads
                Then the relevant achievements are retrieved as per the correct filters
    
    Scenario: Administrator wants to get achievements based on incorrect achievements filter payloads
        Given Administrator has access to SLP service with the incorrect achievements filter payloads
            When Administrator wants to filter achievements based on incorrect achievements filter payloads
                Then the relevant achievements are retrieved as per the incorrect achievements filter payloads
    
    Scenario: Administrator wants to get Goals based on correct filter payloads
        Given Administrator has access to SLP service with the correct Goals filter payloads
            When Administrator wants to filter Goals based on correct filter payloads
                Then the relevant Goals are retrieved as per the correct filters
    
    Scenario: Administrator wants to get Goals based on incorrect filter payloads
        Given Administrator has access to SLP service with the incorrect Goals filter payloads
            When Administrator wants to filter Goals based on incorrect filter payloads
                Then the user gets no retreived Goal
    
    Scenario: Administrator wants to get archived Learner with correct request payload
        Given There is an archived Learner in database 
            When Administrator fetches the archived Learner with correct request payload
                Then the relevant Learner is retrieved
    
    Scenario: Administrator wants to get un-archived Learner with correct request payload
        Given There is an un-archived Learner in database 
            When Administrator fetches the un-archived Learner with correct request payload
                Then the relevant Learners are retrieved
    
    Scenario: Administrator wants to get archived and un-archived Learner with correct request payload
        Given There is an archived and an un-archived Learner in database
            When Administrator fetches the Learner with correct request payload
                Then the relevant Learner(s) are retrieved

    Scenario: Administrator wants to get archived Learner Profile with correct request payload
        Given There is an archived Learner Profile in database 
            When Administrator fetches the archived Learner Profile with correct request payload
                Then the relevant Learner Profile is retrieved

    Scenario: Administrator wants to get un-archived Learner Profile with correct request payload
        Given There is an un-archived Learner Profile in database
            When Administrator fetches the un-archived Learner Profile with correct request payload
                Then the relevant Learner Profiles are retrieved
    
    Scenario: Administrator wants to get archived Achievement with correct request payload
        Given There is an archived Achievement in database 
            When Administrator fetches the archived Achievement with correct request payload
                Then the relevant Achievement is retrieved
    
    Scenario: Administrator wants to get un-archived Achievement with correct request payload
        Given There is an un-archived Achievement in database 
            When Administrator fetches the un-archived Achievement with correct request payload
                Then the relevant Achievements are retrieved

    Scenario: Administrator wants to get archived and un-archived Achievement with correct request payload
        Given There is an archived and an un-archived Achievement in database 
            When Administrator fetches the Achievement with correct request payload
                Then the relevant Achievement(s) are retrieved
    
    Scenario: Administrator wants to get archived Goal with correct request payload
        Given There is an archived Goal in database 
            When Administrator fetches the archived Goal with correct request payload
                Then the relevant Goal is retrieved
    
    Scenario: Administrator wants to get un-archived Goal with correct request payload
        Given There is an un-archived Goal in database 
            When Administrator fetches the un-archived Goal with correct request payload
                Then the relevant Goals are retrieved

    Scenario: Administrator wants to get archived and un-archived Goal with correct request payload
        Given There is an archived and an un-archived Goal in database 
            When Administrator fetches the Goal with correct request payload
                Then the relevant Goal(s) are retrieved