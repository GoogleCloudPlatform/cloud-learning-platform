---
sidebar_label: CRUD APIs for Assessment
sidebar_position: 2
---

# CRUD APIs for Assessment

The following steps are to create, view and update Assessment.


### Create an Assessment:

To create a assessment, a **POST** request has to be made to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment`**.
The request body for the API is as follows:

```json

{
    "name": "Assessment 1",
    "type": "practice",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": "learnosity"
    },
    "max_attempts": 3,
    "pass_threshold": 70,
    "achievements": [],
    "alignments": {
      "competency_alignment": [],
      "skill_alignment": [],
      "learning_resource_alignment": [],
      "rubric_alignemt": []
      },
    "references": {
      "competencies": [],
      "skills": []
      },
    "parent_nodes": {
      "learning_objects": []
      },
    "child_nodes": {
      "assessments": [],
      "rubric_items": []
    },
    "prerequisites": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": [],
    },
    "metadata": {},
    "resource_paths": null,
    "instructions": null
  }
```

| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| name |  str | Name of the Assessment Data Item that will be created |
| type |    str   |   Type of the Assessment Item that will be created, currently can be either practice or final |
| author_id | str |    User ID of the author who created the Assessment |
| instructor_id | str |    User ID of the instructor who is assigned the Assessment |
| assessor_id | str |    User ID of the assessor who is assigned the Assessment |
| assessment_reference | dict |    Dict field containing the external reference if the assessment is created via an external service ```{"activity_id": str, "activity_template_id": str, "source": str}```  |
| max_attempts | int |    Maximum number attempts that can be done on an Assessment  |
| is_autogradable | bool |    Whether the assessment is autogradable  |
| resource_paths | list[str] |    Resource file gcs paths   |
| instructions | str |    Instruction Rich Text for the assessment  |
| pass_threshold | int |    Pass threshold score of the Assessment |
| achievements | list |    List containing IDs of Achievements that have been tagged to the Assessment |
| alignments | dict |    Dict containing competency and skills as keys and list of IDs as values that have been aligned by ML algorithm |
| references | dict |    Dict containing competency and skills as keys and list of IDs as values that have been tagged by the author |
| parent_nodes | dict |    Dict containing learning_objects as keys and list of IDs as values. ```{"parent_nodes": {"learning_objects": [str]}}``` |
| child_nodes | dict |    Dict containing assessment_items and rubrics as keys and list of IDs as values. ```{"child_nodes": {"assessment_items": [str]}, {"rubrics": [str]} }``` |
| prerequisites | dict |    Dict containing Learning Hierarchy node items as keys and list of IDs as values. It helps to determine the prerequisite nodes to be completed to unlock the Assessment Data |
| metadata | dict |    Dict containing metadata regarding the Assessment |
| tags | dict |    Dict containing the tags of Assessment. Tags are automatically fetched from Learnosity if `assessment_reference` is set. |
| created_time | datetime |    Creation time of the Assessment |
| last_modified_time | datetime |    Last modified time of the Assessment |


Here, `type` field can take one of the following values, namely - `practice` (formative assessments), `project` (summative assessments), `pretest`, `srl`, `static_srl`, `cognitive_wrapper`. Sending the request body in correct format would result in the creation of a new Assessment data item in Assessments Data Model in Firestore with a new UUID.

::: note

- Currently, validation to check if `assessor_id` and `instructor_id` exists or not is absent.
- Under `parent_nodes` and `child_nodes` the UUIDs that are being sent in the request body should be present in the DB before hand otherwise, the API endpoint would throw `ResourceNotFoundException` with a status code of `404`.
- If `assessment_reference` is passed and is a valid Learnosity activity id then all the items along with their tags are fetched from Learnosity at the time of creation and stored in the `metadata` field of assessment. It also updates the `is_autogradable` flag based on Learnosity tags.

:::


The format of the response is shown below:
```json
{
  "success": true,
  "message": "Successfully created the assessment",
  "data": {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Assessment 1",
    "type": "practice",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": "learnosity"
    },
    "max_attempts": 3,
    "pass_threshold": 70,
    "achievements": [],
    "alignments": {
      "competency_alignment": [],
      "skill_alignment": [],
      "learning_resource_alignment": [],
      "rubric_alignment": []
      },
    "references": {
      "competencies": [],
      "skills": []
      },
    "parent_nodes": {
      "learning_objects": []
      },
    "child_nodes": {
      "assessments": [],
      "rubric_items": []
    },
    "prerequisites": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": [],
    },
    "metadata": {},
    "resource_paths": null,
    "instructions": null,
    "tags": {},
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

### Get all assessment:

