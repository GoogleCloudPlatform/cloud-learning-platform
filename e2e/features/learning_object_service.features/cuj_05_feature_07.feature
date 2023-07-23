Feature: Delete full learning hierarchy

  @filter-api
  Scenario: LXE/CD wants to delete the full learning that with a valid pathway ID
    Given that a LXE/CD has access to the content authoring tool and has a valid pathway ID that needs to be deleted with all of its components
      When they hit the endpoint with the valid pathway ID
        Then the full learning hierarchy is deleted
          And the achievements associated with node items in the hierarchy are deleted

  @filter-api
  Scenario: LXE/CD wants to delete the full learning that with an invalid pathway ID
    Given that a LXE/CD has access to the content authoring tool and has a invalid pathway ID that needs to be deleted with all of its components
      When they hit the endpoint with the invalid pathway ID
        Then the full learning hierarchy is not deleted and the endpoint throws 404 ResourceNotFound Error
