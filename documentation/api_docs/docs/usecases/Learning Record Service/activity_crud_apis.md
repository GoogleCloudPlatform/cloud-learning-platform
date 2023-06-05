---
sidebar_label: CRUD APIs for Activity
sidebar_position: 3
---

# CRUD APIs for Activity

The following steps are regarding the CRUD APIs for Activities


### Create an Activity

To create an Activity, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity`** .

The request body for the API is as follows:

```json
{
    "name": "Tin Can Prototypes Launcher",
    "authority": "",
    "canonical_data": {
        "id": "http://id.tincanapi.com/activity/tincan-prototypes/launcher",
        "definition": {
            "name": {
                "en-US": "Tin Can Prototypes Launcher"
            },
            "type": "http://id.tincanapi.com/activitytype/lms",
            "description": {
                "en-US": "A tool for launching the Tin Can prototypes. Simulates the role of an LMS in launching experiences."
            }
        }
    }
}

```

A new Activity with the request body details and with a new uuid(unique ID of the Activity) is added. After successfully adding new Activity document to the collection, you will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the activity",
  "data": {
    "name": "Tin Can Prototypes Launcher",
    "authority": "",
    "canonical_data": {
      "id": "http://id.tincanapi.com/activity/tincan-prototypes/launcher",
      "definition": {
        "type": "http://id.tincanapi.com/activitytype/lms",
        "name": {
          "en-US": "Tin Can Prototypes Launcher"
        },
        "description": {
          "en-US": "A tool for launching the Tin Can prototypes. Simulates the role of an LMS in launching experiences."
        }
      }
    },
    "uuid": "rZl9p7gGEGoVM3CUDxau",
    "created_time": "2022-09-01 07:33:09.750993+00:00",
    "last_modified_time": "2022-09-01 07:33:10.077393+00:00"
  }
}

```

### Get all Activities

When we need to fetch all the Activities available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of Activity array to be returned which takes a default value **`10`** if not provided. This will fetch the list of Activities.

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "name": "Tin Can Prototypes Launcher",
      "authority": "",
      "canonical_data": {
        "definition": {
          "description": {
            "en-US": "A tool for launching the Tin Can prototypes. Simulates the role of an LMS in launching experiences."
          },
          "type": "http://id.tincanapi.com/activitytype/lms",
          "name": {
            "en-US": "Tin Can Prototypes Launcher"
          }
        },
        "id": "http://id.tincanapi.com/activity/tincan-prototypes/launcher"
      },
      "uuid": "rZl9p7gGEGoVM3CUDxau",
      "created_time": "2022-09-01 07:33:09.750993+00:00",
      "last_modified_time": "2022-09-01 07:33:10.077393+00:00"
    }
  ]
}
```

### Get a specific Activity

When we need to fetch the details of a specific Activity then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity/{uuid}`** where **`uuid`** is the unique ID of the activity.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the activity",
  "data": {
    "name": "Tin Can Prototypes Launcher",
    "authority": "",
    "canonical_data": {
      "definition": {
        "name": {
          "en-US": "Tin Can Prototypes Launcher"
        },
        "type": "http://id.tincanapi.com/activitytype/lms",
        "description": {
          "en-US": "A tool for launching the Tin Can prototypes. Simulates the role of an LMS in launching experiences."
        }
      },
      "id": "http://id.tincanapi.com/activity/tincan-prototypes/launcher"
    },
    "uuid": "rZl9p7gGEGoVM3CUDxau",
    "created_time": "2022-09-01 07:33:09.750993+00:00",
    "last_modified_time": "2022-09-01 07:33:10.077393+00:00"
  }
}
```

If the Activity is not present for a given uuid - **`zxtPzcjdkl5JvVGjl01j`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Activity with uuid zxtPzcjdkl5JvVGjl01j not found",
  "data": null
}
```

### Update a Activity:

When we need to update the details of a Activity then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity/{uuid}`** where **`uuid`** is the unique ID of the Activity.
The request body would be as follows:

```json
{
  "name": "Updated Activity"
}
```

After the validation of Activity for given uuid, Activity for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the activity",
  "data": {
    "name": "Updated Activity",
    "authority": "",
    "canonical_data": {
      "id": "http://id.tincanapi.com/activity/tincan-prototypes/launcher",
      "definition": {
        "name": {
          "en-US": "Tin Can Prototypes Launcher"
        },
        "type": "http://id.tincanapi.com/activitytype/lms",
        "description": {
          "en-US": "A tool for launching the Tin Can prototypes. Simulates the role of an LMS in launching experiences."
        }
      }
    },
    "uuid": "rZl9p7gGEGoVM3CUDxau",
    "created_time": "2022-09-01 07:33:09.750993+00:00",
    "last_modified_time": "2022-09-01 07:35:27.355463+00:00"
  }
}
```
If the Activity is not present for a given uuid - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Activity with uuid o1nv13n6sbu0ny not found",
  "data": null
}
```

### Delete a Activity:

When we need to delete a Activity then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-record-service/api/v1/activity/{uuid}`** where **`uuid`** is the unique ID of the Activity.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the Activity"
}
```

If the Activity is not present for a given uuid - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Activity with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```