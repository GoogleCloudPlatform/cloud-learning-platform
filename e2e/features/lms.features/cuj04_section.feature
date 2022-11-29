Feature: Add student to section
    @fixture.create.section
    Scenario: Add student to a section using a payload
        Given A user has access privileges and wants to enroll a student into a section 
            When API request is sent to enroll student to a section with correct request payload and valid section uuid
                Then Section will be fetch using the given uuid and student is enrolled using student credentials and a response model object will be return
    
    Scenario:Unable to Add student to a section using a payload
        Given A user has access to portal and needs to enroll a student into a section 
            When API request is sent to enroll student to a section with correct request payload and invalid section uuid
                Then Student will not be enrolled and API will throw a resource not found error
    @fixture.create.section
    Scenario:Unable to enroll student to a section using request data
        Given A user has access to the portal and wants to enroll a student into a section
            When API request is sent to enroll student to a section with incorrect request payload and valid section uuid
                Then Student will not be enrolled and API will throw a validation error
