Feature: Fetching Coach details for a learner

  Scenario: Fetch Coach details for a learner that is part of valid learner assocition group by giving valid learner uuid
    Given that a valid learner, coressponding user, valid coach exists and a valid AssociationGroup is present in the DB where the learner user and coach have already been added
      When API request is sent to fetch coach details by providing a valid learner id
        Then the details for coach present in the corresponding learner association group are fetched

  Scenario: Fetch Coach details by providing invalid learner uuid
    Given that all valid data exists and user corresponding to given learner uuid is part of learner assocaition group
      When the endpoint is hit to fetch coach details with invalid learner ID
        Then endpoint throws ResourceNotFoundException for the given invalid learner ID

  Scenario: Fetch Coach details by providing valid learner uuid which is not part of any learner association group
    Given that all valid data exists but user corresponding to given learner uuid is not part of any assocaition group
      When the endpoint is hit to fetch coach details with learner uuid that is not associated in any group
        Then endpoint throws ValidationError stating that user corresponding to given learner uuid is not linked to any association group

  Scenario: Fetch Coach details by providing valid learner uuid for which no active coach exists in any learner association group
    Given that all valid data exists but coach is not active in any learner assocaition group
      When the endpoint is hit to fetch coach details with learner uuid for which no active coach exists in learner association group
        Then endpoint throws ValidationError stating that no active coach exists in learner assocition group corresponding to given learner uuid
