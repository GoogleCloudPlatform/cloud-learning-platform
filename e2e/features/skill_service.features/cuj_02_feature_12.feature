@skill-service
Feature: Align roles to skills
    
    @matching-engine
    Scenario: Fetch skills that align with role name and description
        Given That a user can align skills to role via Skill Management
            When The mechanism to align skills to role is applied with correct request payload with role name & description
                Then Skill Service will align and return skills that are relevant to the given role name and description

    @matching-engine
    Scenario: Fetch skills that align with role name only
        Given That a user is able to align skills to role via Skill Management
            When The mechanism to align skills to role is applied with correct request payload with role name only
                Then Skill Service will align and return skills that are relevant to the given role name

    @matching-engine
    Scenario: Fetch skills that align with role description only
        Given That a user is allowed to align skills to role via Skill Management
            When The mechanism to align skills to role is applied with correct request payload with role description only
                Then Skill Service will align and return skills that are relevant to the given role description

    Scenario: Unable to fetch skills that align with role when both role name and description are empty strings
        Given That a user has the ability to align skills to role via Skill Management
            When The mechanism to align skills to role is applied with incorrect request payload with missing role name and description
                Then Skill Service will throw an internal error to the user while trying to align roles to skills

    Scenario: Unable to fetch skills that align with role when invalid skill alignment source is given
        Given That a user has acess to align skills to role via Skill Management
            When The mechanism to align skills to role is applied with invalid skill alignment source
                Then Skill Service will throw a validation error to the user while trying to align roles to skills

    @matching-engine
    Scenario: Fetch skills that align with roles for given role ID
        Given That a user can align skills to role by given role id via Skill Management
            When The mechanism to align skills to role by id is applied with correct request payload (a valid role ID)
                Then Skill Service will align and return skills that are relevant to the role corresponding to given role ID

    Scenario: Unable to fetch skills that align with roles by ID when invalid role ID is given
        Given That a user has access to align skills to role by given role id via Skill Management
            When The mechanism to align skills to role by id is applied with incorrect request payload (invalid role ID)
                Then Skill Service will throw an internal error to the user while trying to align roles to skills by ID

    Scenario: Unable to fetch skills that align with roles by ID when invalid skill alignment source is given
        Given That a user has privileges to align skills to role by given role id via Skill Management
            When The mechanism to align skills to role by id is applied with incorrect request payload (invalid skill alignment source)
                Then Skill Service will throw an internal error to the user while aligning roles to skills by ID

    @matching-engine
    Scenario: Update skills that align with roles for given role ID on firestore by triggering batch job with correct request payload
        Given That a user can update aligned skills to role for given role id by triggering batch job via Skill Management
            When The mechanism to update aligned skills to role by triggering a batch job is applied with correct request payload
                Then Skill Service will create a batch job to align and update skills that are relevant to the role

    @matching-engine
    Scenario: Update skills that align with roles for given role ID on firestore by triggering batch job with missing source name field in request payload
        Given That a user can update aligned skills to role for given role id in request body with missing source name field via Skill Management
            When The mechanism to update aligned skills to role by triggering a batch job is applied with missing source name field
                Then Skill Service will create a batch job to align and update skills from all sources that are relevant to the role

    Scenario: Unable to update skills that align with roles for given role ID on firestore by triggering batch job when invalid role ID given
        Given That a user can update aligned skills to role for given role id in request body with invalid role ID via Skill Management
            When The mechanism to update aligned skills to role by triggering a batch job is applied with invalid role ID
                Then the batch job triggered by Skill Service will fail as role ID given is invalid