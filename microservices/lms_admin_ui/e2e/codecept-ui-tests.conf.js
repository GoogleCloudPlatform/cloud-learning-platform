const { setHeadlessWhen, setWindowSize } = require('@codeceptjs/configure');

setWindowSize(1600, 1100);
setHeadlessWhen(process.env.HEADLESS);

let testPath = './ui-tests/**/*.js';

exports.config = {
  tests: testPath,
  output: './ui_tests_output',
  helpers: {
    Puppeteer: {
      url: 'http://localhost:4401/',
      show: true,
      waitForNavigation: 'networkidle0',
      restart: false,
      keepCookies: true,
      keepBrowserState: true,
      chrome: {
        args: [
        '--disable-web-security',
        ]
      }
    },
    // FirebaseHelper: {
    //   require: './utils/firebase-helper.js'
    // }
  },
  bootstrap: null,
  mocha: {},
  name: 'lms_admin_ui',
  plugins: {
    pauseOnFail: {},
    retryFailedStep: {
      enabled: true
    },
    tryTo: {
      enabled: true
    },
    screenshotOnFail: {
      enabled: true
    }
  }
}