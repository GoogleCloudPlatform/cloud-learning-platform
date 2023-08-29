---
sidebar_label: CRUD APIs for Application
sidebar_position: 4
---

# CRUD APIs for Application

The following steps are to create, view and update application.


### Create a application:

To create a application, a **POST** request has to be made to the API endpoint - **`<APP_URL>/user-management/api/v1/application`**. The name field in the request body should be unique for every application creation.
The request body for the API is as follows:

```json
{
  "name": "content management",
  "description": "application for content creation",
  "modules": [
    "44qxEpc35pVMb6AkZGbi"
  ]
}
```

A new application with the request body details and with a new uuid(unique ID of the application) is added to the application. After successfully adding new application document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the application",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "content management",
    "description": "application for content creation",
    "modules": [
      "44qxEpc35pVMb6AkZGbi"
    ]
  }
}
```

### Get all applications:

To fetch all the applications available, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/applications`** with **`skip`** and **`limit`** where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of applications array to be returned which takes a default value **`10`**.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": {
    "records": [
    {
      "uuid": "124hsgxR77QKS8uS7Zgm",
      "name": "content management",
      "description": "application for content creation",
      "modules": [
        "44qxEpc35pVMb6AkZGbi"
      ]
    }
  ],
    "total_count": 10000
  }
}
```

### Get a specific application:

To fetch the details of a specific application, we would make a **GET** request to the API endpoint - **`<APP_URL>/user-management/api/v1/application/{uuid}`** where **`uuid`** is the unique ID of the application.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the application",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "content management",
    "description": "application for content creation",
    "modules": [
      "44qxEpc35pVMb6AkZGbi"
    ]
  }
}
```

If the application is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update a application:

To update the details of a application, we would make a **PUT** request to the API endpoint - **`<APP_URL>/user-management/api/v1/application/{uuid}`** where **`uuid`** is the unique ID of the application. The name field in the request body should be unique for every application updation.
The request body would be as follows:

```json
{
  "name": "content management",
  "description": "application for content creation",
  "modules": [
    "44qxEpc35pVMb6AkZGbi"
  ]
}
```

After the validation of application for given uuid, application for the given uuid is updated and the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully updated the application",
  "data": {
    "uuid": "124hsgxR77QKS8uS7Zgm",
    "name": "content management",
    "description": "application for content creation",
    "modules": [
      "44qxEpc35pVMb6AkZGbi"
    ]
  }
}
```

If the application is not present for a given uuid - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a Application:

To delete a application, we would make a **DELETE** request to the API endpoint - **`<APP_URL>/user-management/api/v1/application/{uuid}`** where **`uuid`** is the unique ID of the application.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the application"
}
```

If the application is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Resource with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```
