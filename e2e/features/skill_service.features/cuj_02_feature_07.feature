@skill-service
Feature: Compare similar skills
    
    @matching-engine
    Scenario: Fetch similar skills for a given skill
        Given That a user has the ability to compare skills via Skill Management
            When The mechanism to compare similar skills is applied within the management interface with correct request payload
                Then Skill Service will retrieve the relevant skills that are similar and serve that data back to the management interface

    Scenario: Fetch similar skills for a given skill if incorrect uuid is provided in request
        Given That a user can compare skills via Skill Management
            When The mechanism to compare similar skills is applied within the management interface with incorrect request payload
                Then Skill Service will throw error to the user
    
    Scenario: Fetch similar skills for a given if no uuid is provided in request
        Given That a user is able to compare skills via Skill Management
            When The mechanism to compare similar skills is applied within the management interface with no IDs in request payload
                Then Skill Service will throw validation error to the user

    Scenario: Successfully compute semantic similarity score between two valid skills
        Given That a user is able to compute semantic similarity between skills via Skill Management
            When The mechanism to compute semantic similarity score is applied within the management interface with valid skill IDs in request payload
                Then Skill Service will return a semantic similarity score between the two given skill objects

    Scenario: Unable to compute semantic similarity score if invalid skill id provided
        Given That a user can compute semantic similarity between skills via Skill Management
            When The mechanism to compute semantic similarity score is applied within the management interface with invalid skill IDs in request payload
                Then Skill Service will throw internal error to the user

    Scenario: Unable to compute semantic similarity score if only 1 skill id provided
        Given That a user has the ability to compute semantic similarity between skills via Skill Management
            When The mechanism to compute semantic similarity score is applied within the management interface with only 1 skill ID in request payload
                Then Skill Service will throw validation error to the user as only 1 skill provided