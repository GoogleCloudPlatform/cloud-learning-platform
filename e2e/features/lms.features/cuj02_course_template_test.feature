@fixture.get.header
Feature: Create, Read, Retive all and delete APIs for Course Template

  Scenario: Create Course Template with correct request payload
    Given A user has access privileges and needs to create a Course Template Record
    When API request is sent to create Course Template Record with correct request payload
    Then Course Template Record will be created in a third party tool and classroom master course will be create with provided payload and all metadata will be ingested and stored in Cousre Template service and uuid for learning experiences will be stored in Cousre Template service

  Scenario: Unable to create Course Template with incorrect request payload
    Given A user has access to admin portal and wants to create a Course Template Record
    When API request is sent to create Course Template Record with incorrect request payload
    Then Course Template Record Record will not be created and Course Template API will throw a validation error

  @fixture.create.course_template
  Scenario: Retrieve Course Template Record by giving valid uuid
    Given A user has access privileges and needs to retrieve a Course Template Record
    When API request is sent to retrieve Course Template Record by providing correct uuid
    Then Course Template Record corresponding to given uuid will be returned successfully

  Scenario: Unable to retrieve Course Template Record when invalid uuid given
    Given A user has access to admin portal and wants to retrieve a Course Template Record
    When API request is sent to retrieve Course Template Record by providing invalid uuid
    Then Course Template Record will not be returned and API will throw a resource not found error

  @fixture.create.course_template
  Scenario: Update Course Template Record by giving valid uuid and request payload
    Given A user has access privileges and needs to update a Course Template Record
    When API request is sent to update Course Template Record by providing correct uuid and request payload
    Then Course Template Record will be updated successfully

  Scenario: Unable to Update Course Template Record when invalid uuid and valid request payload given
    Given A user has access to admin portal and wants to update a Course Template Record
    When API request is sent to delete Course Template Record by providing invalid uuid and valid payload
    Then Course Template Record will not be update and API will throw a resource not found error

  @fixture.create.course_template
  Scenario: Delete Course Template Record by giving valid uuid
    Given A user has access privileges and needs to delete a Course Template Record
    When API request is sent to delete Course Template Record by providing correct uuid
    Then Course Template Record will be deleted successfully

  Scenario: Unable to delete Course Template Record when invalid uuid given
    Given A user has access to admin portal and wants to delete a Course Template Record
    When API request is sent to delete Course Template Record by providing invalid uuid
    Then Course Template Record will not be deleted and API will throw a resource not found error

  Scenario: Retrieve all Course Template Records
    Given A user has access privileges and needs to fetch all Course Template Records
    When API request is sent to fetch all Course Template Records
    Then Course Template API will return all existing Course Template Records successfully

  @fixture.create.cohort
  Scenario: Retive all Cohort Records by giving valid Course Template uuid
    Given A user has access privileges and needs to fetch all Cohort Records using course template
    When API request is sent to fetch all Cohorts Records by providing Course template valid uuid
    Then Course Template list Cohort API will return all existing Cohort Records successfully

  Scenario: Unable to retrieve list of Cohort Records when invalid Course Template uuid given
    Given A user has access to admin portal and wants to retrieve list of Cohort Records using course template
    When API request is sent to fetch all Cohorts Records by providing Course template invalid uuid
    Then Course Template list Cohort API will throw a resource not found error
