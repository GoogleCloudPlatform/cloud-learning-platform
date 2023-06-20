CREATE OR REPLACE VIEW
`lms_analytics.teacherListView` as
SELECT
roster_resource.userId,
roster_collection,
user_emailAddress,
user_name.fullName, 
course_id,
section_name,
cohort_name,
FROM `lms_analytics.courseRosterEnrichmentView`
WHERE roster_collection = 'courses.teachers'