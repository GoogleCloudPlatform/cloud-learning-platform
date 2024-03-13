import "cypress-iframe";
describe("Test Harmonize Deeplinking", () => {
  const getIframeDocument = () => {
    console.log(cy.get("#ltiIframe"));
    return cy.get("#ltiIframe").its("0.contentDocument").should("exist");
  };

  const getIframeBody = () => {
    console.log("body", getIframeDocument().its("body"));
    return getIframeDocument()
      .its("body")
      .should("not.be.undefined")
      .then(cy.wrap);
  };

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
    cy.get("mat-option").contains("Harmonize Google Dev").click();
    cy.get('mat-select[formcontrolname="course_work_type"]').click();
    cy.get("mat-option").contains("Coursework").click();
    cy.get('[formcontrolname="lti_assignment_title"]').type(
      "Harmonize Google Dev testing"
    );
    cy.contains("Select Content").click();
    cy.wait(20000);

    // check if we are on home page of harmonize
    getIframeBody()
      .contains("Which component would you like to add?")
      .should("be.visible");
    getIframeBody().contains("Discussion").click();
    getIframeBody().contains("Create New").click();

    // type text in discussion title input box
    cy.wait(5000);
    getIframeBody().find(".highlight-box").as("parentElement");
    cy.get("@parentElement")
      .find('input[type="text"]')
      .type("Hello, World! Testing Discussions");
    cy.get("@parentElement").find('input[type="number"]').type(50);
    cy.get("@parentElement").contains("Create Discussion").click();

    // type text in discussion title input box
    cy.wait(10000);
    cy.get("#ltiIframe").should("not.exist");

    cy.intercept(
      "POST",
      "https://gcp-classroom-dev.cloudpssolutions.com/classroom-shim/api/v1/lti-assignment"
    ).as("apiRequest");

    cy.get('button[type="submit"]').contains("Save").click();
    cy.wait("@apiRequest").then((interception) => {
      const response = interception.response;
      cy.writeFile(
        "cypress/fixtures/HARMONIZE_LTI_ASSIGNMENT_ID.txt",
        response.body.data.id
      );
      cy.log("response.body.id", response.body.data.id);
      expect(response.statusCode).to.equal(200);
    });
    // let sectionId =
    //   window.location.href.split("/")[
    //     window.location.href.split("/").length - 1
    //   ];
    // let url = `https://gcp-classroom-dev.cloudpssolutions.com/lms/api/v1/sections/${sectionId}/teachers`;
    // cy.log("url", url);
    // cy.intercept("POST", url).as("addTeacherApiRequest");

    cy.contains(" Add Teacher").click();
    cy.get('[formcontrolname="email"]').type(
      "test_user_1@dhodun.altostrat.com"
    );
    cy.get(".mat-dialog-actions button").contains(" Add ").click();
    // cy.wait("@addTeacherApiRequest").then((interception) => {
    //   if (interception.response.statusCode == 200) {
    //     cy.log("Teacher added successfully");
    //   } else if (interception.response.statusCode == 409) {
    //     cy.log("Teacher already existed");
    //     cy.get("button").contains("No").click();
    //   }
    // });
  });
});
