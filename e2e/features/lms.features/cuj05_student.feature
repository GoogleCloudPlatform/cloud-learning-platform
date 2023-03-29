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
  Scenario:  A student is invited to section and has not accepted the invite
    Given A student is invited and has not accepted the invite via email
    When cron job is triggered and calls update_invites endpoint
    Then student details will be updated in user collection and course enrollment mapping once invite is accepted

  @fixture.create.section
  Scenario: Invite student to cohort by admin
    Given A user is invited to a cohort_id using email
    When API request is sent with valid cohort id and email
    Then Invitation is sent to student via email and student invited to section with min enrolled student count

  @fixture.create.section
  Scenario: Add student to a section using a payload
    Given A user has access privileges and wants to enroll a student into a section
    When API request is sent to enroll student to a section with correct request payload and valid section id
    Then Section will be fetch using the given id and student is enrolled using student credentials and a response model object will be return

  Scenario: Unable to Add student to a section using a payload
    Given A user has access to portal and needs to enroll a student into a section
    When API request is sent to enroll student to a section with correct request payload and invalid section id
    Then Student will not be enrolled and API will throw a resource not found error

  @fixture.create.section
  Scenario: Unable to enroll student to a section using request data
    Given A user has access to the portal and wants to enroll a student into a section
    When API request is sent to enroll student to a section with incorrect request payload and valid section id
    Then Student will not be enrolled and API will throw a validation error
