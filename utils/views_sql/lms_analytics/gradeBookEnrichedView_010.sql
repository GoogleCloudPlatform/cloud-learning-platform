CREATE OR REPLACE VIEW
  `lms_analytics.gradeBookEnrichedView` AS
WITH studentCourse as (
SELECT * FROM `lms_analytics.courseRosterEnrichmentView`
WHERE roster_collection="courses.students" ),
courseWorkCollection as (
  SELECT * FROM studentCourse 
  join `lms_analytics.courseWorkCollectionView` as courseWorkCollection 
  on studentCourse.course_id=courseWorkCollection.courseId
  )
SELECT 
course_id,			
course_name,			
course_section,			
course_description,
course_url,						
user_gaia_id,			
courseWorkCollection.user_name,			
courseWorkCollection.user_emailAddress as user_email_address,								
courseWorkCollection.user_photoUrl as user_photo_url,			
courseWorkCollection.user_permissions,			
courseWorkCollection.user_verifiedTeacher as  user_verified_teacher,			
section_id,			
section_name,			
cohort_id,			
cohort_name,			
cohort_description,			
cohort_registration_start_date,			
cohort_registration_end_date,			
cohort_start_date,			
cohort_end_date,			
cohort_max_students,						
id as course_work_id,					
title as course_work_title,			
description as course_work_description,			
materials as course_work_materials,			
state as course_work_state,			
alternateLink as course_work_alternate_link,			
creationTime as course_work_creation_time,			
updateTime as course_work_update_time,			
dueDate as course_work_due_date,			
dueTime as course_work_due_time,			
scheduledTime as course_work_schedule_time,			
maxPoints as course_work_max_points,			
workType as course_work_work_type,			
associatedWithDeveloper as course_work_associated_with_developer,			
assigneeMode as course_work_assignee_mode,			
individualStudentsOptions as course_work_individual_students_options,			
submissionModificationMode as course_work_submission_modification_mode,			
creatorUserId as course_work_creator_user_id,			
topicId as course_work_topic_id,			
gradeCategory as course_work_grade_category,			
assignment as course_work_assignment,			
multipleChoiceQuestion as course_work_multiple_choice_question,																	
submission_id,			
submission_user_id,			
submission_creation_time,			
submission_update_time,			
submission_state,			
submission_late,			
submission_draft_grade,			
submission_assigned_grade,			
submission_alternate_link,			
submission_course_work_type,			
submission_associated_with_developer,			
submission_assignment_submission,			
submission_submission_history,			
submission_short_answer_submission,			
submission_multiple_choice_submission	
FROM courseWorkCollection 
left outer join `lms_analytics.submittedCourseWorkCollectionView` as submittedCourseWorkCollection  
on courseWorkCollection.id=submittedCourseWorkCollection.submission_course_work_id 
and courseWorkCollection.user_gaia_id=submittedCourseWorkCollection.submission_user_id 
