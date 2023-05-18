Feature: Integration with 3rd Party Tool | Frost (learning experience storage)
  
  @filter-api
  Scenario: LXE/CD wants to filter on learning objects with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter learning objects with correct parameters
      When they filter for learning objects within that tool with correct parameters
        Then LOS will serve up the most relevant search results based on the filter
  
  Scenario: LXE/CD wants to filter on learning object with multiple parametes on parent/child nodes
    Given that an LXE or CD has access to the content authoring tool to filter learning objects with multiple parent/child node parameters
      When they filter for learning objects within that tool with multiple parameters on parent/child nodes
        Then LOS will throw Internal Server Error when filtering for learning objects

  Scenario: LXE/CD wants to filter on learning experience with multiple parametes on parent/child nodes
    Given that an LXE or CD has access to the content authoring tool to filter learning experiences with multiple parent/child node parameters
      When they filter for learning experiences within that tool with multiple parameters on parent/child nodes
        Then LOS will throw Validation Failed when filtering for learning experiences

  @filter-api
  Scenario: LXE/CD wants to filter on learning experience with correct parameters
  Given that an LXE or CD has access to the content authoring tool to filter learning experiences with correct parameters
    When they filter for learning experiences within that tool with correct parameters
      Then LOS will serve up the most relevant learning experiences based on the filter

  Scenario: LXE/CD wants to filter on learning experience with multiple parametes on parent/child nodes
    Given that an LXE or CD has access to the content authoring tool to filter learning objects with multiple parent/child node parameters
      When they filter for learning objects within that tool with multiple parameters on parent/child nodes
        Then LOS will throw Internal Server Error when filtering for learning objects

  @filter-api
  Scenario: LXE/CD wants to filter on learning resources with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter learning resources with correct parameters
      When they filter for learning resources within that tool with correct parameters
        Then LOS will serve up the most relevant learning resources based on the filter

  Scenario: LXE/CD wants to filter on learning resources with multiple parametes on parent/child nodes
    Given that an LXE or CD has access to the content authoring tool to filter learning resources with multiple parent/child node parameters
      When they filter for learning resources within that tool with multiple parameters on parent/child nodes
        Then LOS will throw Validation Failed when filtering for learning resources

    
  