CREATE OR REPLACE VIEW
  `lms_analytics.submittedCourseWorkCollectionView` AS
SELECT * FROM
(SELECT uuid	as user_uuid,	
id as user_id,
name as user_name,		
emailAddress as user_email_address,
photoUrl	as user_photo_url,			
verifiedTeacher	as user_verified_teacher,		
permissions	as user_permissions,		
event_type	as user_event_type,			
timestamp	as user_timestamp,			
message_id as user_message_id FROM(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.userCollection`
) a
    WHERE
      a.row_num = 1
      AND a.event_type != 'DELETED') as user,(SELECT uuid as submission_uuid,
        courseId as submission_course_id,
        courseWorkId as submission_course_work_id,
        id as submission_id,
        userId as submission_user_id,
        creationTime as submission_creation_time,
        updateTime as submission_update_time,
        `state` as submission_state,
        late as submission_late,
        draftGrade as submission_draft_grade,
        assignedGrade as submission_assigned_grade,
        alternateLink as submission_alternate_link,
        courseWorkType as submission_course_work_type,
        associatedWithDeveloper as submission_associated_with_developer,
        assignmentSubmission as submission_assignment_submission,
        submissionHistory as submission_submission_history,
        shortAnswerSubmission as submission_short_answer_submission,
        multipleChoiceSubmission as submission_multiple_choice_submission,
        event_type as submission_event_type,
        `timestamp` as submission_timestamp,
        message_id as submission_message_id FROM(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.submittedCourseWorkCollection`
) b
    WHERE
      b.row_num = 1
      AND b.event_type != 'DELETED') as submitted where user.user_id=submitted.submission_user_id
