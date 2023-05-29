---
sidebar_label: CRUD APIs for Activity State
sidebar_position: 4
---

# CRUD APIs for Activity State

The following steps are regarding the CRUD APIs for Activity states


### Create an Activity State

To create an Activity State, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity-state`** .

The request body for the API is as follows:

```json
{
  "agent_id": "rZl9p7gGEGoVM3CUDxau",
  "activity_id": "adh9p7gGEGoVM3CUDhtf",
  "canonical_data": {}
}
```

A new Activity State with the request body details and with a new uuid(unique ID of the Activity State) is added. After successfully adding new Activity State document to the collection, you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the activity state",
  "data": {
    "agent_id": "rZl9p7gGEGoVM3CUDxau",
    "activity_id": "adh9p7gGEGoVM3CUDhtf",
    "canonical_data": {},
    "uuid": "vI9wSexRl2Uf5ws4uaCe",
    "created_time": "2022-09-01 07:39:34.690999+00:00",
    "last_modified_time": "2022-09-01 07:39:35.011675+00:00"
  }
}

```

### Get all Activity states

When we need to fetch all the Activity states available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity-state`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of Activity State array to be returned which takes a default value **`10`** if not provided. This will fetch the list of Activity states.

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "uuid": "1Tusjz6W1JI2aFr4SiIw",
      "created_time": "2022-03-03 09:22:49.843674+00:00",
      "last_modified_time": "2022-03-03 09:22:49.843674+00:00",
      "agent_id": "e05aa883-acaf-40ad-bf54-02c8ce485fb0",
      "activity_id": "12345678-1234-5678-1234-567812345678",
      "canonical_data": {}
    }
  ]
}
```

### Get a specific Activity State

When we need to fetch the details of a specific Activity State then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity-state/{uuid}`** where **`uuid`** is the unique ID of the activity state.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the activity state",
  "data": {
    "agent_id": "rZl9p7gGEGoVM3CUDxau",
    "activity_id": "adh9p7gGEGoVM3CUDhtf",
    "canonical_data": {},
    "uuid": "vI9wSexRl2Uf5ws4uaCe",
    "created_time": "2022-09-01 07:39:34.690999+00:00",
    "last_modified_time": "2022-09-01 07:39:35.011675+00:00"
  }
}
```

If the Activity State is not present for a given uuid - **`zxtPzcjdkl5JvVGjl01j`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Activity State with uuid zxtPzcjdkl5JvVGjl01j not found",
  "data": null
}
```

### Update a Activity State:

When we need to update the details of a Activity State then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity-state/{uuid}`** where **`uuid`** is the unique ID of the Activity State.
The request body would be as follows:

```json
{
   "canonical_data":{
      "current_state":"state_1",
      "key_2":"value_2"
   }
}
```

After the validation of Activity State for given uuid, Activity State for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the activity state",
  "data": {
    "agent_id": "rZl9p7gGEGoVM3CUDxau",
    "activity_id": "adh9p7gGEGoVM3CUDhtf",
    "canonical_data": {
      "key_2": "value_2",
      "current_state": "state_1"
    },
    "uuid": "vI9wSexRl2Uf5ws4uaCe",
    "created_time": "2022-09-01 07:39:34.690999+00:00",
    "last_modified_time": "2022-09-01 07:43:46.803296+00:00"
  }
}
```
If the Activity State is not present for a given uuid - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Activity State with uuid o1nv13n6sbu0ny not found",
  "data": null
}
```

### Delete a Activity State:

When we need to delete an Activity State then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity-state/{uuid}`** where **`uuid`** is the unique ID of the Activity State.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the Activity State"
}
```

If the Activity State is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Activity State with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```