CREATE OR REPLACE VIEW
`lms_analytics.studentGradeBookView` as
SELECT
a.submission_course_id AS course_id,
a.submission_course_work_id AS courseWork_id,
a.user_email_address AS emailAddress,
a.user_name.fullName AS fullName,
b.courseWork_title AS coursework_title,
b.courseWork_maxPoints AS maxPoints,
a.submission_assigned_grade AS assignedGrade,
a.submission_draft_grade AS draftGrade,
b.section_name AS section,
b.cohort_name AS cohort
FROM `lms_analytics.submittedCourseWorkCollectionView` a
JOIN `lms_analytics.courseWorkCollEnrichedView` b ON a.submission_course_work_id = b.courseWork_id