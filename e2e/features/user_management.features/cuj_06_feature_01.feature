Feature: CRUD for managing permissions in user management

  Scenario: Create permission with correct request payload
    Given user wants to create permission in user management with correct request payload
      When API request is sent to create permission with correct request payload
        Then the permission has been created successfully

  Scenario: Create permission with incorrect request payload
    Given user wants to create permission in user management with incorrect request payload
      When API request is sent to create permission with incorrect request payload
        Then the permission has been failed to create for incorrect request payload

  Scenario: Update the permission with correct permission ID
    Given user want to update their permission with correct permission ID
      When API request is sent to update permission with correct permission ID
        Then the permission has been updated successfully with correct permission ID

  Scenario: Update the permission with incorrect permission ID
    Given user try to update their permission with incorrect permission ID
      When API request is sent to update the permission for incorrect permission ID
        Then the permission has been failed to update with incorrect permission ID

  Scenario: Get the permission for correct permission ID
    Given permission is fetch from the datastore with correct permission ID
      When API request is sent to fetch the permission details with correct permission ID
        Then the permission is fetched successfully with correct permission ID

  Scenario: Get the permission for incorrect permission ID
    Given User try to fetch their permission with incorrect permission ID
      When API request is sent to fetch the permission with incorrect permission ID
        Then the permission details is failed to fetch for incorrect permission ID

  Scenario: Get All the permission details
    Given fetch all the permissions from the datastore
      When API request is sent to fetch all the permissions
        Then the permissions is fetched successfully

  @filter-api
  Scenario: Get All the permissions for a given application_id
    Given fetch all the permissions from the datastore for a given application_id
      When API request is sent to fetch all the permissions for a given application_id
        Then the permissions for given application_id are fetched successfully

  Scenario: Get All the permissions for incorrect query params
    Given fetch all the permissions for incorrect query params
      When API request is sent for fetch all the permissions with incorrect query params
        Then the permissions is failed to fetch for incorrect query params

  Scenario: Filter the permission based on the action name
    Given fetch all the permissions for action name
      When API request is sent for fetch all the permissions based on action name
        Then the permissions is failed to fetch for action name

  Scenario: Filter the permission based on the module name
    Given fetch all the permissions for module name
      When API request is sent for fetch all the permissions based on module name
        Then the permissions is failed to fetch for module name

  Scenario: Filter the permission based on the application name
    Given fetch all the permissions for application name
      When API request is sent for fetch all the permissions based on application name
        Then the permissions is failed to fetch for application name

  Scenario: Filter the permission based on the group name
    Given fetch all the permissions for group name
      When API request is sent for fetch all the permissions based on group name
        Then the permissions is failed to fetch for group name

  Scenario: Filter the permission based on the permission name
    Given fetch all the permissions for permission name
      When API request is sent for fetch all the permissions based on permission name
        Then the permissions is failed to fetch for permission name

  Scenario: Filter the permission for incorrect search query
    Given fetch all the permissions for incorrect search query
      When API request is sent for fetch all the permissions for incorrect search query
        Then the permissions is failed to fetch for incorrect search query

  Scenario: Delete permission object within User management by giving valid uuid
    Given A user has access to User management and needs to delete a permission
        When API request is sent to delete permission by providing correct uuid
            Then permission object will be deleted successfully

  Scenario: Retrieve permissions within User management by providing valid application id
    Given A user has access to User management and needs to fetch all permissions using valid application id
        When API request is sent to fetch permissions by providing valid application id
            Then API will return a list of permissions based on the provided application id

  Scenario: Retrieve permissions within User management by providing valid user group id
    Given A user has access to User management and needs to fetch all permissions using valid user group id
        When API request is sent to fetch permissions by providing valid user group id
            Then API will return a list of permissions based on the provided user group id

  Scenario: Retrieve permissions within User management by providing valid application, module and action ids
    Given A user has access to User management and needs to fetch all permissions using valid application, module and action ids
        When API request is sent to fetch permissions by providing valid application, module and action ids
            Then API will return a list of permissions based on the provided ids

  Scenario: Retrieve permissions within User management by providing valid user group id and invalid module id
    Given A user has access to User management and needs to fetch all permissions using valid user group id and invalid module id
        When API request is sent to fetch permissions by providing valid user group id and invalid module id
            Then API will return an empty list of permissions based on the provided user group and module ids

  Scenario: Retrieve permissions within User management by providing invalid user group id and valid action id
    Given A user has access to User management and needs to fetch all permissions using invalid user group id and valid action id
        When API request is sent to fetch permissions by providing invalid user group id and valid action id
            Then API will return an empty list of permissions based on the provided user group and action ids  

  Scenario: Retrieve permissions within User management by providing invalid application, module and action ids
    Given A user has access to User management and needs to fetch all permissions using invalid application, module and action ids
        When API request is sent to fetch permissions by providing invalid application, module and action ids
            Then API will return an empty list of permissions based on the provided ids

  Scenario: Fetch unique applications, modules, actions and user groups
    Given Retrieve all unique applications, modules, actions and user groups
       When API request is sent to fetch unique records
          Then Object will be returned with unique values
