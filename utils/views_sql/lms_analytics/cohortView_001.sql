CREATE OR REPLACE VIEW
`lms_analytics.cohortView` as
SELECT 
cohortId,			
name,		
description,			
startDate,			
endDate,			
registrationStartDate,			
registrationEndDate,			
maxStudents,			
timestamp
 FROM
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY cohortId ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.cohort`
) cohort
WHERE cohort.row_num = 1