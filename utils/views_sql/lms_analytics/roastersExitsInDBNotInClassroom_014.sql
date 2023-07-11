CREATE OR REPLACE VIEW
`lms_analytics.roastersExitsInDBNotInClassroom` AS
(WITH sectionClassroomRoasterView AS (SELECT
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
AND roasterView.user_emailAddress=enrollmentView.user_email)
SELECT user_email,
user_id,
enrollment_id,
enrollment_status,
section_id,
cohort_id,
invitation_id,
enrollment_role FROM sectionClassroomRoasterView WHERE user_gaia_id is NULL);