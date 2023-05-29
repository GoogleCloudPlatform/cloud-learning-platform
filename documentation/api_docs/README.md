# Cloud Learning Platform(CLP) Documentation
`This documentation is built using Docusaurus 2.0, a modern static website generator.` <br>
`The redocusaurus plugin is used to integrate redoc into the docusaurus tool.`

## Installation of dependencies
> npm install or yarn install

## Prerequisites
Below environment variables are required to be exported before running documentation on local or before running npm run start or npm run build. <br>

> export FIREBASE_API_KEY = <FIREBASE_API_KEY> <br>
> export FIREBASE_AUTH_DOMAIN = <FIREBASE_AUTH_DOMAIN> <br>
> export WHITELIST_DOMAINS = <WHITELIST_DOMAINS> <br>
> export API_DOMAIN = <API_DOMAIN> <br>
> export SHOW_ALL_SERVICES_IN_DOCS = <SHOW_ALL_SERVICES_IN_DOCS> <br>

- `FIREBASE_API_KEY` and `FIREBASE_AUTH_DOMAIN` are required for firebase authentication.
- `WHITELIST_DOMAINS` is required to whitelist users who have a specific domain in their email address in order to view documentation. While logging-in using SSO, if the domain in users email address present in `WHITELIST_DOMAINS`, backend validation of user email to check if permission to view API documentation is granted. eg. example01.com,example02.com
- `API_DOMAIN` is the domain url where other backend microservices are hosted. These microservices will be used to fetch the openapi.json for generating redoc API documentation.
- `SHOW_ALL_SERVICES_IN_DOCS` should either be 'true' or 'false'. This will decide if all the services needs to be displayed in api reference docs section of documentation.

## Local Development
Once the required variables are exported we can run the documentation on local machine using: <br>

> npm run start or yarn run start 

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build
> npm run build or yarn run build

This command generates static content into the build directory and can be served using any static contents hosting service.

## Authentication

- We are using firebase authentication for logging in the user to product documentation.
- The domain needs to be added in allowed domains in firebase authentication for hosting this product documentation.
- Authentication service which is hosted in `API_DOMAIN` domain will be used to validate whether the user has permissions to access/login into the documentation. The underlying check will be done based on user email which is passed from frontend and validating `access_api_docs` key in firestore users collection from backend.