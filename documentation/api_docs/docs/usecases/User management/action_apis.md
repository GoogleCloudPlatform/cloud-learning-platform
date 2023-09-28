---
sidebar_label: CRUD APIs for Action
sidebar_position: 6
---

# CRUD APIs for Action

The following steps are to create, view and update action.


### Create a action:

To create a action, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/action`**. The name field in the request body should be unique for every action creation.
The request body for the API is as follows:

```json
{
  "name": "edit",
  "description": "Edit includes view and create permissions",
  "action_type": "other"
}
```

A new action with the request body details and a new uuid(unique ID of the action) is added to the action. After successfully adding new action document to the collection, the response would be similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the action",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "edit",
    "description": "edit includes view and create permissions",
    "action_type": "other"
  }
}
```

### Get All Actions:

 To fetch all the actions available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/actions`** with **`skip`** , **`limit`** and **`fetch_tree`** where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of applications array to be returned which takes a default value **`10`**.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": {
    "records": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "name": "edit",
      "description": "edit includes view and create permissions",
      "action_type": "other"
    }
  ],
    "total_count": 10000
  }
}
```

### Get a specific action:

To fetch the details of a specific action,we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/action/{uuid}`** where **`uuid`** is the unique ID of the action.
Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "name": "edit",
      "description": "edit includes view and create permissions",
      "action_type": "other"
    }
  ]
}
```

If the action is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update a action:

To update the details of a action, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/action/{uuid}`**, where **`uuid`** is the unique ID of the action. The name field in the request body should be unique for every action updation.
The request body would be as follows:

```json
{
  "name": "edit",
  "description": "edit includes view and create permissions",
  "action_type": "other"
}
```

After the validation of action for given uuid, action for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the action",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "edit",
    "description": "edit includes view and create permissions",
    "action_type": "other"
  }
}
```

If the action is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a Action:

To delete a action, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/action/{uuid}`** where **`uuid`** is the unique ID of the action.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the action"
}
```

If the action is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```
