CREATE OR REPLACE VIEW
`lms_analytics.roastersExitsInClassroomNotInDB` AS
(WITH classroomSectionRoasterView AS (SELECT
roasterView.user_emailAddress,
roasterView.user_gaia_id,
roasterView.section_id,
roasterView.cohort_id,
roasterView.course_id,
roasterView.roster_collection,
enrollmentView.enrollment_id
FROM `lms_analytics.courseRosterEnrichmentView` roasterView
LEFT OUTER JOIN `lms_analytics.sectionEnrollmentRecordView` enrollmentView
ON roasterView.section_id=enrollmentView.section_id AND roasterView.user_emailAddress=enrollmentView.user_email)
SELECT user_emailAddress,
user_gaia_id,
section_id,
cohort_id,
course_id,
roster_collection FROM classroomSectionRoasterView WHERE enrollment_id IS NULL)