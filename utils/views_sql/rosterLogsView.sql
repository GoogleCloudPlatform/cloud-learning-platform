CREATE OR REPLACE VIEW
  rosterLogsView AS
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
FROM `lms_analytics.userCollection`
) a
    WHERE
      a.row_num = 1
      AND a.event_type != 'DELETED') as user,(SELECT 
      message_id as roster_message_id,
        collection	as roster_collection,						
        resource	as roster_resource,
        publish_time	as roster_publish_time,			
        event_type as roster_event_type,
        `timestamp` as roster_timestamp FROM(
SELECT *, ROW_NUMBER() OVER(PARTITION BY resource.userId ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.rosterLogs`
) b
    WHERE
      b.row_num = 1
      AND b.event_type != 'DELETED') as roster where user.userColl_id=roster.roster_resource.userId
