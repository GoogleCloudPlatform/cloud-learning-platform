Feature: Delete uploaded files during assessment authoring and submission

    Scenario: User wants to delete uploaded file during assessment authoring
        Given that valid user_id exists and files are successfully uploaded
            When API request is sent to delete a file from temp folder of the user
                Then the API will successfully delete the file from temp folder of the user

    Scenario: User wants to delete uploaded file during assessment authoring but invalid path is sent
        Given that valid user_id exists but the file to be deleted does not exist
            When API request is sent to delete a file from temp folder of the user with invalid path
                Then the API will return resource not found error for the file to be deleted from temp folder of the user
    
    Scenario: User wants to delete uploaded file during assessment subission
        Given that valid learner_id and assessment_id exists and files are successfully uploaded
            When API request is sent to delete a file from temp folder of the learner
                Then the API will successfully delete the file from temp folder of the learner

    Scenario: User wants to delete uploaded file during assessment subission but invalid path is sent
        Given that valid learner_id and assessment_id exists but the file to be deleted does not exist
            When API request is sent to delete a file from temp folder of the learner with invalid path
                Then the API will return resource not found error for the file to be deleted from temp folder of the learner
