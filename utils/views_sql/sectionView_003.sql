CREATE OR REPLACE VIEW
`lms_analytics.sectionView` as
with section as (SELECT * from(
SELECT *, ROW_NUMBER() OVER(PARTITION BY courseId ORDER BY timestamp DESC) AS row_num
FROM `lms_analytics.section`
) a where a.row_num=1 )

SELECT
section.sectionId AS sectionId,
section.courseId AS courseId,
section.name AS sectionName,
section.description AS description,
courseTemplate.name AS courseTemplateName,
section.classroomUrl AS classroomUrl,
section.courseTemplateId AS courseTemplateId,
section.cohortId AS cohortId,
section.status AS sectionStatus,
section.timestamp AS timestamp
FROM section
JOIN `lms_analytics.courseTemplateView` as courseTemplate ON section.courseTemplateId = courseTemplate.courseTemplateId 
    