@skill-service
Feature: Align curriculum to skills
    
    @matching-engine
    Scenario: Fetch skills that align with curriculum name and description
        Given That a user can to align skills to curriculum via Skill Management
            When The mechanism to align skills to curriculum is applied with correct request payload with curriculum name & description
                Then Skill Service will align and return skills that are relevant to the given curriculum name and description

    @matching-engine
    Scenario: Fetch skills that align with curriculum name only
        Given That a user is able to align skills to curriculum via Skill Management
            When The mechanism to align skills to curriculum is applied with correct request payload with curriculum name only
                Then Skill Service will align and return skills that are relevant to the given curriculum name

    @matching-engine
    Scenario: Fetch skills that align with curriculum description only
        Given That a user is allowed to align skills to curriculum via Skill Management
            When The mechanism to align skills to curriculum is applied with correct request payload with curriculum description only
                Then Skill Service will align and return skills that are relevant to the given curriculum description

    Scenario: Unable to fetch skills that align with curriculum when both curriculum name and description are empty strings
        Given That a user has the ability to align skills to curriculum via Skill Management
            When The mechanism to align skills to curriculum is applied with incorrect request payload with missing curriculum name and description
                Then Skill Service will throw a validation error to the user as both name and description should not be empty

    Scenario: Unable to fetch skills that align with curriculum when invalid skill alignment source is given
        Given That a user has acess to align skills to curriculum via Skill Management
            When The mechanism to align skills to curriculum is applied with invalid skill alignment source
                Then Skill Service will throw an internal error to the user as no embeddings exist for given invalid skill alignment source
