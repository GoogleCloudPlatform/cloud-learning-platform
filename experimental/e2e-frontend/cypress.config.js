const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
      return {
        browsers: config.browsers.filter(
          (b) => b.family === "chromium" && b.name !== "electron"
        ),
      };
    },
    experimentalRunAllSpecs: true,
    chromeWebSecurity: false,
    viewportHeight: 1080,
    viewportWidth: 1920,
    experimentalOriginDependencies: true,
  },
});
