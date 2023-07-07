Feature: Get files uploaded to temp folder on GCS

    Scenario: User wants to fetch the files present in the Assessment Author's temp folder on GCS
        Given that valid user_id exists and files are successfully uploaded to Assessment Author's temp folder on GCS
            When API request is sent to get list of files from Assessment Author's temp folder on GCS
                Then the API will successfully fetch the files from Assessment Author's temp folder on GCS

    Scenario: User wants to fetch the files present in the Learner's temp folder on GCS
        Given that valid user_id exists and files are successfully uploaded to Learner's temp folder on GCS
            When API request is sent to get list of files from Learner's temp folder on GCS
                Then the API will successfully fetch the files from Learner's temp folder on GCS
