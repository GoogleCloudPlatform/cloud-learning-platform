export const environment = {
  production: true,
  apiurl: 'https://' + $ENV.API_DOMAIN + '/lms/api/v1/',
  auth_apiUrl: 'https://' + $ENV.API_DOMAIN + '/authentication/api/v1/',
  firebase: {
    apiKey: $ENV.FIREBASE_API_KEY,
    authDomain: $ENV.FIREBASE_AUTH_DOMAIN,
    projectId: $ENV.FIREBASE_PROJECT_ID,
    storageBucket: $ENV.FIREBASE_STORAGE_BUCKET,
    appId: $ENV.FIREBASE_APP_ID,
  }
};