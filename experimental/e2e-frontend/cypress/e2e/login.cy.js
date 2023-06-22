describe('LocalStorage Test', () => {
    const getIframeDocument = () => {
        console.log(cy.get('#ltiIframe'))
        return cy
            .get('#ltiIframe')
            .its('0.contentDocument').should('exist')
    }

    const getIframeBody = () => {
        return getIframeDocument()
            .its('body').should('not.be.undefined')
            .then(cy.wrap)
    }
    const iframeElement = () => {
        const iframe = cy.get("#ltiIframe");
        return iframe
            .should(($iframe) => // Make sure its not blank
                expect($iframe.attr('src')).not.to.include('about:blank')
            )
            .should(($iframe) =>
                expect($iframe.attr('src')).not.to.be.empty) // Make sure its not empty
            .then(($inner) => {
                const iWindow = $inner[0].contentWindow;
                return iWindow.document
            })
            .then((iDoc) => {
                return cy.wrap(iDoc.body); // Wrap the element to access Cypress API
            });
    };

    it('should set an item in localStorage for a specific domain', () => {
        const domain = 'https://core-learning-services-dev.cloudpssolutions.com';
        const key1 = 'idToken';
        const value1 = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjhkMDNhZTdmNDczZjJjNmIyNTI3NmMwNjM2MGViOTk4ODdlMjNhYTkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUmFtIENoYXVkaGFyaSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BRWRGVHA0d0l4Um53NTBoVzdfYmppcVlPTWdkaHB0MEd6OWR3MUQ2THBPQT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9jb3JlLWxlYXJuaW5nLXNlcnZpY2VzLWRldiIsImF1ZCI6ImNvcmUtbGVhcm5pbmctc2VydmljZXMtZGV2IiwiYXV0aF90aW1lIjoxNjg3NDM0NDk3LCJ1c2VyX2lkIjoiTkh2cEJBZTVFTFJ4aVZJWDdDR0VsUHRwck5qMiIsInN1YiI6Ik5IdnBCQWU1RUxSeGlWSVg3Q0dFbFB0cHJOajIiLCJpYXQiOjE2ODc0MzQ0OTcsImV4cCI6MTY4NzQzODA5NywiZW1haWwiOiJyYW0uY2hhdWRoYXJpQHF1YW50aXBoaS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTExMzc3MTk1MzUxNTAyMTQyMiJdLCJlbWFpbCI6WyJyYW0uY2hhdWRoYXJpQHF1YW50aXBoaS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.F18Orw9RsvtiP1lZaYVc9zwSkUwZVhQ0q8zUd_TjVZtUXzoYApaUwLaBWFXpJocrBLXNQv9ociWDcKkvU9xw-E0UQW73_Ek6W4gHXSOWYrOpymHqcJjzqAbkSEWaYL2LXCfKZSenUhnyx3R4QFAfzETEiqohLbld93R30_IafFqPIF2s8Xw7LJCsWTcZXh449Td4bIIBWnUEbnFQ1Zm0YXevPKPv-MXaTFToSMopy008v5J_f6UpRrIuJufebd2VS-vH7pxjY7J8WDgkkCxyZJW-Yz9rM7OcII1Ro0niomPUBBJU8goba6U1NLOV_jGvbjTzXUY4lJo3Hv4GgLGLxA';
        const key2 = "user"
        const value2 = "Ram Chaudhari"
        const key3 = "userId"
        const value3 = "vcmt4ZemmyFm59rDzl1U"

        cy.visit(domain);
        window.localStorage.setItem(key1, value1);
        window.localStorage.setItem(key2, value2);
        window.localStorage.setItem(key3, value3);
        cy.reload();

        cy.contains('Section List').click()
        cy.contains('Test_Section_2').click()
        cy.contains(' Add LTI Assignment').click()
        cy.get('mat-select[formcontrolname="tool_id"]').click()
        cy.get('mat-option').contains('Harmonize Google Dev').click()
        cy.get('[formcontrolname="lti_assignment_title"]').type("Harmonize Google Dev testing")
        cy.contains('Select Content').click()
        cy.wait(20000)
        getIframeBody().contains('Which component would you like to add?').should('be.visible')
        getIframeBody().contains('Discussion').click()
        getIframeBody().contains('Create New').click()
        console.log(getIframeBody())
        getIframeDocument()
            .its('body').should('not.be.undefined').contains('What is the title of the discussion?').should('be.visible')

        getIframeBody().get('input[type="number"]').type(50)
        getIframeBody().get('input[type="text"]').type('Hello, World! Testing Discussions')
        getIframeBody().contains('Create Discussion').click()
    });
});

