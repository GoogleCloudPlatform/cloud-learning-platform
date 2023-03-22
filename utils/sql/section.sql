CREATE TABLE IF NOT EXISTS section (
        sectionId STRING  OPTIONS(description = "firestore uuid from sections table"),
        courseId STRING  OPTIONS(description = "course id of google classroom course"),
        name STRING  OPTIONS(description = "name of section as mentioned in google classroom"),
        description STRING  OPTIONS(description = "description of section as mentioned in google classroom"),
        classroomUrl STRING  OPTIONS(description = "url of the class in google classroom"),
        courseTemplateId STRING  OPTIONS(description = "firestore uuid from courseTemplate table"),
        cohortId STRING  OPTIONS(description = "firestore uuid from cohort table"),
        timestamp TIMESTAMP );