Feature: A user with appropriate permissions wants to get user account information
    Scenario: User information is to be fetched for a single user with correct uuid
        Given Required User already exists in the database and correct uuid will be used to find user
            When A GET api call is made to the User Management Service with correct uuid
                Then The User data is correctly fetched

    Scenario: User information is to be fetched for a single user with incorrect uuid
        Given Required User does not exists in the database and incorrect uuid will be used to find the user
            When A GET api call is made to the User Management Service with incorrect uuid
                Then The User Not Found error response is returned

    Scenario: User information is to be searched with user email
        Given Required User already exists in the database and correct email address will be used for query
            When A GET api call is made to the User Management Service with correct email
                Then A list of matching users is returned

    Scenario: User information is to be searched with user incorrect email
        Given Required User already exists in the database and incorrect email address will be used for query
            When A GET api call is made to the User Management Service with incorrect email
                Then Invalid email error response raised
    
    @filter-api
    Scenario: User information is to be fetched for all users
        Given Users already exist in the database
            When A GET api call is made to the User Management Service to fetch all
                Then A list of users is returned

    @filter-api
    Scenario: Fetch users from User management based on given filter
        Given A user has access to User management and needs to fetch users
            When API request is sent to fetch users along with a filter
                Then User management will successfully return users for the given filter

    @filter-api
    Scenario: Fetch users from User management based on given sort order by email
        Given A user has access to User management and needs to fetch users on a specific sort order by email
            When API request is sent to fetch users along with a sort order by email
                Then User management will successfully return users for the given sort order by email

    @filter-api
    Scenario: Fetch users from User management based on given sort order by firstname
        Given A user has access to User management and needs to fetch users on a specific firstname sort order
            When API request is sent to fetch users along with a sort order by firstname
                Then User management will successfully return users for the given sort order by firstname

    @filter-api
    Scenario: Fetch users from User management based on given sort order by lastname
        Given A user has access to User management and needs to fetch users on a specific lastname sort order
            When API request is sent to fetch users along with a sort order by lastname
                Then User management will successfully return users for the given sort order by lastname

    @filter-api
    Scenario: Fetch users from User management based on given sort order by email in ascending
        Given A user has access to User management and needs to fetch users on a specific sort order by email in ascending
            When API request is sent to fetch users along with a sort order by email in ascending
                Then User management will successfully return users for the given sort order by email in ascending

    @filter-api
    Scenario: Fetch users from User management based on given sort order by firstname in ascending
        Given A user has access to User management and needs to fetch users on a specific firstname sort order in ascending
            When API request is sent to fetch users along with a sort order by firstname in ascending
                Then User management will successfully return users for the given sort order by firstname in ascending

    @filter-api
    Scenario: Fetch users from User management based on given sort order by lastname in ascending
        Given A user has access to User management and needs to fetch users on a specific lastname sort order in ascending
            When API request is sent to fetch users along with a sort order by lastname in ascending
                Then User management will successfully return users for the given sort order by lastname in ascending
        