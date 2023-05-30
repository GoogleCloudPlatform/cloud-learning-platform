---
sidebar_label: CRUD APIs for Learning Experience
sidebar_position: 1
---

# CRUD APIs for Learner Experience

The following steps are to create, view and update Learning Experience.


### Create a learning experience:

To create a learning experience, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-experience`**.
The request body for the API is as follows:

```json
{
  "name": "Kubernetes",
  "display_name": "Kubernetes",
  "description": "",
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
    "assessments": []
  },
  "parent_nodes": {
    "learning_opportunities": [],
    "curriculum_pathways": []
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

A new learning experience with the request body details and with a new uuid(unique ID of the learning experience) is added to the learning experience. After successfully adding new learning experience document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the learning experience",
  "data": {
    "name": "Kubernetes",
    "display_name": "Kubernetes",
    "description": "",
    "author": "TestUser",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {
      "learning_objects": []
    },
    "parent_nodes": {
      "learning_opportunities": [],
      "curriculum_pathways": []
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
    "uuid": "fMxRymndXeBgZhRGXSaz",
    "version": 1,
    "is_archived": false,
    "parent_version_uuid": "",
    "root_version_uuid": "fMxRymndXeBgZhRGXSaz",
    "created_time": "2022-11-15 12:13:01.174422+00:00",
    "last_modified_time": "2022-11-15 12:13:01.548783+00:00"
  }
}
```

### Get all learning experience:

When we need to fetch all the learning experiences available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-experience`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of learning experience array to be returned which takes a default value **`10`** if not provided. This will fetch the list of learning experiences.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": [
    {
      "name": "Kubernetes",
      "display_name": "Kubernetes",
      "description": "",
      "author": "TestUser",
      "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
      },
      "references": {
        "competencies": [],
        "skills": []
      },
      "child_nodes": {
        "learning_objects": []
      },
      "parent_nodes": {
        "learning_opportunities": [],
        "curriculum_pathways": []
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
      "uuid": "fMxRymndXeBgZhRGXSaz",
      "version": 1,
      "is_archived": false,
      "parent_version_uuid": "",
      "root_version_uuid": "fMxRymndXeBgZhRGXSaz",
      "created_time": "2022-11-15 12:13:01.174422+00:00",
      "last_modified_time": "2022-11-15 12:13:01.548783+00:00"
    }
  ]
}
```

### Get a specific learning experience:

When we need to fetch the details of a specific learning experience then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-experience/{uuid}`** where **`uuid`** is the unique ID of the learning experience.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the learning experiences",
  "data": {
    "name": "Kubernetes",
    "display_name": "Kubernetes",
    "description": "",
    "author": "TestUser",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {
      "learning_objects": []
    },
    "parent_nodes": {
      "learning_opportunities": [],
      "curriculum_pathways": []
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
    "uuid": "fMxRymndXeBgZhRGXSaz",
    "version": 1,
    "is_archived": false,
    "parent_version_uuid": "",
    "root_version_uuid": "fMxRymndXeBgZhRGXSaz",
    "created_time": "2022-11-15 12:13:01.174422+00:00",
    "last_modified_time": "2022-11-15 12:13:01.548783+00:00"
  }
}
```

If the learning experience is not present for a given learning_experience_id - **`zxtPzcjdkl5JvVGjl01j`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Experience with uuid zxtPzcjdkl5JvVGjl01j not found",
  "data": null
}
```

### Update a learning experience:

When we need to update the details of a learning experience then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-experience/{uuid}`** where **`uuid`** is the unique ID of the learning experience.
The request body would be as follows:

```json
{
  "name": "Kubernetes",
  "display_name": "Kubernetes",
  "description": "",
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
    "learning_objects": []
  },
  "parent_nodes": {
    "learning_opportunities": [],
    "curriculum_pathways": []
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

After the validation of learning experience for given learning_experience_id, learning experience for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the learning experience",
  "data": {
    "name": "Kubernetes",
    "display_name": "Kubernetes",
    "description": "",
    "author": "TestUser",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {
      "learning_objects": []
    },
    "parent_nodes": {
      "learning_opportunities": [],
      "curriculum_pathways": []
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
    "uuid": "fMxRymndXeBgZhRGXSaz",
    "version": 1,
    "is_archived": false,
    "parent_version_uuid": "",
    "root_version_uuid": "fMxRymndXeBgZhRGXSaz",
    "created_time": "2022-11-15 12:13:01.174422+00:00",
    "last_modified_time": "2022-11-15 12:15:20.966679+00:00"
  }
}

```
If the learning experience is not present for a given learning_experience_id - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Experience with uuid o1nv13n6sbu0ny not found",
  "data": null
}
```

### Delete a learner experience:

When we need to delete a learning experience then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-experience/{uuid}`** where **`uuid`** is the unique ID of the learning experience.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the learning experience"
}
```

If the learning experience is not present for a given learning_experience_id - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Experience with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```