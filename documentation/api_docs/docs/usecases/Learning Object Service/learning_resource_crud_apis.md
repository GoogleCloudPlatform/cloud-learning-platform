---
sidebar_label: CRUD APIs for Learning Resource
sidebar_position: 3
---

# CRUD APIs for Learner Resource

The following steps are to create, view and update Learning resource.


### Create a learning resource:

To create a learning resource, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-resource`**.
The request body for the API is as follows:

```json
{
  "name": "Text Books",
  "display_name": "Text Books",
  "description": "Testing description",
  "type": "html",
  "resource_path": "test_file.html",
  "lti_content_item_id": "H4w2CJBwM8AIzW8nN4Ib",
  "course_category": [
    "Testing category"
  ],
  "alignments": {
    "competency_alignments": [],
    "skill_alignments": []
  },
  "references": {
    "skills": [],
    "competencies": []
  },
  "parent_nodes": {
    "learning_objects": []
  },
  "child_nodes": {
    "concepts": []
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

A new learning resource with the request body details with a new uuid(unique ID of the learning resource) is added to the learning resource. After successfully adding new learning resource document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the learning resource",
  "data": {
    "name": "Text Books",
    "display_name": "Text Books",
    "description": "Testing description",
    "type": "html",
    "resource_path": "test_file.html",
    "lti_content_item_id": "H4w2CJBwM8AIzW8nN4Ib",
    "course_category": [
      "Testing category"
    ],
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {
      "concepts": []
    },
    "parent_nodes": {
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
    "uuid": "JSkNlMZtoIIulW4ShMLZ",
    "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "JSkNlMZtoIIulW4ShMLZ",
    "is_archived": false,
    "created_time": "2022-11-15 07:31:05.423165+00:00",
    "last_modified_time": "2022-11-15 07:31:05.593248+00:00"
  }
}
```

### Get all learning resource:

When we need to fetch all the learning resources available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-object`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of learning object array to be returned which takes a default value **`10`** if not provided. This will fetch the list of learning resources.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": {
    "records": [
    {
      "name": "Text Books",
      "display_name": "Text Books",
      "description": "Testing description",
      "type": "html",
      "resource_path": "test_file.html",
      "lti_content_item_id": "H4w2CJBwM8AIzW8nN4Ib",
      "course_category": [
        "Testing category"
      ],
      "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
      },
      "references": {
        "competencies": [],
        "skills": []
      },
      "child_nodes": {
        "concepts": []
      },
      "parent_nodes": {
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
      "uuid": "JSkNlMZtoIIulW4ShMLZ",
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "JSkNlMZtoIIulW4ShMLZ",
      "is_archived": false,
      "created_time": "2022-11-15 07:31:05.423165+00:00",
      "last_modified_time": "2022-11-15 07:31:05.593248+00:00"
    },
    {
      "name": "Text Books",
      "display_name": "Text Books",
      "description": "Testing description",
      "type": "html",
      "resource_path": "test_file.html",
      "lti_content_item_id": "H4w2CJBwM8AIzW8nN4Ic",
      "course_category": [
        "Testing category"
      ],
      "alignments": {
        "competency_alignments": [],
        "skill_alignments": []
      },
      "references": {
        "competencies": [],
        "skills": []
      },
      "child_nodes": {
        "concepts": []
      },
      "parent_nodes": {
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
      "uuid": "JSkNlMZtoIIulW4ShMLZ",
      "version": 1,
      "parent_version_uuid": "",
      "root_version_uuid": "JSkNlMZtoIIulW4ShMLZ",
      "is_archived": false,
      "created_time": "2022-11-15 07:31:05.423165+00:00",
      "last_modified_time": "2022-11-15 07:31:05.593248+00:00"
    }
  ],
    "total_count": 10000
  }
}
```

### Get a specific learning resource:

When we need to fetch the details of a specific learning resource then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-resource/{uuid}`** where **`uuid`** is the unique ID of the learning resource.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the learning resource",
  "data": {
    "name": "Text Books",
    "display_name": "Text Books",
    "description": "Testing description",
    "type": "html",
    "resource_path": "test_file.html",
    "lti_content_item_id": "H4w2CJBwM8AIzW8nN4Ib",
    "course_category": [
      "Testing category"
    ],
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {
      "concepts": []
    },
    "parent_nodes": {
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
    "uuid": "JSkNlMZtoIIulW4ShMLZ",
    "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "JSkNlMZtoIIulW4ShMLZ",
    "is_archived": false,
    "created_time": "2022-11-15 07:31:05.423165+00:00",
    "last_modified_time": "2022-11-15 07:31:05.593248+00:00"
  }
}
```

If the learning resource is not present for a given learning_resource_id - **`MjoDGh296E5kC4ttDT5k`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Resource with uuid MjoDGh296E5kC4ttDT5k not found",
  "data": null
}
```

### Update a learning resource:

When we need to update the details of a learning resource then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-resource/{uuid}`** where **`uuid`** is the unique ID of the learning resource.
The request body would be as follows:

```json
{
  "name": "Updated Text Book name",
  "display_name": "Text Books",
  "description": "Testing description",
  "type": "html",
  "resource_path": "test_file.html",
  "lti_content_item_id": "H4w2CJBwM8AIzW8nN4Ib",
  "course_category": [
    "Testing category"
  ],
  "alignments": {
    "competency_alignments": [],
    "skill_alignments": []
  },
  "references": {
    "skills": [],
    "competencies": []
  },
  "parent_nodes": {
    "learning_objects": []
  },
  "child_nodes": {
    "concepts": []
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

After the validation of learning resource for given learning_resource_id, respective learning resource is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the learning resource",
  "data":{
    "name": "Updated Text Book name",
    "display_name": "Text Books",
    "description": "Testing description",
    "type": "html",
    "resource_path": "test_file.html",
    "lti_content_item_id": "H4w2CJBwM8AIzW8nN4Ib",
    "course_category": [
      "Testing category"
    ],
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {
      "concepts": []
    },
    "parent_nodes": {
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
    "uuid": "JSkNlMZtoIIulW4ShMLZ",
    "version": 1,
    "parent_version_uuid": "",
    "root_version_uuid": "JSkNlMZtoIIulW4ShMLZ",
    "is_archived": false,
    "created_time": "2022-11-15 07:31:05.423165+00:00",
    "last_modified_time": "2022-11-15 07:31:05.593248+00:00"
  }
}
```

If the learning resource is not present for a given learning_resource_id - **`o1nv13n6sbu0ny`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Resource with uuid o1nv13n6sbu0ny not found",
  "data": null
}
```

### Delete a learner resource:

When we need to delete a learning resource then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/learning-resource/{uuid}`** where **`uuid`** is the unique ID of the learning resource.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the learning resource"
}
```

If the learning resource is not present for a given learning_resource_id - **`1HFXhcO7A384fdcq`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Resource with uuid 1HFXhcO7A384fdcq not found",
  "data": null
}
```
