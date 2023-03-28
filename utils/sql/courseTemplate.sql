CREATE TABLE IF NOT EXISTS courseTemplate (
        courseTemplateId STRING OPTIONS(description = "firestore uuid from courseTemplate table"),
        classroomId STRING OPTIONS(description = "course id of google classroom course"),
        name STRING OPTIONS(description = "name of Course Template as mentioned in google classroom"),
        description STRING OPTIONS(description = "description of Course Template as mentioned in google classroom"),
        instructionalDesigner STRING ,
        timestamp TIMESTAMP );