describe("Test Harmonize Resource Launch", () => {
  it("should be able to launch the resource which was created in earlier step", () => {
    let idToken = null;
    let facultyEmail = "test_user_1@dhodun.altostrat.com";
    let facultyPassword = "gudvuk-sEnjo0-vosduv";
    cy.request(
      "POST",
      "https://core-learning-services-dev.cloudpssolutions.com/authentication/api/v1/sign-in/credentials",
      {
        email: facultyEmail,
        password: facultyPassword,
      }
    ).then((res) => {
      idToken = res.body.data.idToken;
      cy.request({
        method: "GET",
        url: `https://core-learning-services-dev.cloudpssolutions.com/classroom-shim/api/v1/launch-assignment?lti_assignment_id=${Cypress.env.LTI_ASSIGNMENT_ID}`,
        headers: {
          Authorization: `Bearer ${idToken}`,
        },
      }).then((resp) => {
        cy.request({
          method: "POST",
          url: resp.body.url,
          json: resp.body.message_hint,
          headers: {
            Authorization: `Bearer ${idToken}`,
          },
        }).then((response) => {
          cy.log("response.body.url", response.body.url);
          cy.config("experimentalOriginDependencies", true);
          cy.origin(
            response.body.url,
            {
              args: {
                response: response,
              },
            },
            () => {
              cy.visit(response.body.url);
            }
          );
        });
      });
    });
  });
});
