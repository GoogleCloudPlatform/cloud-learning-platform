@content-serving-api
Feature: User should be able to upload a learning content with sync api

  Scenario: User wants to upload a learning content file with sync api
    Given that an LXE or CD has access to the content authoring tool and wants to upload a learning content file with sync api
      When API request is sent to upload a learning content file with sync api
        Then LOS will return a json response with file and folder list of the uploaded file

  Scenario: User wants to upload a learning content zip with sync api
    Given that an LXE or CD has access to the content authoring tool and wants to upload a learning content zip with sync api
      When API request is sent to upload a learning content zip with sync api
        Then LOS will return a json response with file and folder list of the uploaded zip

  Scenario: User wants to upload a learning content with invalid content headers
    Given that an LXE or CD has access to the content authoring tool and wants to upload a learning content file with invalid content headers
      When API request is sent to upload a learning content file with invalid content headers
        Then LOS will return a validation error for invalid content headers

  Scenario: User wants to upload a learning content where content headers and file extension does not match
    Given that an LXE or CD has access to the content authoring tool and wants to upload a learning content file where content headers and file extension does not match
      When API request is sent to upload a learning content file where content headers and file extension does not match
        Then LOS will return a validation error for mismatched content headers and file extension
