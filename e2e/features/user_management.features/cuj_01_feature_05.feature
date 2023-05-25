@inspace
Feature: CRUD on Inspace User alongwith backend user
    Scenario: An Inspace User account is to be created alongwith backend user
        Given A user has access to the application and enters valid details for user creation
            When An api call is made to the User Management Service with correct details for user creation
                Then The User will be successfully created alongwith Inspace User

    Scenario: No Inspace User account is to be created alongwith backend user
        Given A user has access to the application and enters valid details for only backend user creation
            When An api call is made to the User Management Service with correct details for backend user creation
                Then The backend User will be successfully created

    Scenario: An Inspace User info is to be updated along with backend user
        Given A user has access to the application and enters valid details for user updation
            When An api call is made to the User Management Service with correct details for user updation
                Then The User will be successfully updated alongwith Inspace User
    
    Scenario: An Inspace User info is to be deleted along with backend user
        Given A user has access to the application and enters valid details for user deletion
            When An api call is made to the User Management Service with correct details for user deletion
                Then The User will be successfully deleted alongwith Inspace User
    
    Scenario: An Inspace User info is to be updated along with backend user but Inspace user does not exists
        Given A user has access to the application and enters valid details for user updation but Inspace user does not exists
            When An api call is made to the User Management Service with correct details for user updation but Inspace user does not exists
                Then The User will not be updated alongwith Inspace User
    
    Scenario: An Inspace User info is to be deleted along with backend user but Inspace user does not exists
        Given A user has access to the application and enters valid details for user deletion but Inspace user does not exists
            When An api call is made to the User Management Service with correct details for user deletion but Inspace user does not exists
                Then The User will not be deleted alongwith Inspace User