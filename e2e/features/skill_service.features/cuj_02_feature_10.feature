@skill-service
Feature: Align knowledge nodes to skills

    Scenario: Update knowledge nodes that align with skills belonging to given source name on firestore by triggering batch job
        Given That a user has access to align and update knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills for given source name with aligned knowledge nodes by triggering a batch job is applied
                Then Skill Service will create a batch job to align and update relevant knowledge nodes to skills belonging to given source name

    Scenario: Update knowledge nodes that align with skills for given skill ids on firestore by triggering batch job
        Given That a user can access functionality to align and update knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills for given ids with aligned knowledge nodes by triggering a batch job is applied
                Then Skill Service will create a batch job to align and update relevant knowledge nodes to skills for given ids

    Scenario: Unable to align and update knowledge nodes to skills as both source name and skill ids are given
        Given That a user can align and update knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills with aligned knowledge nodes is applied by giving both source name and skill ids
                Then Skill Service will throw an internal error as both source name and skill ids were given and batch job will not be triggered

    Scenario: Unable to align and update knowledge nodes to skills as both source name and skill ids are missing
        Given That a user can update aligned knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills with aligned knowledge nodes is applied without giving both source name and skill ids
                Then Skill Service will throw an internal error as both source name and skill ids are missing and batch job will not be triggered

    Scenario: Unable to align and update knowledge nodes to skills when invalid source name is given
        Given That a user has access to update aligned knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills with aligned knowledge nodes is applied by providing an invalid source name
                Then Skill Service will throw an internal error as invalid source name was given and batch job will not be triggered

    Scenario: Unable to align and update knowledge nodes to skills when invalid skill id is given
        Given That a user has access to update knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills with aligned knowledge nodes is applied by providing an invalid skill id
                Then Skill Service will throw an internal error as invalid skill id was given and batch job will not be triggered

    Scenario: Unable to align and update knowledge nodes to skills when learning resource id key is missing
        Given That a user is privileged to update aligned knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills with aligned knowledge nodes is applied without providing learning resource id key
                Then Skill Service will throw an internal error as learning resource id key is missing and batch job will not be triggered

    Scenario: Unable to align and update knowledge nodes to skills when invalid learning resource id is given
        Given That a user is privileged to update knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills with aligned knowledge nodes is applied by providing invalid learning resource id
                Then Skill Service will throw an internal error as invalid learning resource id was given and batch job will not be triggered

    Scenario: Unable to align and update knowledge nodes to skills when invalid output alignment source key is given
        Given That a user can access functionality update aligned knowledge nodes to skills by triggering batch job via Skill Management
            When The mechanism to update skills with aligned knowledge nodes is applied with invalid output alignment source key
                Then the batch job will not get triggered and Skill Service will throw an internal error as invalid output alignment source key was given

    Scenario: Fetch knowledge nodes that align with given skill name and description
        Given That a user can align knowledge nodes to skill by query via Skill Management
            When The mechanism to align knowledge nodes to skills is applied with skill name & description
                Then Skill Service will align and return knowledge nodes that are relevant to the given skill name and description

    Scenario: Fetch knowledge nodes that align with given skill name only
        Given That a user is able to align knowledge nodes to skill by query via Skill Management
            When The mechanism to align knowledge nodes to skill is applied with skill name only
                Then Skill Service will align and return knowledge nodes that are relevant to the given skill name

    Scenario: Fetch knowledge nodes that align with given skill description only
        Given That a user is allowed to align knowledge nodes to skill by query via Skill Management
            When The mechanism to align knowledge nodes to skill is applied with skill description only
                Then Skill Service will align and return knowledge nodes that are relevant to the given skill description

    Scenario: Unable to align knowledge nodes to skill when both skill name and description are empty strings
        Given That a user has the ability to align knowledge nodes to skill by query via Skill Management
            When The mechanism to align knowledge nodes to skill is applied when both skill name and description is missing
                Then Skill Service will throw an internal error while aligning knowledge nodes as both name and description are empty strings

    Scenario: Unable to align knowledge nodes to skill when invalid learning resource id is given
        Given That a user has access to align knowledge nodes to skill by query via Skill Management
            When The mechanism to align knowledge nodes to skill is applied by providing invalid learning resource id
                Then Skill Service will throw an internal error while aligning knowledge nodes as invalid learning resource id was given

    Scenario: Fetch knowledge nodes that align to skill by id for given skill id
        Given That a user can align knowledge nodes to skill by id via Skill Management
            When The mechanism to align knowledge nodes to skills is applied with correct request payload
                Then Skill Service will align and return knowledge nodes that are relevant to the skill corresponding given skill id

    Scenario: Unable to align knowledge nodes to skill by id when invalid skill id is given
        Given That a user has access to align knowledge nodes to skill by id via Skill Management
            When The mechanism to align knowledge nodes to skill by id is applied by providing invalid skill id
                Then Skill Service will throw an internal error while aligning knowledge nodes as invalid skill id was given

    Scenario: Unable to align knowledge nodes to skill by id when invalid output alignment source is given
        Given That a user has the ability to align knowledge nodes to skill by id via Skill Management
            When The mechanism to align knowledge nodes to skill by id is applied by providing invalid output alignment source
                Then Skill Service will throw an internal error while aligning knowledge nodes as invalid output alignment source was given

    Scenario: Unable to align knowledge nodes to skill by id when learning resource id is missing
        Given That a user has the access to align knowledge nodes to skill by id via Skill Management
            When The mechanism to align knowledge nodes to skill by id is applied with missing learning resource id
                Then Skill Service will throw an internal error while aligning knowledge nodes as learning resource id was missing

    Scenario: Unable to align knowledge nodes to skill by id when invalid learning resource id is given
        Given That a user is allowed to align knowledge nodes to skill by id via Skill Management
            When The mechanism to align knowledge nodes to skill by id is applied by providing invalid learning resource id
                Then Skill Service will throw an internal error while aligning knowledge nodes by id as invalid learning resource id was given

    Scenario: Unable to align knowledge nodes to skill by id when given value of learning resource id is asterisk
        Given That a user has privileges to align knowledge nodes to skill by id via Skill Management
            When The mechanism to align knowledge nodes to skill by id is applied by providing asterisk as value for learning resource id
                Then Skill Service will throw an internal error while aligning knowledge nodes as asterisk was given as value for learning resource id
