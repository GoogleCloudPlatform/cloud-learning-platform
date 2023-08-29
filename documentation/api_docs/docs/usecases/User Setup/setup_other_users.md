---
sidebar_label: Setting up other user types
sidebar_position: 2
---

# Setting up other user types

The following steps need to be followed to setup a user of any type other than Learner.

<!-- :::note

**`APP_URL`** used in the below URLs is **<https://snhu-glidepath-dev-api.cloudpssolutions.com>**

::: -->

### Create other type of User (eg: faculty):

A new user with desired user_type (eg: Faculty) needs to be created in the Users collection.
To create a new user of faculty type, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/user`**.
The request body for the API is as follows:

```json
{
  "first_name": "jon",
  "last_name": "doe",
  "email": "jon.doe@example.com",
  "user_type": "faculty",
  "user_type_ref": "",
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

A new user of faculty type with the request body details and new user_id (unique ID of the user) will get added to the Users collection and this user will also get added to the given usergroups. After successful execution, response will be similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the user",
  "data": {
    "user_id": "hsgxR77QKS8uS7Zgm",
    "first_name": "jon",
    "last_name": "doe",
    "email": "jon.doe@example.com",
    "user_type": "faculty",
    "user_type_ref": "",
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

### Create an Agent:

An Agent object needs to be created for the newly created faculty user.
To create an Agent, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/agent`**

The request body for the API is as follows:

```json
{
  "object_type": "agent",
  "name": "jon doe",
  "mbox": "mailto:jon.doe@example.com",
  "mbox_sha1sum": "",
  "open_id": "",
  "account_homepage": "",
  "account_name": "jon_doe",
  "members": [],
  "user_id": "hsgxR77QKS8uS7Zgm"
}
```

The **`user_id`** in the above input payload is the existing user's id in the firestore collection and it will be used as reference in the Agent data model. If the user is not present, a **`ResourceNotFoundException`** exception is raised. It is necessary to create a user before accessing the same user id in the Agent data model in order to prevent this.

If an agent already exists with the same **`user_id`** then **`ConflictError`** exception is raised.

If the response is successful then a new Agent with the request body details and with a new uuid(unique ID of the Agent) is added. After successfully adding new Agent document to the collection, you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the agent",
  "data": {
    "object_type": "agent",
    "name": "jon.doe@example.com",
    "mbox": "mailto:jon.doe@example.com",
    "mbox_sha1sum": "",
    "open_id": "",
    "account_homepage": "",
    "account_name": "jon_doe",
    "members": [],
    "user_id": "hsgxR77QKS8uS7Zgm",
    "uuid": "fJoM6HpyV5K7kmKE",
    "created_time": "2022-09-01 07:13:34.801165+00:00",
    "last_modified_time": "2022-09-01 07:13:35.001616+00:00"
  }
}
```