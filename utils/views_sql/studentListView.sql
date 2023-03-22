CREATE OR REPLACE VIEW
`lms_analytics.studentListView` as
SELECT 
a.message_id AS message_id,
a.resource.userId AS userId,
a.collection AS collection,
a.event_type AS event_type,
b.emailAddress AS emailAddress,
b.name.fullName AS fullName, 
a.resource.courseId AS courseId,
c.courseTemplateName AS courseTemplateName,
c.sectionName AS sectionName,
d.name AS cohortName
FROM `lms_analytics.rosterLogs` a
JOIN `lms_analytics.userCollection` b ON a.message_id = b.message_id
JOIN `lms_analytics.sectionView` c ON a.resource.courseId = c.courseId
JOIN `lms_analytics.cohortView` d ON c.cohortId = d.cohortId
WHERE collection = 'courses.students'