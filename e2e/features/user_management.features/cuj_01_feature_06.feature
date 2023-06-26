Feature: User Deactivation flow

    Scenario: Learner is removed from Learner Association Group when deactivated
        Given A learner is part of a learner association group
            When A API request is sent to deactivate the learner
                Then the learner is removed from learner association group

    Scenario: Coach is removed from Learner Association Group when deactivated
        Given A coach is part of a learner association group
            When A API request is sent to deactivate the coach
                Then the coach is removed from learner association group

    Scenario: Assessor is removed from Discipline Association Group when deactivated
        Given A assessor is part of a discipline association group
            When A API request is sent to deactivate the assessor
                Then the assessor is removed from discipline association group

    Scenario: Instructor is removed from Learner Association Group and Discipline Association Group when deactivated
        Given An instructor is part of a learner association group and discipline association group
            When A API request is sent to deactivate the instructor
                Then the instructor is removed from learner association group and discipline association group
