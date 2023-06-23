Feature: CRUD for managing Staff in user management

	Scenario: Create a Staff with correct request payload
		Given A user has permission to user management and wants to create a Staff with correct request payload
			When API request is sent to create Staff with correct request payload
				Then Staff object will be created in the database as per given request payload

  Scenario: Create a Staff with incorrect request payload
		Given A user has permission to user management and wants to create a Staff with incorrect request payload
			When API request is sent to create Staff with incorrect request payload
				Then Staff object will not be created in the database and a ValidationError will be thrown

  Scenario: Search a Staff with correct request payload
		Given A user has permission to user management and wants to search a Staff with correct request payload
			When API request is sent to search Staff with correct request payload
				Then Staff object will be retrieved from the database as per given request payload

  Scenario: Search a Staff with incorrect request payload
		Given A user has permission to user management and wants to search a Staff with incorrect request payload
			When API request is sent to search Staff with incorrect request payload
				Then Invalid payload error response raised

  Scenario: Retrieve the Staff with correct uuid
		Given A user has permission to user management and wants to retrieve the Staff with correct uuid
			When API request is sent to retrieve the Staff with correct uuid
				Then Staff object will be retrieved from the database as per given uuid

  Scenario: Retrieve the Staff with incorrect uuid
		Given A user has permission to user management and wants to retrieve the Staff with incorrect uuid
			When API request is sent to retrieve the Staff with incorrect uuid
				Then Staff object will not be retrieved from the database and a ResourceNotFoundException will be thrown

  @filter-api
  Scenario: Retrieve all Staff with correct request payload
		Given A user has permission to user management and wants to retrieve all Staff with correct request payload
			When API request is sent to retrieve all Staff with correct request payload
				Then All Staff objects will be retrieved from the database

  Scenario: Retrieve all Staff with incorrect request payload
		Given A user has permission to user management and wants to retrieve all Staff with incorrect request payload
			When API request is sent to retrieve all Staff with incorrect request payload
				Then Staff objects will not be retrieved from the database and a ValidationError will be thrown

  Scenario: Update a Staff with correct request payload
		Given A user has permission to user management and wants to update a Staff with correct request payload
			When API request is sent to update a Staff with correct request payload
				Then Staff object will be updated in the database

  Scenario: Update a Staff with incorrect request payload
		Given A user has permission to user management and wants to update a Staff with incorrect request payload
			When API request is sent to update a Staff with incorrect request payload
				Then Staff object will not be updated in the database and a ValidationError will be thrown

  Scenario: Delete a Staff with correct request payload
		Given A user has permission to user management and wants to delete a Staff with correct request payload
			When API request is sent to delete a Staff with correct request payload
				Then Staff object will be deleted from the database

  Scenario: Delete a Staff with incorrect uuid
		Given A user has permission to user management and wants to delete a Staff with incorrect uuid
			When API request is sent to delete a Staff with incorrect uuid
				Then Staff object will not be deleted from the database and a ResourceNotFoundException will be thrown

  Scenario: Import Staffs from a JSON file with correct request payload
		Given A user has permission to user management and wants to import Staffs from JSON file with correct request payload
			When API request is sent to import Staffs with correct request payload
				Then All the Staff objects in the JSON file will be created and added in the database

  Scenario: Import Staffs from an invalid JSON file
		Given A user has permission to user management and wants to import Staffs from an invalid JSON file
			When API request is sent to import Staffs from invalid JSON file
				Then Staff objects will not be imported and a ValidationError will be thrown
