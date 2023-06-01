---
sidebar_label: CRUD APIs for UserGroup
sidebar_position: 2
---

# CRUD APIs for UserGroup

The following steps are to create, view and update UserGroup.


### Create a UserGroup:

To create a user group, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group`**. The name field in the request body should be unique for every user group creation. By using this api, only muttable(can update name and description, can delete) user groups can be created. The Immutable user groups are already present in the UserGroup Collection. Immutable usergroups can be identified based on **`is_immutable`** field of usergroup, if it is **`true`**  the that usergroup is a Immutable usergroup.

Following are the query parameters that can be used to filter the response:
| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| sort_by | Literal["name", "created_time"] | field by which the submitted assessments will be sorted. (default="created_time") |
| sort_order |  Literal["ascending", "descending"] | Ascending or Descending sort (default="descending") |
The request body for the API is as follows:

```json
{
  "name": "muttable user group",
  "description": "group of muttable user group"
}
```

A new user group with the request body details and with a new uuid(unique ID of the user group) is added to the user group. By default **`is_immutable`** is set to **`False`**
After successfully adding new user group document to the collection. You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "muttable user group",
    "description": "group of muttable user group",
    "users": [],
    "permissions": [],
    "roles": [],
    "applications": [],
    "is_immutable": false
  }
}
```

### Get all UserGroups:

To fetch all the user groups available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-groups`** with **`skip`**, **`limit`** and **`fetch_tree`** and **`is_immutable`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of learning experience array to be returned which takes a default value **`10`** if not provided and

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "name": "muttable user group",
      "description": "group of muttable user group",
      "users": [
        "44qxEpc35pVMb6AkZGbi"
      ],
      "permissions": [
        "U2DDBkl3Ayg0PWudzhI"
      ],
      "roles": [],
      "applications": [
        "dfeSo7867vDSDDFC89HJ"
      ],
      "is_immutable": false
    }
  ]
}
```

### Get a specific UserGroup:

To fetch the details of a specific user group, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group/{uuid}`** where **`uuid`** is the unique ID of the user group and the query parameter  **`fetch_tree`** is to fetch the complete object when set **`true`** if not it takes the default value **`false`** returning only UUID.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "muttable user group",
    "description": "group of muttable user group",
    "users": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "permissions": [
      "U2DDBkl3Ayg0PWudzhI"
    ],
    "roles": [],
    "applications": [
      "dfeSo7867vDSDDFC89HJ"
    ],
    "is_immutable": false
  }
}
```

If the user group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "UserGroup with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update a UserGroup:

To update the details of a user group, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group/{uuid}`** where **`uuid`** is the unique ID of the user group. Name of the immutable usergroup cannot be changed by using this api.

The request body would be as follows:

```json
{
  "name": "muttable user group",
  "description": "group of muttable user group"
}
```

After the validation of user group for given uuid, user group for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "muttable user group",
    "description": "group of muttable user group",
    "users": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "permissions": [
      "U2DDBkl3Ayg0PWudzhI"
    ],
    "roles": [],
    "applications": [
      "dfeSo7867vDSDDFC89HJ"
    ],
    "is_immutable": false
  }
}
```

If the user group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a UserGroup:

To delete a user group, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group/{uuid}`** where **`uuid`** is the unique ID of the user group. The deleted user group will be unassinged from its assocaited users. Immutable usergroups cannot be deleted by this api.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the user group"
}
```

If the user group is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "UserGroup with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```

### Search a UserGroup

To search a user group Record based on the `name` of the user group Record, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group/search`**, where **`name`** is the name that is used to search. This will fetch all the user group Records of the given **`name`**.

Then response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the user group",
  "data": [{
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "muttable user group",
    "description": "group of muttable user group",
    "users": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "permissions": [
      "U2DDBkl3Ayg0PWudzhI"
    ],
    "roles": [],
    "applications": [
      "dfeSo7867vDSDDFC89HJ"
    ],
    "is_immutable": false
  }]
}
```

### Add User To UserGroup

To add users to the user group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group/{uuid}/users/add`** where **`uuid`** is the unique ID of the user group. If the **`uuid`** belongs to a immutable usergroup, then only users with **`user_type`** equals to usergroup **`name`** can be added to the usergroup.

The request body would be as follows:

```json
{
  "user_ids": [
    "44qxEpc35pVMb6AkZGbi"
  ]
}
```

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully added user to user group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "muttable user group",
    "description": "group of muttable user group",
    "users": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "permissions": [
      "U2DDBkl3Ayg0PWudzhI"
    ],
    "roles": [],
    "applications": [
      "dfeSo7867vDSDDFC89HJ"
    ],
    "is_immutable": false
  }
}
```

If the user group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "UserGroup with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Remove User From UserGroup:

To remove the user from the user group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group/{uuid}/user/remove`** where **`uuid`** is the unique ID of the user group.

The request body would be as follows:

```json
{
  "user_id": "44qxEpc35pVMb6AkZGbi"
}
```

After the validation of user group for given uuid, user with the given user_id is removed from the usergroup and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully removed user from user group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "muttable user group",
    "description": "group of muttable user group",
    "users": [],
    "permissions": [
      "U2DDBkl3Ayg0PWudzhI"
    ],
    "roles": [],
    "applications": [
      "dfeSo7867vDSDDFC89HJ"
    ],
    "is_immutable": false
  }
}
```

If the user group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "UserGroup with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update applications access to a UserGroup

To update applications access to a group, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group/{uuid}/applications`** where **`uuid`** is the unique ID of the user group.

The request body would be as follows:

```json
{
  "applications": [
    "44qxEpc35pVMb6AkZGbi"
  ],
  "action_id" : "GHT5343vdfssgfrt787"
}
```
The applications list in the above request body contains the final list of applications for which user group should have access. The **action_id** is the id of the default action that should be given permission for the user-group. By default the usergroup will get the default permissions of the application.
Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully added user to user group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "muttable user group",
    "description": "group of muttable user group",
    "users": [
      "Ft6hkkyVVjjijkklkbi"
    ],
    "permissions": [
      "U2DDBkl3Ayg0PWudzhI"
    ],
    "roles": [],
    "applications": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "is_immutable": false
  }
}
```

If the user group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "UserGroup with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update Permissions of a UserGroup

To update permissions related to an application to a user-group, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user-group/{uuid}/application/{application_uuid}/permissions`** where **`uuid`** is the unique ID of the user group, **`application_uuid`**  is the unique ID of the application. Only the permissions related to the applications for which the user-group has already access can be assigned or unassigned to the user-group.

The request body would be as follows:

```json
{
  "permission_ids" : ["GHT5343vdfssgfrt787"]
}
```
The permission_ids list in the above request body contains the final list of permissions related to an application for the user group. 
Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully added user to user group",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "muttable user group",
    "description": "group of muttable user group",
    "users": [
      "Ft6hkkyVVjjijkklkbi"
    ],
    "permissions": [
      "GHT5343vdfssgfrt787"
    ],
    "roles": [],
    "applications": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "is_immutable": false
  }
}
```

If the user group is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`**, then the response would be as follows:

```json
{
  "success": false,
  "message": "UserGroup with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```