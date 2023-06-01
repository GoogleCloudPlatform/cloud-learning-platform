---
sidebar_label: Sign In with Google Account
sidebar_position: 3
---

# Token generation to access APIs

Use the below steps to Sign in using Google Account.

### Sign in using Google Acount

Given the user have a google account and have access to the GCP Project and the user email is already added to the Database. To sign in to the application, the user should make a **POST** request to the sign in API endpoint - **`<APP_URL>/authentication/api/v1/sign-in/token`**. Google Auth token is added as Bearer Token in the request headers.

The request headers for the API should be as follows:

```json
{
  "Authorization": "Bearer <Google-Oauth-token>"
}
```

On Successfull SignIn the Authentication service returns following json response.

```json
{
  "success": true,
  "message": "Successfully signed in",
  "data": {
    "user_id": "asd98798as7dhjgkjsdfh",
    "kind": "identitytoolkit#VerifyPasswordResponse",
    "localId": "XmtYBlBM9dZKDIQ1cP0lh2kBY163",
    "email": "jon.doe@gmail.com",
    "displayName": "",
    "idToken": "eyJhbGciOiJSUzI1NiIJ...X2ybGwFvMhw",
    "registered": true,
    "refreshToken": "AOEOulblOMdQ4OU...lbRSuDcUAZPUbYL1_u",
    "expiresIn": "3600",
    "session_id": "asd98798as7dhjgkjsdfh"
  }
}
```
The **`idToken`** generated in the above response can be used to access the other API endpoints.

And incase if the user email doesn't exists in the Database, the the Authentication service will return following error response:

```json
{
  "success": false,
  "message": "User is not authorized",
  "data": []
}
```

