describe("Test Honorlock Deeplinking", () => {
  it("should visit the login page with username password", () => {
    const EMAIL = Cypress.env("E2E_TEST_EMAIL");
    const PASSWORD = Cypress.env("E2E_TEST_PASSWORD");
    const domain =
      "https://gcp-classroom-dev.cloudpssolutions.com/login/e2e";
    cy.visit(domain);
    cy.url().should(
      "eq",
      "https://gcp-classroom-dev.cloudpssolutions.com/login/e2e"
    );

    // sign in with a account
    cy.get('[type="email"]').type(EMAIL);
    cy.get('[type="password"]').type(PASSWORD);
    cy.contains("Login").click();

    // check if domain is right
    cy.url().should(
      "contain",
      "https://gcp-classroom-dev.cloudpssolutions.com"
    );
    cy.log("User logged in");

    cy.intercept(
      "GET",
      "https://gcp-classroom-dev.cloudpssolutions.com/lms/api/v1/sections?skip=0&limit=10"
    ).as("getAllSections");

    // go to section
    cy.contains("Section List").click();
    cy.wait("@getAllSections");
    cy.get("a.text").first().click();
    cy.contains(" Add LTI Assignment").click();
    cy.get('mat-select[formcontrolname="tool_id"]').click();
    cy.get("mat-option").contains("Honorlock QA Tool").click();
    cy.get('mat-select[formcontrolname="course_work_type"]').click();
    cy.get("mat-option").contains("Coursework").click();
    cy.get('[formcontrolname="lti_assignment_title"]').type(
      "Honorlock QA Tool testing"
    );
    cy.wait(3000);
    cy.contains("Create Content Item").then(($button) => {
      if ($button.is(":disabled")) {
        cy.log("found existing content item");
      } else {
        cy.log("no existing content item was found");
        cy.contains("Create Content Item").click();
        cy.wait(3000);
        cy.get("button").contains("Create Content Item").should("be.disabled");
      }
    });

    cy.intercept(
      "POST",
      "https://gcp-classroom-dev.cloudpssolutions.com/classroom-shim/api/v1/lti-assignment"
    ).as("apiRequest");

    cy.get('button[type="submit"]').contains("Save").click();

    // Assert that the API call was made and wait for the response
    cy.wait("@apiRequest").then((interception) => {
      const response = interception.response;
      cy.writeFile(
        "cypress/fixtures/HONORLOCK_LTI_ASSIGNMENT_ID.txt",
        response.body.data.id
      );
      cy.log("response.body.id", response.body.data.id);
      expect(response.statusCode).to.equal(200);
    });

    cy.contains(" Add Teacher").click();
    cy.get('[formcontrolname="email"]').type(
      "test_user_1@dhodun.altostrat.com"
    );
    cy.get(".mat-dialog-actions button").contains(" Add ").click();
  });
});
