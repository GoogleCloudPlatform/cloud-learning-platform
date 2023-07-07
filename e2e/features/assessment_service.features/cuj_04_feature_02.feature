Feature: Upload File for Assessment Authoring

    Scenario: LXE wants to upload a single file for assessment authoring
        Given that valid user_id exists
            When API request is sent to upload a file for assessment authoring
                Then the API will upload file to user-id/temp folder on GCS
    
    Scenario: LXE wants to reupload a file with same name for assessment authoring
        Given that valid user_id exists and file is already uploaded
            When API request is sent to reupload a file for assessment authoring
                Then the API will respond with validation error for already existing file with same name

    Scenario: LXE wants to upload a file for assessment authoring with invalid user_id
        Given that user_id is invalid
            When API request is sent to upload a file for assessment authoring with invalid user_id
                Then the API will respond with validation error for invalid user_id
