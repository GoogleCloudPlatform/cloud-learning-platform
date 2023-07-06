Feature: Creation and authoring of Human Graded Assessments

  Scenario: Creating a Human Graded Assessment with the correct request payload
    Given that a LXE  has access to Assessment Service and need to create a Human Graded Assessment
      When API request is sent to create a HUman Graded Assessment with correct request payload
        Then that Human Graded Assessment object will be created in the database with skills updated from rubric_criteria
          And the assessment resources are moved to a proper gcs path
            And the child Rubric would also also be created and linked
              And the leaf Rubric criterion will also be created and updated

  Scenario: Creating a Human Graded Assessment with an incorrect payload
    Given that a LXE has access to Assessment Service but has an incorrect payload to create a Human Graded Assessment
      When API request is sent to create a Human Graded Assessment with incorrect payload
        Then Human Graded Assessment object will not be created and will throw a validation error
  
  Scenario: Updating a Human Graded Assessment with the correct request payload
    Given that a LXE  has access to Assessment Service and has created a Human Graded Assessment
      When API request is sent to update a Human Graded Assessment with correct request payload
        Then that Human Graded Assessment object will be updated corrrectly in the database
  
  Scenario: Updating a Human Graded Assessment with the correct request payload with rubric and rubric_criterion
    Given that a LXE  has access to Assessment Service and has created a Human Graded Assessment with rubric details
      When API request is sent to update a Human Graded Assessment with updates to existing and new rubric and rubric_criteria
        Then that Human Graded Assessment object will be updated with the list of old and new rubrics
          And the old rubrics will be updated and new rubrics will be created