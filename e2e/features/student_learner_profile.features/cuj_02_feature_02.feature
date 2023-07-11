Feature: Reigstrar can view and maintain a learner's academic record

    Scenario: Registrar can access learner academic records
        Given A learner is having some academic records
            When Registrar wants to access academic records of a particular learner
                Then SLP should return the academic records of the particular learner to Reigstrar
    
    Scenario: Registrar cannot learner academic records
        Given A learner is enrolled is having some academic records
            When Registrar wants to access academic records of a learner with invalid ID
                Then SLP should return error message to Registrar
