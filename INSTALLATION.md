# Installation

## Google Classroom / Workspace Setup

- Google workspace - allow all users to accomodate for other workspaces or Personal (gmail) accounts
  ![](docs/static/images/classroom_personal_accounts.png)

## Create an Account in Google Admin to be the designated Admin Account for CLP-LMS

- Normal workspace User account to be the "Admin Teacher" and own all Classroom class
  #TODO: validate if following can be removed?
- Place this email in the `lms-service-user` secret in Google Secret Manager

## Domain Wide Delegation

Get the unique id (numeric) for the gke-pod-sa Service Account in your project
![](docs/static/images/sa_unique_value.png)

Go to the Domain Wide Delegation page of Google Admin
![](docs/static/images/domain_wide_delegation.png)

Click **Add new**

Add this numeric value, and the following scopes:
https://www.googleapis.com/auth/classroom.announcements,https://www.googleapis.com/auth/classroom.announcements.readonly,https://www.googleapis.com/auth/classroom.courses,https://www.googleapis.com/auth/classroom.courses.readonly,https://www.googleapis.com/auth/classroom.coursework.me,https://www.googleapis.com/auth/classroom.student-submissions.me.readonly,https://www.googleapis.com/auth/classroom.coursework.students,https://www.googleapis.com/auth/classroom.student-submissions.students.readonly,https://www.googleapis.com/auth/classroom.courseworkmaterials,https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly,https://www.googleapis.com/auth/classroom.rosters,https://www.googleapis.com/auth/classroom.rosters.readonly,https://www.googleapis.com/auth/classroom.topics,https://www.googleapis.com/auth/classroom.topics.readonly,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/forms.body.readonly,https://www.googleapis.com/auth/classroom.push-notifications,https://www.googleapis.com/auth/classroom.profile.photos,https://www.googleapis.com/auth/classroom.profile.emails

It should look like this when you're done:

![](docs/static/images/client_id_access.png)

## DNS for Front-End

Add an entry for front-end in addition to backend API

## Scopes needed for Service Account

- https://www.googleapis.com/auth/classroom.announcements
- https://www.googleapis.com/auth/classroom.announcements.readonly
- https://www.googleapis.com/auth/classroom.courses
- https://www.googleapis.com/auth/classroom.courses.readonly
- https://www.googleapis.com/auth/classroom.coursework.me
- https://www.googleapis.com/auth/classroom.student-submissions.me.readonly
- https://www.googleapis.com/auth/classroom.coursework.students
- https://www.googleapis.com/auth/classroom.student-submissions.students.readonly
- https://www.googleapis.com/auth/classroom.courseworkmaterials
- https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly
- https://www.googleapis.com/auth/classroom.rosters
- https://www.googleapis.com/auth/classroom.rosters.readonly
- https://www.googleapis.com/auth/classroom.topics
- https://www.googleapis.com/auth/classroom.topics.readonly
- https://www.googleapis.com/auth/drive
- https://www.googleapis.com/auth/forms.body.readonly
- https://www.googleapis.com/auth/classroom.push-notifications
- https://www.googleapis.com/auth/classroom.profile.emails
- https://www.googleapis.com/auth/classroom.profile.photos
- https://www.googleapis.com/auth/classroom.profile.emails

## Scopes needed for Generating OAuth access to enroll student

- https://www.googleapis.com/auth/classroom.rosters,
- https://www.googleapis.com/auth/userinfo.email,
- https://www.googleapis.com/auth/userinfo.profile

## Firebase Authentication Settings

- Adding Google and email/password auth options
  ![](docs/static/images/auth_providers.png)
- Add frontend domain as an "Authorized Domain"
  ![](docs/static/images/authorized_domain.png)

## Add gke-pod-sa key

Create and download a key for the `gke-pod-sa` service account and place it in the `gke-pod-sa-key` secret.

## LTI keys setup

LTI Service requires a pair of rsa private and public keys for signing the jwt token (also referred as lti_message in LTI documentation) and a issuer url.

A pair of RSA private and public keys can be generated using the `generate_rsa_keys.py` script found in the utils folder.

For running the LTI service, a set of RSA public and private keys are picked with the terms `lti-service-public-key` and `lti-service-private-key` from Google secret manager.

## Adding Initial user in the DB

The initial user has to be entered into the database manually. Subsequent users can be added via API after that first user grabs an ID token from the UI or other method.

