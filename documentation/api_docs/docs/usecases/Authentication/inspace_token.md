---
sidebar_label: Token API for Inspace
sidebar_position: 4
---

# Token API for inpsace user

The following steps are to get the inpsace token.

### Get Token inpsace user

To fetch the inspace token, we would make a **GET** request to the API endpoint - **`<APP_URL>/authentication/api/v1/inspace/token/{user_id}`** where **`user_id`** is the unique ID of the user

Then the response would be as follows: 

```json
{
  "success": true,
  "message": "Successfully fetched the inspace token",
  "data": {
    "token": "eyJhbGciOiJSUzI1NiIJ...X2ybGwFvMhw"
  }
}
``` 
