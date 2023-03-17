CREATE OR REPLACE VIEW
  userCollectionView AS
SELECT * FROM
(
SELECT *, ROW_NUMBER() OVER(PARTITION BY id ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.userCollection`
) a
    WHERE
      a.row_num = 1
      AND a.event_type != 'DELETED'