Create a new `users` collection in Firestore and add the first user as follows:
![](docs/static/images/first_db_user_1.png)
![](docs/static/images/first_db_user_2.png)

## Generate Bearer Token

Using this new user in the database, you can generate an ID Token through the frontend for use in other APIs.

- Using user account already in the databse log into the Admin UI
- Open **Developer Tools** in Chrome
  ![](docs/static/images/chrome_developer_tools.png)
  -Grab your ID Token (Bearer Token) Check the **Application** top tab, follow by **Local Storage** section. Grab the idToken
  ![](docs/static/images/bearer_token.png)
- Alternatively, grab the Bearer token in the **Network** tab from some of the backend API calls
  ![](docs/static/images/network_bearer_token.png)
- [Option 1]: In Open API, provide this as the Bearer Token. https://FRONTEND-DOMAIN.com/lms/api/v1/docs#
  ![](docs/static/images/open_api_authorize.png)
- You can now make API calls:
  ![](docs/static/images/open_api_calls.png)
- [Option 2]: Use POSTMan or similar, set your ID token as the Bearer token:
  ![](docs/static/images/postman_bearer_token.png)

## Setting up OAuth for Registrations API

In order to enable PubSub Notifications from Classroom, the backend SA must call the [Classroom Registrations API](https://developers.google.com/classroom/reference/rest/v1/registrations). This API has a particular restriction that **the user must have an existing OAuth grant on these scopes before domain-wide delegation can be used to call the API**.

The scopes must be allowed once via an OAuth flow and remain accepted. The `access_token` from the OAuth flow is not used.

To setup:

- Open the OAuth Credentials screen in your project, setup the app and click **Edit**
  ![](docs/static/images/oauth_consent.png)
- Add appropriate emails and click **Next** to the SCOPES page
- Add the following scopes:
  ![](docs/static/images/oauth_scopes.png)
- Finish the flow

Then click on the **Credentials** menu:

- **+ Create Credentials**
- OAuth Client ID
- application type: Web Application
- make sure to include the following redirect URL
  ![](docs/static/images/redirect_uri.png)
- Click Save and download the credentials file.

Rename this file `credentials.json` and place it alongside the following script:
`./experimental/classroom-experiments/classroom_registration.py`
Run this script and accept the permissions using your Admin Teacher account.

You can verify the permissions have been given in the Google settings page: https://myaccount.google.com/data-and-privacy in the **Data from apps and services you use**.

You can also test the `/enable_notifications` API in the `lms` microservice to verify.

## Adding Backend Robot User

A backend robot (service account) user is needed in the database to allow backend services to make authenticated API calls to each other when a User bearer token is not in the API flow. This is particularly neede for cronjobs and LTI callback flows.

1. Hit POST method for users api in user-management microservice with new user's emain id in the api body

API :

`POST https://<base url>/user-management/api/v1/user`

Authorization :

`Bearer Token = <id_token>`

Body :

```
{
"first_name": "Backend",
"last_name": "Bot",
"email": "bot@core-learning-services-dev.cloudpssolutions.com",
"user_type": "other"
}
```

Then add this account manually into firebase. You will need to generate a secure password:

![](docs/static/images/add_robot_firebase.png)

Lastly, store both the full email and the pass into Secret Manager in the following two values:

![](docs/static/images/robot_secret_manager.png)

## Steps to add new user

1. Hit POST method for users api in user-management microservice with new user's emain id in the api body

API :

`POST https://<base url>/user-management/api/v1/user`

Authorization :

`Bearer Token = <id_token>`

Body :

```
{
"first_name": "",
"last_name": "",
"email": "abc@def.com",
"user_type": "learner",
"user_groups": [],
"status": "active",
"is_registered": true,
"failed_login_attempts_count": 0,
"access_api_docs": false,
"gaia_id": ""
}
```

Response samples:

**200**

```
{
"success": true,
"message": "Successfully created the user",
"data": {
"user_id": "124hsgxR77QKS8uS7Zgm",
"first_name": "",
"last_name": "",
"email": "steve.jobs@example.com",
"user_type": "other",
"user_groups": [],
"status": "active",
"is_registered": true,
"failed_login_attempts_count": 0,
"access_api_docs": false,
"gaia_id": ""
}
}
```

**401**

```
{
"success": false,
"message": "Unauthorized",
"data": { }
}
```

**422**

```
{
"success": false,
"message": "Validation Failed",
"data": [ ]
}
```

**500**

```
{
"success": false,
"message": "Internal server error",
"data": { }
}
```
