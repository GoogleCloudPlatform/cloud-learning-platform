@fixture.get.header
Feature: Create, Read, Retrieve all and delete APIs for Course Template

  Scenario: Create Course Template with correct request payload
    Given A user has access privileges and needs to create a Course Template Record
    When API request is sent to create Course Template Record with correct request payload
    Then Course Template Record will be created in a third party tool and classroom master course will be create with provided payload and all metadata will be ingested and stored in Cousre Template service and id for learning experiences will be stored in Cousre Template service

  Scenario: Unable to create Course Template with incorrect request payload
    Given A user has access to admin portal and wants to create a Course Template Record
    When API request is sent to create Course Template Record with incorrect request payload
    Then Course Template Record Record will not be created and Course Template API will throw a validation error

  @fixture.create.course_template
  Scenario: Retrieve Course Template Record by giving valid id
    Given A user has access privileges and needs to retrieve a Course Template Record
    When API request is sent to retrieve Course Template Record by providing correct id
    Then Course Template Record corresponding to given id will be returned successfully

  Scenario: Unable to retrieve Course Template Record when invalid id given
    Given A user has access to admin portal and wants to retrieve a Course Template Record
    When API request is sent to retrieve Course Template Record by providing invalid id
    Then Course Template Record will not be returned and API will throw a resource not found error

  @fixture.create.course_template
  Scenario: Update Course Template Record by giving valid id and request payload
    Given A user has access privileges and needs to update a Course Template Record
    When API request is sent to update Course Template Record by providing correct id and request payload
    Then Course Template Record will be updated successfully

  Scenario: Unable to Update Course Template Record when invalid id and valid request payload given
    Given A user has access to admin portal and wants to update a Course Template Record
    When API request is sent to delete Course Template Record by providing invalid id and valid payload
    Then Course Template Record will not be update and API will throw a resource not found error

  @fixture.create.course_template
  Scenario: Delete Course Template Record by giving valid id
    Given A user has access privileges and needs to delete a Course Template Record
    When API request is sent to delete Course Template Record by providing correct id
    Then Course Template Record will be deleted successfully

  Scenario: Unable to delete Course Template Record when invalid id given
    Given A user has access to admin portal and wants to delete a Course Template Record
    When API request is sent to delete Course Template Record by providing invalid id
    Then Course Template Record will not be deleted and API will throw a resource not found error

  Scenario: Retrieve all Course Template Records
    Given A user has access privileges and needs to fetch all Course Template Records
    When API request is sent to fetch all Course Template Records
    Then Course Template API will return all existing Course Template Records successfully

  @fixture.create.cohort
  Scenario: Retrieve all Cohort Records by giving valid Course Template id
    Given A user has access privileges and needs to fetch all Cohort Records using course template
    When API request is sent to fetch all Cohorts Records by providing Course template valid id
    Then Course Template list Cohort API will return all existing Cohort Records successfully

  Scenario: Unable to retrieve list of Cohort Records when invalid Course Template id given
    Given A user has access to admin portal and wants to retrieve list of Cohort Records using course template
    When API request is sent to fetch all Cohorts Records by providing Course template invalid id
    Then Course Template list Cohort API will throw a resource not found error

  @fixture.enroll.instructional_designer.course_template
  Scenario: Get instructional designer from course template using course template id and user id
    Given A user has access privileges wants to get instructional designer with valid course template id and valid instructional designer id
    when Get request with valid data is sent
    Then Get instructional designer API will show user details

    
  Scenario: Get instructional designer from course template using course template id and invalid user id
    Given A user has access privileges wants to get instructional designer with valid course template id and invalid instructional designer id
    when Get request with invalid data is sent to get instructional designer
    Then Get instructional designer API will throw user not found error

  @fixture.enroll.instructional_designer.course_template
  Scenario: Delete instructional designer in course template with given course_template id and email
    Given A user has access to admin portal and needs to delete the instructional designer with valid course template id and email
    When Delete request is sent which contains valid course template id and email
    Then Set inactive instructional designer from enrollment mapping collection

  
  @fixture.enroll.instructional_designer.course_template
  Scenario: List instructional designer in course template with given course_template id
    Given A user has access to admin portal and needs to get the instructional designer with valid course template id
    When Get request is sent which contains valid course template id to list instructional_designers
    Then fetch list of Id for given course template

  @fixture.create.course_template
  Scenario: Delete instructional designer from course template using course template id and user id
    Given A user has access privileges wants to delete instructional designer with valid course template id and invalid indtructional designer id
    When API request is sent which contains valid course template id and invalid user id to delete instructional designer
    Then Delete instructional designer API throw user not found error

  @fixture.create.course_template
  Scenario: Enroll instructional designer in a Course Template using course_template id and request payload
    Given A user has access privileges wants to enroll the instructional designer using valid section id and email
    When Post request is sent which contains valid course template id and payload which contains valid email
    Then The instruction designer enrolled in classroom and a enrollment mapping is created and return user details with enrollment details
