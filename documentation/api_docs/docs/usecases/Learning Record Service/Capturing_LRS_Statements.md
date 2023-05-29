---
sidebar_label: Capturing valid xAPI Statements
sidebar_position: 5
---

# Capturing valid xAPI Statements

The following steps are required to send valid xAPI Statements to LRS

LRS expects the following parameters to be valid:

Session ID
Agent Information
User Information
Verb Name
Object Information

### Getting session information

When users get authenticated during SignIn step, a **POST** request has to be made to the authentication API endpoint - **`<APP_URL>/authentication/api/v1/sign-in/credentials`** .
The response body contains 'session_id' which should be passed in LRS statement.

### Getting User information

During User SignUp step, a **POST** request will be made to the user management API endpoint
- **`<APP_URL>/user-management/api/v1/user`** . 
This API creates a new user. Along with this corresponding learner, learner profile (only if user_type is 'learner') and associated agent profile get created. The response body contains 'user_id' which should be passed inside actor information in LRS statement

### Getting Agent (Actor) information
For a given user, a **GET** request will be made to the LRS agent API endpoint to get the agent information
- **`<APP_URL>/learner-record-service/api/v1/agents?user_id=={user_id}`** .

The response body contains agent information which should be passed in actor information in LRS statement

### Getting Verbs
For every incoming statement, LRS validates verb information and expects the verb information to be present in the database

To ensure, correct verb information, first get all the verbs from the database using the **GET** request to the LRS verb endpoint - **`<APP_URL>/learner-record-service/api/v1/verbs`** .

The verb information that is passed in LRS statement must be present in these list of verbs.

#### This part is meant for development purposes only. The exhaustive, standardised list of verbs will be made available to the developers at some point in the future
If the required verb information is not present in the database, the same can be created with a **POST** request to the LRS verb endpoint - **`<APP_URL>/learner-record-service/api/v1/verb`** .

### Getting Object Information
The object type in LRS statement will always be of type 'activity'
Here activity can be either of these
 1. A node from the Learning Hierarchy (E.g. User started 'Learning Resource 1')
 2. Component in UX with which an user can interact (E.g User visited 'Pathways Page')
 3. User Action ('Learner successfully Logged In')

If the object to be captured in LRS statement is a node from Learning Hierarchy, then that node information should be captured in object's canonical_data field

For other types of activities, currently there is no backend validation.

#### This part is meant for development purposes only. The exhaustive, standardised list of activites will be made available to the developers at some point in the future
Instead of filling activity related information with random data, it is advised to create a set of activities using the **POST** request to LRS Activity API EndPoint **`<APP_URL>/learner-record-service/api/v1/activity`** . and confine to those activities for development purposes. To get the list of activities available a **GET** request has to be made to LRS Activity API EndPoint **`<APP_URL>/learner-record-service/api/v1/activities`** .