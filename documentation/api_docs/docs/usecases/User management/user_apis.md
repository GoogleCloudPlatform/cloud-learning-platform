---
sidebar_label: CRUD APIs for User
sidebar_position: 1
---

# CRUD APIs for User

The following steps are to create, view and update user.


### Create a user:

To create a user, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/user`** with query parameter  **`create_inpsace_user`** to create an inspace user along with the gpcore user.
The request body for the API is as follows:

```json
{
  "first_name": "steve",
  "last_name": "jobs",
  "email": "steve.jobs@example.com",
  "user_type": "learner",
  "user_groups": [
    "44qxEpc35pVMb6AkZGbi"
  ],
  "status": "active",
  "is_registered": true,
  "failed_login_attempts_count": 0,
  "access_api_docs": false,
  "gaia_id": "F2GGRg5etyty"
}
```

Here, in the above request body, only `first_name`, `last_name`, `email`, and `user_type` are the required fields. Rest are optional.

Once the above request is sent, a new user with the request body details and with a new user_id (unique ID of the user) is added to the Users collection and this user will also get added to the given usergroups.
Along with the User, an Agent is also created in the Agents collection.
Depending on the `user_type`:
If the `user_type` is `learner`, a Learner is added in the Learners collection, and a Learner Profile is created, with `first_name`, `last_name`, and `email` as mentioned in the request body.
If the `user_type` is `faculty`, a Staff is added in the Staffs collection, with `first_name`, `last_name`, and `email` as mentioned in the request body.
If the query param **`create_inpsace_user`** is set **`true`**, an inspace user is created along with the gpcore user.
After successfully adding new user document to the collection, the response will be similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created User and corresponding agent",
  "data": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "first_name": "steve",
    "last_name": "jobs",
    "email": "steve.jobs@example.com",
    "user_type": "learner",
    "user_type_ref": "U2DDBkl3Ayg0PWudzhI",
    "user_groups": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "status": "active",
    "is_registered": true,
    "failed_login_attempts_count": 0,
    "access_api_docs": false,
    "gaia_id": "F2GGRg5etyty",
    "photo_url" :"//lh3.googleusercontent.com/a/default-user",
    "inspace_user": {
      "is_inspace_user": true,
      "inspace_user_id": 123456
    }
  }
}
```

### Get all users:

To fetch all the users available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/users`** with **`skip`**, **`limit`** , **`fetch_tree`**, **`user_type`** , **`user_group`**  and **`status`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of learning experience array to be returned which takes a default value **`10`** if not provided,  **`fetch_tree`** is to fetch the complete object when set **`true`** if not it takes the default value **`false`** returning only UUID, **`user_type`** is to fetcg a user of provided type, **`user_group`** is to fetch users of provided group and **`status`** is to fetch the user of provided satus.
Following are the query parameters that can be used to filter the response:
| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| sort_by | Literal["first_name", "last_name", "email", "created_time"] | field by which the submitted assessments will be sorted. (default="created_time") |
| sort_order |  Literal["ascending", "descending"] | Ascending or Descending sort (default="descending") |
Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "user_id": "124hsgxR77QKS8uS7Zgm",
      "first_name": "steve",
      "last_name": "jobs",
      "email": "steve.jobs@example.com",
      "user_type": "learner",
      "user_type_ref": "U2DDBkl3Ayg0PWudzhI",
      "user_groups": [
        "44qxEpc35pVMb6AkZGbi"
      ],
      "status": "active",
      "is_registered": true,
      "failed_login_attempts_count": 0,
      "access_api_docs": false,
      "gaia_id": "F2GGRg5etyty"
    }
  ]
}
```

### Get a specific user:

To fetch the details of a specific user, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/{user_id}`** where **`user_id`** is the unique ID of the user and the query parameter  **`fetch_tree`** is to fetch the complete object when set **`true`** if not it takes the default value **`false`** returning only UUID

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the user",
  "data": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "first_name": "steve",
    "last_name": "jobs",
    "email": "steve.jobs@example.com",
    "user_type": "learner",
    "user_type_ref": "U2DDBkl3Ayg0PWudzhI",
    "user_groups": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "status": "active",
    "is_registered": true,
    "failed_login_attempts_count": 0,
    "access_api_docs": false,
    "gaia_id": "F2GGRg5etyty"
  }
}
```

If the user is not present for a given user_id - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": {}
}
```

### Update a user:

To update the details of a user, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/{user_id}`** where **`user_id`** is the unique ID of the user.
The request body would be as follows:

```json
{
  "first_name": "steve",
  "last_name": "jobs",
  "user_groups": [
    "44qxEpc35pVMb6AkZGbi"
  ],
  "access_api_docs": false
}
```

