Feature: CRUD for managing Activity State model in Learning Record Service

	Scenario: Create Activity State with correct request payload
		Given A user has access to Learning Record Service and needs to create an Activity State
			When API request is sent to create Activity State with correct request payload
				Then that Activity State object will be created in the database


	Scenario: Create Activity State with incorrect request payload
		Given A user can access Learning Record Service and needs to create an Activity State
			When API request is sent to create Activity State with incorrect request payload
				Then Activity State object will not be created and Learning Record Service will throw a Validation error


	Scenario: Read a particular Activity State using correct Activity State id
		Given A user has access to Learning Record Service and needs to fetch an Activity State
			When API request is sent to fetch the Activity State with correct Activity State id
				Then the Learning Record Service will serve up the requested Activity State


	Scenario: Read a particular Activity State using incorrect Activity State id
		Given A user can access Learning Record Service and needs to fetch an Activity State
			When API request is sent to fetch the Activity State with incorrect Activity State id
				Then The Activity State will not be fetched and Learning Record Service will throw ResourceNotFound error


	Scenario: Read all Activity States with correct request payload
		Given A user has access to Learning Record Service and needs to fetch all Activity States
			When API request is sent to fetch all Activity States with correct request payload
				Then the Learning Record Service will show all the Activity States


	Scenario: Read all Activity States with incorrect request payload
		Given A user can access Learning Record Service and needs to fetch all Activity States
			When API request is sent to fetch all Activity States with incorrect request payload
				Then The Activity States will not be fetched and Learning Record Service will throw a Validation error


	Scenario: Update Activity State with correct request payload
		Given A user has access to Learning Record Service and needs to update an Activity State
			When API request is sent to update the Activity State with correct request payload
				Then that Activity State will be updated in the database


	Scenario: Update Activity State with incorrect Activity State id
		Given A user can access Learning Record Service and needs to update an Activity State
			When API request is sent to update the Activity State with incorrect Activity State id
				Then The Activity State will not be updated and Learning Record Service will throw ResourceNotFound error


	Scenario: Delete a particular Activity State using correct Activity State id
		Given A user has access to Learning Record Service and needs to delete an Activity State
			When API request is sent to delete the Activity State with correct Activity State id
				Then that Activity State will be deleted from the database


	Scenario: Delete a particular Activity State using incorrect Activity State id
		Given A user can access Learning Record Service and needs to delete an Activity State
			When API request is sent to delete the Activity State with incorrect Activity State id
				Then The Activity State will not be deleted and Learning Record Service will throw ResourceNotFound error


	Scenario: Import Activity States with correct JSON in request payload
		Given A user has access to Learning Record Service and needs to import Activity State from JSON file
			When the Activity States are imported from correct JSON in request payload
				Then those Activity States will be added in the database


	Scenario: Import Activity States with incorrect JSON in request payload
		Given A user can access Learning Record Service and needs to import Activity State from JSON file
			When the Activity States are imported from incorrect JSON in request payload
				Then The Activity States will not be imported and Learning Record Service will throw Validation error
