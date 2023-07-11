import "cypress-iframe";

describe("Test Harmonize Deeplinking", () => {
  it("should visit the login page with username password", () => {
    const domain =
      "https://core-learning-services-dev.cloudpssolutions.com/login/e2e";
    cy.visit(domain);
    window.localStorage.setItem("userId", "hVo8p8wupciYtjfWK8GP");
    cy.url().should(
      "eq",
      "https://core-learning-services-dev.cloudpssolutions.com/login/e2e"
    );

    // sign-in with a account
    cy.get('[type="email"]').type("e2e_7112f773_1a53_email@gmail.com");
    cy.get('[type="password"]').type("!45RK&2L!m9%Ef");
    cy.contains("Login").click();

    // check if domain is right
    cy.url().should(
      "contain",
      "https://core-learning-services-dev.cloudpssolutions.com"
    );

    // go to section
    cy.contains("Section List").click();
    cy.get("a.text").first().click();
    cy.contains(" Add LTI Assignment").click();
    cy.get('mat-select[formcontrolname="tool_id"]').click();
    cy.get("mat-option").contains("Honorlock QA Tool").click();
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
      "https://core-learning-services-dev.cloudpssolutions.com/classroom-shim/api/v1/lti-assignment"
    ).as("apiRequest");

    cy.get('button[type="submit"]').contains("Save").click();

    // Assert that the API call was made and wait for the response
    cy.wait("@apiRequest").then((interception) => {
      const response = interception.response;
      expect(response.statusCode).to.equal(200);
    });
  });
});
