Feature: Fetching Learner Progress for any learning hierarchy node that returns progress for the given node and progress for all child nodes

    Scenario: Fetch Learner progress with correct curriculum pathway uuid and learner uuid
        Given that the learner, learner profile, curriculum pathway and the learner progress already exists
            When the curriculum pathway uuid and learner uuid is correctly passed to fetch learner progress
                Then the learner progress for that currciculum pathway will be correctly fetched

    Scenario: Fetch Learner progress with incorrect curriculum pathway uuid and learner uuid
        Given that the curriculum pathway uuid is incorrect and learner uuid is correct
            When the incorrect currciculum pathway uuid and learner uuid is passed to fetch learner progress
                Then the api responds with 404 status and message as Curriculum Pathway not found, cannot fetch progress

    Scenario: Fetch Learner progress with correct curriculum pathway uuid and incorrect learner uuid
        Given that the curriculum pathway to fetch progress already exists
            When the correct currciculum pathway uuid and invalid learner uuid is passed
                Then the api responds with 404 status and message as Learner not found, cannot fetch progress

    Scenario: Fetch Learner progress with correct learning experience uuid and learner uuid
        Given that the learner, learner profile, learning experience and the learner progress already exists
            When the learning experience uuid and learner uuid is correctly passed to fetch learner progress
                Then the learner progress for that learning experience will be correctly fetched

    Scenario: Fetch Learner progress with incorrect learning experience uuid and learner uuid
        Given that the learning experience uuid is incorrect
            When the incorrect learning experience uuid and learner uuid is passed
                Then the api responds with 404 status and message as learning experience not found
    Scenario: Fetch Learner progress with correct learning object uuid and learner uuid
        Given that the learner, learner profile, learning object and the learner progress already exists
            When the learning object uuid and learner uuid is correctly passed to fetch learner progress
                Then the learner progress for that learning object will be correctly fetched

    Scenario: Fetch Learner progress with incorrect learning object uuid and learner uuid
        Given that the learning object uuid is incorrect
            When the incorrect learning object uuid and learner uuid is passed
                Then the api responds with 404 status and message as learning object not found

    Scenario: Fetch Learner progress with correct learning resource uuid and learner uuid
        Given that the learner, learner profile, learning resource and the learner progress already exists
            When the learning resource uuid and learner uuid is correctly passed to fetch learner progress
                Then the learner progress for that learning resource will be correctly fetched

    Scenario: Fetch Learner progress with incorrect learning resource uuid and learner uuid
        Given that the learning resource uuid is incorrect
            When the incorrect learning resource uuid and learner uuid is passed
                Then the api responds with 404 status and message as learning resource not found



