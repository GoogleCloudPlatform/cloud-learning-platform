---
sidebar_label: Viewing, Flagging and Non-Evaluating Submitted Assessments
sidebar_position: 1
---

# Viewing, Flagging and Non-Evaluating Submitted Assessments

The following steps are to create the flow for viewing, flagging and marking  Submitted Assessments as non-evaluated.


### Viewing list of Submitted Assessments assigned to a given assessor (To evaluate/Evaluated)

To create the screen where the list of all submitted assessments assigned to an assessor, the following endpoint of Assessment Service will be used where assessor's user_id is used as a path parameter. The endpoint will only filter out those submitted assessments which are tagged to that assessor and has the status as `evaluation_pending` or `evaluated`.
The assessor's user_id can be retrieved when the Assessor logs in.

To get the list for **To Evaluate** section sorted by time left to review::

**`[GET] <APP_URL>/assessment-service/api/v1/submitted-assessments?assessor_id=<>&status=evaluation_pending&sort_by=timer_start_time&sort_order=ascending`**

To get the list for **Evaluated** section sorted by time when the submission was evaluated::

**`[GET] <APP_URL>/assessment-service/api/v1/submitted-assessments?assessor_id=<>&status=evaluated&sort_by=timer_start_time&sort_order=ascending`**

Upon successfully hitting the endpoint with a valid `user_id`, the following response will be received:
```json
{
    "success": true,
    "message": "Successfully fetched the submitted assessments",
    "data": [
        {
            "assessment_id": "uuid of assessment for which the submitted assessment is created",
            "learner_id": "uuid of learner submitting the assessment",
            "assessor_id": "uuid of assessor who will assess the submitted assessment",
            "type": "type of assessment",
            "plagiarism_score": null,
            "plagiarism_report_path": null,
            "submission_gcs_paths": [],
            "result": null,
            "pass_status": true,
            "status": "evaluation_pending or evaluated",
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
            "created_time": "2023-01-02 13:11:50.331743+00:00",
            "last_modified_time": "2023-01-02 13:11:50.531421+00:00",
            "created_by": "",
            "last_modified_by": "",
            "unit_name": "Learning Experience Name",
            "assessor_to": "Assessor Name",
            "instructor_name": "Instructor Name",
            "instructor_id": "Instructor ID",
            "learner_name": "Learner Name",
            "uuid": "AmifBsWI5uPx23cn6E9L",
            "max_attempts": 1
        }
    ]
}
```

