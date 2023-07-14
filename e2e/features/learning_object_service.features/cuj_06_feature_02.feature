@publish-draft-mode
Feature: User should be able to link uploaded content with a learning resource

  Scenario: User wants to link an existing file with a valid learning resource
    Given that an LXE or CD has access to the content authoring tool and wants to link an existing file with a valid learning resource
      When API request is sent to link the content with learning resource
        Then LOS will return a json response with signed URl for preview of linked content from learning resource

  Scenario: User wants to link an existing file with invalid learning resource
    Given that an LXE or CD has access to the content authoring tool and wants to link an existing file with invalid learning resource
      When API request is sent to link the content with invalid learning resource
        Then LOS will return a resource is not found error response for invalid learning resource uuid for linking content

  Scenario: User wants to link a nonexisting file with learning resource
    Given that an LXE or CD has access to the content authoring tool and wants to link a non existing file with learning resource
      When API request is sent to link the non existent content with a learning resource
        Then LOS will return a resource is not found error response for nonexisting file
