---
sidebar_label: Creation and updation of Human Graded Assessment
sidebar_position: 2
---

# API for creation and ingestion of Human Graded Assessment into the Hierarchy

The following steps are to create and ingest/replace/link a Human Graded Assessment into the learning hierarchy


### Create a Human Graded Assessment:

To create a human graded assessment, a **POST** request has to be made to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment/human-graded`**.
**NOTE:** performance_indicators added to rubric_criteria will be copied over to assessment data model during creation to allow filter on
Assessments on performance_indicator easily.
The request body for the API is as follows:

```json

{
  "name": "Assessment 1",
  "type": "practice",
  "order": 1,
  "author_id": "author_id",
  "instructor_id": "instructor_id",
  "assessor_id": "assessor_id",
  "assessment_reference": {},
  "max_attempts": 3,
  "pass_threshold": 0.7,
  "achievements": [],
  "alignments": {},
  "references": {},
  "parent_nodes": {"assessments":[]},
  "child_nodes": {
  "rubrics":[
                { "name": "Short name or label for the rubric.",
                    "description": "Full text description of the rubric.",
                    "author": "Author name",
                    "parent_nodes": {},
                    "child_nodes": {
                        "rubric_criteria":[
                        {
                        "name": "Short name or label for the rubric criterion.",
                        "description": "Full text description of the rubric criterion.",
                        "author": "Author name",
                        "parent_nodes": {"rubrics":[]},
                        "performance_indicators": ["001KVB2tqQG4zmMGUXCm"]}
                        ]}
                }]
    },
  "prerequisites": {},
  "metadata": {},
  "alias": "assessment",
  "resource_paths": []
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
| instructions | dict |    Instruction Rich Text for the assessment  |
| pass_threshold | int |    Pass threshold score of the Assessment |
| achievements | list |    List containing IDs of Achievements that have been tagged to the Assessment |
| alignments | dict |    Dict containing competency and skills as keys and list of IDs as values that have been aligned by ML algorithm |
| references | dict |    Dict containing competency and skills as keys and list of IDs as values that have been tagged by the author |
| parent_nodes | dict |    Dict containing learning_objects as keys and list of IDs as values. ```{"parent_nodes": {"learning_objects": [str]}}``` |
| child_nodes | dict |    Dict containing assessment_items and rubrics as keys and list of IDs as values. Rubrics should be a list of dictionary where each dictiory represetns the information for that specific rubric. Inside each rubrci dictionary there is are child_nodes which represent the list of rubric_criterion. It is again a lsit of dicitonary where each dictionary contains the requried information for a rubric criteria. |
| prerequisites | dict |    Dict containing Learning Hierarchy node items as keys and list of IDs as values. It helps to determine the prerequisite nodes to be completed to unlock the Assessment Data |
| performance_indicators| list| List containing list of IDs of skills that will be tagged to rubric criteria. |
| metadata | dict |    Dict containing metadata regarding the Assessment |
| tags | dict |    Dict containing the tags of Assessment. Tags are automatically fetched from Learnosity if `assessment_reference` is set. |
| created_time | datetime |    Creation time of the Assessment |
| last_modified_time | datetime |    Last modified time of the Assessment |


Here, `type` field can take one of the following values, namely - `practice` (formative assessments) or `final` (summative assessments). Sending the request body in correct format would result in the creation of a new Assessment data item in Assessments Data Model in Firestore with a new UUID.

::: note
Currently, validation to check if `assessor_id` and `instructor_id` exists or not is absent.
Under `parent_nodes` the UUIDs that are being sent in the request body should be present in the DB before hand otherwise, the API endpoint would throw `ResourceNotFoundException` with a status code of `404`.
Under `child_nodes`  the list of dictionaries to be sent in the request body should be retain the required schema as per rubric and rubric_crtieria as indicated in the example above. If not a required `ValidationError` will be thrown
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
      "skills": ["001KVB2tqQG4zmMGUXCm"]
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

### Replacing a Placeholder Assessment with a Human Graded Assessment:

Given, there exists a placeholder assessment that has been ingested during the ingestion of the learning hierarchy, this sceanrio i;lustrates the steps for
replacing the `placeholder assessment` with the freshly authored `Human Graded Assessment`.

The `Human Graded Assessment` can be created by making a **POST** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment/human-graded`** as indicated in the previous section.

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

Once, the user has a `Human Graded Assessment` created, the `uuid` from the repsone body can be used to replace/link it with the placeholder assessment in the original learning hierarchy.

To replace an older assessment(placeholder) with the newly create Human Graded Assessment, the user needs to make a **PUT** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment/replace/{old_assessment_uuid}`** where **`old_assessment_uuid`** is the unique ID of the older assessment(placeholder assessment ingested via the learning hierarhcy) with the query_params containing the **`new_assessment_uuid`** which is the unique ID of the Human Graded Assessment.

This would return a result json which is the linked/ingested manually graded assessment:

```json
{
    "success": true,
    "message": "Successfully linked the assessment",
    "data": {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Assessment 1",
    "type": "practice",
    "order": 1,
    "author_id": "author_id",
    "instructor_id": "instructor_id",
    "assessor_id": "assessor_id",
    "assessment_reference": { },
    "max_attempts": 3,
    "pass_threshold": 0.7,
    "achievements": [ ],
    "alignments": { },
    "references": { },
    "parent_nodes": {},
    "child_nodes": { },
    "prerequisites": { },
    "metadata": { },
    "alias": "assessment",
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
    }
}
```