After the validation of user for given user_id, user for the given user_id is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the user",
  "data": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "first_name": "steve",
    "last_name": "jobs",
    "email": "steve.jobs@example.com",
    "user_type": "learner",
    "user_type_ref": "U2DDBkl3Ayg0PWudzhI",
    "user_groups": [
      "44qxEpc35pVMb6AkZGbi"
    ],
    "status": "active",
    "is_registered": true,
    "failed_login_attempts_count": 0,
    "access_api_docs": false,
    "gaia_id": "F2GGRg5etyty"
  }
}
```

If the user is not present for a given user_id - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a User:

To delete a user, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/{user_id}`** where **`user_id`** is the unique ID of the user. A deleted user will also be removed from any associated user groups.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the user and associated agent, learner/faculty"
}
```

If the user is not present for a given user_id - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```

### Search a user by email

To search a user Record based on the `email` of the user Record, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/search/email`**, where **`email`** is the email that is to be searched. This will fetch all the user Records that has email as **`email`**. Please note - here, the exact matching is used i.e. only the user records whose `email` is **`email`** are fetched.

The response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the learners",
  "data": [
    {
      "user_id": "124hsgxR77QKS8uS7Zgm",
      "first_name": "steve",
      "last_name": "jobs",
      "email": "steve.jobs@example.com",
      "user_type": "learner",
      "user_type_ref": "U2DDBkl3Ayg0PWudzhI",
      "user_groups": [
        "44qxEpc35pVMb6AkZGbi"
      ],
      "status": "active",
      "is_registered": true,
      "failed_login_attempts_count": 0,
      "access_api_docs": false,
      "gaia_id": "F2GGRg5etyty"
    }
  ]
}
```

### Import Learners From Json File

To import learners from JSON file, we would make a **POST** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/import/json`**, along with **`json_file`** of type binary consisting of learners.json_schema which matches the learner model. This will create the new users for all the entries in the file.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully created the users",
  "data": ["124hsgxR77QKS8uS7Zgm"]
}
```

### Update a user staus:

To update the details of a user we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/{user_id}/status`** where **`user_id`** is the unique ID of the user. A user is removed from the assigned user groups and is no longer allowed to access any APIs when their status changes from active to inactive.

The request body would be as follows:

```json
{
  "status": "inactive"
}
```

After the validation of user for given user_id, status for the given user_id is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the user",
  "data": {
    "user_id": "124hsgxR77QKS8uS7Zgm",
    "first_name": "steve",
    "last_name": "jobs",
    "email": "steve.jobs@example.com",
    "user_type": "learner",
    "user_type_ref": "U2DDBkl3Ayg0PWudzhI",
    "user_groups": [],
    "status": "inactive",
    "is_registered": true,
    "failed_login_attempts_count": 0,
    "access_api_docs": false,
    "gaia_id": "F2GGRg5etyty"
  }
}
```

If the user is not present for a given user_id - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Search users

To filter users based on the provided `search_query`, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/search`**, where **`search_query`** is the key that is to be searched against email, first name and last name of the users along with query parameters **`skip`**, **`limit`**  where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of users list to be returned which takes a default value **`10`** if not provided

The response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the learners",
  "data": [
    {
      "user_id": "124hsgxR77QKS8uS7Zgm",
      "first_name": "steve",
      "last_name": "jobs",
      "email": "steve.jobs@example.com",
      "user_type": "learner",
      "user_type_ref": "U2DDBkl3Ayg0PWudzhI",
      "user_groups": [
        "44qxEpc35pVMb6AkZGbi"
      ],
      "status": "active",
      "is_registered": true,
      "failed_login_attempts_count": 0,
      "access_api_docs": false,
      "gaia_id": "F2GGRg5etyty"
    }
  ]
}
```

### Get Applications of user

To get all the applications for which user has access, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/{user_id}/applications`**, where **`user_id`** is the unique ID of the user.

The response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched applications assigned to the user",
  "data": {
    "applications": [
      {
        "application_name": "content management",
        "application_id": "RT34swyyiutdhjiiou"
      }
    ]
  } 
}
```

### Get User Groups of user

To get all the Usergroups to which the user is added, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/user/{user_id}/user-groups`**  with **`immutable`** as optional param  and **`user_id`** is the unique ID of the user. 
To get only immutable user groups of a user, then the **`immutable`** should be sent as **`True`**
To get only mutable user groups of a user, then the **`immutable`** should be sent as **`False`**
To get all the usergroups to which user is added then the **`immutable`** param is not required or can be sent as **`None`**

The response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched user groups the user",
  "data": [
    {
        "name": "learner",
        "uuid": "44qxEpc35pVMb6AkZGbi",
        "description": "group of learners"
    },
    {
        "name": "assessor",
        "uuid": "1qchPPgeBXs2ZvK7QIjy",
        "description": "group of assessors"
    }
  ]
    
}
```


