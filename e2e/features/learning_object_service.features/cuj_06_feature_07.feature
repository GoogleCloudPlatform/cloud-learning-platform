@publish-draft-mode
Feature: User should be able to upload a learning content with async api

  Scenario: User wants to upload a learning content with async api
    Given that an LXE or CD has access to the content authoring tool and wants to upload a learning content zip with async api
      When API request is sent to upload a learning content zip with async api
        Then LOS will return a json response with file and folder list of the uploaded zip for async api

  Scenario: User wants to upload a learning content with invalid content headers with async api
    Given that an LXE or CD has access to the content authoring tool and wants to upload a learning content file with invalid content headers with async api
      When API request is sent to upload a learning content file with invalid content headers with async api
        Then LOS will return a validation error for invalid content headers for async api

  Scenario: User wants to upload a learning content where content headers and file extension does not match
    Given that an LXE or CD has access to the content authoring tool and wants to upload a learning content zip where content headers and file extension does not match
      When API request is sent to upload a learning content file where content headers and zip file extension does not match
        Then LOS will return a validation error for mismatched content headers and file extension for async api
