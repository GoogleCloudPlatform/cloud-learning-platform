Feature: Learner can view updated personal information.

    Scenario: Learner wants to view updated personal information.
        Given Learner changed their personal infomation in the account.
            When Learner view their learner-facing profile interface.
                Then the current information that is logged in the SLP is visible after it has been updated.

    Scenario: Learner cannot update non-editable personal information
       Given Learner tries to update non-editable personal information
            When the request is sent to SLP
                Then SLP should return error message saying personal non-editable information cannot be updated.