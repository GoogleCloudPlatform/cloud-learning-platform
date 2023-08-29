---
sidebar_label: CRUD APIs for Submitted Assessment
sidebar_position: 3
---

# CRUD APIs for Submitted Assessment

The following steps are to create, view and update Submitted Assessment.


### Create a submitted assessment:

To create a submitted assessment, a **POST** request has to be made to the API endpoint - **`<APP_URL>/assessment-service/api/v1/submitted-assessment`**.
The request body for the API is as follows:

```json
{
  "assessment_id": "uuid of assessment for which the submitted assessment is created",
  "learner_id": "uuid of learner submitting the assessment",
  "learner_session_id": "session id of the learners submission"
}
```

| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| assessment_id |  str | Assessment ID with which the Submitted Assessment Data Item will be linked to |
| learner_id |    str   |   Learner ID of the learner who is adding a new Submitted Assessment Data item |
| assessment_session_id | str |    Session ID of the learner during which the submission of the assessment has taken place |


A new submitted assessment with the request body details and with a new uuid(unique ID of the submitted assessment) is added to the submitted assessment. The assessor_id will automatically get added from the list of available assessors in a round robin fashion during the **POST** request. After successfully adding new submitted assessment document to the collection You will get a response similar to the below json:

```json
{
    "success": true,
    "message": "Successfully created the submitted assessment.",
    "data": {
        "assessment_id": "uuid of assessment for which the submitted assessment is created",
        "learner_id": "uuid of learner submitting the assessment",
        "assessor_id": "uuid of assessor who will assess the submitted assessment",
        "type": "type of assessment",
        "plagiarism_score": null,
        "plagiarism_report_path": null,
        "submission_gcs_paths": [],
        "result": null,
        "pass_status": true,
        "status": "status of the submitted assessment",
        "is_flagged": false,
        "comments": null,
        "timer_start_time": "2023-01-02 13:11:50.331743+00:00",
        "attempt_no": 5,
        "learner_session_id": "session id of learnosity",
        "learner_session_data": {
            "max_score": 40,
            "responses": [
                {
                    "score": 1,
                    "item_reference": "293486384",
                    "dt_score_updated": "2017-06-19T02:03:19Z",
                    "response_id": "2571d802-0095-4d66-94bc-4cfa44b0ebbe",
                    "max_score": 1
                }
            ],
            "session_id": "4d3115f0-1235-4613-5be6fc6e6b2e",
            "status": "Completed",
            "activity_id": "chemistry_classtest1",
            "subscores": [
                {
                    "score": 19,
                    "num_attempted": 20,
                    "num_questions": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "id": "subscore-1",
                    "title": "biochem",
                    "attempted_max_score": 20,
                    "max_score": 20
                },
                {
                    "attempted_max_score": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "num_attempted": 20,
                    "num_questions": 20,
                    "max_score": 20,
                    "score": 20,
                    "title": "inorganics",
                    "id": "subscore-2"
                }
            ],
            "user_id": "17c456c0-89ad-4f72-8010-2f7d991f54bd",
            "score": 39
        },
        "assessor_session_id": null,
        "submitted_rubrics": null,
        "overall_feedback": null,
        "uuid": "AmifBsWI5uPx23cn6E9L",
        "created_time": "2023-01-02 13:11:50.331743+00:00",
        "last_modified_time": "2023-01-02 13:11:50.531421+00:00",
        "created_by": "",
        "last_modified_by": ""
    }
}
```

| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| assessment_id |  str | Assessment ID with which the Submitted Assessment Data Item will be linked to |
| learner_id |    str   |   Learner ID of the learner who is adding a new Submitted Assessment Data item |
| learner_session_id | str |    Session ID of the learner during which the submission of the assessment has taken place |
| type |  str | Type of the Submitted Assessment. Currently, can be of only practice or final type  |
| plagiarism_score |  str | Final score of plagiarism from TurnItIn/Other external service |
| plagiarism_report_path |  str | GCS Path where the full plagiarism report will be stored |
| submission_gcs_paths |  list | GCS Paths of the Submitted Assessment where the submission on the Assessment will be stored |
| result |  str | Assessment ID with which the Submitted Assessment Data Item will be linked to |
| pass_status |  str | The final evaluation on the submitted assessment |
| status |  str | Field which helps to determine the state of submission of the submitted assessment. Can be non-evaluated, submitted, evaluated |
| is_flagged |  str | Flag determining if the submitted assessment has been flagged by an assessor |
| timer_start_time |  str | The time at which submission is stored in DB based on which the assigned assessor's timer will start|
| comments |  list[dict] | Field to store history of comments on the submitted assessment by assessor/instructor |
| attempt_no |  str | Attempt Number on the Assessment which is linked to the Submitted Assessment Data |
| learner_session_data |  dict | Field storing evaluation data coming from Learnosity |
| assessor_session_id |  str | Field story data pertaining to the rubrics that are submitted by the assessor|
| submitted_rubrics |  list[dict] | Rubric criteria submitted by assessor |
| overall_feedback |  str | Overall feedback submitted by assessor |
| created_time |  str | Creation time of the Submitted Assessment Data |
| last_modified_time |  str | Last modified time of the Submitted Assessment Data |
| created_by |  str | User ID of the author of the submitted assessment |
| last_modified_by |  str | User ID of the person who last modified the Submitted Assessment Data |

### Get a specific submitted assessment:

When we need to fetch the details of a specific submitted assessment then we would get those details by making a **GET** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/submitted-assessment/{uuid}`** where **`uuid`** is the unique ID of the submitted assessment.

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully created the submitted assessment.",
  "data": {
        "assessment_id": "uuid of assessment for which the submitted assessment is created",
        "learner_id": "uuid of learner submitting the assessment",
        "assessor_id": "uuid of assessor who will assess the submitted assessment",
        "type": "type of assessment",
        "plagiarism_score": null,
        "plagiarism_report_path": null,
        "submission_gcs_paths": [],
        "result": null,
        "pass_status": true,
        "status": "evaluated",
        "is_flagged": false,
        "comments": null,
        "timer_start_time": "2023-01-02 08:35:51.168319+00:00",
        "attempt_no": 4,
        "learner_session_id": "learner_session_id1",
        "learner_session_data": {
            "subscores": [
                {
                    "max_score": 20,
                    "num_attempted": 20,
                    "num_questions": 20,
                    "id": "subscore-1",
                    "score": 19,
                    "attempted_max_score": 20,
                    "title": "biochem",
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ]
                },
                {
                    "num_questions": 20,
                    "num_attempted": 20,
                    "max_score": 20,
                    "title": "inorganics",
                    "attempted_max_score": 20,
                    "score": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "id": "subscore-2"
                }
            ],
            "score": 39,
            "status": "Completed",
            "user_id": "17c456c0-89ad-4f72-8010-2f7d991f54bd",
            "session_id": "4d3115f0-1235-4613-5be6fc6e6b2e",
            "responses": [
                {
                    "score": 1,
                    "dt_score_updated": "2017-06-19T02:03:19Z",
                    "item_reference": "293486384",
                    "max_score": 1,
                    "response_id": "2571d802-0095-4d66-94bc-4cfa44b0ebbe"
                }
            ],
            "activity_id": "chemistry_classtest1",
            "max_score": 40
        },
        "assessor_session_id": null,
        "submitted_rubrics": null,
        "overall_feedback": null,
        "uuid": "k73fX3BvEY3cPTgvZPUK",
        "created_time": "2023-01-02 08:35:51.168319+00:00",
        "last_modified_time": "2023-01-02 08:35:52.761592+00:00",
        "created_by": "",
        "last_modified_by": ""
    }
}
```

If the submitted assessment is not present for a given uuid - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Submitted Assessment with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Update a submitted assessment:

