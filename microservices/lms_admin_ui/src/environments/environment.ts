// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  apiurl: "https://clp-sandbox.gostudyhall.com/lms/api/v1/",
  ltiUrl: "https://clp-sandbox.gostudyhall.com/lti/api/v1/",
  classroomShimUrl: "https://clp-sandbox.gostudyhall.com/classroom-shim/api/v1/",
  auth_apiUrl: "https://clp-sandbox.gostudyhall.com/authentication/api/v1/",
  firebase: {
      apiKey: "AIzaSyAbrin_xZLhKzRt9hvNVIw8c92LGStKLao",
      authDomain: "gcp-classroom-dev.firebaseapp.com",
      projectId: "gcp-classroom-dev",
      storageBucket: "gcp-classroom-dev.appspot.com",
      appId: "1:636807882786:web:0f8979da60a1b806a4c27b"
  }
}

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.