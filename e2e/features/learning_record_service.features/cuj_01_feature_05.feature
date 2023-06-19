Feature: CRUD APIs for managing Statement data in Learning Record Service

    Scenario: Create xAPI Statement object within Learning Record Service with correct request payload
        Given A user has access to Learning Record Service and needs to create xAPI Statements
            When API request is sent to create Statements with correct request payload
                Then The xAPI Statements will be created successfully
                And API request is sent to fetch the created Statements
                And The fetched Statements are same as the created Statements

    Scenario: Create xAPI Statement object within Learning Record Service with incorrect request payload
        Given A user has access privileges to Learning Record Service and needs to create an xAPI Statement
            When API request is sent to create Statement with incorrect request payload
                Then The xAPI Statement object creation will fail

	Scenario: Read a particular xAPI Statement object using incorrect Statement uuid
		Given A user has access to Learning Record Service and needs to fetch an xAPI Statement
			When API request is sent to fetch the xAPI Statement with incorrect Statement uuid
				Then The xAPI Statement will not be fetched and Learning Record Service will throw ResourceNotFound error

	Scenario: Fetch all xAPI Statement objects using correct request parameters
		Given A user has access to Learning Record Service and needs to fetch all xAPI Statements
			When API request is sent to fetch all the xAPI Statements with correct request parameters
				Then the Learning Record Service will serve up all the xAPI Statements

	Scenario: Fetch all xAPI Statement objects using incorrect request parameters
		Given A user has access privileges to Learning Record Service and needs to fetch all xAPI Statements
			When API request is sent to fetch all the xAPI Statements with incorrect request parameters
				Then The xAPI Statements will not be fetched and Learning Record Service will throw validation error
	Scenario: Fetch the details of Learning Record Service
		Given A user has access to Learning Record Service and needs to fetch its details
			When API request is sent to fetch the details of Learning Record Service
				Then The Learning Record Service will return its details