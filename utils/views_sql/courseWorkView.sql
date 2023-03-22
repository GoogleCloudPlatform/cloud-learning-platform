CREATE OR REPLACE VIEW
  courseWorkCollectionView AS
SELECT 
uuid,			
id,			
courseId,			
title,			
description,			
materials,			
state,			
alternateLink,			
creationTime,			
updateTime,			
dueDate,			
dueTime,			
scheduledTime,			
maxPoints,			
workType,			
associatedWithDeveloper,			
assigneeMode,			
individualStudentsOptions,			
submissionModificationMode,			
creatorUserId,			
topicId,			
gradeCategory,			
assignment,			
multipleChoiceQuestion,			
event_type,			
timestamp,			
message_id
 FROM
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.courseWorkCollection`
) a
    WHERE
      a.row_num = 1
      AND a.event_type != 'DELETED'
