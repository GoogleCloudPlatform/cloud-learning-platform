const { config } = require('../../codecept-ui-tests.conf');
let url = config.helpers.Puppeteer.url;
credentials = JSON.parse(process.env.account)

Feature('User Login');

Scenario('User opens login page and sees login button', async ({ I }) => {
  I.amOnPage(url+'login/e2e');
  I.see('Login');
  I.see('Management portal');
});

Scenario('User sees Dashboard after logged in.', async ({ I }) => {
  I.fillField('Email', credentials['email']);
  I.fillField('Password', credentials['password']);
  I.click('Login');
  I.wait(5)
  I.see('Course Template List');
  I.see('Cohort List');
  I.see('Section List');
  I.wait(10);
});

// Scenario('open my website', ({ I }) => {
//   I.amOnPage('http://localhost:4401/login/e2e');
//   pause();
// });