@fixture.get.header
Feature: Retive all courses, Copy course and enable notification APIs of classroom courses endpoints

  Scenario: Retrieve all classroom courses Records
    Given A user has access privileges and needs to fetch all Courses Records
    When API request is sent to fetch all Courses Records
    Then Classroom Courses API will return all existing Courses Records successfully

  Scenario: Copy Course with correct request payload
    Given A user has access privileges and wants to create a Copy of existing Classroom Course
    When API request is sent to Copy Course with correct request payload
    Then Existing course details will be fetch and using that details new course will be created and Copy course will send the details of new course

  Scenario: Enable notifications for a course using a valid Course id
    Given A user has access privileges and wants to enable notifications for a course
    When API request is sent to enable notifications for a course using valid course id
    Then Notifications will be enabled using unique course id and a response model object will be return

  Scenario: Unable to enable notifications for a course
    Given A user has access to portal and needs to enable notifications for a course
    When API request is sent to enable notifications for a section using invalid course id
    Then Notifications will not be enabled and API will throw a resource not found error