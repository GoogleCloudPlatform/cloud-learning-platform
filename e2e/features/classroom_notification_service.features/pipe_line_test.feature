@fixture.create.analytics.data
Feature: Retrieve messages from Pub/Sub and push them to bigquery

  Scenario: Roaster Changes Occurs in a registered Classroom
    Given A user has been added to classroom as a student
    When Pipline got messages related to roster changes 
    Then Pipline get user related details from classroom and store user details and Pub/Sub message in bigquery
  
  Scenario: Course Work changes Occurs in a registered Classroom
    Given A teacher created a course work
    When Pipline got messages related to create Course work 
    Then Pipline get course work details from classroom and store course work details and Pub/Sub message in bigquery
  
  Scenario: Course Work Submission changes Occurs in a registered Classroom
    Given A student submitted a course work
    When Pipline got messages related to create Submitted Course work 
    Then Pipline get submitted course work details from classroom and store Submitted Course Work details and Pub/Sub message in bigquery