Feature: CRUD for managing modules in user management

  Scenario: Create module with correct request payload
    Given user wants to create module in user management with correct request payload
      When API request is sent to create module with correct request payload
        Then the module has been created successfully

  Scenario: Create module with incorrect request payload
    Given user wants to create module in user management with incorrect request payload
      When API request is sent to create module with incorrect request payload
        Then the module has been failed to create for incorrect request payload

  Scenario: Unable to create module with name that already exists in database
		Given A user wants to create an module with name already existing in database
			When API request is sent to create module with name already existing in database
				Then module object will not be created and a conflict error is thrown

  Scenario: Update the module with correct module ID
    Given user want to update their module with correct module ID
      When API request is sent to update module with correct module ID
        Then the module has been updated successfully with correct module ID

  Scenario: Update the module with incorrect module ID
    Given user try to update their module with incorrect module ID
      When API request is sent to update the module for incorrect module ID
        Then the module has been failed to update with incorrect module ID

  Scenario: Get the module for correct module ID
    Given module is fetch from the datastore with correct module ID
      When API request is sent to fetch the module details with correct module ID
        Then the module is fetched successfully with correct module ID

  Scenario: Get the module for incorrect module ID
    Given User try to fetch their module with incorrect module ID
      When API request is sent to fetch the module with incorrect module ID
        Then the module details is failed to fetch for incorrect module ID

  Scenario: Get All the module details
    Given fetch all the modules from the datastore
      When API request is sent to fetch all the modules
        Then the modules is fetched successfully

  Scenario: Get All the modules for incorrect query params
    Given fetch all the modules for incorrect query params
      When API request is sent for fetch all the modules with incorrect query params
        Then the modules is failed to fetch for incorrect query params