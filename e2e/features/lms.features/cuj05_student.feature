@fixture.get.header
Feature:Delete, List students in section

  @fixture.create.enroll_student_course
  Scenario: List students in section
    Given A section has a students enrolled
    When API request with valid section Id is sent
    Then Section will be fetch using the given id and list of studnets enrolled

  @fixture.create.enroll_student_course
  Scenario: Delete student in section using user id
    Given A section has a students enrolled and has course enrollment mapping present 
    When API request with valid section Id and user id is sent to delete student
    Then Student is marked as inactive in course enrollment mapping and removed from google classroom using user id

  @fixture.create.enroll_student_course
  Scenario: Delete student in section using email
    Given A user wants to remove a student from a section using email id
    When API request with valid section Id and email is sent to delete student
    Then Student is marked as inactive in course enrollment mapping and removed from google classroom using email id
