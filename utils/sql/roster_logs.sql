CREATE TABLE IF NOT EXISTS rosterLogs (
        message_id STRING NOT NULL OPTIONS(description = "unique ID"),
        `collection` STRING NOT NULL,
        event_type STRING NOT NULL,
        `resource` STRUCT <userId STRING, courseId STRING>,
        publish_time TIMESTAMP,
        `timestamp` TIMESTAMP);