// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false,
  apiurl: 'http://localhost:4200/lms/api/v1/',
  ltiUrl: 'http://localhost:4200/lti/api/v1/',
  classroomShimUrl: 'http://localhost:4200/classroom-shim/api/v1/',
  auth_apiUrl: 'http://localhost:4200/authentication/api/v1/',
  firebase: {
    apiKey: "AIzaSyC7ZF4D98P6woFEYCeIpdFSY4S73btYA7Y",
    authDomain: "core-learning-services-dev.firebaseapp.com",
    projectId: "core-learning-services-dev",
    storageBucket: "core-learning-services-dev.appspot.com",
    appId: "1:142865211726:web:4a5a50aa0173200602be1f",
  }
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.