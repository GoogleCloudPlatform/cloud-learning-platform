CREATE TABLE IF NOT EXISTS cohort (
        cohortId STRING OPTIONS(description = "firestore uuid from cohort table"),
        name STRING  OPTIONS(description = "cohort name"),
        description STRING,
        startDate TIMESTAMP ,
        endDate TIMESTAMP ,
        registrationStartDate TIMESTAMP ,
        registrationEndDate TIMESTAMP ,
        maxStudents INTEGER ,
        timestamp TIMESTAMP);