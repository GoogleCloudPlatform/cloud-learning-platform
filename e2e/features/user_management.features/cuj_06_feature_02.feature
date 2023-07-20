Feature: Unique permissions filter in user management

  Scenario: Fetch unique applications, modules, actions and user groups from permission collection without passing query params
    Given Retrieve all unique applications, modules, actions and user groups from permission collection
       When API request is sent to fetch unique records from permission collection
          Then Object will be returned with unique values from permission collection

  Scenario: Fetch unique applications, modules, actions and user groups from permission collection by passing query params
    Given Retrieve all unique applications, modules, actions and user groups matching query params
       When API request is sent to fetch unique records from permission collection matching query params
          Then Object will be returned with unique values from permission collection matching query params

  Scenario: Fetch unique applications, modules, actions and user groups from permission collection by passing invalid query params
    Given Retrieve all unique applications, modules, actions and user groups matching invalid query params
       When API request is sent to fetch unique records from permission collection matching invalid query params
          Then Object will be returned with empty filter data