Feature: Import full Learning Hierarchy from JSON

Scenario: LXE/CD ingest the full learning that is designed to be ingested via JSON
  Given that a LXE/CD has access to the content authoring tool and has a valid JSON that needs to be ingested into the system
    When they hit the endpoint with the valid JSON
      Then the full learning hierarchy is ingested
        And the achievements associated with node items in the hierarchy are ingested
        And the competencies associated with node items in the hierarchy are ingested
        And the skills associated with node items in the hierarchy are ingested
        And relationships established in the JSON are maintained

Scenario: LXE/CD ingest the full learning that is designed to be ingested via invalid JSON
  Given that a LXE/CD has access to the content authoring tool and has an invalid JSON that needs to be ingested into the system
    When they hit the endpoint with the invalid JSON
      Then the full learning hierarchy is not ingested and the endpoint throws 422 Validation Error
