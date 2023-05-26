"""
Sample objects for the schema
"""
# pylint: disable=line-too-long

### Validate token response example
BASIC_VALIDATE_TOKEN_RESPONSE_EXAMPLE = {
    "name": "Test User",
    "picture": "https://lh3.googleusercontent.com/photo.jpg",
    "iss": "https://securetoken.google.com/core-learning-services-dev",
    "aud": "core-learning-services-dev",
    "auth_time": 1663140772,
    "user_id": "Yfgfst2hgynghjfgh",
    "sub": "Yfgfst2hgynghjfgh",
    "iat": 1663140772,
    "exp": 1663144372,
    "email": "api-testing@test.com",
    "email_verified": False,
    "firebase": {
        "identities": {
            "email": ["api-testing@test.com"]
        },
        "sign_in_provider": "password"
    },
    "uid": "Yfgfst2hgynghjfgh",
    "access_api_docs": False,
    "user_type": "others"
}

### Generate response example
BASIC_GENERATE_TOKEN_RESPONSE_EXAMPLE = {
    "access_token": "eyJhbGciOi.........p21BIQiipxCaStyNvpjq8Q",
    "expires_in": 3600,
    "token_type": "Bearer",
    "refresh_token": "AOEOulZY2lQk.........u8qbYkiX1BgqwI50qcPiEOYoaA",
    "id_token": "eyJhbGciOiJSUzIoOW9q.............StyNvpjq8Q",
    "project_id": "6762662575765",
    "user_id": "fiurc7.....Lt1Gr2"
}

SIGN_UP_WITH_CREDENTIALS_API_INPUT_EXAMPLE = {
    "email": "jon.doe@gmail.com",
    "password": "Test@1234"
}

SIGN_UP_WITH_CREDENTIALS_API_RESPONSE_EXAMPLE = {
    "user_id": "asd98798as7dhjgkjsdfh",
    "kind": "identitytoolkit#SignupNewUserResponse",
    "idToken": "eyJhbGciOiJSUzI1NiIJ...X2ybGwFvMhw",
    "email": "jon.doe@gmail.com",
    "refreshToken": "AOEOulblOMdQ4OU...lbRSuDcUAZPUbYL1_u",
    "expiresIn": "3600",
    "localId": "bIj8K69RzActKzcCN6yE1V13Pqr1",
    "session_id": "asd98798as7dhjgkjsdfh"
}

SIGN_UP_WITH_CREDENTIALS_RESPONSE_NEGATIVE_EXAMPLE = {
    "error": {
        "code":
        400,
        "message":
        "EMAIL_EXISTS",
        "errors": [{
            "message": "EMAIL_EXISTS",
            "domain": "global",
            "reason": "invalid"
        }]
    }
}

SIGN_IN_WITH_CREDENTIALS_API_INPUT_EXAMPLE = {
    "email": "jon.doe@gmail.com",
    "password": "Test@1234"
}

SIGN_IN_WITH_CREDENTIALS_API_RESPONSE_EXAMPLE = {
    "user_id": "asd98798as7dhjgkjsdfh",
    "kind": "identitytoolkit#VerifyPasswordResponse",
    "localId": "XmtYBlBM9dZKDIQ1cP0lh2kBY163",
    "email": "jon.doe@gmail.com",
    "displayName": "",
    "idToken": "eyJhbGciOiJSUzI1NiIJ...X2ybGwFvMhw",
    "registered": True,
    "refreshToken": "AOEOulblOMdQ4OU...lbRSuDcUAZPUbYL1_u",
    "expiresIn": "3600",
    "session_id": "asd98798as7dhjgkjsdfh"
}

SIGN_IN_WITH_TOKEN_RESPONSE_EXAMPLE = {
    "user_id": "asd98798as7dhjgkjsdfh",
    "federatedId": "https://accounts.google.com/103166258427660192046",
    "providerId": "google.com",
    "email": "jon.doe@gmail.com",
    "emailVerified": True,
    "firstName": "Jon",
    "fullName": "Jon Doe",
    "lastName": "Doe",
    "photoUrl": "https://lh3.googleusercontent.com/a/Abc",
    "localId": "a7xVTFpFPNM6bugWCZso7ptmPcz1",
    "displayName": "Jon Doe",
    "idToken": "eyJhbGciOiJSUzI1NiIJ...X2ybGwFvMhw",
    "refreshToken": "AOEOulblOMdQ4OU...lbRSuDcUAZPUbYL1_u",
    "expiresIn": "3600",
    "oauthIdToken": "eyJhbGciOiJSUzI1NiIJ...X2ybGwFvMhw",
    "rawUserInfo": "{'iss':...662452577}",
    "kind": "identitytoolkit#VerifyAssertionResponse",
    "session_id": "asd98798as7dhjgkjsdfh"
}

