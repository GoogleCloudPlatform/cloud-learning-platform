@publish-draft-mode
Feature: User should be able to get all versions of a learning content

  Scenario: User wants to get all versions of initial learning content
    Given that an LXE or CD has access to the content authoring tool and wants to get all versions of initial learning content
      When API request is sent to get all versions of initial learning content
        Then LOS will return a json response with list of learning resource documents including only initial learning content

  Scenario: User wants to get all versions in a generic case
    Given that an LXE or CD has access to the content authoring tool and wants to get all versions in a generic case
      When API request is sent to get all versions in a generic case
        Then LOS will return a json response with list of learning resource documents

  Scenario: User wants to get all versions for invalid learning resource
    Given that an LXE or CD has access to the content authoring tool and wants to get all versions for invalid learning resource
      When API request is sent to get all versions for invalid learning resource
        Then LOS will return a resource not found error for learning resource

  Scenario: User wants to get all versions in a generic case with status filter
    Given that an LXE or CD has access to the content authoring tool and wants to get all versions in a generic case with status filter
      When API request is sent to get all versions in a generic case with status filter
        Then LOS will return a json response with list of learning resource documents with status filter