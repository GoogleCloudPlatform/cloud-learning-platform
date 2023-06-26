Feature: Grant Access to an Application for a UserGroup

	Scenario: Grant Access to an Application for a UserGroup
		Given A UserGroup and an application already exists and Admin wants to grant access for the UserGroup to the application
			When API request is sent to link application to a UserGroup
				Then the UserGroup document will hold reference to the application
                    And the users belong to the UserGroup have access to the linked application

    Scenario: A UserGroup should not get access to an invalid Application
		Given A UserGroup already exists and Admin wants to link UserGroup to an invalid application
			When API request is sent to link invalis application to a UserGroup
				Then Resource not found exception for application will be thrown by the user management
    
    Scenario: An invalid UserGroup should not get access to an Application
		Given A UserGroup doesn't exists and Admin wants to give access to a invalid UserGroup to an application
			When API request is sent to link application to a invalid UserGroup
				Then Resource not found exception for UserGroup will be thrown by the user management