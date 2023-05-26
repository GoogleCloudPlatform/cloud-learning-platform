Feature: Faculty should be able to archive/un-archive a Learner.

    Scenario: Faculty wants to archive a Learner.
        Given A Learner is present with Learner Profile and Achievements.
            When Faculty archives the Learner with correct payload.
                Then Learner gets archived
                And Learner Profile associated with Learner gets archived

    Scenario: Faculty wants to un-archive a Learner
       Given An archived Learner is present with Learner Profile and Achievements.
            When Faculty un-archives the Learner with correct payload.
                Then Learner gets un-archived
                And Learner Profile associated with Learner gets un-archived