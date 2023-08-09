CREATE TABLE IF NOT EXISTS enrollmentFailureLogs (
        email STRING NOT NULL OPTIONS(description = "user email ID"),
        error_type STRING OPTIONS(description = "type of error which is stored"),
        traceback STRING OPTIONS(description = "error traceback"),
        log_time TIMESTAMP OPTIONS(description = "error timestamp"),
        section_id STRING OPTIONS(description = "section Id for enrollment user"),
        cohort_id STRING OPTIONS(description = "cohort Id for enrollment user")
        );