The above stated response is a list of Submitted Assessments assigned to an Assessor with given status.

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
| is_autogradable |  bool | Fetch autograded, or manual graded or both (for None) submissions |
| unit_name |    List[str]   |   Disciplines to filter on |
| unit_name |    List[str]   |   Pathway units to filter on |
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
    "data": [{
        "assessment_id": "uuid of assessment for which the submitted assessment is created",
        "learner_id": "uuid of learner submitting the assessment",
        "assessor_id": "uuid of assessor who will assess the submitted assessment",
        "learner_name": "name of learner who has attempted the submitted assessment",
        "unit_name": "name of pathway unit of the assessment for which the submitted assessment is created",
        "max_attempts": 3,
        "instructor_id": "uuid of instructor",
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
        "type": "type of assessment",
        "learner_name": "name of learner who has attempted the submitted assessment",
        "unit_name": "name of pathway unit of the assessment for which the submitted assessment is created",
        "max_attempts": 3,
        "instructor_id": "uuid of instructor",
        "instructor_name": "name of instructor who has created the assessment",
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
    ]
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

### Flagging a Submitted Assessment
Flagging of a Submitted Assessment can be done by assessor on the account when the submitted assessment might have been plagiarized or the assessor is questioning the Learner's integrity on the Submitted Assessment. Upon marking a submission as flagged, assessor's timer to complete evaluation will stop.
To flag a Submitted Assessment, the following endpoint of Assessment Service will be used with the following request body,
**`[PUT]<APP_URL>/assessment-service/api/v1/submitted-assessment/<submitted_assessment_id>`**

The request body is as follows (subject to change):
```json
{
    "is_flagged": true,
    "comments": {
        "comment": "str",
        "type": "str", 
        "access": "ID",
        "author": ""
    }

}
```
:::note

- **type** field can only have **non-eval and flag** as values
- **author** field is the **user_id** of the user who has commented
- **access** field is used to store the group_id which can view the comment

:::

Upon successfully hitting the API endpoint with the given request body, the submitted assessment will be updated with updated `is_flagged` status and `comments` will give the following response:
```json
{   "success": true,
    "message": "Successfully updated the submitted assessment",
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
        "is_flagged": true,
        "comments": [
            {
            "comment": "str",
            "type": "str", 
            "access": "ID",
            "author": "",
            "created_time": "DateTime"
            }
        ],
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

### Unflagging a submitted assessment
Internal discussion between assessor and instructor might lead to unflagging of a submission. To unflag a submission, the following endpoint will be used with the following request body:
**`[PUT]<APP_URL>/assessment-service/api/v1/submitted-assessment/<submitted_assessment_id>`**


The request body is as follows (subject to change):
```json
{
    "is_flagged": false,
    "comments": {
        "comment": "str",
        "type": "str", 
        "access": "ID",
        "author": ""
    }
}
```
Upon successfully hitting the API endpoint, the submitted assessment data will be updated with updated  `is_flagged` value and `comments`, and `timer_start_time` will be automatically updated to the `DateTime` when the unflagging of the submission was done and timer will again start for the assessor for that particular assessment.

```json
{       "success": true,
        "message": "Successfully updated the submitted assessment",
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
                "comments": [
                                {
                                "comment": "str",
                                "type": "str", 
                                "access": "ID",
                                "author": "",
                                "created_time": "DateTime"
                                }
                            ],
                "timer_start_time": "Updated DateTime",
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

### Marking a Submitted Assessment as non-evaluated
After viewing a learner's submission, the assessor can mark a particular submission as non-evaluated when there are discrepancies with the learner's submission like missing pages or unattempted questions which can happen due to various unknown reasons. In such cases, the assessor has t he ability to mark a submitted assessment as non-evaluated. In this case, the submission is not counted as an attempt for the learner and the learner is asked to re-submit the attempt for the assessment.

To successfully run this entire flow the following endpoint of rules-engine will be used with the below mentioned request body.
**`[POST]<APP_URL>/rules-engine/api/v1/execute-rule`**

To get more information on how to execute rules refer [Execute Rules Engine EndPoint](../Rules%20Engine/execute_rules_engine_endpoint.md)

```json
 {
    "node_id": "str",
    "node_type": "submitted_assessments",
    "user_id": "str",
    "session_id": "str",
    "verb": "non-evaluated",
    "data": {
            "comment": "str",
            "type": "str", 
            "access": "ID",
            "author": ""
        }
    }
 }
        
```

:::note

**type** field can only have **non-eval and flag** as values
**author** field is the **user_id** of the user who has commented
**access** field is used stored the group_id which can view the comment

:::

Upon successfully hitting the endpoint will result in the following things:
1. `attempt_no` is updated for the learner for that assessment in the LearnerProfile and in the SubmittedAssessment Data Item for which the submission was marked as non-evaluated.
2. `status` in LearnerProfile for the assessment ID which is linked to the SubmittedAssessment and the status of the SubmittedAssessment Data item will be updated to evaluated.

Both of these updates will take place via internal API call to Learner Profile Service and Assessment Service respectively.

The response will look like:
```json
{
    "success": true,
    "message": "Successfully executed the rules",
    "data": [
        {
            "assessment_id": "uuid of assessment for which the submitted assessment is created",
            "learner_id": "uuid of learner submitting the assessment",
            "assessor_id": "uuid of assessor who will assess the submitted assessment",
            "type": "type of assessment",
            "plagiarism_score": null,
            "plagiarism_report_path": null,
            "submission_gcs_paths": [],
            "result": "Final result of the submitted assessment",
            "pass_status": false,
            "status": "evaluated",
            "is_flagged": false,
            "comments": [
                            {
                            "comment": "str",
                            "type": "str", 
                            "access": "ID",
                            "author": "",
                            "created_time": "DateTime"
                            }
                        ],
            "timer_start_time": "Updated DateTime",
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
    ]
}
```
