# Installation

- Google workspace - allow all users
  ![](docs/static/images/classroom_personal_accounts.png)

## Enable Classroom API

The Classroom API Needs to be enabled in the project where the backend Service Account lives

https://console.cloud.google.com/apis/api/classroom.googleapis.com

## DNS for Front-End

Add an entry for front-end in addition to backend API

## Scopes needed for Service Account

- https://www.googleapis.com/auth/classroom.announcements
- https://www.googleapis.com/auth/classroom.announcements.readonly
- https://www.googleapis.com/auth/classroom.courses
- https://www.googleapis.com/auth/classroom.courses.readonly
- https://www.googleapis.com/auth/classroom.coursework.me
- https://www.googleapis.com/auth/classroom.coursework.me.readonly
- https://www.googleapis.com/auth/classroom.coursework.students
- https://www.googleapis.com/auth/classroom.coursework.students.readonly
- https://www.googleapis.com/auth/classroom.courseworkmaterials
- https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly
- https://www.googleapis.com/auth/classroom.rosters
- https://www.googleapis.com/auth/classroom.rosters.readonly
- https://www.googleapis.com/auth/classroom.topics
- https://www.googleapis.com/auth/classroom.topics.readonly
- https://www.googleapis.com/auth/drive
- https://www.googleapis.com/auth/forms.body.readonly

## LTI keys setup

LTI Service requires a pair of rsa private and public keys for signing the jwt token (also referred as lti_message in LTI documentation) and a issuer url.

A pair of RSA private and public keys can be generated using the `generate_rsa_keys.py` script found in the utils folder.

For running the LTI service, a set of RSA public and private keys are picked with the terms `lti-service-public-key` and `lti-service-private-key` from Google secret manager.
