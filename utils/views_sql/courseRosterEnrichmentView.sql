CREATE OR REPLACE VIEW
`lms_analytics.courseRosterEnrichmentView` as
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
      AND a.event_type != 'DELETED'),
      roster as (SELECT * FROM
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY resource.courseId,resource.userId ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.rosterLogs`
) a
    WHERE
      a.row_num = 1 and event_type!="DELETED"),
course as (
  SELECT 
      section.courseId as course_id,
      section.courseTemplateName as course_name,
      section.sectionName as course_section,
      section.description as course_description,
      section.classroomUrl as course_url,
      section.sectionId as section_id,
      section.courseTemplateName as section_name,
      cohort.cohortId as cohort_id,
      cohort.name as cohort_name,
      cohort.description as cohort_description,
      cohort.registrationStartDate as cohort_registration_start_date,
      cohort.registrationEndDate as cohort_registration_end_date,
      cohort.startDate as cohort_start_date,
      cohort.endDate as cohort_end_date,
      cohort.maxStudents as cohort_max_students  
      FROM `lms_analytics.sectionView` as section JOIN
      `lms_analytics.cohortView` as cohort 
      on section.cohortId=cohort.cohortId )
SELECT  course_id,
        course_name,
        course_section,
        course_description,
        roster_collection,
        user_gaia_id,
        user_name,
        user_emailAddress,
        course_url,
        roster_resource,
        roster_message_id,
        roster_publish_time,
        roster_timestamp,
        user_photoUrl,
        user_permissions,
        user_verifiedTeacher,
        section_id,
        course.section_name,
        course.cohort_id,
        course.cohort_name,
        course.cohort_description,
        course.cohort_registration_start_date,
        course.cohort_registration_end_date,
        course.cohort_start_date,
        course.cohort_end_date,
        course.cohort_max_students

        FROM(
SELECT 
      roster.message_id as roster_message_id,
        roster.collection	as roster_collection,
        roster.resource	as roster_resource,
        roster.publish_time	as roster_publish_time,			
        roster.timestamp as roster_timestamp,
        user.id as user_gaia_id,
        user.name as user_name,		
        user.emailAddress as user_emailAddress,
        user.photoUrl	as user_photoUrl,			
        user.verifiedTeacher	as user_verifiedTeacher,		
        user.permissions	as user_permissions        
FROM  roster 
JOIN  user on user.id=roster.resource.userId 
ORDER BY roster.timestamp DESC
) as rosterView JOIN course 
on rosterView.roster_resource.courseId=course.course_id 
ORDER BY course.course_id