import 'cypress-iframe'

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
        const value1 = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjhkMDNhZTdmNDczZjJjNmIyNTI3NmMwNjM2MGViOTk4ODdlMjNhYTkiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiUmFtIENoYXVkaGFyaSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BRWRGVHA0d0l4Um53NTBoVzdfYmppcVlPTWdkaHB0MEd6OWR3MUQ2THBPQT1zOTYtYyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS9jb3JlLWxlYXJuaW5nLXNlcnZpY2VzLWRldiIsImF1ZCI6ImNvcmUtbGVhcm5pbmctc2VydmljZXMtZGV2IiwiYXV0aF90aW1lIjoxNjg3NDM4MTY4LCJ1c2VyX2lkIjoiTkh2cEJBZTVFTFJ4aVZJWDdDR0VsUHRwck5qMiIsInN1YiI6Ik5IdnBCQWU1RUxSeGlWSVg3Q0dFbFB0cHJOajIiLCJpYXQiOjE2ODc0MzgxNjgsImV4cCI6MTY4NzQ0MTc2OCwiZW1haWwiOiJyYW0uY2hhdWRoYXJpQHF1YW50aXBoaS5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTExMzc3MTk1MzUxNTAyMTQyMiJdLCJlbWFpbCI6WyJyYW0uY2hhdWRoYXJpQHF1YW50aXBoaS5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.yxrk97IlupKXGOcW3rToAiuG1y67DGh5iy97G5Mrek1z5S6b1PVW-1szCgbE4aO3cljALt3dKhVnlbCaWPFIpp4S4IPWY_ZizWBkittHwOsy78eEO7MSBg-ZpZXosjxvn4Pi8fcLccKJZkayJUkMvT0ziR9psLRKMxk86D3sC-yPw0A9lsxiFCPaY5ivKN2kjMuiJEB9EVQAKkzwzZJfJ_4BDKw_tiBsTdN4CIQYGSOv_xhvPOzvF4DmcJeg7--DQxgXax1xOyB1Cy-qKUsHWwu8nsAOvOhDn_EtJg1n9sNBFY9I_uVZWWIlOJWhLFpf5GOLtNN3om6Reah1R_-CyA';
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
        cy.frameLoaded("#ltiIframe")
        cy.iframe().contains('Which component would you like to add?').should('be.visible')
        cy.iframe().contains('Discussion').click()
        cy.iframe().contains('Create New').click()
        // getIframeBody().contains('Which component would you like to add?').should('be.visible')
        // getIframeBody().contains('Discussion').click()
        // getIframeBody().contains('Create New').click()
        cy.frameLoaded("#ltiIframe")
        // cy.iframe().contains('What is the title of the discussion?').should('be.visible')
        console.log("cy.iframe()", cy.iframe())
        cy.iframe().get('input[type="number"]').type(50)
        cy.iframe().get('input[type="text"]').type('Hello, World! Testing Discussions')
        cy.iframe().contains('Create Discussion').click()
    });
});

