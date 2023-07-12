Feature: Integration with 3rd Party Tool | Filter on Curriculum Pathways

  @filter-api
  Scenario: LXE/CD wants to filter on archived curriculum pathways with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter archived curriculum pathways with correct parameters
      When they filter for archived curriculum pathways within that tool with correct parameters
        Then LOS will serve up the most relevant archived curriculum pathways based on the filter

  @filter-api
  Scenario: LXE/CD wants to filter on unarchived curriculum pathways with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter unarchived curriculum pathways with correct parameters
      When they filter for unarchived curriculum pathways within that tool with correct parameters
        Then LOS will serve up only the unarchived curriculum pathways based on the filter

  @filter-api
  Scenario: LXE/CD wants to filter on curriculum pathways with correct parameters
    Given that an LXE or CD has access to the content authoring tool to filter curriculum pathways with correct parameters
      When they filter for curriculum pathways within that tool with correct parameters
        Then LOS will serve up the most relevant curriculum pathways based on the filter

  @filter-api
  Scenario: LXE/CD wants to filter on curriculum pathway with multiple parametes on parent/child nodes
    Given that an LXE or CD has access to the content authoring tool to filter curriculum pathways with multiple parent/child node parameters
      When they filter for curriculum pathways within that tool with multiple parameters on parent/child nodes
        Then LOS will throw Validation Failed when filtering for curriculum pathways