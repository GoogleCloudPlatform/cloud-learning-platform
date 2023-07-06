Feature: CRUD for managing SubmittedAssessment model in Assessment services

    Scenario: Create a Submitted Assessment for existing learner and assessment with correct request payload
        Given that an existing student needs to answer an existing assessment
            When API request is sent to create a Submitted Assessment with correct request payload
                Then that Submitted Assessment object will be created in the database

    Scenario: Create a Submitted Assessment for nonexistent learner and assessment with correct request payload
        Given that a nonexistent student needs to answer a non-existent assessment
            When API request is sent to create Submitted Assessment with correct request payload
                Then that Submitted Assessment object will not be created and Assessment Service will throw a ResourceNotFound error

    Scenario: Create a Submitted Assessment for existing learner and assessment with incorrect request payload
        Given that an existing student wants to answer an existing assessment
            When API request is sent to create a Submitted Assessment with incorrect request payload
                Then that Submitted Assessment object will not be created and Assessment Service will throw a Validation error

    Scenario: Fetch all the Submitted Assessments for an existing learner and assessment
        Given that an assessor has access to Assessment Service and need to fetch all the Submitted Assessments for an existing learner and assessment
            When API request is sent to fetch all the Submitted Assessments with correct submitted assessment id
                Then all the Submitted Assessment objects for a learner for an assessment will be fetched

    Scenario: Fetch all the Submitted Assessments for a non-existent learner and assessment
        Given that an assessor has access to Assessment Service and need to fetch all the Submitted Assessments for a non-existent learner and assessment
            When API request is sent to fetch all the Submitted Assessments with incorrect submitted assessment id
                Then all the Submitted Assessment objects will not be fetched and Assessment Service will throw a ResourceNotFound error

    Scenario: Fetch the last Submitted Assessment for an existing learner and assessment
        Given that an assessor has access to Assessment Service and need to fetch the last Submitted Assessment for an existing learner and assessment
            When API request is sent to fetch the Submitted Assessment with correct submitted assessment id
                Then the last Submitted Assessment object for a learner for an assessment will be fetched

    Scenario: Fetch the last Submitted Assessment for a non-existent learner and assessment
        Given that an assessor has access to Assessment Service and need to fetch a Submitted Assessment for a non-existent learner and assessment
            When API request is sent to fetch the Submitted Assessment with incorrect submitted assessment id
                Then the last Submitted Assessment object will not be fetched and Assessment Service will throw a ResourceNotFound error

    Scenario: Fetch a particular Submitted Assessment with correct id
        Given that an assessor has access to Assessment Service and want to fetch a Submitted Assessment
            When API request is sent to fetch the Submitted Assessment with correct id
                Then the Submitted Assessment object will be fetched

    Scenario: Fetch a particular Submitted Assessment with incorrect id
        Given that an assessor has access to Assessment Service and need to fetch a Submitted Assessment
            When API request is sent to fetch the Submitted Assessment with incorrect id
                Then the Submitted Assessment object will not be fetched and Assessment Service will throw a ResourceNotFound error

    Scenario: Update a particular Submitted Assessment with correct id
        Given that an assessor has access to Assessment Service and wants to update a Submitted Assessment
            When API request is sent to update the Submitted Assessment with correct id
                Then the Submitted Assessment object will be updated in the database

    Scenario: Update a particular Submitted Assessment with incorrect id
        Given that an assessor has access to Assessment Service and need to update a Submitted Assessment
            When API request is sent to update the Submitted Assessment with incorrect id
                Then the Submitted Assessment object will not be updated and Assessment Service will throw a ResourceNotFound error

    Scenario: Delete a particular Submitted Assessment with correct id
        Given that an assessor has access to Assessment Service and want to delete a Submitted Assessment
            When API request is sent to delete the Submitted Assessment with correct id
                Then the Submitted Assessment object will be deleted from the database

    Scenario: Delete a particular Submitted Assessment with incorrect id
        Given that an assessor has access to Assessment Service and need to delete a Submitted Assessment
            When API request is sent to delete the Submitted Assessment with incorrect id
                Then the Submitted Assessment object will not be deleted and Assessment Service will throw a ResourceNotFound error
    
    Scenario: Assigning the assessor id while ceating a Submitted Assessment for existing learner and assessment
        Given that an existing student needs to answer existing assessment
            When API request is sent to create a Submitted Assessment with correct request payload. Assessor will automatically get added from the list of available assessor using round robin algorithm
                Then that Submitted Assessment object having assessor id will be created
