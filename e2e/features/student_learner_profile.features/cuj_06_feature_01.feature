Feature: Fetching Instructor details for a given discipline and learner

  Scenario: Fetch Instructor details for a valid discipline and a learner
    Given that a valid learner, valid discipline, valid instructor exists and a valid AssociationGroup is present in the DB where the learner, discipline and instructor have already been added
      When the valid discipline uuid and a valid learner uuid is correctly passed
        Then the instructor details are fetched

  Scenario: Fetch Instructor details for a valid discipline and but invalid learner ID
    Given that all valid data exists except for Learner
      When the endpoint is hit to fetch instructor details with invalid learner ID
        Then endpoint throws ResourceNotFoundException for the given learner ID
  
  Scenario: Fetch Instructor details for an invalid discipline but a valid learner ID
    Given that all valid data exists except for discipline
      When the endpoint is hit to fetch instructor details with invalid pathway ID
        Then endpoint throws ResourceNotFoundException for the given pathway ID
  
  Scenario: Fetch Instructor details for a invalid pathwayID where alias is not discipline and a valid learner ID
    Given that all valid data exists except for pathway where alias is not discipline
      When the endpoint is hit to fetch instructor details with pathway ID where alias is not discipline
        Then endpoint throws ValidationError for the given pathway ID where alias is not discipline
  
  Scenario: Fetch Instructor details for a valid discipline and a valid learner but the learner is not associated to any AssociationGroup of type learner
    Given that all valid data exists except for a AssociationGroup of type learner
      When the endpoint is hit to fetch instructor details with pathway ID where Leaner is not added to any AssociationGroup
        Then endpoint throws ValidationError as Leaner is not added to any AssociationGroup
  
  Scenario: Fetch Instructor details for a valid discipline and a valid learner but there are no active instructors
    Given that all valid data exists except for an active instructor
      When the endpoint is hit with valid IDs
        Then endpoint throws ValidationError as there are no active instructors for the given learner and instructor ID

  Scenario: Fetch details for instructors corresponding to a valid program and a learner
    Given that a valid learner, discipline, program, instructor exists and tagged to a Learner AssociationGroup
      When API request is sent to fetch details for all instructors by providing valid program id and learner id
        Then list of details for all instructor tagged to the given learner and program are fetched