@fixture.create.analytics.data
@fixture.get.header
Feature: Get Anaytics data
  Scenario: Retrive Anaytics data using valid student email
    Given A user has access to the portal and wants student analytics data
    When API request is send get analytics data using valid student email
    Then Analytics data will be fetch from Big query view using student email

  Scenario: Retrive Anaytics data using valid student id
    Given A user has access privileges and wants to get student analytics data
    When API request is send get analytics data using valid student id
    Then Get student email using user API and using that email analytics data will be fetch from bq view

  Scenario: Retrive Anaytics data using invalid student id
    Given A user has access privileges to the portal and wants to get student analytics data
    When API request is send get analytics data using invalid student id
    Then API throw not found error

  Scenario: Retrive Anaytics data using invalid student email
    Given A user has access to the portal and wants to get student analytics data
    When API request is send get analytics data using invalid student email
    Then API will throw user not found by this id error
