CREATE OR REPLACE VIEW
`lms_analytics.enrollmentFailureLogsView` as
SELECT 
email ,
error_type,
traceback ,
log_time ,
section_id,
cohort_id
 FROM
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY email ORDER BY log_time DESC) AS row_num
FROM `lms_analytics.enrollmentFailureLogs`
) logs
WHERE logs.row_num = 1