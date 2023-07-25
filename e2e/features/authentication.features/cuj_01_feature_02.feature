@auth-api
Feature: Users want to get access to backend APIs using email and password authentication

    Scenario: The user wants to set password to the backend using sign-up api with valid email-id
        Given the user email id already exists in the backend firestore database
            When API request is sent to sign up with backend with valid email in the request body
                Then the Authentication service successfully signs up the user with the backend 
                    Then the user can sign in to the backend using correct email and password

    Scenario: The user wants to set password to the backend using sign-up api with invalid email-id
        Given the user email id doesn't exists in the backend firestore database
            When API request is sent to set the password with invalid email in the request body
                Then the Authentication service will not sign up the user instead throws Unauthorized user
    
    Scenario: The user wants to sign-in in to the backend with correct email-id and password
        Given the user have already signed up with the backend
            When API request is sent to sign in with correct request body
                Then the user successfully logs in to backend and receives response that contains a valid id-token of the backend project
    
    Scenario: The user wants to sign-in in to the backend with incorrect email-id and password
        Given the user is not already signed up with the backend
            When In Valid User sends API request to sign in to the backend
                Then the Authentication service throws Unauthorized user
    
    Scenario: The user tries to sign-in in to the backend with correct email-id and wrong password
        Given the user is already a signed up user of backend
            When API request is sent to sign in with wrong password
                Then the Authentication service returns error response invalid credentials
    
    Scenario: The user wants to change sign in password of backend using valid id-token
        Given the user already signs in to the backend and has a valid id-token
            When API request with valid Id token is sent to Authentication service to change sign in password
                Then the Authentication service successfully changes users sign in password and return successfully changed password message in response
                    Then the user can sign in to the backend using changed password

    Scenario: The user wants to change sign in password of backend using Invalid id-token
        Given the user already signs in to the backend 
            When API request with invalid Id token is sent to Authentication service to change sign in password 
                Then the Authentication service returns an error response invalid token