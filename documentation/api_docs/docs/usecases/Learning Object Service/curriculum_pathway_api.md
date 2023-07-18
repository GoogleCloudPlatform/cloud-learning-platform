---
sidebar_label: CRUD APIs for Curriculum Pathway
sidebar_position: 5
---

# CRUD APIs for Curriculum Pathway

The following steps are to create, view and update Curriculum Pathway.

### Create a curriculum pathway:

To create a curriculum pathway, a **POST** request has to be made to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/curriculum-pathway`**.
The request body for the API is as follows:

```json
{
  "name": "Kubernetes",
  "display_name": "Introduction to Kubernetes",
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
    "learning_experiences": [],
    "curriculum_pathways": []
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

A new curriculum pathway with the request body details and with a new uuid(unique ID of the curriculum pathway) is added to the curriculum pathway. After successfully adding new curriculum pathway document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the curriculum pathway",
  "data": {
    "name": "Kubernetes",
    "display_name": "Introduction to Kubernetes",
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
      "learning_experiences": [],
      "curriculum_pathways": []
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
    "uuid": "hg78KprfKzxU0KfniZ58",
    "version": 1,
    "is_archived": false,
    "parent_version_uuid": "",
    "root_version_uuid": "hg78KprfKzxU0KfniZ58",
    "created_time": "2022-11-15 12:24:33.582899+00:00",
    "last_modified_time": "2022-11-15 12:24:33.760657+00:00",
    "progress": null,
    "status": null
  }
}
```

### Get all curriculum pathway:

When we need to fetch all the curriculum pathways available then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/curriculum-pathway`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of curriculum pathway array to be returned which takes a default value **`10`** if not provided. This will fetch the list of curriculum pathways.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": {
    "records": [
    {
      "name": "Kubernetes",
      "display_name": "Introduction to Kubernetes",
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
        "learning_experiences": [],
        "curriculum_pathways": []
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
      "uuid": "hg78KprfKzxU0KfniZ58",
      "version": 1,
      "is_archived": false,
      "parent_version_uuid": "",
      "root_version_uuid": "hg78KprfKzxU0KfniZ58",
      "created_time": "2022-11-15 12:24:33.582899+00:00",
      "last_modified_time": "2022-11-15 12:24:33.760657+00:00",
      "progress": null,
      "status": null
    }
  ],
    "total_count": 10000
  }
}
```

### Get a specific curriculum pathway:

When we need to fetch the details of a specific curriculum pathway then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/curriculum-pathway/{uuid}`** where **`uuid`** is the unique ID of the curriculum pathway.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully created the curriculum pathway",
  "data":{
    "name": "Kubernetes",
    "display_name": "Introduction to Kubernetes",
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
      "learning_experiences": [],
      "curriculum_pathways": []
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
    "uuid": "hg78KprfKzxU0KfniZ58",
    "version": 1,
    "is_archived": false,
    "parent_version_uuid": "",
    "root_version_uuid": "hg78KprfKzxU0KfniZ58",
    "created_time": "2022-11-15 12:24:33.582899+00:00",
    "last_modified_time": "2022-11-15 12:24:33.760657+00:00",
    "progress": null,
    "status": null
  }
}
```

If the curriculum pathway is not present for a given curriculum_pathway_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Curriculum Pathway with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Update a curriculum pathway:

When we need to update the details of a curriculum pathway then we would make a **PUT** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/curriculum-pathway/{uuid}`** where **`uuid`** is the unique ID of the curriculum pathway.
The request body would be as follows:

```json
{
  "name": "Kubernetes",
  "display_name": "Introduction to Kubernetes",
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
    "learning_experiences": [],
    "curriculum_pathways": []
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

After validaing the given curriculum_pathway_id, the respective curriculum pathway will be updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the curriculum pathway",
  "data": {
    "name": "Kubernetes",
    "display_name": "Introduction to Kubernetes",
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
      "learning_experiences": [],
      "curriculum_pathways": []
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
    "uuid": "hg78KprfKzxU0KfniZ58",
    "version": 1,
    "is_archived": false,
    "parent_version_uuid": "",
    "root_version_uuid": "hg78KprfKzxU0KfniZ58",
    "created_time": "2022-11-15 12:28:32.892848+00:00",
    "last_modified_time": "2022-11-15 12:28:52.777407+00:00",
    "progress": null,
    "status": null
  }
}
```
If the curriculum pathway is not present for a given curriculum_pathway_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learning Experience with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Delete a learner experience:

When we need to delete a curriculum pathway then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/curriculum-pathway/{uuid}`** where **`uuid`** is the unique ID of the curriculum pathway.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the curriculum pathway"
}
```

If the curriculum pathway is not present for a given curriculum_pathway_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Curriculum Pathway with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Upload Learning Hierarchy:

When we need to upload the learning hierarchy then we would make a **Post** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/curriculum-pathway/bulk-import/json`** the request will be a multi-part form where we need to send hierarchy json file in **json_file** parameter

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully inserted the learning hierarchy",
  "data": [
    "7Z0Sw4MUksDU1VAXxUWi"
  ]
}
```

### Get a Learning Hierarchy:

When we need to fetch the details of a learning hierarchy then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/curriculum-pathway/{uuid}`** where **`uuid`** is the unique ID of the curriculum pathway and **`fetch_tree`** is **`false`** by default. This flag is used to determine whether to fetch tree or not

The response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the curriculum pathway",
  "data": {
    "name": "Kubernetes",
    "display_name": "Introduction to Kubernetes",
    "description": "",
    "author": "TestUser",
    "alignments": {
      "competency_alignments": [],
      "skill_alignments": []
    },
    "references": {
      "competencies": [
              "WtLpN9852VVlmYNZNuVx"
          ],
          "skills": [
              "EfeWD7TNjI7yrx7eFWV8"
          ]
    },
    "child_nodes": {
      "learning_experiences": [],
      "curriculum_pathways": []
    },
    "parent_nodes": {
      "learning_opportunities": [],
      "curriculum_pathways": [
        "h83EA9oYWYdFaGMou8Ma",
        "lTjgiA0ongzGhSyXer4S"
      ]
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
    "uuid": "PAC9gNFvVabyayKIslFq",
    "version": 1,
    "is_archived": false,
    "parent_version_uuid": "",
    "root_version_uuid": "PAC9gNFvVabyayKIslFq",
    "created_time": "2022-11-15 12:28:32.892848+00:00",
    "last_modified_time": "2022-11-15 12:28:52.777407+00:00",
    "progress": null,
    "status": null
  }
}
```

### Fetch all nodes of given alias under a Program:

When we need to fetch all the nodes of a given alias under a Program then we would make a **GET** request to the API endpoint - **`<APP_URL>/learning-object-service/api/v1/curriculum-pathway/{uuid}/nodes`** with **`alias`** param, where **`uuid`** is the unique id of the Program. For eg. if we want to fetch all the `levels` under a Program with `uuid`=`0SbilGJ0B4BzzVR39WvY`, we will keep `alias=level` and `uuid` as `0SbilGJ0B4BzzVR39WvY`. The default value of **`alias`** is `discipline`.

Then the response would be as follows:

```json
{
    "success": true,
    "message": "Data fetched successfully",
    "data": [
        {
            "name": "Module Overview",
            "alias": "lesson",
            "uuid": "Fpk9nILvriuY7F3JIgsO"
        },
        {
            "name": "Overview of the Humanities",
            "alias": "lesson",
            "uuid": "vbRiY4YHsHsxtMvLyTgR"
        }
    ]
}
```
