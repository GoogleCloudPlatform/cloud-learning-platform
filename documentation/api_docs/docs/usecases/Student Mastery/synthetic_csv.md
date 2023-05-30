---
sidebar_label: Generate Synthetic Data
sidebar_position: 2
---

# Generate Synthetic Data

For quick experiment, one can leverage the following API to generate a csv with synthetic data that can be used to create user events using bulk-upload endpoint described in the earlier section.

The user needs to enter the number of rows required in the csv.

The API endpoint <APP_URL>/deep-knowledge-tracing/api/v1/synthetic-data accepts the number of rows required as a parameter. On successful POST, the service writes a synthetic CSV to GCS and returns the GCS path in the response.

```json
{
  "success": true,
  "message": "Successfully created the synthetic data in a csv",
  "gcs_path": "gs://project-id/mastery_model/user_events_synthetic/synthetic_events1673005223.csv"
}
```
