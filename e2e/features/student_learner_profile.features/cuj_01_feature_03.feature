Feature: Learner achievements are updated as the user progresses through a learning pathway

    Scenario: Learner completes an Achievement and fetches with correct payload
        Given The learner completes competencies/credits and/or credentials (i.e.: 'achievements' associated with a learning pathway) as they progress through a learning pathway
            When Achievements are completed
                Then Achievement is logged in SLP so that the learner can view an up-to-date record of their achievements through the learner-facing profile interface

    Scenario: Learner completes an Achievement and tries updating incorrect achievement in learner profile
        Given The learner completes competencies/credits and/or credentials (i.e.: 'achievements' associated with a learning pathway) as they progress through a learning pathway (negative)
            When Achievements are completed and incorrect achievement is tried to be updated in learner profile
            Then SLP will throw a resource not found error as incorrect achievement was given
    
    @filter-api
    Scenario: Learner can view all achievements associated for a Program along with the status
        Given The learner with an existing learner profile enrolled into a valid curriculum pathway program 
            When Learner fetches achievements for a valid program
            Then SLP will return all achievements for the program along with the status of learner for each achievement
    
    Scenario: Learner cannot view achievements associated for an invalid Program
       Given The learner with valid learner profile try to fetch learner achievements for an invalid Program
            When learner fetches achievements for an invalid program
            Then SLP will throw a resource not found error as incorrect program curriculum pathway was given