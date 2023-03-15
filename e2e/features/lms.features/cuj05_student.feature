@fixture.get.header
Feature:Delete, List students in section

  @fixture.create.enroll_student_course
  Scenario: List students in section
    Given A section has a students enrolled
    When API request with valid section Id is sent
    Then Section will be fetch using the given id and list of studnets enrolled
  

  @fixture.create.enroll_student_course
  Scenario:  Get students in cohort
    Given A section has a students enrolled in cohort
    When API request with valid cohort Id  user_id is sent
    Then student details will be fetch using the given id for cohort

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
  Scenario: Invite student to section by admin
    Given A user is invited to a section using email
    When API request is sent with valid section id and email
    Then Invitation is sent to student via email and course enrollmet object with status invited is created


  @fixture.invite.student
  Scenario:  A student is invited to section and has accepted the invite
    Given A student is invited and has accepted the invite via email
    When cron job is triggered and calls update_invites endpoint
    Then student details will be updated in user collection and course enrollment mapping status is updated to active