@skill-service
Feature: Manage batch jobs

  Scenario: Unable to fetch batch job by giving correct job type and incorrect job name
    Given Format the API request url to fetch batch job using correct job type and incorrect job name
      When API request is sent to get the batch job
        Then Skill Service will throw an error message while trying to get the batch job

  Scenario: Unable to fetch batch job when job type not given
    Given Format the API request url to fetch batch job using correct job name without job type
      When API request is sent to fetch the batch job
        Then Skill Service will throw an error message while trying to fetch the batch job

  Scenario: Successfully fetch all the batch jobs for correct job type
    Given Format the correct API request url to get all the jobs using correct job type
      When API request is sent to get all batch jobs
        Then Skill Service will fetch all batch jobs

  Scenario: Unable to fetch all the batch jobs for incorrect job type
    Given Format the correct API request url to get all the jobs using incorrect job type
      When API request is sent to fetch all batch jobs
        Then Skill Service will throw an error message while trying to get the batch jobs

  Scenario: Successfully delete batch job for correct job name
    Given Format the correct API request url to delete the batch job using correct job name
      When API request is sent to delete the batch job
        Then Skill Service will successfully delete the requested batch job

  Scenario: Unable to delete the batch job for incorrect job name
    Given Format the correct API request url to delete the batch job using incorrect job name
      When API request is sent to delete the batch job with incorrect name
        Then Skill Service will throw an error message while trying to delete the batch job
