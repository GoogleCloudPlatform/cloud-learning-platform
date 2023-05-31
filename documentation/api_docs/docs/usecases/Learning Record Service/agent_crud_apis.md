---
sidebar_label: CRUD APIs for Agent
sidebar_position: 2
---

# CRUD APIs for Agent

The following steps are regarding the CRUD APIs for Agents


### Create an Agent

To create an Agent, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/agent`**

The request body for the API is as follows:

```json
{
  "object_type": "agent",
  "name": "Test Agent",
  "mbox": "mailto:test_agent@example.org",
  "mbox_sha1sum": "",
  "open_id": "",
  "account_homepage": "",
  "account_name": "test_account_name",
  "members": [],
  "user_id": "user_id_1234"
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
    "name": "Test Agent",
    "mbox": "mailto:test_agent@example.org",
    "mbox_sha1sum": "",
    "open_id": "",
    "account_homepage": "",
    "account_name": "test_account_name",
    "members": [],
    "user_id": "user_id_1234",
    "uuid": "AAVqfJoM6HpyV5K7kmKE",
    "created_time": "2022-09-01 07:13:34.801165+00:00",
    "last_modified_time": "2022-09-01 07:13:35.001616+00:00"
  }
}
```

### Get all Agents

When we need to fetch all the Agents available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/agent`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of Agent array to be returned which takes a default value **`10`** if not provided. This will fetch the list of Agents.

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "object_type": "agent",
      "name": "Test Agent",
      "mbox": "mailto:test_agent@example.org",
      "mbox_sha1sum": "",
      "open_id": "",
      "account_homepage": "",
      "account_name": "test_account_name",
      "members": [],
      "user_id": "user_id_1234",
      "uuid": "AAVqfJoM6HpyV5K7kmKE",
      "created_time": "2022-09-01 07:13:34.801165+00:00",
      "last_modified_time": "2022-09-01 07:13:35.001616+00:00"
    }
  ]
}
```

### Get a specific Agent

When we need to fetch the details of a specific Agent then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/agent/{uuid}`** where **`uuid`** is the unique ID of the agent.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the agent",
  "data": {
    "object_type": "agent",
    "name": "Test Agent",
    "mbox": "mailto:test_agent@example.org",
    "mbox_sha1sum": "",
    "open_id": "",
    "account_homepage": "",
    "account_name": "test_account_name",
    "members": [],
    "user_id": "user_id_1234",
    "uuid": "AAVqfJoM6HpyV5K7kmKE",
    "created_time": "2022-09-01 07:13:34.801165+00:00",
    "last_modified_time": "2022-09-01 07:13:35.001616+00:00"
  }
}
```

If the Agent is not present for a given uuid - **`zxtPzcjdkl5JvVGjl01j`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Agent with uuid zxtPzcjdkl5JvVGjl01j not found",
  "data": null
}
```

### Update an Agent:

When we need to update the details of an Agent then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/agent/{uuid}`** where **`uuid`** is the unique ID of the Agent.
The request body would be as follows:

```json
{
  "name": "Updated Agent"
}
```

After the validation of Agent for given uuid, Agent for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the agent",
  "data": {
    "object_type": "activities",
    "name": "Updated Agent",
    "mbox": "",
    "mbox_sha1sum": "",
    "open_id": "",
    "account_homepage": "",
    "account_name": "",
    "members": [],
    "user_id": "",
    "uuid": "AAVqfJoM6HpyV5K7kmKE",
    "created_time": "2022-09-01 07:13:34.801165+00:00",
    "last_modified_time": "2022-09-01 07:16:26.944046+00:00"
  }
}
```

If the Agent is not present for a given uuid - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Agent with uuid o1nv13n6sbu0ny not found",
  "data": null
}
```

### Delete a Agent:

When we need to delete a Agent then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/agent/{uuid}`** where **`uuid`** is the unique ID of the Agent.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the Agent"
}
```

If the Agent is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Agent with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```
