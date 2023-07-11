Feature: Filter and Search on SubmittedAssessment in Assessment services

    Scenario: Fetch list of all SubmittedAssessments submitted by a learner
        Given that an existing student has submitted a bunch of assessments
            When API request is sent to fetch list of all SubmittedAssessments by that learner
                Then the API gives response with the list of all SubmittedAssessments for that learner

    Scenario: Fetch list of all SubmittedAssessments submitted by a learner when leaner id is not found
        Given that a student has submitted a bunch of assessments but the learner id is not created for the student
            When API request is sent to fetch list of all SubmittedAssessments by that learner for the given learner id
                Then the API gives ResourceNotFound Exception as the learner id does not exist

    @filter-api
    Scenario: Fetch unique values of type, result and competency for all manually graded submitted assessments assigned to an existing assessor
        Given that an assessor has access to Assessment Service and wants to fetch all the unique values of type, result and competency for all manually graded submitted assessments assigned to an assessor
            When API request is sent to fetch the unique values with correct assessor id
                Then all the unique values of type, result and competency for all manually graded submitted assessments assigned to the assessor are returned

    Scenario: Fetch unique values of type, result and competency for all manually graded submitted assessments assigned to a nonexistant assessor
        Given that an assessor has access to Assessment Service and needs to fetch all the unique values of type, result and competency for all manually graded submitted assessments assigned to an assessor
            When API request is sent to fetch the unique values with incorrect assessor id
                Then the unique values of type, result and competency will not be fetched and Assessment Service will throw a ResourceNotFound error

    @filter-api
    Scenario: Filter manual graded Submitted Assessments assigned to an existing assessor based on type and result and ascending sort by time to review with correct skip and limit values
        Given that an existing assessor has access to Assessment Service and wants to fetch all the manual graded Submitted Assessments assigned to him based on a list of type and result and sorted by time to review in ascending order
            When API request is sent to fetch filtered Submitted Assessments assigned to the assessor with correct skip and limit value
                Then all the manual graded Submitted Assessments objects assigned to the assessor containing that type and result are fetched in ascending order of time to review

    @filter-api
    Scenario: Filter on type and result and search on name and ascending sort by time to review for manual graded Submitted Assessments assigned to an existing assessor with correct skip and limit values
        Given that an existing assessor has access to Assessment Service and wants to fetch the manual graded Submitted Assessments assigned to him by filtering on a list of type and result and searching on name and sorted by time to review in ascending order
            When API request is sent to fetch filtered and searched Submitted Assessments assigned to an assessor with correct skip and limit value
                Then all the manual graded Submitted Assessments objects assigned to the assessor containing that type, result and name are fetched in ascending order of time to review

    Scenario: Filter/Search Submitted Assessments assigned to an existing assessor with incorrect skip and limit values
        Given that an existing assessor has access to Assessment Service and needs to fetch all the filtered/searched Submitted Assessments assigned to him
            When API request is sent to fetch filtered/searched Submitted Assessments assigned to him with incorrect skip and limit value
                Then the Submitted Assessment objects assigned to him will not be fetched and Assessment Service will throw a Validation error

    Scenario: Filter/Search Submitted Assessments assigned to a nonexisting assessor with correct skip and limit values
        Given that a nonexisting assessor has access to Assessment Service and needs to fetch all the filtered/searched Submitted Assessments assigned to him
            When API request is sent to fetch filtered/searched Submitted Assessments assigned to him with correct skip and limit value
                Then the Submitted Assessment objects assigned to him will not be not be fetched and Assessment Service will throw a ResourceNotFound error

    @filter-api
    Scenario: Assessor wants to see the list of submitted assessments sorted by ascending order for time to review that are required by the assessor to evaluate
        Given that an assessor has access to Assessment Service and wants to fetch the Submitted Assessments that are required to be evaulated sorted by ascending order for time to review
            When API request is sent to fetch the Submitted Assessments that are required to be evaluated by the assessor
                Then the list of Submitted Assessments that are required to be evaluated are fetched in ascending order by time to review

    Scenario: Assessor wants to see the list of submitted assessments sorted by ascending order for time to review that are required by the assessor to evaluate with wrong assessor_id
        Given that an assessor has access to Assessment Service and wants to fetch the Submitted Assessments that are required to be evaulated with wrong assessor_id
            When API request is sent to fetch the Submitted Assessments that are required to be evaluated by the assessor with wrong assessor_id
                Then Assessment Service raises 404 User not Found Exception

    @filter-api
    Scenario: Assessor wants to see the list of submitted assessments of a learner for given experience that can be reviewed
        Given that an Assessor has access to Assessment Service and wants to fetch the Submitted Assessments of a learner for a given experience that can be reviewed
            When API request is sent to fetch the Submitted Assessments of a learner for a given experience that can be reviewed
                Then the list of Submitted Assessments belonging to a learner and the given experience that can be reviewed will be fetched

    Scenario: Assessor wants to see the list of submitted assessments of a learner for given experience that can be reviewed with wrong learner_id
        Given that an Assessor has access to Assessment Service and wants to fetch the Submitted Assessments of a learner for a given experience that can be reviewed with wrong learner_id
            When API request is sent to fetch the Submitted Assessments of a learner for a given experience that can be reviewed with wrong learner_id
                Then Assessment Service raises 404 Learner not Found Exception

    Scenario: Assessor wants to see the list of submitted assessments of a learner for given experience that can be reviewed with wrong learning_experience_id
        Given that an Assessor has access to Assessment Service and wants to fetch the Submitted Assessments of a learner for a given experience that can be reviewed with wrong learning_experience_id
            When API request is sent to fetch the Submitted Assessments of a learner for a given experience that can be reviewed with wrong learning_experience_id
                Then Assessment Service raises 404 LearningExperience not Found Exception