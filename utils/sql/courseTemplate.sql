CREATE TABLE IF NOT EXISTS courseTemplate (
        courseTemplateId STRING NULLABLE OPTIONS(description = "firestore uuid from courseTemplate table"),
        classroomId STRING NULLABLE OPTIONS(description = "course id of google classroom course"),
        name STRING NULLABLE OPTIONS(description = "name of section as mentioned in google classroom"),
        description STRING NULLABLE OPTIONS(description = "description of section as mentioned in google classroom"),
        instructionalDesigner STRING NULLABLE,
        timestamp TIMESTAMP NULLABLE);