When we need to fetch all the assessments available then we would make a **GET** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of assessment array to be returned which takes a default value **`10`** if not provided. This will fetch the list of assessments.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the assessments",
  "data": {
    "records": [
    {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Assessment 1",
    "type": "practice",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": "learnosity"
    },
    "max_attempts": 3,
    "pass_threshold": 70,
    "achievements": [],
    "alignments": {
      "competency_alignment": [],
      "skill_alignment": [],
      "learning_resource_alignment": [],
      "rubric_alignment": []
      },
    "references": {
      "competencies": [],
      "skills": []
      },
    "parent_nodes": {
      "learning_objects": []
      },
    "child_nodes": {
      "assessments": [],
      "rubric_items": []
    },
    "prerequisites": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": [],
    },
    "metadata": {},
    "resource_paths": null,
    "instructions": null,
    "tags": {},
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
  ],
    "total_count": 10000
  }
}
```

### Get a specific assessment:

When we need to fetch the details of a specific assessment then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment/{uuid}`** where **`uuid`** is the unique ID of the assessment.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully created the assessment",
  "data": {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Assessment 1",
    "type": "practice",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": "learnosity"
    },
    "max_attempts": 3,
    "pass_threshold": 70,
    "achievements": [],
    "alignments": {
      "competency_alignment": [],
      "skill_alignment": [],
      "learning_resource_alignment": [],
      "rubric_alignment": []
      },
    "references": {
      "competencies": [],
      "skills": []
      },
    "parent_nodes": {
      "learning_objects": []
      },
    "child_nodes": {
      "assessments": [],
      "rubric_items": []
    },
    "prerequisites": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": [],
    },
    "metadata": {},
    "resource_paths": null,
    "instructions": null,
    "tags": {},
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

If the assessment is not present for the given UUID - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Assessment with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Search assessments:

When we need to search for assessments based on `name` then we would perform that search by making a **GET** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment/search?name=<search_name>`** where **`search_name`** is the name we want to search for.

:::note

This endpoint does keyword search, only results with exact match would be returned.

:::

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the assessment",
  "data":[
    {
      "uuid": "asd98798as7dhjgkjsdfh",
      "name": "Assessment 1",
      "type": "practice",
      "author_id": "author_id",
      "instructor_id": "instructor_id",
      "assessor_id": "assessor_id",
      "assessment_reference": {
        "activity_id": "",
        "activity_template_id": "",
        "source": "learnosity"
      },
      "max_attempts": 3,
      "pass_threshold": 70,
      "achievements": [],
      "alignments": {
        "competency_alignment": [],
        "skill_alignment": [],
        "learning_resource_alignment": [],
        "rubric_alignment": []
        },
      "references": {
        "competencies": [],
        "skills": []
        },
      "parent_nodes": {
        "learning_objects": []
        },
      "child_nodes": {
        "assessments": [],
        "rubric_items": []
      },
      "prerequisites": {
        "curriculum_pathways": [],
        "learning_experiences": [],
        "learning_objects": [],
        "learning_resources": [],
        "assessments": [],
      },
      "metadata": {},
      "resource_paths": null,
      "instructions": null,
      "tags": {},
      "created_time": "2022-03-03 09:22:49.843674+00:00",
      "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
    }
  ]
}
```

If there is no assessment present for the given `name` then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the assessment",
  "data": []
}
```

### Update an Assessment:

When we need to update the details of an Assessment data item then we would make a **PUT** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment/{uuid}`** where **`uuid`** is the unique ID of the assessment.
The request body would be as follows:

```json
{
    "name": "Assessment 1",
    "type": "final",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": "learnosity"
    },
    "max_attempts": 3,
    "pass_threshold": 70,
    "achievements": [],
    "alignments": {
      "competency_alignment": [],
      "skill_alignment": [],
      "learning_resource_alignment": [],
      "rubric_alignment": []
      },
    "references": {
      "competencies": [],
      "skills": []
      },
    "parent_nodes": {
      "learning_objects": []
      },
    "child_nodes": {
      "assessments": [],
      "rubric_items": []
    },
    "prerequisites": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": [],
    },
    "metadata": {},
    "resource_paths": null,
    "instructions": null,
    "tags": {}
}
```

After the validation of assessment for given assessment_id, assessment for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully updated the assessment",
  "data": {
    "name": "Assessment 1",
    "type": "final",
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": "learnosity"
    },
    "max_attempts": 3,
    "pass_threshold": 70,
    "achievements": [],
    "alignments": {
      "competency_alignment": [],
      "skill_alignment": [],
      "learning_resource_alignment": [],
      "rubric_alignment": []
      },
    "references": {
      "competencies": [],
      "skills": []
      },
    "parent_nodes": {
      "learning_objects": []
      },
    "child_nodes": {
      "assessments": [],
      "rubric_items": []
    },
    "prerequisites": {
      "curriculum_pathways": [],
      "learning_experiences": [],
      "learning_objects": [],
      "learning_resources": [],
      "assessments": [],
    },
    "metadata": {},
    "resource_paths": null,
    "instructions": null,
    "tags": {},
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```
If the assessment is not present for the given assessment_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Assessment with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Delete a Assessment:

When we need to delete a assessment then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment/{uuid}`** where **`uuid`** is the unique ID of the assessment.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the assessment"
}
```

If the assessment is not present for the given assessment_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Assessment with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Bulk import Assessments:

When we need to delete a assessment then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment/{uuid}`** where **`uuid`** is the unique ID of the assessment.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the assessment"
}
```

If the assessment is not present for the given assessment_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Assessment with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```