CREATE OR REPLACE VIEW
`lms_analytics.roastersInvitedInDBExitsInClassroom` AS
(WITH classroomSectionRoasterView AS (SELECT
enrollmentView.user_email,
enrollmentView.user_id,
enrollmentView.enrollment_id,
enrollmentView.enrollment_status,
enrollmentView.section_id,
enrollmentView.cohort_id,
enrollmentView.invitation_id,
enrollmentView.enrollment_role,
roasterView.roster_collection,
roasterView.user_gaia_id
FROM `lms_analytics.sectionEnrollmentRecordView` enrollmentView LEFT OUTER JOIN
`lms_analytics.courseRosterEnrichmentView` roasterView
ON enrollmentView.section_id=roasterView.section_id
AND lower(roasterView.user_emailAddress) = lower(enrollmentView.user_email))
SELECT lower(user_email) as user_email,				
user_id,			
enrollment_id,				
enrollment_status,			
section_id,		
cohort_id,				
invitation_id,			
enrollment_role,			
roster_collection,				
user_gaia_id	 FROM classroomSectionRoasterView WHERE 
user_gaia_id IS NOT NULL and enrollment_status="invited");