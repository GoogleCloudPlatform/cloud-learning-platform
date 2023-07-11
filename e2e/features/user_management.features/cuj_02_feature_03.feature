Feature: Update permissions related to an application for a UserGroup

	Scenario: Update permissions related to an assigned application for a UserGroup
		Given A UserGroup already has access to an application and Admin wants to update permissions for the application to the UserGroup
			When API request is sent to update permissions of a UserGroup
				Then the UserGroup is updated with the permissions
                    And the permissions will hold the reference of UserGroup

    Scenario: Update permissions related to an unassigned application for a UserGroup
		Given A UserGroup already exists and Admin wants to update permissions related to unassigned application for UserGroup 
			When API request is sent to update permissions related to unassigned application of a UserGroup 
				Then Validation error for application is thrown by the User management service
    
    Scenario: Update permissions related to an assigned application for a UserGroup but provided invalid permissions
		Given Admin wants to update permissions for the application to the UserGroup but provided permissions not related to valid application in request body
			When API request is sent to update permissions of a UserGroup but provided permissions not related to valid application in request body
				Then Validation error of permission is thrown by the User management service