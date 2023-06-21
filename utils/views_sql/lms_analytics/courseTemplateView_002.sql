CREATE OR REPLACE VIEW
`lms_analytics.courseTemplateView` as
SELECT 
courseTemplateId,			
name,		
description,			
classroomId,
instructionalDesigners,
timestamp
 FROM
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY courseTemplateId ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.courseTemplate`
) coursetemplate
    WHERE
      coursetemplate.row_num = 1