When we need to update the details of a submitted assessment then we would make a **PUT** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/submitted-assessment/{uuid}`** where **`uuid`** is the unique ID of the submitted assessment.
The request body would be as follows:

```json
{
  "status": "Status of the submitted assessment",
  "result": "Final result of the submitted assessment"
}
```

After the validation of submitted assessment for given uuid, submitted assessment for the given uuid is updated and the response will look like this:

```json
{
    "success": true,
    "message": "Successfully updated the submitted assessment.",
    "data": {
        "assessment_id": "uuid of assessment for which the submitted assessment is created",
        "learner_id": "uuid of learner submitting the assessment",
        "assessor_id": "uuid of assessor who will assess the submitted assessment",
        "type": "type of assessment",
        "plagiarism_score": null,
        "plagiarism_report_path": null,
        "submission_gcs_paths": [],
        "result": "Final result of the submitted assessment",
        "pass_status": false,
        "status": "Status of the submitted assessment",
        "is_flagged": false,
        "comments": null,
        "timer_start_time": "2023-01-02 13:11:50.331743+00:00",
        "attempt_no": 5,
        "learner_session_id": "learnosity_session_id1",
        "learner_session_data": {
            "responses": [
                {
                    "item_reference": "293486384",
                    "response_id": "2571d802-0095-4d66-94bc-4cfa44b0ebbe",
                    "score": 1,
                    "max_score": 1,
                    "dt_score_updated": "2017-06-19T02:03:19Z"
                }
            ],
            "status": "Completed",
            "max_score": 40,
            "subscores": [
                {
                    "title": "biochem",
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "id": "subscore-1",
                    "num_questions": 20,
                    "attempted_max_score": 20,
                    "max_score": 20,
                    "score": 19,
                    "num_attempted": 20
                },
                {
                    "max_score": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "attempted_max_score": 20,
                    "num_questions": 20,
                    "title": "inorganics",
                    "id": "subscore-2",
                    "score": 20,
                    "num_attempted": 20
                }
            ],
            "user_id": "17c456c0-89ad-4f72-8010-2f7d991f54bd",
            "score": 39,
            "activity_id": "chemistry_classtest1",
            "session_id": "4d3115f0-1235-4613-5be6fc6e6b2e"
        },
        "assessor_session_id": null,
        "submitted_rubrics": null,
        "overall_feedback": null,
        "uuid": "AmifBsWI5uPx23cn6E9L",
        "created_time": "2023-01-02 13:11:50.331743+00:00",
        "last_modified_time": "2023-01-02 13:57:44.915865+00:00",
        "created_by": "",
        "last_modified_by": ""
    }
}
```

If `submitted_rubrics` is present in the request body (for human graded assessment), then the `result`, `pass_status`, and `status` of the submitted assesement will be updated based on the `submitted_rubrics`.

`result`, `pass_status`, and `status` will be updated based on the following conditions:

- `result` of the submitted assessment will be the lowest of all `result` values in the `submitted_rubrics`.
- If all the `result` values in the `submitted_rubrics` are greater than ("Needs improvement", "Not evident"), then the `status` of the submitted assessment will be "completed" and `pass_status` will be True. Otherwise, `status` will be "evaluated" and `pass_status` will be False.

`result` values = ["Exemplary", "Proficient", "Needs improvement", "Not evident"],
"Exemplary" being the highest and "Not evident" being the lowest.

Example of request body:

```json
{
    "overall_feedback": "overall feedback of the submitted assessment",
    "submitted_rubrics": [
        {
            "rubric_criteria_id": "r_id1",
            "result": "Not evident",
            "feedback": "feedback_1"
        },
        {
            "rubric_criteria_id": "r_id2",
            "result": "Needs improvement",
            "feedback": "feedback_2"
        },
        {
            "rubric_criteria_id": "r_id3",
            "result": "Needs improvement",
            "feedback": "feedback_3"
        },
        {
            "rubric_criteria_id": "r_id4",
            "result": "Not evident",
            "feedback": "feedback_4"
        }
    ]
}
```

After the validation of submitted assessment for given uuid, submitted assessment for the given uuid is updated and the response will look like this:

```json
{
    "success": true,
    "message": "Successfully updated the submitted assessment.",
    "data": {
        "assessment_id": "uuid of assessment for which the submitted assessment is created",
        "learner_id": "uuid of learner submitting the assessment",
        "assessor_id": "uuid of assessor who will assess the submitted assessment",
        "type": "type of assessment",
        "plagiarism_score": null,
        "plagiarism_report_path": null,
        "submission_gcs_paths": [],
        "result": "Not evident",
        "pass_status": false,
        "status": "evaluated",
        "is_flagged": false,
        "comments": null,
        "timer_start_time": "2023-01-02 13:11:50.331743+00:00",
        "attempt_no": 5,
        "learner_session_id": "learnosity_session_id1",
        "learner_session_data": {
            "responses": [
                {
                    "item_reference": "293486384",
                    "response_id": "2571d802-0095-4d66-94bc-4cfa44b0ebbe",
                    "score": 1,
                    "max_score": 1,
                    "dt_score_updated": "2017-06-19T02:03:19Z"
                }
            ],
            "status": "Completed",
            "max_score": 40,
            "subscores": [
                {
                    "title": "biochem",
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "id": "subscore-1",
                    "num_questions": 20,
                    "attempted_max_score": 20,
                    "max_score": 20,
                    "score": 19,
                    "num_attempted": 20
                },
                {
                    "max_score": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "attempted_max_score": 20,
                    "num_questions": 20,
                    "title": "inorganics",
                    "id": "subscore-2",
                    "score": 20,
                    "num_attempted": 20
                }
            ],
            "user_id": "17c456c0-89ad-4f72-8010-2f7d991f54bd",
            "score": 39,
            "activity_id": "chemistry_classtest1",
            "session_id": "4d3115f0-1235-4613-5be6fc6e6b2e"
        },
        "assessor_session_id": null,
        "submitted_rubrics": [
            {
                "rubric_criteria_id": "r_id1",
                "result": "Not evident",
                "feedback": "feedback_1"
            },
            {
                "rubric_criteria_id": "r_id2",
                "result": "Needs improvement",
                "feedback": "feedback_2"
            },
            {
                "rubric_criteria_id": "r_id3",
                "result": "Needs improvement",
                "feedback": "feedback_3"
            },
            {
                "rubric_criteria_id": "r_id4",
                "result": "Not evident",
                "feedback": "feedback_4"
            }
        ],
        "overall_feedback": "overall feedback of the submitted assessment",
        "uuid": "AmifBsWI5uPx23cn6E9L",
        "created_time": "2023-01-02 13:11:50.331743+00:00",
        "last_modified_time": "2023-01-02 13:57:44.915865+00:00",
        "created_by": "",
        "last_modified_by": ""
    }
}
```

If the submitted assessment is not present for a given uuid - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Submitted Assessment with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Delete a Submitted Assessment:

When we need to delete a submitted assessment then we would make a **DELETE** request to the API endpoint - **`<APP_URL>/assessment-service/api/v1/submitted-assessment/{uuid}`** where **`uuid`** is the unique ID of the submitted assessment.

Then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully deleted the submitted assessment.""
}
```

