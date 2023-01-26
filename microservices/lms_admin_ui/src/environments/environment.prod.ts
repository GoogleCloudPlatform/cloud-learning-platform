export const environment = {
  production: true,
  apiurl: 'https://' + $ENV.API_DOMAIN + '/lms/api/v1/',
  auth_apiUrl: 'https://' + $ENV.API_DOMAIN + '/authentication/api/v1/',
  firebase: {
    apiKey: $ENV.FIREBASE_API_KEY,
    authDomain: $ENV.PROJECT_ID + '.firebaseapp.com',
    projectId: $ENV.PROJECT_ID,
    storageBucket: $ENV.PROJECT_ID + '.appspot.com',
    appId: $ENV.FIREBASE_APP_ID,
  }
};