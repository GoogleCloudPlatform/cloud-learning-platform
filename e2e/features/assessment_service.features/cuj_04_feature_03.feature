Feature: Generate Signed URL for Assessment Content

    Scenario: LXE wants to generate signed URL for assessment contents
        Given that valid assessment_id and resource paths exists
            When API request is sent to generate signed urls for assessment contents
                Then the API will return list of signed urls for assessment contents
    
    Scenario: LXE wants to generate signed URL for submitted assessment contents
        Given that valid submitted_assessment_id and resource paths exists
            When API request is sent to generate signed urls for submitted assessment contents
                Then the API will return list of signed urls for submitted assessment contents

    Scenario: LXE wants to generate signed URL for assessment contents with invalid assessment_id
        Given that valid assessment_id does not exists
            When API request is sent to generate signed urls for assessment contents with invalid assessment_id
                Then the API will return resource not found error for invalid assessment_id
    
    Scenario: LXE wants to generate signed URL for submitted assessment contents with invalid submitted_assessment_id
        Given that valid submitted_assessment_id does not exists
            When API request is sent to generate signed urls for submitted assessment contents with invalid submitted_assessment_id
                Then the API will return resource not found error for invalid submitted_assessment_id

    Scenario: LXE wants to generate signed URL for few missing assessment contents
        Given that valid assessment_id exists but some resource paths does not exist
            When API request is sent to generate signed urls for few missing assessment contents
                Then the API will return success response with list of signed urls with resource_not_found error message for few missing contents
    
    Scenario: LXE wants to generate signed URL for invalid assessment contents
        Given that valid assessment_id exists but resource paths does not exist
            When API request is sent to generate signed urls for invalid assessment contents
                Then the API will return failure response with list of signed urls with resource_not_found error message for all contents
