---
sidebar_label: Fetching flagged assessments
sidebar_position: 1
---

### Fetching a list of flagged submitted assessments by an instructor

When an instructor wants to fetch a list of flagged submissions associated to him, then the assessor would use the following endpoint in Assessment Service.
**`[GET]<APP_URL>/assessment-service/api/v1/submitted-assessments?is_flagged=True?assessor_id=<instructor_id>`**

Upon successfully hitting the endpoint will give a list of all flagged submitted assessments submitted by learners who are associated to the instructor `<instructor_id>` in LearnerAssociationGroups.

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
                "is_flagged": true,
                "comments": [
                                {
                                "comment": "Flagged comment",
                                "type": "flag", 
                                "access": "",
                                "author": "",
                                "created_time": "DateTime"
                                }
                            ],
                "timer_start_time": "Updated DateTime",
                "attempt_no": 1,
                "learner_session_id": "learnosity_session_id1",
                "learner_session_data": {},
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
