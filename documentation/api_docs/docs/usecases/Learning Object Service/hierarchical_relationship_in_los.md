---
sidebar_label: Hierarchical Relationship In Learning Object Service
sidebar_position: 4
---

# Hierarchical Relationship In Learning Object Service

The following steps to establish the heirarchical relationship in learning object service

### Associate the learning object with the learning experience

First, you need to create a learning experience, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-experience`**.

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

A new learning experience with the request body details and with a new uuid(unique ID of the learning experience) is added to the learning experience.

The response body for the API is as follows:

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

Now, create a learning object containing the **`uuid`** of the above learning experince in **`parent_nodes`** field. A **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object`**.

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
    "learning_experiences": ["fMxRymndXeBgZhRGXSaz"],
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

After successfully adding learning object document to the collection. Learning object gets associated with the learning experience.

The response body for the API is as follows:

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
      "learning_experiences": ["fMxRymndXeBgZhRGXSaz"],
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

### Update the reference of the new learning experince in the learning object

When we need to update the reference of the learning experince in the learning object then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object/{uuid}`** where **`uuid`** is the unique ID of the learning object and in the **`parent_nodes`** we need to provide the **`uuid`** of the new learning experience.

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
    "learning_experiences": ["bH6REjcgfbxcnqFAwxhR"],
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

After the validation of learning object for given learning_object_id, learning object for the given uuid is updated with the reference of new learning experience.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully updated the learning object",
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
      "learning_experiences": ["bH6REjcgfbxcnqFAwxhR"],
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

If the learning object is not present for a given learining_object_id - **`B5Y8bqSs5O5o2zjF4BN1`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Object with uuid B5Y8bqSs5O5o2zjF4BN1 not found",
  "data": null
}
```

### Delete the reference of the learing object from the learning experience

When we need to delete a reference of the learning object from the learning experience then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object/{uuid}`** where **`uuid`** is the unique ID of the learning object. It would delete the learing object and also remove the reference from the learning experience.

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
