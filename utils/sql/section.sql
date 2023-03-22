CREATE TABLE IF NOT EXISTS section (
        sectionId STRING NULLABLE OPTIONS(description = "firestore uuid from sections table"),
        courseId STRING NULLABLE OPTIONS(description = "course id of google classroom course"),
        name STRING NULLABLE OPTIONS(description = "name of section as mentioned in google classroom"),
        description STRING NULLABLE OPTIONS(description = "description of section as mentioned in google classroom"),
        classroomUrl STRING NULLABLE OPTIONS(description = "url of the class in google classroom"),
        courseTemplateId STRING NULLABLE OPTIONS(description = "firestore uuid from courseTemplate table"),
        cohortId STRING NULLABLE OPTIONS(description = "firestore uuid from cohort table"),
        timestamp TIMESTAMP NULLABLE);