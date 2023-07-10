@fixture.get.header
Feature: Delete student in a section

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

  @fixture.create.section  
  Scenario: Unable to delete student to a section using a email
    Given A user has access to portal and wants to remove a student from a section using invalid email id
    When API request with valid section Id and Invalid email is sent to delete student
    Then API returns student not found in this section error

  @fixture.enroll.student.in_classroom.not_in_db
  Scenario: Retrive list of students exists in classroom not in DB
    Given A user has access to portal and wants to fetch the list of students exists in Classroom not in DB
    When API request is sent to get the list of students
    Then List of students details will be fetched from bq views

  @fixture.enroll.student.in_db.not_in_classroom
  Scenario: Retrive list of students exists in DB not in classroom
    Given A user has access to portal and wants to fetch the list of students exists in DB not in classroom
    When API request is sent to fetch the list of students records
    Then List of student records will be fected from bq views