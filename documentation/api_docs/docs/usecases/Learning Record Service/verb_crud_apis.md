---
sidebar_label: CRUD APIs for Verb
sidebar_position: 1
---

# CRUD APIs for Verb

The following steps are regarding the CRUD APIs for Verbs


### Create a Verb

To create a Verb, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/verb`** .

The request body for the API is as follows:

```json
{
  "name": "played",
  "url": "http://activitystrea.ms/schema/1.0/play",
  "canonical_data": {
    "name": {
      "en-US": "Played"
    },
    "description": {
      "en-US": "Indicates that the actor spent some time enjoying the object. For example, if the object is a video this indicates that the subject watched all or part of the video. The \"play\" verb is a more specific form of the \"consume\" verb."
    }
  }
}
```

If a verb with the same name as the above payload already exists then **`ConflictError`** exception is raised.

If the response is successful then a new Verb with the request body details and with a new uuid(unique ID of the Verb) is added. After successfully adding new Verb document to the collection, you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the verb",
  "data": {
    "name": "played",
    "url": "http://activitystrea.ms/schema/1.0/play",
    "canonical_data": {
      "name": {
        "en-US": "Played"
      },
      "description": {
        "en-US": "Indicates that the actor spent some time enjoying the object. For example, if the object is a video this indicates that the subject watched all or part of the video. The \"play\" verb is a more specific form of the \"consume\" verb."
      }
    },
    "uuid": "X0gxRZC00k4obcBX4acH",
    "created_time": "2022-09-01 06:40:34.829486+00:00",
    "last_modified_time": "2022-09-01 06:40:35.431771+00:00"
  }
}
```

### Get all Verbs

When we need to fetch all the Verbs available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/verb`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of Verb array to be returned which takes a default value **`10`** if not provided. This will fetch the list of Verbs.

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "name": "played",
      "url": "http://activitystrea.ms/schema/1.0/play",
      "canonical_data": {
        "name": {
          "en-US": "Played"
        },
        "description": {
          "en-US": "Indicates that the actor spent some time enjoying the object. For example, if the object is a video this indicates that the subject watched all or part of the video. The \"play\" verb is a more specific form of the \"consume\" verb."
        }
      },
      "uuid": "X0gxRZC00k4obcBX4acH",
      "created_time": "2022-09-01 06:40:34.829486+00:00",
      "last_modified_time": "2022-09-01 06:40:35.431771+00:00"
    }
  ]
}
```

### Get a specific Verb

When we need to fetch the details of a specific Verb then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/verb/{uuid}`** where **`uuid`** is the unique ID of the verb.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the verb",
  "data": {
    "name": "played",
    "url": "http://activitystrea.ms/schema/1.0/play",
    "canonical_data": {
      "name": {
        "en-US": "Played"
      },
      "description": {
        "en-US": "Indicates that the actor spent some time enjoying the object. For example, if the object is a video this indicates that the subject watched all or part of the video. The \"play\" verb is a more specific form of the \"consume\" verb."
      }
    },
    "uuid": "X0gxRZC00k4obcBX4acH",
    "created_time": "2022-09-01 06:40:34.829486+00:00",
    "last_modified_time": "2022-09-01 06:40:35.431771+00:00"
  }
}
```

If the Verb is not present for a given uuid - **`zxtPzcjdkl5JvVGjl01j`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Verb with uuid zxtPzcjdkl5JvVGjl01j not found",
  "data": null
}
```

### Update a Verb:

When we need to update the details of a Verb then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/verb/{uuid}`** where **`uuid`** is the unique ID of the Verb.
The request body would be as follows:

```json
{
  "name": "Updated Verb"
}
```

After the validation of Verb for given uuid, Verb for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the verb",
  "data": {
    "name": "Updated Verb",
    "url": "http://activitystrea.ms/schema/1.0/play",
    "canonical_data": {
      "name": {
        "en-US": "Played"
      },
      "description": {
        "en-US": "Indicates that the actor spent some time enjoying the object. For example, if the object is a video this indicates that the subject watched all or part of the video. The \"play\" verb is a more specific form of the \"consume\" verb."
      }
    },
    "uuid": "X0gxRZC00k4obcBX4acH",
    "created_time": "2022-09-01 06:40:34.829486+00:00",
    "last_modified_time": "2022-09-01 07:04:19.943168+00:00"
  }
}
```

If the Verb is not present for a given uuid - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Verb with uuid o1nv13n6sbu0ny not found",
  "data": null
}
```

### Delete a Verb:

When we need to delete a Verb then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/verb/{uuid}`** where **`uuid`** is the unique ID of the Verb.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the Verb"
}
```

If the Verb is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Verb with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```
