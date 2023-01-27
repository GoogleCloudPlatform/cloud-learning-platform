@fixture.get.header
Feature: List students in section

  @fixture.create.enroll_student_course
  Scenario: List students in section
    Given A section has a students enrolled
    When API request with valid section Id is sent
    Then Section will be fetch using the given id and list of studnets enrolled
