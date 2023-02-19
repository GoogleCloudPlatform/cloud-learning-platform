@fixture.get.header
Feature: Add student to section

  @fixture.create.section
  Scenario: Add student to a section using a payload
    Given A user has access privileges and wants to enroll a student into a section
    When API request is sent to enroll student to a section with correct request payload and valid section id
    Then Section will be fetch using the given id and student is enrolled using student credentials and a response model object will be return

  Scenario: Unable to Add student to a section using a payload
    Given A user has access to portal and needs to enroll a student into a section
    When API request is sent to enroll student to a section with correct request payload and invalid cohort id
    Then Student will not be enrolled and API will throw a resource not found error

  @fixture.create.section
  Scenario: Unable to enroll student to a section using request data
    Given A user has access to the portal and wants to enroll a student into a cohort
    When API request is sent to enroll student to a section with incorrect request payload and valid cohort id
    Then Student will not be enrolled and API will throw a validation error

  @fixture.create.section
  Scenario: Add student to a section using a workspace email and a payload
    Given A user has access privileges and wants to enroll a student using his/her workspace email into a section
    When API request is sent to enroll workspace email as a student to a section with correct request payload and valid section id
    Then Section will be fetch using the given id and student is enrolled using student access token and his workspace email and a response model object will be return

  Scenario: Enable notifications for a course using a payload
    Given A user has access privileges and wants to enable notifications for a course
    When API request is sent to enable notifications for a course with correct request payload which contains valid course id
    Then Notifications will be enabled using unique course id and feed type and a response model object will be return

  @fixture.create.section
  Scenario: Enable notifications for a course using a section id
    Given A user has access privileges and wants to enable notifications for a course using section id
    When API request is sent to enable notifications for a course with correct request payload which contains valid section id
    Then Notifications will be enabled using unique section id and feed type and a response model object will be return

  Scenario: Unable to enable notifications for a course using a section id
    Given A user has access to portal and needs to enable notifications for a course using section id
    When API request is sent to enable notifications for a course with correct request payload which contains invalid section id
    Then Notifications will not be enabled and API will throw a resource not found error

  Scenario: Unable to enable notifications for a course using a payload
    Given A user has access to portal and needs to enable notifications for a course using payload
    When API request is sent to enable notifications for a course with incorrect request payload
    Then Notifications will not be enabled and API will throw a validation error

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

  Scenario: Unable to enable notifications for a course using a section id
    Given A user has access to portal and needs to enable notifications for a course using section id
    When API request is sent to enable notifications for a course with correct request payload which contains invalid section id
    Then Notifications will not be enabled and API will throw a resource not found error

  Scenario: Unable to enable notifications for a course using a payload
    Given A user has access to portal and needs to enable notifications for a course using payload
    When API request is sent to enable notifications for a course with incorrect request payload
    Then Notifications will not be enabled and API will throw a validation error