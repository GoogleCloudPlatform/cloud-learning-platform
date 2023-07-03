Feature: CRUD APIs for managing Sessions data in User Management

    Scenario: Create Session for a valid User with the correct request payload
        Given A User has access to User Management and wants to create a Session with the correct request payload
            When A valid User sends a API request to create a Session with the correct request payload
                Then The User Management will create a Session for the User                

    Scenario: Create Session for an invalid User
        Given A Invalid User wants to create a Session
            When A Invalid User sends a API request to create a Session 
                Then The User Management will not create a Session and returns a ResourceNotFound Exception

    Scenario: Create Session for a valid User with an incorrect request payload
        Given A User has access to User Management and wants to create a Session with an incorrect request payload
            When A valid User sends a API request to create a Session with an incorrect request payload
                Then The User Management will not create a Session for the User and throws a Validation error

    Scenario: User wants to fetch a session by providing a valid Session Id
        Given User has the privilege to access User Management service and wants to get his/her Session by providing correct Session Id
            When User sends a API request to User Management to get a Session by sending a valid Session Id
                Then User Management service will return the requested Session Object in response

    Scenario: User wants to fetch a session by providing a Invalid Session Id
        Given User has the privilege to access User Management service and wants to get his/her Session by providing Incorrect Session Id
            When User sends a API request to User Management to get a Session by sending a Invalid Session Id
                Then User Management service will return ResourceNotFound Exception

    @filter-api
    Scenario: A User wants to fetch all sessions or filter sessions related to his/her User Id, Node Id, and Session Id
        Given A User has access to User Management and wants to fetch all sessions or filter sessions related to his/her User Id, Node Id, and Session Id
            When A valid User sends a API request to fetch all sessions related to his/her User Id, Node Id, and Session Id
                Then The User Management will return the requested sessions

    @filter-api
    Scenario: A User wants to fetch the latest session related to his/her User Id
        Given A User has access to User Management and needs to fetch the latest Session related to his/her User Id
            When A valid User sends a API request to fetch the latest session related to his/her User Id
                Then The User Management will return the latest session related to User Id
    
    Scenario: Rules Engine wants to update session details by providing Session and correct request payload
        Given Rules Engine has access to User Management and wants to update Session using session Id and by sending the correct request payload
            When Rules Engine sends a API request to update the session with the correct request Payload
                Then The User Management will update the session and returns the updated session

    Scenario: Rules Engine wants to update non existing Session
        Given Rules Engine has access to User Management and wants to update a non existing Session
            When Rules Engine sends a API request to update the session with the invalid Session Id
                Then The User Management will return ResourceNotFound Exception
