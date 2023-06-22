@single-sign-on-auth-flow
Feature: Users want to get access to backend APIs using the google single sign on
 
    Scenario: The user will send the sign-in request to the backend with a valid google-id token of their project
        Given the user already exists in the backend firestore database
            When authentication service will validate the requested google-id token and also validate the user in the backend database
                Then send back the response to the user with the valid id-token of the backend project
                    Then the user can access the APIs of backend using the receivedss id-token

    Scenario: User sends the sign-in request to the backend with a valid google-id token of their project
        Given the user is not exist in the backend firestore database
            When authentication service will validate the requested google-id token and also validate the user in the backend database
                Then the user will get an error of unauthorized user
    
    Scenario: User sends the sign-in request to the backend with the invalid google-id token
        Given the user already exists in the backend firestore database
            When the authentication service validates the requested google-id token.
                Then the user will get an error message of an invalid token