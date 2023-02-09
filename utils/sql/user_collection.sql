CREATE TABLE IF NOT EXISTS userCollection (
        uuid STRING NOT NULL OPTIONS(description = "unique id"),
        id STRING NOT NULL OPTIONS(description = "user guy id"),
        `name` STRUCT <givenName STRING, familyName STRING, fullName STRING> NOT NULL,
        `emailAddress` STRING NOT NULL,
        photoUrl STRING,
        verifiedTeacher BOOL,
        Permissions ARRAY < STRING >,
        event_type STRING,
        `timestamp` TIMESTAMP,
        message_id STRING NOT NULL);