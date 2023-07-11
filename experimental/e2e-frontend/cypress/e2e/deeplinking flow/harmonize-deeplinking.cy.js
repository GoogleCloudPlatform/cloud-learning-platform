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
    const domain =
      "https://core-learning-services-dev.cloudpssolutions.com/login/e2e";
    cy.visit(domain);
    window.localStorage.setItem("userId", "hVo8p8wupciYtjfWK8GP");
    cy.url().should(
      "eq",
      "https://core-learning-services-dev.cloudpssolutions.com/login/e2e"
    );

    // signin with a account
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
    cy.get("mat-option").contains("Harmonize Google Dev").click();
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

    // type text in discussion title inputbox
    cy.wait(5000);
    getIframeBody().find(".highlight-box").as("parentElement");
    cy.get("@parentElement")
      .find('input[type="text"]')
      .type("Hello, World! Testing Discussions");
    cy.get("@parentElement").find('input[type="number"]').type(50);
    cy.get("@parentElement").contains("Create Discussion").click();

    // type text in discussion title inputbox
    cy.wait(10000);
    cy.get("#ltiIframe").should("not.exist");

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
