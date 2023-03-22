CREATE OR REPLACE VIEW
`lms_analytics.studentGradeBookView` as
SELECT
a.submittedColl_courseID AS courseWork_id,
a.userColl_emailAddress AS emailAddress,
a.userColl_name.fullName AS fullName,
b.coursework_title AS coursework_title,
b.courseWork_maxPoints AS maxPoints,
a.submittedColl_assignedGrade AS assignedGrade,
a.submittedColl_draftGrade AS draftGrade,
b.section_name AS section,
b.cohort_name AS cohort
FROM `lms_analytics.submittedCourseWorkCollectionView` a
JOIN `lms_analytics.courseWorkCollEnrichedView` b ON a.submittedColl_courseWorkId = b.courseWork_id