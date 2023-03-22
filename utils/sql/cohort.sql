CREATE TABLE IF NOT EXISTS cohort (
        cohortId STRING NULLABLE OPTIONS(description = "firestore uuid from cohort table"),
        name STRING NULLABLE OPTIONS(description = "cohort name"),
        description STRING NULLABLE,
        startDate TIMESTAMP NULLABLE,
        endDate TIMESTAMP NULLABLE,
        registrationStartDate TIMESTAMP NULLABLE,
        registrationEndDate TIMESTAMP NULLABLE,
        maxStudents INTEGER NULLABLE,
        timestamp TIMESTAMP NULLABLE);