If the submitted assessment is not present for a given uuid - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Submitted Assessment with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```

### Getting Unique Values for filters

To fetch the list of unique values for unit_name, type and results for filters, use the endpoint
**`[GET]<APP_URL>/assessment-service/api/v1/submitted-assessments/unique/?assessor_id=<>`**

Upon successfully hitting the endpoint will give the following response:
```json
{
    "success": true,
    "message": "Successfully fetched the unique values",
    "data": {
        "unit_names": ["Name1", "Name2"],
        "types": ["practice", "final"],
        "results": ["proficient"]
    }
}
```

### Filter Submitted Assessments:

To filter, search and sort submitted assessments, a **GET** request has to be made to the API endpoint - **`<APP_URL>/assessment-service/api/v1/submitted-assessments`**.

Following are the query parameters that can be used to filter the response:
| Field Name   |      Type      |  Description |
|----------|:-------------:|------:|
| sort_by | Literal["learner_name", "unit_name", "result", "attempt_no", "timer_start_time"] | field by which the submitted assessments will be sorted. (default="timer_start_time") |
| sort_order |  Literal["ascending", "descending"] | Ascending or Descending sort (default="ascending") |
| name |  str | Search submitted assessment based on assessment name keyword (default=None) |
| assessor_id |  str | Assessor ID to filter based on assessor |
| unit_name |    List[str]   |   Competencies to filter on |
| status | List[str] |    Status of Submitted Assessment |
| type | List[str] |    Type of Submitted Assessment |
| result | List[str] |    Result of Submitted Assessment if any |
| skip | int |    Number of objects to be skipped (default=0) |
| type | int |    The size of array to be returned (default=10) |


:::

Hitting this EndPoint fetches the list of submitted assessment responses which match the provided filter.

```json
{
    "success": true,
    "message": "Successfully fetched the submitted assessments.",
    "data": {
        "records": [{
        "assessment_id": "uuid of assessment for which the submitted assessment is created",
        "learner_id": "uuid of learner submitting the assessment",
        "assessor_id": "uuid of assessor who will assess the submitted assessment",
        "learner_name": "name of learner who has attempted the submitted assessment",
        "unit_name": "name of pathway unit of the assessment for which the submitted assessment is created",
        "max_attempts": 3,
        "instructor_name": "name of instructor who has created the assessment",
        "type": "type of assessment",
        "plagiarism_score": null,
        "plagiarism_report_path": null,
        "submission_gcs_paths": [],
        "result": null,
        "pass_status": true,
        "status": "status of the submitted assessment",
        "is_flagged": false,
        "comments": null,
        "timer_start_time": "2023-01-02 13:11:50.331743+00:00",
        "attempt_no": 1,
        "learner_session_id": "session id of learnosity",
        "learner_session_data": {
            "max_score": 40,
            "responses": [
                {
                    "score": 1,
                    "item_reference": "293486384",
                    "dt_score_updated": "2017-06-19T02:03:19Z",
                    "response_id": "2571d802-0095-4d66-94bc-4cfa44b0ebbe",
                    "max_score": 1
                }
            ],
            "session_id": "4d3115f0-1235-4613-5be6fc6e6b2e",
            "status": "Completed",
            "activity_id": "chemistry_classtest1",
            "subscores": [
                {
                    "score": 19,
                    "num_attempted": 20,
                    "num_questions": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "id": "subscore-1",
                    "title": "biochem",
                    "attempted_max_score": 20,
                    "max_score": 20
                },
                {
                    "attempted_max_score": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "num_attempted": 20,
                    "num_questions": 20,
                    "max_score": 20,
                    "score": 20,
                    "title": "inorganics",
                    "id": "subscore-2"
                }
            ],
            "user_id": "17c456c0-89ad-4f72-8010-2f7d991f54bd",
            "score": 39
        },
        "assessor_session_id": null,
        "submitted_rubrics": null,
        "overall_feedback": null,
        "uuid": "AmifBsWI5uPx23cn6E9L",
        "created_time": "2023-01-02 13:11:50.331743+00:00",
        "last_modified_time": "2023-01-02 13:11:50.531421+00:00",
        "created_by": "",
        "last_modified_by": ""
    },
    {
        "assessment_id": "uuid of assessment for which the submitted assessment is created",
        "learner_id": "uuid of learner submitting the assessment",
        "assessor_id": "uuid of assessor who will assess the submitted assessment",
        "learner_name": "name of learner who has attempted the submitted assessment",
        "unit_name": "name of pathway unit of the assessment for which the submitted assessment is created",
        "max_attempts": 3,
        "instructor_name": "name of instructor who has created the assessment",
        "type": "type of assessment",
        "plagiarism_score": null,
        "plagiarism_report_path": null,
        "submission_gcs_paths": [],
        "result": null,
        "pass_status": true,
        "status": "status of the submitted assessment",
        "is_flagged": false,
        "comments": null,
        "timer_start_time": "2023-01-02 13:11:50.331743+00:00",
        "attempt_no": 2,
        "learner_session_id": "session id of learnosity",
        "learner_session_data": {
            "max_score": 40,
            "responses": [
                {
                    "score": 1,
                    "item_reference": "293486384",
                    "dt_score_updated": "2017-06-19T02:03:19Z",
                    "response_id": "2571d802-0095-4d66-94bc-4cfa44b0ebbe",
                    "max_score": 1
                }
            ],
            "session_id": "4d3115f0-1235-4613-5be6fc6e6b2e",
            "status": "Completed",
            "activity_id": "chemistry_classtest1",
            "subscores": [
                {
                    "score": 19,
                    "num_attempted": 20,
                    "num_questions": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "id": "subscore-1",
                    "title": "biochem",
                    "attempted_max_score": 20,
                    "max_score": 20
                },
                {
                    "attempted_max_score": 20,
                    "items": [
                        "293486384",
                        "293481468",
                        "293475858",
                        "293475234",
                        "292922805"
                    ],
                    "num_attempted": 20,
                    "num_questions": 20,
                    "max_score": 20,
                    "score": 20,
                    "title": "inorganics",
                    "id": "subscore-2"
                }
            ],
            "user_id": "17c456c0-89ad-4f72-8010-2f7d991f54bd",
            "score": 39
        },
        "assessor_session_id": null,
        "submitted_rubrics": null,
        "overall_feedback": null,
        "uuid": "AmifBsWI5uPx23cn6E9Lk",
        "created_time": "2023-01-02 13:11:50.331743+00:00",
        "last_modified_time": "2023-01-02 13:11:50.531421+00:00",
        "created_by": "",
        "last_modified_by": ""
    }
    ],
        "total_count": 10000
    }
}
```

If no submitted assessment match the given filter or search parameters then the response would be as follows:

```json
{
  "success": true,
  "message": "Successfully fetched the submitted assessments.",
  "data": []
}
```
