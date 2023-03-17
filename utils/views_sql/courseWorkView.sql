CREATE OR REPLACE VIEW
  courseWorkCollectionView AS
SELECT * FROM
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.courseWorkCollection`
) a
    WHERE
      a.row_num = 1
      AND a.event_type != 'DELETED'
