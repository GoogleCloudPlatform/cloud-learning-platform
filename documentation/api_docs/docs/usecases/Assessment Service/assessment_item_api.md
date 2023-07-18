---
sidebar_label: CRUD APIs for Assessment Item
sidebar_position: 1
---

# CRUD APIs for Assessment Item

The following steps are to create, view and update Assessment Item.


### Create a assessment item:

To create a assessment item, a **POST** request has to be made to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment-item`**.
The request body for the API is as follows:

```json
{
  "name": "Short name or label for the assessment item.",
  "question": "Assessment item question",
  "answer": "Answer for the question",
  "context": "Context from which the question was created",
  "options": [],
  "question_type": "Type of question",
  "activity_type": "Type of activity",
  "use_type": "Field to distinguish the type of assessment profile (Formative/Summative)",
  "metadata": {},
  "author": "A person or organization chiefly responsible for the intellectual or artistic content of this assessment item",
  "difficulty": 1,
  "alignments": {},
  "parent_nodes": {
    "learning_experiences": [],
    "learning_objects": []
  },
  "references": {
    "competencies": [],
    "skills": []
  },
  "child_nodes": {},
  "assessment_reference": {
    "activity_id": "",
    "activity_template_id": "",
    "source": ""
  },
  "achievements": [],
  "pass_threshold": 1,
}
```


| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| name |  str | Name of the Assessment Item Data that will be created |
| question |    str   |   Question fo the Assessment Item Data|
| answer | str |    Answer of the Assessment Item Data |
| context | str |    Context from which the question is created from |
| options | list |    List of options if available for the question one of which will be an answer |
| pass_threshold | int |    Minimum score to get to pass the particular assessment item |
| question_type | str |    Field to determine the question type of the assessment item data|
| activity_type | str |    Field to determine the activity type of the assessment item data  |
| use_type | int |    Field to determine the use type of the assessment item data |
| author | str |    User ID of the author who created the assessment item |
| difficulty | int |    Field to determine difficulty of the assessment item. As the number increases so does the difficulty of the assessment item |
| achievements | list |    List containing IDs of Achievements that have been tagged to the Assessment Item |
| alignments | dict |    Dict containing competency and skills as keys and list of IDs as values that have been aligned by ML algorithm |
| references | dict |    Dict containing competency and skills as keys and list of IDs as values that have been tagged by the author |
| parent_nodes | dict |    Dict containing assessments as keys and list of IDs as values. ```{"parent_nodes": {"assessments": [str]}}``` |
| child_nodes | dict |    Dict containing Data Models as keys and list of IDs as values, currently there will be no child nodes for assessment items |
| prerequisites | dict |    Dict containing Learning Hierarchy node items as keys and list of IDs as values. It helps to determine the prerequisite nodes to be completed to unlock the Assessment Item Data |
| metadata | dict |    Dict containing metadata regarding the Assessment Item |
| created_time | datetime |    Creation time of the Assessment Item |
| last_modified_time | datetime |    Last modified time of the Assessment Item |
| assessment_reference | dict |    Dict field containing the external reference if the assessment is created via an external service ```{"activity_id": str, "activity_template_id": str, "source": str}``` . This field will be moved to Assessments Data Model |

A new assessment item with the request body details and with a new uuid(unique ID of the assessment item) is added to the assessment item. After successfully adding new assessment item document to the collection You will get a response similar to the below json:

```json
{
  "success": true,
  "message": "Successfully created the assessment_item",
  "data": {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Short name or label for the assessment item.",
    "question": "Assessment item question",
    "answer": "Answer for the question",
    "context": "Context from which the question was created",
    "options": [],
    "question_type": "Type of question",
    "activity_type": "Type of activity",
    "use_type": "Field to distinguish the type of assessment profile (Formative/Summative)",
    "metadata": {},
    "author": "A person or organization chiefly responsible for the intellectual or artistic content of this assessment item",
    "difficulty": 1,
    "alignments": {},
    "parent_nodes": {
      "learning_experiences": [],
      "learning_objects": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {},
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": ""
    },
    "achievements": [],
    "pass_threshold": 1,
    "is_flagged" : false,
    "comments" : "",
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

### Get all assessment item:

When we need to fetch all the assessment items available then we would make a **GET** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment-item`** with **`skip`** and **`limit`** params where **`skip`** is the number of objects to be skipped which takes a default value **`0`** if not provided and **`limit`** is the size of assessment item array to be returned which takes a default value **`10`** if not provided. This will fetch the list of assessment items.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Data fetched successfully",
  "data": {
    "records": [
    {
      "uuid": "asd98798as7dhjgkjsdfh",
      "name": "Short name or label for the assessment item.",
      "question": "Assessment item question",
      "answer": "Answer for the question",
      "context": "Context from which the question was created",
      "options": [],
      "question_type": "Type of question",
      "activity_type": "Type of activity",
      "use_type": "Field to distinguish the type of assessment profile (Formative/Summative)",
      "metadata": {},
      "author": "A person or organization chiefly responsible for the intellectual or artistic content of this assessment item",
      "difficulty": 1,
      "alignments": {},
      "parent_nodes": {
        "learning_experiences": [],
        "learning_objects": []
      },
      "references": {
        "competencies": [],
        "skills": []
      },
      "child_nodes": {},
      "assessment_reference": {
        "activity_id": "",
        "activity_template_id": "",
        "source": ""
      },
      "achievements": [],
      "pass_threshold": 1,
      "is_flagged" : false,
      "comments" : "",
      "created_time": "2022-03-03 09:22:49.843674+00:00",
      "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
    }
  ],
    "total_count": 10000
  }
}
```

### Get a specific assessment item:

When we need to fetch the details of a specific assessment item then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment-item/{uuid}`** where **`uuid`** is the unique ID of the assessment item.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully created the assessment_item",
  "data": {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Short name or label for the assessment item.",
    "question": "Assessment item question",
    "answer": "Answer for the question",
    "context": "Context from which the question was created",
    "options": [],
    "question_type": "Type of question",
    "activity_type": "Type of activity",
    "use_type": "Field to distinguish the type of assessment profile (Formative/Summative)",
    "metadata": {},
    "author": "A person or organization chiefly responsible for the intellectual or artistic content of this assessment item",
    "difficulty": 1,
    "alignments": {},
    "parent_nodes": {
      "learning_experiences": [],
      "learning_objects": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {},
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": ""
    },
    "achievements": [],
    "pass_threshold": 1,
    "is_flagged" : false,
    "comments" : "",
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```

If the assessment item is not present for a given learning_experience_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Assessment Item with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Update a assessment item:

When we need to update the details of a assessment item then we would make a **PUT** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment-item/{uuid}`** where **`uuid`** is the unique ID of the assessment item.
The request body would be as follows:

```json
{
  "name": "Short name or label for the assessment item.",
  "question": "Assessment item question",
  "answer": "Answer for the question",
  "context": "Context from which the question was created",
  "options": [],
  "question_type": "Type of question",
  "activity_type": "Type of activity",
  "use_type": "Field to distinguish the type of assessment profile (Formative/Summative)",
  "metadata": {},
  "author": "A person or organization chiefly responsible for the intellectual or artistic content of this assessment item",
  "difficulty": 1,
  "alignments": {},
  "parent_nodes": {
    "learning_experiences": [],
    "learning_objects": []
  },
  "references": {
    "competencies": [],
    "skills": []
  },
  "child_nodes": {},
  "assessment_reference": {
    "activity_id": "",
    "activity_template_id": "",
    "source": ""
  },
  "achievements": [],
  "pass_threshold": 1,
  "is_flagged" : true,
  "comments" : "comments"
}
```

After the validation of assessment item for given assessment_item_id, assessment item for the given uuid is updated and the response will look like this:

```json
{
  "success": true,
  "message": "Successfully created the assessment_item",
  "data": {
    "uuid": "asd98798as7dhjgkjsdfh",
    "name": "Short name or label for the assessment item.",
    "question": "Assessment item question",
    "answer": "Answer for the question",
    "context": "Context from which the question was created",
    "options": [],
    "question_type": "Type of question",
    "activity_type": "Type of activity",
    "use_type": "Field to distinguish the type of assessment profile (Formative/Summative)",
    "metadata": {},
    "author": "A person or organization chiefly responsible for the intellectual or artistic content of this assessment item",
    "difficulty": 1,
    "alignments": {},
    "parent_nodes": {
      "learning_experiences": [],
      "learning_objects": []
    },
    "references": {
      "competencies": [],
      "skills": []
    },
    "child_nodes": {},
    "assessment_reference": {
      "activity_id": "",
      "activity_template_id": "",
      "source": "learnosity"
    },
    "achievements": [],
    "pass_threshold": 1,
    "is_flagged" : true,
    "comments" : "comments",
    "created_time": "2022-03-03 09:22:49.843674+00:00",
    "last_modified_time": "2022-03-03 09:22:49.843674+00:00"
  }
}
```
If the assessment item is not present for a given assessment_item_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Assessment Item with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Delete a Assessment Item:

When we need to delete a assessment item then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/assessment-item/{uuid}`** where **`uuid`** is the unique ID of the assessment item.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the assessment item"
}
```

If the assessment item is not present for a given assessment_item_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Assessment Item with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```