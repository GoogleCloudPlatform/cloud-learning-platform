@assessment
Feature: Upload File for Assessment Submission

    Scenario: Learner wants to upload a single file for assessment submission
        Given that valid learner and assessment exists
            When API request is sent to upload a file for assessment submission
                Then the API will upload file to learner-id/assessment-id/temp folder on GCS
    
    Scenario: Learner wants to reupload a file with same name for assessment submission
        Given that valid learner and assessment exists and file is already uploaded
            When API request is sent to reupload a file for assessment submission
                Then the API will respond with validation error for already existing file with same name for same assessment

    Scenario: Learner wants to upload a file for assessment submission with invalid assessment_id
        Given that learner_id is valid but assessment_id is invalid
            When API request is sent to upload a file for assessment submission with invalid assessment_id
                Then the API will respond with validation error for invalid assessment_id
    
    Scenario: Learner wants to upload a file for assessment submission with invalid learner_id
        Given that learner_id is invalid but assessment_id is valid
            When API request is sent to upload a file for assessment submission with invalid learner_id
                Then the API will respond with validation error for invalid learner_id
    
    Scenario: Learner wants to upload a file for assessment submission with current attempt greater than max attempt
        Given that valid learner,learner profile and assessment exists
            When API request is sent to upload a file for assessment submission with current attempt greater than max attempt
                Then the API will respond with validation error for  current attempt greater than max attempt
