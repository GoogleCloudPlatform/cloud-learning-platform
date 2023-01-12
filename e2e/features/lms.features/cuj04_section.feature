@fixture.get.header
Feature: Add student to section

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

  Scenario: Register a course to a Pub/Sub topic using a payload
    Given A user has access privileges and wants to register a course to a pub/sub topic
    When API request is sent to register a course to a pub/sub topic with correct request payload and valid course id
    Then Course will be register using unique course id and feed type to a pub/sub topic and a response model object will be return

  @fixture.create.section
  Scenario: Add student to a section using a workspace email and a payload
    Given A user has access privileges and wants to enroll a student using his/her workspace email into a section
    When API request is sent to enroll workspace email as a student to a section with correct request payload and valid section id
    Then Section will be fetch using the given id and student is enrolled using student access token and his workspace email and a response model object will be return
