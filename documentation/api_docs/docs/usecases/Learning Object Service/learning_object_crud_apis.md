---
sidebar_label: CRUD APIs for Learning Object
sidebar_position: 2
---

# CRUD APIs for Learner Object

The following steps are to create, view and update Learning object.


### Create a learning object:

To create a learning object, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object`**.
The request body for the API is as follows:

```json
{
  "name": "Online presentation",
  "display_name": "Online presentation",
  "description": "testing out online ppt",
  "author": "TestUser",
  "alignments": {
    "competency_alignments": [],
    "skill_alignments": []
  },
  "references": {
    "skills": [],
    "competencies": []
  },
  "child_nodes": {
    "learning_objects": [],
    "learning_resources": [],
    "assessments": []
  },
  "parent_nodes": {
    "learning_experiences": [],
    "learning_objects": []
  },
  "metadata": {},
  "achievements": [],
  "completion_criteria": {
    "curriculum_pathways": [],
    "learning_experiences": [],
    "learning_objects": [],
    "learning_resources": [],
    "assessments": []
  },
  "prerequisites": {
    "curriculum_pathways": [],
    "learning_experiences": [],
    "learning_objects": [],
    "learning_resources": [],
    "assessments": []
  },
  "is_locked": false
}
```

A new learning object with the request body details and with a new uuid(unique ID of the learning object) is added to the learning object. After successfully adding new learning object document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the learning object",
  "data": {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Online presentation",
    "display_name": "Online presentation",
    "description": "testing out online ppt",
    "author": "TestUser",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "references": {
      "skills": [],
      "competencies": []
    },
    "child_nodes": {
      "learning_objects": [],
      "learning_resources": [],
      "assessments": []
    },
    "parent_nodes": {
      "learning_experiences": [],
      "learning_objects": []
    },
    "metadata": {},
    "achievements": [],
    "completion_criteria": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": []
    },
    "prerequisites": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": []
    },
    "is_locked": false,
    "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "",
    "is_archived": false,
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

### Get all learning object:

When we need to fetch all the learning objects available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object`** with **`skip`**, **`limit`** and **relation** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided, **`limit`** is the size of learning experience array to be returned which takes a default value **`10`** if not provided and **`relation`** points where to filter the learning object, from parent_nodes or child_nodes which takes a default value **`child`** if not provided This will fetch the list of learning objects.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": {
    "records": [
    {
      "uuid": "asd98798as7dhjgkjsdfh",
      "name": "Online presentation",
      "display_name": "Online presentation",
      "description": "testing out online ppt",
      "author": "TestUser",
      "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
      },
      "references": {
        "skills": [],
        "competencies": []
      },
      "child_nodes": {
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
      },
      "metadata": {},
      "achievements": [],
      "completion_criteria": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "prerequisites": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "is_locked": false,
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "",
      "is_archived": false,
      "created_time": "2022-03-03 09:22:49.843674+00:00",
      "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
    },
    {
      "uuid": "pfrrthgvhjghf7dhjgkjsh",
      "name": "Online presentation 2",
      "display_name": "Online presentation 2",
      "description": "testing out online ppt 2",
      "author": "TestUser",
      "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
      },
      "references": {
        "skills": [],
        "competencies": []
      },
      "child_nodes": {
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
      },
      "metadata": {},
      "achievements": [],
      "completion_criteria": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "prerequisites": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "is_locked": false,
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "",
      "is_archived": false,
      "created_time": "2022-03-03 09:22:49.843674+00:00",
      "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
    }
  ],
    "total_count": 10000
  }
}
```

### Get a specific learning object:

When we need to fetch the details of a specific learning object then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object/{uuid}`** where **`uuid`** is the unique ID of the learning object.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the learning object",
  "data": [
    {
      "uuid": "asd98798as7dhjgkjsdfh",
      "name": "Online presentation",
      "display_name": "Online presentation",
      "description": "testing out online ppt",
      "author": "TestUser",
      "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
      },
      "references": {
        "skills": [],
        "competencies": []
      },
      "child_nodes": {
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
      },
      "metadata": {},
      "achievements": [],
      "completion_criteria": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "prerequisites": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "is_locked": false,
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "",
      "is_archived": false,
      "created_time": "2022-03-03 09:22:49.843674+00:00",
      "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
    }
  ]
}
```

If the learning object is not present for a given learning_object_id - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Object with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Update a learning object:

When we need to update the details of a learning object then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object/{uuid}`** where **`uuid`** is the unique ID of the learning object.
The request body would be as follows:

```json
{
  "name": "Online presentation",
  "display_name": "Online presentation",
  "description": "testing out online ppt",
  "author": "TestUser",
  "alignments": {
    "competency_alignments": [],
    "skill_alignments": []
  },
  "references": {
    "skills": [],
    "competencies": []
  },
  "child_nodes": {
    "learning_objects": [],
    "learning_resources": [],
    "assessments": []
  },
  "parent_nodes": {
    "learning_experiences": [],
    "learning_objects": []
  },
  "metadata": {},
  "achievements": [],
  "completion_criteria": {
    "curriculum_pathways": [],
    "learning_experiences": [],
    "learning_objects": [],
    "learning_resources": [],
    "assessments": []
  },
  "prerequisites": {
    "curriculum_pathways": [],
    "learning_experiences": [],
    "learning_objects": [],
    "learning_resources": [],
    "assessments": []
  },
  "is_locked": false
}
```

After the validation of learning object for given learning_object_id, learning object for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the learning object",
  "data":    {
      "uuid": "asd98798as7dhjgkjsdfh",
      "name": "Online presentation",
      "display_name": "Online presentation",
      "description": "testing out online ppt",
      "author": "TestUser",
      "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
      },
      "references": {
        "skills": [],
        "competencies": []
      },
      "child_nodes": {
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
      },
      "metadata": {},
      "achievements": [],
      "completion_criteria": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "prerequisites": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": []
      },
      "is_locked": false,
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "",
      "is_archived": false,
      "created_time": "2022-03-03 09:22:49.843674+00:00",
      "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
    }
}
```

If the learning object is not present for a given learining_object_id - **`JAnZNzyh490mbPoE5StZ`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Object with uuid JAnZNzyh490mbPoE5StZ not found",
  "data": null
}
```

### Delete a learner object:

When we need to delete a learning object then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object/{uuid}`** where **`uuid`** is the unique ID of the learning object.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the learning object"
}
```

If the learning object is not present for a given learning_object_id - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Object with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```
