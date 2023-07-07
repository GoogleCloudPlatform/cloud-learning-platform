CREATE OR REPLACE VIEW
  `lms_analytics.sectionEnrollmentRecordView` AS
SELECT 
enrollment_id,
email as user_email,
user_id,
role as enrollment_role,
status as enrollment_status,
invitation_id,
section_id,
cohort_id,
course_id,
`timestamp`
FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY enrollment_id ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.sectionEnrollmentRecord`
) a where a.row_num = 1 and a.status!="inactive"