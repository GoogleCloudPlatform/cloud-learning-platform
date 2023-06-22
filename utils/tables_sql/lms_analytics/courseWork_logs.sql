CREATE TABLE IF NOT EXISTS courseWorkLogs (
        message_id STRING NOT NULL OPTIONS(description = "unique ID"),
        `collection` STRING NOT NULL,
        event_type STRING NOT NULL,
        `resource` JSON,
        publish_time TIMESTAMP,
        `timestamp` TIMESTAMP);