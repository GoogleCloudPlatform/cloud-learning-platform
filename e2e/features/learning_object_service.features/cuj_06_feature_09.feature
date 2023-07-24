@content-serving-api
Feature: User should be able to link valid madcap htm file against a learning resource

  Scenario: User wants to be able to link valid madcap htm file against a learning resource
    Given that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against a learning resource
      When API request is sent to link valid madcap htm file against a learning resource
        Then LOS will return a success response for the link
  
  Scenario: User wants to link a file against a learning resource which is not allowed by the learning experience
    Given that an LXE or CD has access to the content authoring tool and wants to link file against a learning resource which is not allowed by the learning experience
      When API request is sent to link file against a learning resource which is not allowed by the learning experience
        Then LOS will return a validation error for a file which does not share prefix with the parent learning experience
  
  Scenario: User wants to link valid madcap htm file against a learning resource but invalid learning experience
    Given that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against a learning resource but invalid learning experience
      When API request is sent to link valid madcap htm file against a learning resource but invalid learning experience
        Then LOS will return a validation error for the invalid learning experience in link api
  
  Scenario: User wants to link valid madcap htm file against invalid learning resource
    Given that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against invalid learning resource
      When API request is sent to link valid madcap htm file against invalid learning resource
        Then LOS will return a validation error for the invalid learning resource in link api

  Scenario: User wants to link valid madcap htm file against a learning resource which is not child of given learning experience
    Given that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against a learning resource which is not child of given learning experience
      When API request is sent to link valid madcap htm file against a learning resource which is not child of given learning experience
        Then LOS will return a validation error for the invalid learning resource and learning experience pair

  Scenario: User wants to link valid madcap htm file against a learning resource for which the learning experience does not have a resource_path
    Given that an LXE or CD has access to the content authoring tool and wants to link valid madcap htm file against a learning resource for which the learning experience does not have a resource_path
      When API request is sent to link valid madcap htm file against a learning resource for which the learning experience does not have a resource_path
        Then LOS will return a validation error for the missing resource_path for the learning experience
