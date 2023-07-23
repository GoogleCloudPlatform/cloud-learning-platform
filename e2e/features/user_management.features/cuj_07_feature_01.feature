Feature: CRUD for managing actions in user management

  Scenario: Create action with correct request payload
    Given user wants to create action in user management with correct request payload
      When API request is sent to create action with correct request payload
        Then the action has been created successfully

  Scenario: Create action with incorrect request payload
    Given user wants to create action in user management with incorrect request payload
      When API request is sent to create action with incorrect request payload
        Then the action has been failed to create for incorrect request payload

  Scenario: Unable to create action with name that already exists in database
		Given A user wants to create an action with name already existing in database
			When API request is sent to create action with name already existing in database
				Then action object will not be created and a conflict error is thrown

  Scenario: Update the action with correct action ID
    Given user want to update their action with correct action ID
      When API request is sent to update action with correct action ID
        Then the action has been updated successfully with correct action ID

  Scenario: Update the action with incorrect action ID
    Given user try to update their action with incorrect action ID
      When API request is sent to update the action for incorrect action ID
        Then the action has been failed to update with incorrect action ID

  Scenario: Get the action for correct action ID
    Given action is fetch from the datastore with correct action ID
      When API request is sent to fetch the action details with correct action ID
        Then the action is fetched successfully with correct action ID

  Scenario: Get the action for incorrect action ID
    Given User try to fetch their action with incorrect action ID
      When API request is sent to fetch the action with incorrect action ID
        Then the action details is failed to fetch for incorrect action ID

  Scenario: Get All the action details
    Given fetch all the actions from the datastore
      When API request is sent to fetch all the actions
        Then the actions is fetched successfully

  Scenario: Get All the actions for incorrect query params
    Given fetch all the actions for incorrect query params
      When API request is sent for fetch all the actions with incorrect query params
        Then the actions is failed to fetch for incorrect query params