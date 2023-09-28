---
sidebar_label: Fetch Submitted Assessments for a Learner
sidebar_position: 4
---

# Fetch Submitted Assessments for a Learner


### Fetch List of All Submitted Assessments responses for a Learner for a given Assessment:

To fetch list of all submitted assessments responses for a given learner for a given assessment, a **GET** request has to be made to the API endpoint - **`<APP_URL>/assessment-service/api/v1/submitted-assessment/<submitted_assessment_id>/learner/all-submissions`**.


Hitting this EndPoint fetches the list of submitted assessment responses for a given learner for a given assessment.

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

If the submitted assessment is not present for a given uuid - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Submitted Assessment with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```


### Fetch the latest submitted assessment response of a Learner on a given Assessment

To fetch the latest submitted assessment response of a learner on a given assessment, a **GET** request has to be made to the API endpoint - **`<APP_URL>/assessment-service/api/v1/submitted-assessment/<submitted_assessment_id>/learner/latest-submission`**.


Hitting this EndPoint fetches the last response of submitted assessment for a given learner on a given assessment.

```json
{
    "success": true,
    "message": "Successfully fetched the submitted assessment",
    "data": {
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


### Fetch all submitted assessments of a learner

To fetch all submitted assessments of a learner (for all the assessments), a **GET** request has to be made to the API endpoint - **`<APP_URL>/assessment-service/api/v1/learner/<learner_id>/submitted-assessments`**.


Hitting this EndPoint fetches the list of all responses of submitted assessment for a given learner.

```json
{
    "success": true,
    "message": "Successfully fetched the submitted assessments.",
    "data": {
        "records": [{
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
    }],
        "total_count": 10000
    }
}
```
If the learner is not present for a given learner_id - **`asd98798as7dhjgkjsdfh`** then the response would be as follows:

```json
{
  "success": false,
  "message": "Learner with uuid asd98798as7dhjgkjsdfh not found",
  "data": null
}
```