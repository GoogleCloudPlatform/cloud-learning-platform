const firebase = require('firebase');
const { v4: uuidv4 } = require('uuid');
const generator = require('generate-password');
const Helper = require('@codeceptjs/helper');

class FirebaseHelper extends Helper {
  constructor() {
    super();
    this.testUserEmail = null;
    this.testUserPassword = null;
    this.userIdToken = null;
    this.session_details = {};
  }

  _before() {
    this.initFirebasaeApp();
  }

  initFirebasaeApp() {
    if (firebase.apps.length === 0) {
      firebase.initializeApp({
        apiKey: process.env.FIREBASE_API_KEY,
        authDomain: process.env.FIREBASE_AUTH_DOMAIN,
        projectId: process.env.FIREBASE_PROJECT_ID,
      });
    }
  }

  getUniqID() {
    return uuidv4();
  }

  setSessionDetails(key, value) {
    this.session_details[key] = value;
  }

  getSessionDetails(key) {
    return this.session_details[key] || null;
  }

  async registerNewTestUser(uniqID) {
    this.initFirebasaeApp();
    this.testUserEmail = 'e2e-test-' + uniqID + '@gmail.com';
    this.testUserPassword = generator.generate({
      length: 10,
      numbers: true
    });

    // Authenticate user using email and password.
    await firebase.auth().createUserWithEmailAndPassword(
      this.testUserEmail, this.testUserPassword);

    await firebase.auth().currentUser.updateProfile({
      displayName: uniqID
    });

  }

  async deleteTestUser() {
    await firebase.auth().signInWithEmailAndPassword(
      this.testUserEmail, this.testUserPassword);
    let user = firebase.auth().currentUser;
    await user.delete().then(() => {
    }).catch(function(error) {
      console.error(error);
    });
  }

  getTestUserEmail() {
    return this.testUserEmail;
  }

  getTestUserPassword() {
    return this.testUserPassword;
  }

  async loginFirebaseAsTestUser() {
    await this.loginFirebase(this.testUserEmail, this.testUserPassword);
  }

  async loginFirebase(email, password) {
    this.initFirebasaeApp();

    // Authenticate user using email and password.
    await firebase.auth().signInWithEmailAndPassword(
      email || this.testUserEmail, password || this.testUserPassword);
  }

  async getUserIdToken() {
    await this.loginFirebase();
    this.userIdToken = await firebase.auth().currentUser.getIdToken();

    return this.userIdToken;
  }

  async logout() {
    let auth = await firebase.auth();
    if (auth) {
      await auth.logout();
    }
  }
}

module.exports = FirebaseHelper;