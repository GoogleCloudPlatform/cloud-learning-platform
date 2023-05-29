---
sidebar_label: CRUD APIs for Permission
sidebar_position: 3
---

# CRUD APIs for Permission

The following steps are to create, view and update permission.


### Create a permission:

To create a permission, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/permission`**.
The request body for the API is as follows:

```json
{
  "name": "assessment_authoring.summative_assessment.edit",
  "description": "edit permission",
  "application_id": "Dfchd56otyghfgfjioiK",
  "module_id": "55txEec45pVMf6Akvcew",
  "action_id": "44qxEpc35pVMb6AkZGbi",
  "user_groups": [
    "U2DDBkl3Ayg0PWudzhI"
  ]
}
```

A new permission with the request body details and with a new uuid(unique ID of the permission) is added to the permission. After successfully adding new permission document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the permission",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "assessment_authoring.summative_assessment.edit",
    "description": "edit permission",
    "application_id": "Dfchd56otyghfgfjioiK",
    "module_id": "55txEec45pVMf6Akvcew",
    "action_id": "44qxEpc35pVMb6AkZGbi",
    "user_groups": [
      "U2DDBkl3Ayg0PWudzhI"
    ]
  }
}
```

### Get all permissions:

To fetch all the permissions available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/permissions`** with **`skip`** , **`limit`**, **`application_ids`**, **`module_ids`**, **`action_ids`**, **`user_groups`** and **`fetch_tree`** where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of permissions array to be returned which takes a default value **`10`**, **`application_ids`** is the comma delimited string of uuid's of the applications, **`module_ids`** is the comma delimited string of uuid's of the modules, **`action_ids`** is the comma delimited string of uuid's of the actions, **`user_groups`** is the comma delimited string of uuids of the users and **`fetch_tree`** is to fetch the complete action, module and application objects when set **`true`** if not it takes the default value **`false`** returning only respective UUIDs.


Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "name": "assessment_authoring.summative_assessment.edit",
      "description": "edit permission",
      "application_id": "Dfchd56otyghfgfjioiK",
      "module_id": "55txEec45pVMf6Akvcew",
      "action_id": "44qxEpc35pVMb6AkZGbi",
      "user_groups": [
        "U2DDBkl3Ayg0PWudzhI"
      ]
    }
  ]
}
```

### Get a specific permission:

To fetch the details of a specific permission, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/permission/{uuid}`** where **`uuid`** is the unique ID of the permission and query parameter **`fetch_tree`** is to fetch the complete action, module and application object when set **`true`** if not it takes the default value **`false`** returning only their respecticve UUIDs.
Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the permission",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "assessment_authoring.summative_assessment.edit",
    "description": "edit permission",
    "application_id": "Dfchd56otyghfgfjioiK",
    "module_id": "55txEec45pVMf6Akvcew",
    "action_id": "44qxEpc35pVMb6AkZGbi",
    "user_groups": [
      "U2DDBkl3Ayg0PWudzhI"
    ]
  }
}
```

If the permission is not present for a given permission_id - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update a permission:

To update the details of a permission, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/permission/{uuid}`** where **`uuid`** is the unique ID of the permission.
The request body would be as follows:

```json
{
  "name": "assessment_authoring.summative_assessment.edit",
  "description": "edit permission",
  "application_id": "Dfchd56otyghfgfjioiK",
  "module_id": "55txEec45pVMf6Akvcew",
  "action_id": "44qxEpc35pVMb6AkZGbi",
  "user_groups": [
    "U2DDBkl3Ayg0PWudzhI"
  ]
}
```

After the validation of permission for given uuid, permission for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the permission",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "assessment_authoring.summative_assessment.edit",
    "description": "edit permission",
    "application_id": "Dfchd56otyghfgfjioiK",
    "module_id": "55txEec45pVMf6Akvcew",
    "action_id": "44qxEpc35pVMb6AkZGbi",
    "user_groups": [
      "U2DDBkl3Ayg0PWudzhI"
    ]
  }
}
```

If the permission is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a Permission:

To delete a permission, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/permission/{uuid}`** where **`uuid`** is the unique ID of the permission.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the permission"
}
```

If the permission is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```

### Search all permissions:

To search the permissions available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1//permission/search`** with **`skip`** , **`limit`** where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of permissions array to be returned which takes a default value **`10`**, **`search_query`** is query parm to fetch permission.


Then the response would be as follows: 

```json
{
    "success": true,
    "message": "Successfully fetched the permissions",
    "data": [
        {
            "name": "admin",
            "description": "Description for permission",
            "application_id": {
                "uuid": "A9VHdDD2mjpLQe1nULHi",
                "name": "ContentManagement",
                "description": "Description for application"
            },
            "module_id": {
                "uuid": "IOb3DCZYPZbLVU4sMANx",
                "name": "Assessment",
                "description": "Description for module"
            },
            "action_id": {
                "uuid": "HgGzCoTOEilE3HBHztet",
                "name": "create",
                "description": "Description for action"
            },
            "user_groups": [
                {
                    "uuid": "0XejbYpJTouaQA16HbCD",
                    "name": "9ef71b60-82ba-4dce-a21b-ea7ac0565920",
                    "description": "DEscription for Assessor group"
                }
            ],
            "uuid": "vIdHRti4bA4i2Je9Mhev",
            "created_time": "2023-02-28 05:42:38.726113+00:00",
            "last_modified_time": "2023-02-28 05:42:38.903716+00:00"
        }
    ]
}
``` 

### Get unique permission filters:

To fetch all the unique values with uuid and name for applications, modules, actions and user_groups, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1//permission_filter/unique`**

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the unique values for applications, modules, actions and user_groups.",
  "data": {
    "applications": [
      {"uuid": "124hsgxR77QKS8uS7Zgm", "name": "content management"} ],
    "modules": [
      {"uuid": "124hsgxR77QKS8uioZgm", "name": "learning resource"}],
    "actions": [
      {"uuid": "1579jkR77QKS8uS7Zgm", "name": "edit"}],
    "user_groups": [
      {"uuid": "147dvlgxR77QKS8uS76", "name": "assessors"}]
  }
}
```
