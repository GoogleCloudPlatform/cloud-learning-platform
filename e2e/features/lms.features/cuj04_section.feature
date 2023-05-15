@fixture.get.header
Feature: Add student to cohort

  @fixture.create.section
  Scenario: Add student to a cohort using a payload
    Given A user has access privileges and wants to enroll a student into a cohort
    When API request is sent to enroll student to a section with correct request payload and valid cohort id
    Then Section will be fetch using the given id and student is enrolled using student credentials and a response model object will be return

  Scenario: Unable to Add student to a cohort using a payload
    Given A user has access to portal and needs to enroll a student into a cohort
    When API request is sent to enroll student to a section with correct request payload and invalid cohort id
    Then Student will not be enrolled and API will throw a resource not found error

  @fixture.create.section
  Scenario: Unable to enroll student to a section using request data
    Given A user has access to the portal and wants to enroll a student into a cohort
    When API request is sent to enroll student to a section with incorrect request payload and valid cohort id
    Then Student will not be enrolled and API will throw a validation error

  @fixture.create.section
  Scenario: Add student to a section using a workspace email and a payload
    Given A user has access privileges and wants to enroll a student using his/her workspace email into a cohort
    When API request is sent to enroll workspace email as a student to a cohort with correct request payload and valid cohort id
    Then Section will be fetch using the given id and student is enrolled using student access token and his workspace email and a response model object will be return

  @fixture.create.section
  Scenario: Enable notifications for a course using a section id
    Given A user has access privileges and wants to enable notifications for a section
    When API request is sent to enable notifications for a section using valid section id
    Then Notifications will be enabled using unique section id and a response model object will be return

  Scenario: Unable to enable notifications for a section
    Given A user has access to portal and needs to enable notifications for a section
    When API request is sent to enable notifications for a section using invalid section id
    Then Notifications will not be enabled and API will throw a resource not found error

@fixture.create.assignment
  Scenario: Retrieve Assignment details by giving valid section id and assignment id
    Given A user has access to portal and needs to retrieve a assignment using section id and assignment id
    When API request is sent to retrieve assignment details of a section with correct section id and assignment id
    Then Assignment Record corresponding to given assignment id will be returned successfully

  Scenario: Unable to retrieve Assignment details when invalid section id given
    Given A user has access to admin portal and wants to retrieve a assignment using assignment id and section id
    When API request is sent to retrieve assignment details by providing invalid section id
    Then Assignment details will not be returned and API will throw a resource not found error

  @fixture.create.section
  Scenario: List teachers in section with given section id
    Given A user has access to admin portal and needs to retrieve the list of teachers with vailid section id
    When API request is sent which contains valid section id
    Then List of teachers will be given with there details
  
  Scenario: List teachers in section with wrong section id
    Given A user has access to admin portal and needs to retrieve the list of teachers with invailid section id
    When API request is sent which contains invalid section id
    Then Section not found error is sent in response

  @fixture.enroll.teacher.section
  Scenario:Get teacher details in section with given section id and teacher email
    Given A user has access to admin portal and needs to retrieve the details teacher with valid section id and teacher_email
    When API request is sent which contains valid section id and teacher email
    Then Get the details of teacher from user collection

  @fixture.create.section
  Scenario:Fetch teacher details in section with given section id and teacher email
    Given A user has access privileges wants to retrieve the details teacher with valid section id and invalid teacher_email
    When API request is sent which contains valid section id and invalid teacher email
    Then Get teacher API will throw teacher not found error

  @fixture.enroll.teacher.section
  Scenario:Delete teacher in section with given section id and teacher email
    Given A user has access to admin portal and needs to delete the teacher with valid section id and teacher_email
    When API request is sent which contains valid section id and teacher email
    Then Set inactive teacher from enrollment mapping collection

  @fixture.create.section
  Scenario:Delete teacher from section using section id and teacher id
    Given A user has access privileges wants to delete teacher with valid section id and invalid teacher id
    When API request is sent which contains valid section id and invalid teacher id to delete teacher
    Then Delete teacher API throw teacher not found error

 @fixture.create.section
  Scenario: Enroll teacher in a section using section id and teacher email
    Given A user has access privileges wants to enroll the teacher using valid section id and teacher_email
    When API request is sent which contains valid section id and teacher email
    Then The teacher enrolled in classroom and a enrollment mapping is created and return user details with enrollment details

  @fixture.import.google_form_grade
  Scenario:Update the student  assignment grades for non domain students who has not Turn_in assignment
    Given A teacher has access to portal and wants to  update grades of student for a coursework with form quize of a section
    When API request is sent which has valid section_id and coursework_id
    Then Student grades are not updated in classroom
  
  @fixture.import.google_form_grade
  Scenario:Update the student  assignment grades for non domain students who has Turn_in assignment
    Given A teacher wants to update grades of student for a coursework with for turnIn  assignment with google form
    When API request is sent which has valid input
    Then Student grades are  updated in classroom ans student_email is present in api response

  @fixture.create.section
  Scenario: Update classroom code of a section using a section id
    Given A user has access privileges and wants to update classroom code for a section
    When API request is sent to update classroom code for a section using valid section id
    Then Code will be updated using unique section id and a response model object will be return

  Scenario: Unable to update section for a section
    Given A user has access to portal and needs to update classroom code for a section
    When API request is sent to update classroom code for a section using invalid section id
    Then Code will not be updated and API will throw a resource not found error
