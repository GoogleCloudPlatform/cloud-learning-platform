CREATE OR REPLACE VIEW
  `lms_analytics.rosterLogsView` AS
WITH user as (
  SELECT id,
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
      FROM `lms_analytics.sectionView` as section,
      `lms_analytics.cohortView` as cohort 
      where section.cohortId=cohort.cohortId )
      SELECT  roster.message_id as roster_message_id,
        roster.event_type as roster_event_type,
        roster.collection	as roster_collection,
        user.id as user_id,
        user.name.fullName as user_name,	
        user.emailAddress as user_emailAddress,	
        user.photoUrl	as user_photoUrl,				
        course_id,
        course_name,
        course_section,
        course_description,
        course.course_url,			
        section_id,
        course.section_name,
        course.cohort_id,
        course.cohort_name,
        course.cohort_description,
        course.cohort_registration_start_date,
        course.cohort_registration_end_date,
        course.cohort_start_date,
        course.cohort_end_date,
        course.cohort_max_students,
        user.name as user_name_record,
        user.verifiedTeacher	as user_verifiedTeacher,		
        user.permissions	as user_permissions,
        roster.resource	as roster_resource,
        roster.publish_time	as roster_publish_time,	
        roster.timestamp as roster_timestamp       
FROM  `lms_analytics.rosterLogs` as roster 
JOIN  user on user.id=roster.resource.userId 
JOIN course on roster.resource.courseId=course.course_id
ORDER BY roster.timestamp DESC