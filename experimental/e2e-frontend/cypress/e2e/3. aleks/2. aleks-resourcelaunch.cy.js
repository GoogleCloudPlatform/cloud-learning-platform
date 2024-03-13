describe("Test ALEKS Resource Launch", () => {
  it("should be able to launch the resource which was created in earlier step", () => {
    let idToken = null;
    let facultyEmail = "test_user_1@dhodun.altostrat.com";
    let facultyPassword = "gudvuk-sEnjo0-vosduv";
    cy.request(
      "POST",
      "https://gcp-classroom-dev.cloudpssolutions.com/authentication/api/v1/sign-in/credentials",
      {
        email: facultyEmail,
        password: facultyPassword,
      }
    ).then((res) => {
      idToken = res.body.data.idToken;
      cy.readFile("cypress/fixtures/ALEKS_LTI_ASSIGNMENT_ID.txt").then(
        (assignmentId) => {
          cy.visit({
            method: "GET",
            url: `https://gcp-classroom-dev.cloudpssolutions.com/classroom-shim/api/v1/e2e-resource-launch?lti_assignment_id=${assignmentId}`,
            headers: {
              Authorization: `Bearer ${idToken}`,
            },
          });
        }
      );
    });
    cy.wait(30000);
  });
});
