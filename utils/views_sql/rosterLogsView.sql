CREATE OR REPLACE VIEW
  lms_analytics.rosterLogsView AS
WITH user as (SELECT id,
        name,		
        emailAddress,
        photoUrl,			
        verifiedTeacher,		
        permissions FROM(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.userCollection`
) a
    WHERE
      a.row_num = 1
      AND a.event_type != 'DELETED')
SELECT 
      roster.message_id as roster_message_id,
        roster.collection	as roster_collection,					
        roster.resource	as roster_resource,
        roster.publish_time	as roster_publish_time,			
        roster.event_type as roster_event_type,
        roster.timestamp as roster_timestamp,
        user.id as user_gaia_id,
        user.name as user_name,		
        user.emailAddress as user_emailAddress,
        user.photoUrl	as user_photoUrl,			
        user.verifiedTeacher	as user_verifiedTeacher,		
        user.permissions	as user_permissions        
FROM `lms_analytics.rosterLogs` as roster JOIN  user on user.id=roster.resource.userId ORDER BY roster.timestamp DESC
