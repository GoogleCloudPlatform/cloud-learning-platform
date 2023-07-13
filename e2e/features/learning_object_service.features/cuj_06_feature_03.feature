@publish-draft-mode
Feature: User should be able to publish a learning content version

  Scenario: User wants to publish a valid initial learning content version
    Given that an LXE or CD has access to the content authoring tool and wants to publish a valid initial learning content version
      When API request is sent to publish a valid initial learning content version
        Then LOS will return a json response with signed URl for preview of published content and published initial content uuid

  Scenario: User wants to publish a valid learning content version
    Given that an LXE or CD has access to the content authoring tool and wants to publish a valid learning content version
      When API request is sent to publish a valid learning content version
        Then LOS will return a json response with signed URl for preview of published content and published content uuid


  Scenario: User wants to republish a valid learning content version
    Given that an LXE or CD has access to the content authoring tool and wants to republish a valid learning content version
      When API request is sent to republish a valid learning content version
        Then LOS will return a json response with signed URl for preview of published content and new content uuid

  Scenario: User wants to publish invalid learning content version
    Given that an LXE or CD has access to the content authoring tool and wants to publish invalid learning content version
      When API request is sent to to publish invalid learning content version
        Then LOS will return a resource is not found error response for invalid learning content version

  Scenario: User wants to publish invalid learning resource
    Given that an LXE or CD has access to the content authoring tool and wants to publish invalid learning resource
      When API request is sent to to publish invalid learning resource
        Then LOS will return a resource is not found error response for invalid learning resource
