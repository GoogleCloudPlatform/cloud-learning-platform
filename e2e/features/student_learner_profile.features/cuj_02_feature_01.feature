Feature: Student Experience Staff can access a specific learner's personal information and academic records

    Scenario: Student Experience Staff can access learner personal information and academic records
        Given A learner is enrolled in a Learning Experience and has some academic records
            When Student Experience Staff wants to access learner's personal information and academic records
            Then SLP should return the personal data and academic records of the particular learner
    
    Scenario: Student Experience Staff cannot access learner personal information and academic records
        Given A learner is enrolled in Learning Experience and has some academic records
            When Student Experience Staff wants to access learner's personal information and academic records with invalid student id
            Then SLP should return the error message to Student Experience Staff
