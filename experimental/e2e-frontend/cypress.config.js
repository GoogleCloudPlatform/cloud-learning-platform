const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    experimentalRunAllSpecs: true,
    chromeWebSecurity: false,
    viewportHeight: 1080,
    viewportWidth: 1920
  },
});
