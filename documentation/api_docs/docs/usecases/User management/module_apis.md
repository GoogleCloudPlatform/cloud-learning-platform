---
sidebar_label: CRUD APIs for Module
sidebar_position: 5
---

# CRUD APIs for Module

The following steps are to create, view and update module.


### Create a module:

To create a module, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/module`**. The name field in the request body should be unique for every module creation.
The request body for the API is as follows:

```json
{
  "name": "learning resource",
  "description": "learning resource module",
  "actions": [
    "44qxEpc35pVMb6AkZGbi"
  ]
}
```

A new module with the request body details and with a new uuid(unique ID of the module) is added to the module. After successfully adding new module document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the module",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "learning resource",
    "description": "learning resource module",
    "actions": [
      "44qxEpc35pVMb6AkZGbi"
    ]
  }
}
```

### Get all modules:

To fetch all the modules available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/modules`** with **`skip`** , **`limit`** and **`fetch_tree`** where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of module array to be returned which takes a default value **`10`**, **`fetch_tree`** is to fetch the complete action tree when set **`true`** if not it takes the default value **`false`** returning only action UUID.


Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the module",
  "data": {
    "records": [{
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "learning resource",
    "description": "learning resource module",
    "actions": [
      "44qxEpc35pVMb6AkZGbi"
    ]
  }],
    "total_count": 10000
  }
}
```

### Get a specific module:

To fetch the details of a specific module, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/module/{uuid}`** where **`uuid`** is the unique ID of the module and query parameter **`fetch_tree`** is to fetch the complete action tree when set **`true`** if not it takes the default value **`false`** returning only action UUID.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the module",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "learning resource",
    "description": "learning resource module",
    "actions": [
      "44qxEpc35pVMb6AkZGbi"
    ]
  }
}
```

If the module is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update a module:

To update the details of a module, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/module/{uuid}`** where **`uuid`** is the unique ID of the module. The name field in the request body should be unique for every module updation.
The request body would be as follows:

```json
{
  "name": "learning resource",
  "description": "learning resource module",
  "actions": [
    "44qxEpc35pVMb6AkZGbi"
  ]
}
```

After the validation of module for given uuid, module for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the module",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "learning resource",
    "description": "learning resource module",
    "actions": [
      "44qxEpc35pVMb6AkZGbi"
    ]
  }
}
```

If the module is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a Module:

To delete a module, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/module/{uuid}`** where **`uuid`** is the unique ID of the module.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the module"
}
```

If the module is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```
