@skill-service
Feature: Align skills to knowledge nodes

    @matching-engine
    Scenario: Fetch skills that align with given knowledge node by id with correct request payload
        Given That a user can fetch skills that align with given knowledge node by id via Competency Management
            When The mechanism to align skills to knowledge node is applied with correct request payload
                Then Knowledge service will align and return skills that are relevant to the knowledge node corresponding to given knowledge node id

    Scenario: Unable to align skills to knowledge node by id when invalid knowledge node id is given
        Given That a user has access to fetch skills that align with given knowledge node by id via Competency Management
            When The mechanism to align skills to knowledge node is applied with invalid knowledge node id
                Then Knowledge service will throw an internal error while aligning skills to knowledge node as invalid knowledge node id was given

    Scenario: Unable to align skills to knowledge node by id when invalid skill alignment source is given
        Given That a user is allowed to fetch skills that align with given knowledge node by id via Competency Management
            When The mechanism to align skills to knowledge node is applied with invalid skill alignment source
                Then Knowledge service will throw an internal error while aligning skills to knowledge node as invalid skill alignment source was given

    Scenario: Unable to align skills to knowledge node by id when invalid knowledge level is given
        Given That a user is privileged to fetch skills that align with given knowledge node by id via Competency Management
            When The mechanism to align skills to knowledge node is applied with invalid knowledge level
                Then Knowledge service will throw an internal error while aligning skills to knowledge node as invalid knowledge level was given

    Scenario: Unable to align skills to knowledge node by id when knowledge node id is missing
        Given That a user has privilege to fetch skills that align with given knowledge node by id via Competency Management
            When The mechanism to align skills to knowledge node is applied with missing knowledge node id
                Then Knowledge service will throw a validation error while aligning skills to knowledge node as knowledge node id is missing

    Scenario: Unable to align skills to knowledge node by id when skill alignment source is missing
        Given That a user has privileges to fetch skills that align with given knowledge node by id via Competency Management
            When The mechanism to align skills to knowledge node is applied with missing skill alignment source
                Then Knowledge service will throw a validation error while aligning skills to knowledge node as skill alignment source is missing

    Scenario: Unable to align skills to knowledge node by id when knowledge level is missing
        Given That a user has access privileges to fetch skills that align with given knowledge node by id via Competency Management
            When The mechanism to align skills to knowledge node is applied with missing knowledge level
                Then Knowledge service will throw a validation error while aligning skills to knowledge node as knowledge level is missing

    @matching-engine
    Scenario: Update docs on firestore for given knowledge node ids with skills that align by triggering batch job
        Given That a user has access to align and update knowledge nodes with relevant skills by triggering batch job via Competency Management
            When The mechanism to trigger a batch job to update knowledge nodes for given node ids with aligned skills is applied
                Then Knowledge service will create a batch job to align relevant skills to given knowledge node ids and update the same on firestore

    Scenario: Unable to align & update skills to knowledge node by id when invalid knowledge node id is given
        Given That a user has access to update skills that align with given knowledge node by triggering a batch job via Competency Management
            When The mechanism to trigger a batch job to align and align skills to knowledge node is applied with invalid knowledge node id
                Then Knowledge service will throw an internal error and batch job will not be triggered as invalid knowledge node id was given

    Scenario: Unable to align & update skills to knowledge node by id when invalid skill alignment source is given
        Given That a user is allowed to update skills that align with given knowledge node by triggering a batch job via Competency Management
            When The mechanism to trigger a batch job to align and update skills to knowledge node is applied with invalid alignment source
                Then Knowledge service will throw an internal error and batch job will not be triggered as invalid alignment source was given

    Scenario: Unable to align & update skills to knowledge node by id when invalid knowledge level is given
        Given That a user is privileged to update skills that align with given knowledge node by triggering a batch via Competency Management
            When The mechanism to trigger a batch job to align and update skills to knowledge node is applied with invalid knowledge level
                Then Knowledge service will throw an internal error and batch job will not be triggered as invalid knowledge level was given

    Scenario: Unable to align & update skills to knowledge node by id when knowledge node id is missing
        Given That a user has privilege to update skills that align with given knowledge node by triggering a batch via Competency Management
            When The mechanism to trigger a batch job to align and update skills to knowledge node is applied with missing knowledge node id
                Then Knowledge service will throw a validation error and batch job will not be triggered as knowledge node id is missing

    Scenario: Unable to align & update skills to knowledge node by id when alignment source is missing
        Given That a user has privileges to update skills that align with given knowledge node by triggering a batch via Competency Management
            When The mechanism to trigger a batch job to align and update skills to knowledge node is applied with missing alignment source
                Then Knowledge service will throw a validation error and batch job will not be triggered as alignment source is missing

    Scenario: Unable to align & update skills to knowledge node by id when knowledge level is missing
        Given That a user has access privileges to update skills that align with given knowledge node by triggering a batch via Competency Management
            When The mechanism to trigger a batch job to align and update skills to knowledge node is applied with missing knowledge level
                Then Knowledge service will throw a validation error and batch job will not be triggered as knowledge level is missing
