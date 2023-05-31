---
sidebar_label: Evaluating Submitted Assessments
sidebar_position: 2
---

# Evaluating a Submitted Assessments

The following steps are to create the flow for evaluating Submitted Assessments.


### Starting an Evaluation
When the assessor wants to start evaluating a submitted assessment, then the assessor would use the following endpoint in Assessment Service.
**`[POST]<APP_URL>/assessment-service/api/v1/submitted-assessment/<submitted_assessment_id>/learner/all-submissions`**

Upon successfully hitting the endpoint will give a list of submitted assessments which have the same `learner_id` and `assessment_id` as the passed `submitted_assessment_id`. Each entry of the list would be an attempt on that assessment by that learner. The list would be started by attempt_no which indicates the attempt number of that particular submission. The response would look as mentioned below:

```json
{
    "success": true,
    "message": "Successfully fetched the submitted assessments",
    "data": [
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
                "attempt_no": 1,
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
### Call for Session Creation
The above mentioned response will then be utilized to view previously submitted assessments along with their responses and the latest submission as well for which evaluation is to be completed. When the assessor starts evaluating the latest submission then, there will be a call to Rules Engine with the verb as **evaluation_started**. This will create a new session for the assessor for starting the evaluation and Rules Engine will internally call Assessment Service to update the Submitted Assessment with the assessor's session_id. The following endpoint will be used with the below mentioned request body:
**`[POST]<APP_URL>/rules-engine/api/v1/execute-rule`** 
```json
 {
    "node_id": "submitted_assessment_id",
    "node_type": "submitted_assessments",
    "user_id": "assessor_user_id",
    "session_id": "assessor_login_session_id",
    "verb": "evaluation_started"
}
```

To get more information on how to execute rules refer [Execute Rules Engine EndPoint](../Rules%20Engine/execute_rules_engine_endpoint.md)

Upon successfully hitting the endpoint will give the following data as response:
```json
{
    "success": true,
    "message": "Successfully executed the following rules",
    "data": [
      {
        "user_id": "assessor_user_id",
        "parent_session_id": "assessor_login_session_id",
        "session_data": {
          "learnosity_session_id": "cf71bcf0-516f-4156-8ca9-d65115045a1e",
          "node_id": "submitted_assessment_id",
          "node_type": "submitted_assessments"
        },
        "session_id": "sample_session_id",
        "created_time": "2023-01-17 16:49:54.203242+00:00",
        "last_modified_time": "2023-01-17 16:49:54.403312+00:00"
      }
    ]
}
```
The response for this rule contains a `Session` object. The `learnosity_session_id` along can be used as the feedback or assessor session_id to render rubrics.

### Completing an Evaluation
When the assessor is done with the evaluation and wants to submit the response, then the following endpoint from Rules Engine will be used **`[POST]<APP_URL>/rules-engine/api/v1/execute-rule`** 

```json
{
    "node_id": "submitted_assessment_id",
    "node_type": "submitted_assessments",
    "user_id": "assessor_user_id",
    "session_id": "assessor_session_id",
    "verb": "evaluated",
    "data": {
        "submitted_rubrics": [
            {
                "rubric_criteria_id": "sample_rubric_criteria_id",
                "result": "Exemplary"
            },
            {
                "rubric_criteria_id": "sample_rubric_criteria_id",
                "result": "Not Evident",
                "feedback": "Didn't submit"
            },
            {
                "rubric_criteria_id": "sample_rubric_criteria_id",
                "result": "Needs Improvement",
                "feedback": "Need to redo"
            }
        ],
        "overall_feedback": "Need to resubmit"
    }
}
```

:::note

submitted_rubrics contains following fields:
- **rubric_criteria_id**: uuid for the rubric criteria evaluated by assessor
- **result**: field containing result for the rubric_criteria, allowed values: "Exemplary", "Proficient", "Needs improvement", "Not evident"
- **feedback**: optional field for feedback on individual rubric_criteria 

:::

To get more information on how to execute rules refer [Execute Rules Engine EndPoint](../Rules%20Engine/execute_rules_engine_endpoint.md)

Upon successfully hitting the endpoint, the following events will take place:
1. Assessor's evaluation will be according to submitted_rubrics and will be saved in the Submitted Assessment for the given ID.
2. If all the submitted_rubrics have result as "Exemplary" or "Proficient" then the Learner passes else fails
3, If submitted_assessment is of type SRL (srl, static_srl, cognitive_wrapper) then submitted_rubrics can be passed as empty list since it would always be passed
4. LearnerProfile of the Learner whose submission was evaluated will be updated with final pass_status.
5. If learner passed relative achievements and skills would be updated in LearnerProfile

The response that contains updated Submitted Assessment will look as mentioned below:
```json
{
    "success": true,
    "message": "Successfully executed the following rules",
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
          "pass_status": true,
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
          "attempt_no": 1,
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
