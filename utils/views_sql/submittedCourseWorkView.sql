CREATE OR REPLACE VIEW
  submittedCourseWorkCollectionView AS
SELECT * FROM
(SELECT uuid	as userColl_uuid,	
id as userColl_id,
name as userColl_name,		
emailAddress as userColl_emailAddress,
photoUrl	as userColl_photoUrl,			
verifiedTeacher	as userColl_verifiedTeacher,		
permissions	as userColl_permissions,		
event_type	as userColl_event_type,			
timestamp	as userColl_timestamp,			
message_id as userColl_message_id FROM(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `userCollection`
) a
    WHERE
      a.row_num = 1
      AND a.event_type != 'DELETED') as user,(SELECT uuid as submittedColl_uuid,
        courseId as submittedColl_courseID,
        courseWorkId as submittedColl_courseWorkId,
        id as submittedColl_id,
        userId as submittedColl_userId,
        creationTime as submittedColl_creationTime,
        updateTime as submittedColl_updateTime,
        `state` as submittedColl_state,
        late as submittedColl_late,
        draftGrade as submittedColl_draftGrade,
        assignedGrade as submittedColl_assignedGrade,
        alternateLink as submittedColl_alternateLink,
        courseWorkType as submittedColl_courseWorkType,
        associatedWithDeveloper as submittedColl_associatedWithDeveloper,
        assignmentSubmission as submittedColl_assignmentSubmission,
        submissionHistory as submittedColl_submissionHistory,
        shortAnswerSubmission as submittedColl_shortAnswerSubmission,
        multipleChoiceSubmission as submittedColl_multipleChoiceSubmission,
        event_type as submittedColl_event_type,
        `timestamp` as submittedColl_timestamp,
        message_id as submittedColl_message_id FROM(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `submittedCourseWorkCollection`
) b
    WHERE
      b.row_num = 1
      AND b.event_type != 'DELETED') as submitted where user.userColl_id=submitted.submittedColl_userId
