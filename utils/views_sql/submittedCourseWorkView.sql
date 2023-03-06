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
      AND a.event_type != 'DELETED') as user,(SELECT * FROM(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `submittedCourseWorkCollection`
) b
    WHERE
      b.row_num = 1
      AND b.event_type != 'DELETED') as submitted where user.userColl_id=submitted.userId