SIGN_IN_WITH_TOKEN_RESPONSE_NEGATIVE_EXAMPLE = {
    "error": {
        "code":
        400,
        "message":
        "INVALID_IDP_RESPONSE : Unable to parse Google id_token: eyJhbGcXVhbnRpcGhpX3NuaHU6ODc2MnRhZQ==",
        "errors": [{
            "message":
            "INVALID_IDP_RESPONSE : Unable to parse Google id_token: eyJhbGcXVhbnRpcGhpX3NuaHU6ODc2MnRhZQ==",
            "domain": "global",
            "reason": "invalid"
        }]
    }
}

SIGN_IN_WITH_CREDENTIALS_RESPONSE_NEGATIVE_EXAMPLE = {
    "error": {
        "code":
        400,
        "message":
        "INVALID_EMAIL",
        "errors": [{
            "message": "INVALID_EMAIL",
            "domain": "global",
            "reason": "invalid"
        }]
    }
}

IDP_SEND_PASSWORD_RESET_EMAIL_RESPONSE_EXAMPLE = {
    "kind": "identitytoolkit#GetOobConfirmationCodeResponse",
    "email": "jon.doe@gmail.com"
}

IDP_RESET_PASSWORD_EXAMPLE = {
    "kind": "identitytoolkit#ResetPasswordResponse",
    "email": "jon.doe@gmail.com",
    "requestType": "PASSWORD_RESET"
}

IDP_CHANGE_PASSWORD_EXAMPLE = {
    "kind": "identitytoolkit#SetAccountInfoResponse",
    "email": "jon.doe@gmail.com",
    "idToken": "updatedIdToken",
    "refreshToken": "updatedRefreshToken",
    "expiresIn": "3600"
}

IDP_ERROR_SEND_PASSWORD_RESET_EMAIL_RESPONSE_EXAMPLE = {
    "error": {
        "code":
        400,
        "message":
        "EMAIL_NOT_FOUND",
        "errors": [{
            "message": "EMAIL_NOT_FOUND",
            "domain": "global",
            "reason": "invalid"
        }]
    }
}

IDP_ERROR_RESET_PASSWORD_EXAMPLE = {
    "error": {
        "code":
        400,
        "message":
        "INVALID_OOB_CODE",
        "errors": [{
            "message": "INVALID_OOB_CODE",
            "domain": "global",
            "reason": "invalid"
        }]
    }
}

IDP_ERROR_CHANGE_PASSWORD_EXAMPLE = {
    "error": {
        "code":
        400,
        "message":
        "INVALID_ID_TOKEN",
        "errors": [{
            "message": "INVALID_ID_TOKEN",
            "domain": "global",
            "reason": "invalid"
        }]
    }
}

SEND_PASSWORD_RESET_EMAIL_EXAMPLE = {"email": "jon.doe@gmail.com"}

RESET_PASSWORD_EXAMPLE = {
    "oobCode": "o9vn3v9a8byw1bp98V",
    "newPassword": "dummyPassword"
}

CHANGE_PASSWORD_EXAMPLE = {"password": "dummyPassword"}

RESET_PASSWORD_RESPONSE_EXAMPLE = {
    "success": True,
    "message": "Successfully sent the password reset email",
    "data": {
        "kind": "identitytoolkit#ResetPasswordResponse",
        "email": "jon.doe@gmail.com",
        "requestType": "PASSWORD_RESET"
    }
}

CHANGE_PASSWORD_RESPONSE_EXAMPLE = {
    "success": True,
    "message": "Successfully sent the password reset email",
    "data": {
        "kind": "identitytoolkit#SetAccountInfoResponse",
        "email": "jon.doe@gmail.com",
        "idToken": "updatedIdToken",
        "refreshToken": "updatedRefreshToken",
        "expiresIn": "3600"
    }
}

DECODED_TOKEN_EXAMPLE = {
    "iss": "https://accounts.google.com",
    "azp": "test_azp",
    "aud": "test_aud",
    "sub": "103166258427660192046",
    "hd": "gmail.com",
    "email": "jon.doe@gmail.com",
    "email_verified": True,
    "at_hash": "vIPBbwQ_BdoHfrpz3Un1Tw",
    "nonce": "92348qvhn691vn043v9n0c13vn2",
    "name": "Jon Doe",
    "picture": "https://image_url.com",
    "given_name": "Jon",
    "family_name": "Doe",
    "locale": "en",
    "iat": 1664372561,
    "exp": 1664376161
}

BASIC_USER_MODEL_EXAMPLE = {
    "first_name": "steve",
    "last_name": "jobs",
    "email": "test.user@gmail.com",
    "user_type": "learner",
    "user_type_ref": "U2DDBkl3Ayg0PWudzhI",
    "user_groups": ["44qxEpc35pVMb6AkZGbi"],
    "status": "active",
    "is_registered": True,
    "failed_login_attempts_count": 0,
    "access_api_docs": False
}

INSPACE_TOKEN_EXAMPLE = {
  "token": {
    "eyJhbGciOiJSUzI1NiIJ...X2ybGwFvMhw"
  }
}
