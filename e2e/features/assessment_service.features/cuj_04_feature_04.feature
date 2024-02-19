@assessment
Feature: Learner can download a zip containing all files linked to an assessment

    Scenario: Learner wants to download a zip containing all files linked to an assessment
        Given that valid assessment with linked resources exists
            When API request is sent to download zip of all contents
                Then the API will return a zip file

    Scenario: Learner wants to download a zip but some files are missing on GCS
        Given that valid assessment but some files are missing
            When API request is sent to download zip with missing contents
                Then the API will return an error saying some files are missing on GCS

    Scenario: Learner wants to download a zip but no files are linked to the assessment
        Given that valid assessment but no files are linked to the assessment
            When API request is sent to download zip of missing contents
                Then the API will return an error saying no files are linked to the assessment
