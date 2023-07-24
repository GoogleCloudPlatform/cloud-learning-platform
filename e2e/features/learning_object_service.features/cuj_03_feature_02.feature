Feature: Integration with 3rd Party Tool | Archival

  Scenario: LXE/CD wants to filter on archived learning objects with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter archived learning objects with correct parameters
      When they filter for archived learning objects within that tool with correct parameters
        Then LOS will serve up the most relevant archived learning objects based on the filter
  
  Scenario: LXE/CD wants to filter on unarchived learning objects with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter unarchived learning objects with correct parameters
      When they filter for unarchived learning objects within that tool with correct parameters
        Then LOS will serve up only the unarchived learning objects based on the filter

  Scenario: LXE/CD wants to filter on archived learning experience with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter archived learning experiences with correct parameters
      When they filter for archived learning experiences within that tool with correct parameters
        Then LOS will serve up the most relevant archived learning experiences based on the filter
    
  Scenario: LXE/CD wants to filter on unarchived learning experience with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter unarchived learning experiences with correct parameters
      When they filter for unarchived learning experiences within that tool with correct parameters
        Then LOS will serve up only the unarchived learning experiences based on the filter
  
  Scenario: LXE/CD wants to filter on archived learning resource with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter archived learning resources with correct filter parameters
      When they filter for archived learning resources within that tool with correct filter parameters
        Then LOS will serve up only the most relevant archived learning resources based on the filter
    
  Scenario: LXE/CD wants to filter on unarchived learning resource with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter unarchived learning resources with correct filter parameters
      When they filter for unarchived learning resources within that tool with correct filter parameters
        Then LOS will serve up only the most relevant unarchived learning resources based on the filter
  
